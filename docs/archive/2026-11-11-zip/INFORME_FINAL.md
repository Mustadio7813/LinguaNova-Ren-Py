<!-- 2026-11-11_ALIGERAR_JUEGO -->
# Informe de la revisión 2026-11-11_ALIGERAR_JUEGO — Desarrollador

Se integró en Utilidades la herramienta **Aligerar el juego** (Optimizador Ren'Py v3 sin consola): copia optimizada y cálculo de ahorro, con ffmpeg como programa aparte (incluido en la versión en carpeta y descargado al usarlo en la portable). Se aplicó la misma modificación a las ediciones Desarrollador y Japonés.

Pruebas en Linux: interfaz real en Qt sin pantalla 28/28, pruebas sin red 10/10, scripts de empaquetado y runtime 4/4, descarga verificada con servidor local, instalación opcional de librerías y validación de documentación. Pendiente en Windows: compilar con los dos BAT, procesos del EXE portable, descarga real desde gyan.dev y un juego real.

Fuente: `LinguaNova_Traductor_RenPy.py`, SHA-256 `f22e843941f2b5a2de5aeeb3699e8bad7942030304d4818b2cd4d256514535a3` (antes `c2e37cdec1ddf69764a55c9bf46032db84f2f045bff85274e8b4ebc339a8490f`). Documentación: `docs/ALIGERAR_JUEGO.md`.

---

# Informe final de LinguaNova 1.5.5

## Cambios por unidad

| Unidad | Cambio |
| --- | --- |
| `TLParser.should_skip_text`, `parse_file`, `_parse_all_entries`, `TranslationFile` | El parser conserva un registro separado de los huecos que filtra. Sigue excluyéndolos de su lista de trabajo. |
| `RenPyOutputFormatter._should_skip_translation`, `is_exempt_entry`, `get_translation_stats` | Se comparten el filtro técnico y las reglas de nombres y claves. Las letras Unicode permiten clasificar correctamente texto japonés y de otros alfabetos. Solo se descuentan las copias exentas. |
| `_completion_stats`, `_completion_message`, `_on_pipeline_finished`, QML | Se cuentan los pendientes del archivo guardado y se publica la misma cobertura para el resumen y la barra. El redondeo de pantalla evita mostrar 100 % si queda un pendiente real. El resumen en español e inglés incluye el desglose y la nota sobre pantallas y Python cuando corresponde. |
| `_translate_entries`, `_recover_pending_entries`, `_recover_tagged_segments` | Se conserva la causa de cada intento y se aplica una recuperación con el motor elegido, el guard y la caché. Se protegen las partes técnicas y se verifica el texto completo después de recomponerlo. |
| `_run_pipeline`, `translate_existing_tl`, `run`, `_write_pending_report` | Los flujos de juego y carpeta TL recuperan antes de guardar. El resumen enlaza con `translation_pending.json`. Si se cancela la recuperación, la preparación principal conserva lo escrito y su estado de detención. |
| `EditorBackend._run.worker`, `_on_work_done`, `translatePending.translate/job/safe_job`, `translate_pending_language` | Revisar recoge las respuestas disponibles, vuelve a aplicar las comprobaciones del editor, guarda el lote parcial, libera el estado y emite el aviso de detenido. |
| `GoogleTranslator._wait_out_global_cooldown`, `_get_next_endpoint`, `translate_single`, Bing y Gemini | El cooldown compartido se espera de forma asíncrona y cancelable. La solicitud de recuperación usa el motor elegido sin delegarlo a un respaldo adicional. |

El informe por línea se escribe en `game/tl/.diagnostics/<idioma>/translation_pending.json` para un juego con estructura convencional. En una carpeta TL independiente, el resumen indica la ruta efectiva.

## Pruebas

| Comprobación | Desarrollador | Japonés |
| --- | --- | --- |
| Pruebas nuevas sin red | 10 aprobadas | 10 aprobadas |
| Pruebas históricas de cancelación | 11 aprobadas | 11 aprobadas |
| Scripts históricos de empaquetado y runtime MOD | 4 aprobados | 4 aprobados |
| Detener y guardar con un cooldown simulado de 300 s | 0.010 s | 0.010 s |
| Sintaxis de Python, integridad de los ZIP y compilación desde el ZIP | Aprobadas | Aprobadas |
| Validación de documentación y hashes | Aprobada | Aprobada |
| Lógica JavaScript de finalización de QML ejecutada fuera de Qt | Aprobada | Aprobada |
| Diferencias entre ediciones, sin comentarios ni números de línea | Coinciden con las originales | Coinciden con las originales |

Las pruebas nuevas verificaron símbolos, números, etiquetas, variables, «Hotel», huecos vacíos, letras japonesas y de otros alfabetos, cobertura sin huecos traducibles, el redondeo de una ejecución casi completa, la recuperación individual y por segmentos, el guard, la caché, cuota y cooldown, el guardado desde las rutas de juego y carpeta TL y la cancelación en Revisar. La prueba de Revisar pulsó `stopPending()` en el backend real, comprobó `threading.excepthook`, señales, aviso, estado final, respaldo y escritura de las respuestas que precedían y seguían a la fila detenida en el lote devuelto. Otra prueba provocó un conflicto de disco y una respuesta con una variable perdida.

Las pruebas históricas de cancelación se extrajeron del bloque ejecutable de `docs/PRUEBAS_CANCELACION_CODIGO.md`. Los scripts históricos ejecutados fueron `PRUEBA_PAQUETE_COMPARTIR.py`, `PRUEBA_PAQUETE_SDK.py`, `PRUEBA_PAQUETES_SUMADOS.py` y `PRUEBA_RUNTIME_MOD_V5.py`. Las pruebas nuevas reproducibles están en `docs/PRUEBA_COBERTURA_RECUPERACION_REVISAR.py`.

## Decisiones y alcance

- La recuperación solo usa el motor elegido. Usa una solicitud por texto si hay reintentos habilitados. Conserva las políticas de transporte de cada cliente. Con `max_retries = 0` puede resolver mediante resultados disponibles. Durante un cooldown global 429 difiere las solicitudes nuevas.
- Se registra `source_copy` cuando hay una copia en disco sin evidencia de un intento y `cancelled` para huecos sin intento registrado en una ejecución detenida. Así el informe evita atribuir fallos al motor sin evidencia. Se reconocen nombres cuando la entrada conserva su tipo o contexto. Un nombre aislado sin esa procedencia sigue las mismas reglas de los demás textos.
- La preparación de fuente de esta edición está desactivada en el flujo de prueba. Se añadió la nota informativa solicitada. El informe cubre huecos que el parser pudo identificar y se genera antes de la publicación final del complemento de interfaz.
- Las funciones pequeñas de estadísticas, reporte y editor se sustituyeron como unidades. En las funciones extensas de orquestación se sustituyeron los bloques afectados y se conservó el resto del flujo. La revisión del diff y del AST comprobó los cambios de alcance y la ausencia de definiciones nuevas duplicadas.
- Se revisaron los trabajadores de MOD y su lote de idiomas, la generación de idioma de interfaz, el glosario, el lote principal de idiomas y la sugerencia de Revisar. El fallo del editor quedaba en el trabajador que comparten Revisar y sugerencias. La preparación de interfaz gestiona su interrupción con `InterruptedError`. El MOD independiente y el glosario usan rutas asíncronas propias, y el lote principal usa el manejo de detención de la preparación. Sus estadísticas y trabajadores específicos se conservaron.
- Se conservaron `unicode_escape` y la generación de IDs, la jerarquía de `TranslationInterrupted`, las estadísticas del MOD, los BAT, los recursos y el catálogo de idiomas de cada edición. La función que calcula los IDs también se comparó con el AST original. El índice de definiciones de `docs/` se regeneró. Las referencias históricas y la tabla de líneas incrustada en el encabezado del monolito se conservaron como estaban.

## Límites de verificación

Las pruebas corrieron en Linux con Python 3.12, motores falsos y un doble para las señales de Qt. La medición de detención corresponde a ese entorno. Quedaron sin comprobar la ejecución de QML con Qt real, la interfaz y compilación en Windows, Ren’Py ejecutado con su SDK, el juego del usuario y los proveedores de traducción en vivo. `PRUEBA_SELECTOR_IDIOMAS.py` requiere Qt/QML real. `PRUEBA_SDK_MOD_V5.py`, `PRUEBA_MOD_TRADUCCION_EXISTENTE.py` y `PRUEBA_GLOSARIO_POR_IDIOMA.py` requieren el SDK o sus juegos compilados de prueba.

Los ZIP adjuntos se usaron como línea base. Se verificaron su copia de trabajo y su diff previo antes de editar. No venía un generador documental, así que se recalcularon los hashes, las líneas y los recuentos desde los archivos reales. `DIFERENCIAS_IMPLEMENTACION.diff` refleja cada ZIP adjunto frente al corregido. El diff acumulado de una entrega más antigua queda identificado como antecedente mediante su hash, pues su ZIP base no formaba parte de los adjuntos.
