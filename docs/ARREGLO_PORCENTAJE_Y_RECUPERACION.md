# Cobertura, recuperación e informe de pendientes

## Cobertura de la traducción principal

La cobertura se calcula con lo que quedó en los archivos de traducción. Del total se descuentan las copias de origen exentas. Entre ellas están las entradas técnicas, los nombres identificados como tales cuando su traducción está desactivada y los textos sin letras después de retirar la sintaxis protegida. La detección usa letras Unicode. Por ejemplo, «こんにちは» tiene letras, mientras que «。。。», «♪» y «[nombre]» por sí solos quedan exentos cuando el destino repite la fuente.

Un hueco vacío cuenta como pendiente, incluso si la fuente es técnica. «Hotel» repetido en el destino es un pendiente real. Las traducciones que ya están escritas y difieren de la fuente cuentan como traducidas. Cuando todas las entradas son copias exentas, la cobertura es 100 %. El resumen separa las copias exentas, las copias pendientes, los vacíos y los fallos del motor o del guard. La barra usa la misma cobertura.

## Recuperación automática

Tras el lote principal, se revisan las entradas que devolvieron error, fueron bloqueadas por el guard o quedaron iguales. Se aprovecha una traducción válida del trabajo actual o de la caché antes de enviar una solicitud individual. Si la respuesta completa sigue siendo inutilizable, se intenta traducir los tramos con letras entre etiquetas, interpolaciones y formatos protegidos. Los elementos protegidos se reinsertan en su posición y se valida la línea reconstruida con el mismo guard de salida. Un tramo aceptado por el motor que queda igual puede conservarse si otro tramo cambió y la línea completa supera el guard.

La pasada utiliza el motor ya seleccionado y prescinde de un motor de respaldo adicional. Si el máximo de reintentos es cero, la pasada solo consulta resultados disponibles. Con reintentos habilitados, la pasada envía como máximo una solicitud por texto en cada recuperación. Los motores conservan sus políticas de red. Ante cuota agotada se detiene el envío. Durante un cooldown global 429 no se inician solicitudes de recuperación y las entradas que se difieren quedan identificadas en el informe. Al detener la pasada, se guarda lo que ya superó el guard.

## Informe por línea

En una carpeta convencional de juego queda en `game/tl/.diagnostics/<idioma>/translation_pending.json`. Si se trabaja en una carpeta TL independiente, LinguaNova indica la ruta efectiva en el resumen. Cada registro contiene archivo, línea, original y motivo. Si el hueco está vacío, se registra como `vacía` y, cuando existe, se añade el motivo del intento en `attempt_reason`.

| Motivo | Significado |
| --- | --- |
| `exenta` | La política del traductor conserva la copia deliberadamente. |
| `vacía` | El texto escrito en el hueco está vacío. |
| `guard_<motivo>` | La protección de salida rechazó la respuesta. |
| `unchanged_by_engine` | El motor devolvió la misma fuente sin una alternativa aceptable. |
| `engine_failed` | Hubo un fallo de traducción o faltó la respuesta. |
| `rate_limited_429` | Hubo un HTTP 429 o un cooldown que impidió el reintento. |
| `cancelled` | La operación se detuvo y el hueco quedó sin resultado registrado. |
| `source_copy` | Se leyó una copia sin evidencia de un intento para ese hueco. |

El informe cubre los huecos que pudo leer el parser. Los textos dinámicos de Python y de pantallas que no llegaron a esos archivos se tratan mediante la nota del resumen cuando la preparación de fuente está desactivada.
