<!-- 2026-11-11_ALIGERAR_JUEGO -->
# Revisión actual: Aligerar el juego (11 de noviembre de 2026)


- **Aligerar el juego** nunca escribe en el juego original. La copia se construye en `<destino>.parcial`; si se detiene o falla, esa carpeta se borra y una copia anterior completa se conserva.
- No borra una carpeta de destino que tenga archivos ajenos: pide elegir otra.
- Comprueba que haya al menos 1,3 veces el tamaño del juego libre en el disco.
- Un archivo que no mejora, cambia de duración o falla se deja como estaba (anotado en el informe).
- Límites: no trata imágenes animadas, vídeos con transparencia ni códecs distintos de H.264, VP8, VP9 y Theora; sin ffmpeg no toca audio ni vídeo; la estimación es una muestra. Detalle completo: [Aligerar el juego](ALIGERAR_JUEGO.md).

---

# Revisión actual de cobertura y Revisar

La traducción principal separa las copias exentas de los pendientes reales. Aplica una pasada acotada de recuperación y registra las líneas que siguen en la fuente en `translation_pending.json`. Consulta [Cobertura, recuperación e informe](ARREGLO_PORCENTAJE_Y_RECUPERACION.md). Los reintentos de la fase de recuperación se difieren durante un cooldown global 429.

---

# RECUPERACION Y LIMITES — estado actualizado

Revisión anterior: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

Se conserva la recuperación previa de operaciones y sus límites. La nueva publicación del MOD respalda archivos propios antes de sustituirlos o retirarlos; si falla, restaura las versiones anteriores. Los respaldos de hooks actuales quedan fuera de `game`, en `.linguanova_backups/mod_hooks/`. Un error interno reconocido detiene reintentos inútiles; esto no elimina límites ni fallos de proveedores externos.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# Recuperación e integridad

El diario guarda identidad del juego/idioma/motor, etapa, estado, inventario de fuentes, cambios detectados, respuestas de interfaz aceptadas, respaldos, archivos protegidos y manifiesto de salidas.

El bloqueo es por proyecto, no solo por idioma. Una operación de otro proceso no se interrumpe. En Windows la comprobación de proceso usa OpenProcess/GetExitCodeProcess; nunca os.kill(pid, 0), que no tiene el mismo comportamiento que en Unix. La recuperación de un bloqueo de proceso muerto utiliza además un bloqueo de recuperación; un bloqueo ilegible se conserva y bloquea por seguridad.

Los scripts fuente se identifican por SHA-256. Para RPA grandes se usa tamaño/mtime: cambios que preserven ambos metadatos pueden no detectarse mediante ese inventario. Esa detección no sustituye los validadores de traducción.

Los respaldos de esta edición no se eliminan automáticamente. Pueden ocupar espacio y el historial debe administrarse conscientemente. La escritura es atómica por archivo; no existe una transacción de sistema de archivos que sustituya todos los archivos del juego de forma indivisible ante un corte de energía.

La cancelación principal e interfaz interrumpen sus esperas asíncronas y descartan trabajo pendiente; no esperan el timeout normal del proveedor. Se conservan los resultados ya aceptados mediante los puntos de guardado. Una escritura atómica o acción síncrona local puede requerir un breve cierre seguro. Ver ARREGLO_CANCELACION.md. No se mata el proceso del juego ni se fuerza la terminación de hilos.

La protección manual es por archivo completo detectado a partir del manifiesto anterior. Puede dejar otros textos de ese archivo sin actualizar; se informa como parcial. No se implementa una aprobación humana por segmento ni se inventan porcentajes de revisión.

Los callbacks de traducción principal e interfaz conservan su encadenamiento existente; se reutilizan traducciones old/new del flujo principal antes de enviar nuevas solicitudes. Debe validarse en juegos reales: los tests no garantizan todos los callbacks de cada juego.

Capturas con contexto, OCR, estimación de costes, nuevos motores, integración colaborativa y nuevos formatos de intercambio no se añadieron en esta iteración del flujo sencillo.
