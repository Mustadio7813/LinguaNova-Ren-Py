# Detener en Revisar

El traceback comunicado seguía este recorrido.

```text
EditorBackend._run.worker
  -> translatePending.safe_job
  -> translatePending.job
  -> translate_pending_language
  -> translatePending.translate
  -> TranslationPipeline._translate_entries
  -> retry_unchanged_candidate
  -> execute_single_request_with_retry_mode
  -> InterruptibleLoop.run_until_complete
  -> InterruptibleLoop._wait
  -> TranslationInterrupted
```

`TranslationInterrupted` hereda directamente de `BaseException`. Los manejadores de `Exception` del editor dejaban morir el hilo antes de emitir la señal de finalización. Por eso Revisar conservaba el estado «traduciendo».

El trabajador ahora emite la señal de finalización en `finally`. El cierre que traduce recupera las respuestas ya aceptadas y valida también las respuestas de un lote que el motor ya devolvió. El editor guarda las filas aprobadas con su control de conflictos de disco y su respaldo `editor_backup`, actualiza el estado y presenta el aviso de detención. Una respuesta todavía en vuelo queda pendiente.

Google espera su plazo global mediante una tarea asíncrona. Detener cancela esa tarea, incluso si el plazo simulado es de 300 segundos. La jerarquía de excepciones sigue siendo la misma.

Ejecuta `python docs/PRUEBA_COBERTURA_RECUPERACION_REVISAR.py` con las dependencias de LinguaNova instaladas. Los resultados de esta entrega se detallan en [RESULTADOS_PRUEBAS.md](RESULTADOS_PRUEBAS.md).
