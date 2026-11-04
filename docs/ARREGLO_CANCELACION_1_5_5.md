# Ajuste acotado: detener con un clic

## Causa
El control enviaba una bandera de parada, pero algunas esperas de red, detección, sondeo y reintento no la consultaban hasta que terminaba la petición. Además, durante la etapa inicial idle el botón podía quedar deshabilitado. La finalización tenía llamadas a _t sin el argumento default exigido; esto podía impedir emitir las señales que liberan la interfaz.

## Corrección
- El botón reconoce la primera pulsación inmediatamente, muestra «Deteniendo…» en el idioma de la interfaz y queda deshabilitado mientras se conserva el progreso.
- La petición de parada despierta el bucle asíncrono de la traducción y cancela su tarea activa y sus hijos. El estado no se resuelve pulsando varias veces.
- Las esperas de detección, comprobación del proveedor, traducción principal, recuperación de variantes y reintentos de interfaz pasan por el mismo control de cancelación.
- Los descansos de reintento de interfaz dejan de ser sleep síncronos y también son cancelables.
- La cancelación se propaga como control de flujo, sin confundirse con un fallo del proveedor que deba reintentarse.
- La limpieza al cancelar tiene plazos acotados; no espera al cierre del executor por una llamada síncrona del SDK ya enviada. Su respuesta queda descartada y no reanuda el guardado ni la publicación.
- Se mantienen los puntos de guardado y respaldos. No se termina forzosamente el QThread ni se mata el proceso del juego.
- Las llamadas de traducción de mensajes en la finalización reciben el default requerido para que la señal final siempre libere la interfaz.
- Un nuevo trabajo restablece el estado visual y no hereda la parada del anterior.

## Alcance y límites
El resto de las definiciones existentes y los recursos de interfaz/idioma conservan su contenido, salvo los cambios del botón y la nueva clave trial_stopping. Ver CAMBIOS_CANCELACION.json. La carpeta docs contiene esta adenda y la evidencia actualizada; las referencias a 465 pruebas en la auditoría inicial corresponden a la entrega anterior.

La reacción visual y la cancelación de esperas locales son inmediatas. Guardar el progreso y terminar una escritura atómica puede requerir un breve tiempo. No se interrumpe una escritura a mitad de archivo ni se promete detener una operación síncrona del sistema operativo antes de que devuelva el control. Una solicitud que ya llegó a un proveedor remoto no se puede revocar desde la aplicación; se cancela su espera y se descarta su resultado.

## Pruebas
Se añadieron 11 pruebas de cancelación: solicitud de 60 s, tareas hijas, parada previa, propagación de resultados/errores normales, SDK síncrono en executor, cierre de cliente lento, método real de traducción principal con caché, detección en curso, pulsación única/idempotencia, reintento de 30 s y medición.

La prueba QML invoca el botón real y comprueba el texto, la desactivación, la deduplicación del clic, la finalización y la habilitación para la próxima operación. No se ocultaron excepciones de slots de Python.

Resultado: 476 aprobadas y 1 omitida (fixture de fuente no instalado). Las latencias registradas corresponden a solicitudes simuladas en Linux, no a todos los equipos o proveedores. No se compiló ni probó el .exe de Windows en este entorno.
