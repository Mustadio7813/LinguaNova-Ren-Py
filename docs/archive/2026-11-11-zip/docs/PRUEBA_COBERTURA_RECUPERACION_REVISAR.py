"""Pruebas sin red. Ejecutar con las dependencias del traductor instaladas."""
import asyncio
import json
import os
from pathlib import Path
import runpy
import sys
import tempfile
import threading
import time
from types import SimpleNamespace
import unittest

from PyQt6.QtCore import QCoreApplication, QObject, pyqtSignal


SOURCE = Path(sys.argv.pop(1)).resolve() if len(sys.argv) > 1 else (
    Path(__file__).resolve().parents[1] / 'LinguaNova_Traductor_RenPy.py')
DATA = tempfile.TemporaryDirectory()
os.environ['LINGUANOVA_DATA_DIR'] = DATA.name
g = runpy.run_path(str(SOURCE), run_name='ln_test')
application = QCoreApplication.instance() or QCoreApplication([])
Pipeline = g['LN_src_core_pipeline_orchestrator__TranslationPipeline']
Config = g['LN_src_utils_config__ConfigManager']
Manager = g['LN_src_core_translators_manager__TranslationManager']
Entry = g['LN_src_core_tl_parser__TranslationEntry']
File = g['LN_src_core_tl_parser__TranslationFile']
Parser = g['LN_src_core_tl_parser__TLParser']
Result = g['LN_src_core_translators_base__TranslationResult']
Engine = g['LN_src_core_translators_base__TranslationEngine']
Google = g['LN_src_core_translators_google__GoogleTranslator']
Editor = g['LN_src_backend_editor_backend__EditorBackend']
stats = g['LN_src_core_tl_parser__get_translation_stats']
interrupted = g['LN_src_core_cancellation__TranslationInterrupted']


def answer(req, text, *, success=True, error=None, quota=False):
    return Result(req.metadata['original_text'], text, req.source_lang, req.target_lang,
                  req.engine, success, error, quota_exceeded=quota, metadata=req.metadata)


class App(QObject):
    translationStarted = pyqtSignal()
    translationFinished = pyqtSignal(bool, str)
    logMessage = pyqtSignal(str, str)

    def __init__(self, config, project):
        super().__init__()
        self.config = config
        self._project_path = str(project)
        self.proxy_manager = None

    def _tool_game_dir(self):
        return str(Path(self._project_path) / 'game')

    @staticmethod
    def _engine_from_str(engine):
        return Engine(engine)


