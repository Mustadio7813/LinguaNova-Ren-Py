# Revisión actual de cobertura y Revisar

Al pulsar **Detener** en Revisar, el editor finaliza el trabajo, valida las respuestas disponibles y guarda las aceptadas con el respaldo y el control de conflictos existentes. Consulta [Detener en Revisar](ARREGLO_DETENER_REVISAR.md).

---

# CORRECCIONES AVISOS Y SALIR — estado actualizado

Revisión anterior: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

Se conservan el borde redondeado, el resumen sin claves internas, el aviso temporal superior y la terminología «Salir» para etiquetas completas de interfaz en español. Se añade el título exacto «Traductor de Ren'Py». Los mensajes de detección técnica y de cobertura no se han ocultado; la propuesta de cambiar el primero sigue pendiente de confirmación.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# Correcciones de avisos y botones de salida — 5 de noviembre de 2026

- El cuadro final conserva su contorno redondeado y ya no dibuja la franja recta superior.
- El resumen empieza directamente con el mensaje detallado. Se eliminó el prefijo que mostraba `trial_partial` o `trial_ready` como claves internas.
- El aviso temporal se muestra arriba a la derecha y por encima del cuadro final. Desaparece tras unos 3,5 segundos y deja el resumen abierto.
- Cuando termina correctamente, el aviso en español dice «La traducción terminó correctamente.». Si quedan líneas pendientes o ocurre un error, conserva el aviso correspondiente.
- Los botones completos «Quit» y «Exit» se traducen como «Salir» al elegir español; «Quit Game» y «Exit Game» como «Salir del juego». Se conservan las etiquetas de formato y las mayúsculas.
- La corrección de botones se aplica antes de consultar motores o cachés en la traducción principal y también al regenerar el MOD de interfaz, incluidas traducciones automáticas reutilizadas. Respeta las correcciones manuales y los términos explícitos del glosario. No sustituye la palabra «dejarlo» de los diálogos.

Para corregir una interfaz generada con una versión anterior, vuelve a generar el MOD de interfaz en español. Actualizar el traductor por sí solo no modifica los archivos de un juego ya traducido.

Validación: sintaxis Python, comparación del código con los originales, interfaz Qt en los cinco idiomas de la aplicación, aviso sobre un cuadro modal y desaparición automática, traducción principal con motor simulado y generación real del MOD sobre un proyecto de prueba con traducciones previas. No se ejecutó el juego del usuario.
