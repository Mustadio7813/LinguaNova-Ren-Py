<!-- 2026-11-11_ALIGERAR_JUEGO -->
# Revisión actual: Aligerar el juego (11 de noviembre de 2026)


Edición **Desarrollador**. Entorno: Linux, Python 3.13, PyQt6 6.10, Qt sin pantalla (software).

| Comprobación | Desarrollador | Japonés |
| --- | --- | --- |
| Prueba de interfaz `PRUEBA_ALIGERAR_JUEGO.py` (aplicación real) | 28/28 | 28/28 |
| Pruebas sin red existentes | 10 aprobadas | 10 aprobadas |
| Scripts de empaquetado y runtime MOD | 4 aprobados | 4 aprobados |
| Avisos QML de la tarjeta nueva | 0 | 0 |
| Diferencias entre ediciones (sin comentarios) | Las mismas 81 líneas que antes | Las mismas 81 líneas que antes |
| Descarga de ffmpeg con servidor local: huella correcta / incorrecta | Instalada / rechazada | Mismo código |
| Instalación opcional de librerías en un entorno vacío | Instaladas; 2.º arranque sin espera | Mismo código |
| Validación de documentación y hashes | Aprobada | Aprobada |

La prueba de interfaz recorre: tarjeta visible en Utilidades, ffmpeg detectado, **Calcular ahorro** sin crear carpetas, **Crear copia optimizada** (copia más liviana, `.rpa` extraídos, motor de Linux quitado, traducciones y ajustes de RAM presentes, informe escrito, original idéntico byte a byte), **Detener** (sin carpeta `.parcial` y con la copia anterior conservada) y los textos en los cinco idiomas. Sin ffmpeg en el PATH, la tarjeta muestra el aviso ámbar y la estimación cuenta solo las imágenes.

No se ejecutaron en esta revisión: compilación y EXE en Windows, descarga real desde gyan.dev y un juego Ren'Py real.

---

# Resultados de LinguaNova 1.5.5 corregido

Edición **Desarrollador**.

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

Las señales de Qt se simularon y las respuestas de los motores fueron locales. Para el alcance exacto, consulta [INFORME_FINAL.md](../INFORME_FINAL.md).

---

# Resultados de pruebas — 2026-11-05_MODv5

Fuente actual: `LinguaNova_Traductor_RenPy.py`. SHA-256: `690237036274bfe66f0dd50e39cf5d74978164f13bf97533326fba98484a44ac`.

| Comprobación | Resultado | Alcance |
| --- | --- | --- |
| Recursión de dos hooks v4 | Reproducida | SDK oficial Ren'Py 7.4.4.1439, Linux; fallo esperado registrado. |
| Dos hooks v5, español y ruso | Correcto | SDK 7.4.4.1439; tablas nativas, plantillas y cambio a idioma original. |
| Mezcla de dos hooks v4 y uno v5 | Correcto | SDK 7.4.4.1439; la cadena antigua recursiva no cierra el juego de prueba. |
| Copias repetidas y orden inverso | Correcto | Funciones en ámbito privado y un único registro de callbacks propios. |
| Escala: 62.476 entradas y dos hooks | Correcto | SDK 7.4.4.1439; compilación y registro de un diccionario grande. |
| Guardado y carga | Correcto | SDK 7.4.4.1439; estado real serializado y cargado; captura PNG de prueba sin render. |
| Reentrada de callback del juego | Correcto | Se conserva el callback y se evita una llamada circular. |
| Traducciones nativas previas | Correcto | Conservan prioridad al registrar textos. |
| Fuentes/bytecode de MOD obsoleto | Correcto | Solo se apartan archivos propios reconocidos; se conserva un script ajeno. |
| Fallo durante retirada | Correcto | Restauración de archivos retirados y salida anterior. |
| Generación completa de fixture | Correcto | Nombre de salida estable, informe de migración y respaldo fuera de game. |
| Título Qt y carga completa | Correcto en Linux | Título y nombre visible iguales a «Traductor de Ren'Py». |
| Sintaxis, JSON, índices y manifiesto | Correcto | Se verifican al construir esta entrega. |
| Juego Another Chance completo | No ejecutado | Se recibió su traza, no el juego. |
| DLL y compilación Windows | No ejecutadas | Las pruebas de rutas previas usan datos Windows simulados. |
| Servicios con claves reales | No ejecutados | Las pruebas previas de motores usan respuestas simuladas. |

Los casos estandar y japones del SDK se ejecutaron con sus respectivos generadores. Las pruebas de escala y guardado/carga utilizan el generador estándar y verifican el runtime compartido, comprobado idéntico en ambas fuentes; la captura del guardado es un PNG de prueba sin render.

Los registros anteriores conservados en otros documentos se marcan como históricos. El 99,2 % de una captura del usuario no es un resultado de estas pruebas ni una garantía de funcionamiento de todo el juego.