class Tests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.project = Path(temp.name)
        self.path = self.project / 'game/tl/spanish/test.rpy'
        self.path.parent.mkdir(parents=True)
        self.config = Config()
        self.config.app_settings.ui_language = 'es'
        self.config.translation_settings.source_language = 'en'
        self.config.translation_settings.auto_protect_character_names = False
        self.manager = Manager(config_manager=self.config)
        self.manager.set_proxy_enabled = lambda enabled: None
        self.pipe = Pipeline(self.config, self.manager)
        self.pipe.configure(str(self.project), 'spanish', source_language='en', engine=Engine.GOOGLE)

    def entry(self, original, translated, index, **kwargs):
        return Entry(original, translated, str(self.path), index, kwargs.pop('entry_type', 'string'),
                     translation_id=f'id_{index}', **kwargs)

    def write(self, pairs):
        lines = ['translate spanish strings:', '']
        for old, new in pairs:
            lines.extend([f'    old "{old}"', f'    new "{new}"', ''])
        self.path.write_text('\n'.join(lines), encoding='utf-8')

    def test_stats_unicode_and_empty(self):
        entries = [self.entry(t, t, i) for i, t in enumerate(
            ['...', '♪', '123', '{i}...{/i}', '[nombre]', '。。。', '?X000?', '⟦⟧', 'A', 'Hotel'])]
        entries += [self.entry('Hello there', 'Hola', 20), self.entry('Goodbye', '', 21),
                    self.entry('こんにちは', 'Buenos días', 22)]
        file = File(str(self.path), 'spanish', entries)
        actual = stats([file], self.config)
        self.assertEqual(actual, dict(total=13, translated=2, same_as_source=1, empty=1,
                         exempt=9, translatable=4, untranslated=2, progress=50.0))
        self.assertEqual(stats([File(str(self.path), 'spanish', entries[:9])])['progress'], 100.0)
        self.assertEqual(stats([File(str(self.path), 'spanish', entries[9:])])['progress'], 50.0)
        exempt = g['LN_src_core_tl_parser__is_exempt_entry']
        for word in ('こんにちは', '繁體中文', '한국어', 'Привет', 'مرحبًا', 'γειά'):
            self.assertFalse(exempt(self.entry(word, word, 30), self.config), word)
        self.assertFalse(exempt(self.entry('{color=#fff}こんにちは{/color}', '', 31), self.config))
        self.assertTrue(exempt(self.entry('Ada Lovelace', '', 32, entry_type='character_name'), self.config))
        self.assertTrue(exempt(self.entry('game key', '', 33, character='style_prefix'), self.config))
        self.config.translation_settings.translate_character_names = True
        self.assertFalse(exempt(self.entry('Ada Lovelace', '', 32, entry_type='character_name'), self.config))
        self.assertEqual(stats([File(str(self.path), 'spanish', [self.entry('♪', '', 33)])])['empty'], 1)

    def test_parser_and_pending_json(self):
        self.write([('123','123'), ('♪',''), ('Hotel','Hotel'), ('Hello there','Hola'), ('{}','{}')])
        parsed = Parser().parse_file(str(self.path))
        self.assertEqual(len(parsed.filtered_entries), 2)
        hotel = next(entry for entry in parsed.entries if entry.original_text == 'Hotel')
        self.pipe._translation_attempts = {self.pipe._pending_entry_key(hotel): (hotel, 'engine_failed', 'rate_limited_429')}
        measured = self.pipe._completion_stats([parsed], lang_dir=self.path.parent)
        self.assertEqual((measured['pending'], measured['empty'], measured['exempt']), (1,1,2))
        report = json.loads(Path(measured['pending_report']).read_text(encoding='utf-8-sig'))
        by_original = {row['original']: row for row in report['entries']}
        self.assertEqual(by_original['♪']['reason'], 'vacía')
        self.assertEqual(by_original['123']['reason'], 'exenta')
        self.assertEqual(by_original['Hotel']['reason'], 'rate_limited_429')
        self.assertTrue(all(row['file'] == str(self.path) and row['line'] > 0 for row in by_original.values()))
        self.assertIn('translation_pending.json', self.pipe._completion_message(measured, 1))
        self.assertIn('99.9', self.pipe._completion_message(dict(translated=9999, translatable=10000), 1))

    def test_recovery_retry_segments_and_unchanged(self):
        first = self.entry('A simple sentence.', '', 1)
        guarded = self.entry('{i}The captain{/i} saw [player] yesterday.', '', 2)
        unchanged = self.entry('Hotel', '', 3)
        cached = self.entry('Available in cache.', '', 4)
        entries = [first, guarded, unchanged, cached]
        pipe = self.pipe
        manager = self.manager
        calls = []
        async def batch(requests):
            return [answer(r, '', success=False, error='temporary') if r.metadata['original_text'] in
                    (first.original_text, cached.original_text) else answer(r, 'Perdió las etiquetas.' if
                    r.metadata['original_text'] == guarded.original_text else r.metadata['original_text'])
                    for r in requests]
        async def single(req):
            self.assertFalse(pipe.should_stop)
            original = req.metadata['original_text']
            calls.append(original)
            options = {first.original_text: 'Una frase sencilla.', guarded.original_text: 'Perdió las etiquetas.',
                       'The captain': 'El capitán', 'saw': 'vio a', 'yesterday.': 'ayer.'}
            return answer(req, options.get(original, original))
        translator = SimpleNamespace(translate_single=single)
        manager.translators[Engine.GOOGLE] = translator
        manager.translate_batch = batch
        out = pipe._translate_entries(entries)
        self.assertEqual((pipe._run_counts['engine_failed'], pipe._run_counts['guard_blocked'],
                          pipe._run_counts['unchanged_by_engine']), (2,1,1))
        original_lookup = manager.get_cached_translation
        manager.get_cached_translation = lambda text, *args: (
            SimpleNamespace(success=True, translated_text='Disponible en caché.') if text == cached.original_text
            else original_lookup(text, *args))
        pipe._recover_pending_entries(out)
        self.assertEqual(out['id_1'], 'Una frase sencilla.')
        self.assertEqual(out['id_2'], '{i}El capitán{/i} vio a [player] ayer.')
        self.assertNotIn('id_3', out)
        self.assertEqual(out['id_4'], 'Disponible en caché.')
        self.assertNotIn(cached.original_text, calls)
        self.assertEqual((pipe._run_counts['engine_failed'], pipe._run_counts['guard_blocked'],
                          pipe._run_counts['unchanged_by_engine']), (0,0,1))
        self.assertEqual(pipe.diagnostic_report.total_recovered_by_synthesized_variant, 1)

    def test_recovery_stop_and_cooldown(self):
        one = self.entry('A simple sentence.', '', 1)
        two = self.entry('Another long sentence.', '', 2)
        pipe = self.pipe
        manager = self.manager
        ready = threading.Event()
        async def batch(requests):
            return [answer(r, '', success=False, error='HTTP 429') for r in requests]
        async def single(req):
            if req.metadata['original_text'] == one.original_text:
                return answer(req, 'Una frase sencilla.')
            ready.set()
            await asyncio.sleep(300)
        translator = SimpleNamespace(translate_single=single, _global_cooldown_until=time.time()+300)
        manager.translators[Engine.GOOGLE] = translator
        manager.translate_batch = batch
        out = pipe._translate_entries([one,two])
        pipe._recover_pending_entries(out)
        self.assertFalse(out)
        self.assertFalse(ready.is_set())
        self.assertTrue(all(v[2]=='rate_limited_429' for v in pipe._translation_attempts.values()))
        translator._global_cooldown_until = 0
        marks = []
        def stop():
            if ready.wait(3):
                marks.append(time.monotonic())
                pipe.stop()
        worker = threading.Thread(target=stop)
        worker.start()
        pipe._recover_pending_entries(out)
        worker.join()
        self.assertTrue(marks)
        self.assertLess(time.monotonic() - marks[0], 1.0)
        self.assertTrue(pipe._run_counts['stopped'])
        self.assertEqual(out['id_1'], 'Una frase sencilla.')
        self.assertNotIn('id_2', out)

    def test_recovery_quota_stops_dispatch(self):
        entries = [self.entry('A simple sentence.', '', 1), self.entry('Another long sentence.', '', 2)]
        async def batch(requests):
            return [answer(r, '', success=False, error='temporary') for r in requests]
        calls = []
        async def single(req):
            calls.append(req.metadata['original_text'])
            return answer(req, '', success=False, quota=True)
        self.manager.translate_batch = batch
        self.manager.translators[Engine.GOOGLE] = SimpleNamespace(translate_single=single)
        output = self.pipe._translate_entries(entries)
        self.pipe._recover_pending_entries(output)
        self.assertEqual(calls, [entries[0].original_text])
        self.assertEqual(self.pipe._stop_reason, 'quota')
        self.assertFalse(output)

    def test_tl_route_recovery_writes_before_reporting(self):
        first, pending = 'A simple sentence.', 'Hotel'
        self.write([(first, first), (pending, pending), ('123', '123')])
        async def batch(requests):
            return [answer(req, req.metadata['original_text']) if req.metadata['original_text'] == pending
                    else answer(req, '', success=False, error='temporary') for req in requests]
        async def single(req):
            original = req.metadata['original_text']
            return answer(req, 'Una frase sencilla.' if original == first else original)
        self.manager.translate_batch = batch
        self.manager.translators[Engine.GOOGLE] = SimpleNamespace(translate_single=single)
        result = self.pipe.translate_existing_tl(str(self.path.parent), 'spanish', 'en', Engine.GOOGLE)
        self.assertTrue(result.success, result.message)
        self.assertEqual((result.stats['translated'], result.stats['translatable'], result.stats['exempt'],
                          result.stats['pending']), (1,2,1,1))
        self.assertIn('new "Una frase sencilla."', self.path.read_text(encoding='utf-8-sig'))
        report = json.loads(Path(result.stats['pending_report']).read_text(encoding='utf-8-sig'))
        self.assertEqual({row['original']: row['reason'] for row in report['entries']},
                         {pending: 'unchanged_by_engine', '123': 'exenta'})

    def test_game_route_recovers_and_keeps_original_script(self):
        script = self.path.parents[2] / 'script.rpy'
        original = 'A simple sentence.'
        script.write_text(f'label start:\n    "{original}"\n    return\n', encoding='utf-8')
        before = script.read_bytes()
        async def batch(requests):
            return [answer(req, '', success=False, error='temporary') for req in requests]
        async def single(req):
            return answer(req, 'Una frase sencilla.')
        self.manager.translate_batch = batch
        self.manager.translators[Engine.GOOGLE] = SimpleNamespace(translate_single=single)
        result = self.pipe._run_pipeline()
        self.assertTrue(result.success, result.message)
        self.assertEqual(script.read_bytes(), before)
        self.assertGreaterEqual(result.stats['translated'], 1)
        self.assertEqual(result.stats['progress'], 100.0)
        self.assertTrue(Path(result.stats['pending_report']).is_file())

    def test_no_recovery_requests_when_retries_disabled(self):
        entry = self.entry('A simple sentence.', '', 1)
        async def batch(requests):
            return [answer(req, '', success=False, error='temporary') for req in requests]
        async def single(req):
            self.fail('Max retries is zero')
        self.manager.translate_batch = batch
        self.manager.translators[Engine.GOOGLE] = SimpleNamespace(translate_single=single)
        self.manager.max_retries = 0
        output = self.pipe._translate_entries([entry])
        self.pipe._recover_pending_entries(output)
        self.assertFalse(output)
        self.assertEqual(self.pipe._run_counts['engine_failed'], 1)

    def test_review_stops_real_cooldown_with_partial_save(self):
        first, second = 'A brave sailor reads the map.', 'A second sailor waits for the signal.'
        third = 'A third sailor follows the coast.'
        self.write([(first, first), (second, second), (third, third)])
        before = self.path.read_bytes()
        ready = threading.Event()
        finished = []
        calls = []
        manager = self.manager
        translator = Google(config_manager=self.config)
        async def batch(requests):
            translated = {first: 'Un marinero valiente lee el mapa.',
                          second: second, third: 'Un tercer marinero sigue la costa.'}
            return [answer(r, translated[r.metadata['original_text']]) for r in requests]
        async def single(req):
            calls.append(req.metadata['original_text'])
            translator._global_cooldown_until = time.time() + 300
            ready.set()
            try:
                await translator._wait_out_global_cooldown()
            finally:
                finished.append(True)
        manager.translate_batch = batch
        translator.translate_single = single
        manager.translators[Engine.GOOGLE] = translator
        editor = Editor(App(self.config, self.project))
        editor._language = 'spanish'
        editor.pendingEngineProblem = lambda engine: ''
        editor.refreshLanguages = lambda: None
        states, notices, summaries, thread_errors = [], [], [], []
        editor.pendingStateChanged.connect(lambda: states.append(editor._pending_running))
        editor.notify.connect(lambda *args: notices.append(args))
        editor.pendingSummaryReady.connect(lambda *args: summaries.append(args))
        namespace = Editor.translatePending.__globals__
        symbol = 'LN_src_core_translator__TranslationManager'
        saved_manager = namespace[symbol]
        old_hook = threading.excepthook
        namespace[symbol] = lambda *_: manager
        threading.excepthook = thread_errors.append
        try:
            editor.translatePending('google', False)
            self.assertTrue(ready.wait(3), 'The unchanged retry did not enter the cooldown')
            started = time.monotonic()
            editor.stopPending()
            while (editor._pending_running or not summaries) and time.monotonic() - started < 3:
                application.processEvents()
                time.sleep(0.005)
            elapsed = time.monotonic() - started
        finally:
            threading.excepthook = old_hook
            namespace[symbol] = saved_manager
        self.assertEqual(thread_errors, [])
        self.assertFalse(editor._pending_running)
        self.assertFalse(editor._busy)
        self.assertIsNone(editor._pending_pipeline)
        self.assertIn(False, states)
        self.assertTrue(any('deten' in text.lower() for _,text in notices), notices)
        self.assertTrue(summaries)
        self.assertEqual(calls, [second])
        self.assertEqual(finished, [True])
        self.assertLess(elapsed, 1.0)
        print(f'Revisar detenido y guardado en {elapsed:.3f} s', flush=True)
        text = self.path.read_text(encoding='utf-8-sig')
        self.assertIn('new "Un marinero valiente lee el mapa."', text)
        self.assertIn(f'new "{second}"', text)
        self.assertIn('new "Un tercer marinero sigue la costa."', text)
        self.assertTrue(any(p.read_bytes() == before for p in self.path.parent.parent.rglob('*.bak')))

    def test_review_preserves_conflicts_and_rejects_corruption(self):
        first, second = 'Good morning, [name].', 'Are you ready?'
        self.write([(first, first), (second, second)])
        translate = g['LN_src_core_editor_pending__translate_pending_language']
        def answers(language, rows):
            self.path.write_bytes(self.path.read_bytes() + b'\n# external edit')
            return {rows[0]['id']: 'Buenos días.', rows[1]['id']: '¿Estás listo?'}
        result = translate(str(self.path.parents[2]), 'spanish', answers, str(self.project / 'backup'))
        self.assertEqual((result.rejected, result.translated, len(result.conflicts)), (1,0,1))
        self.assertIn('# external edit', self.path.read_text())


if __name__ == '__main__':
    unittest.main(verbosity=2)
