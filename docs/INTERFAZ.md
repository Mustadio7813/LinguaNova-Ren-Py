<!-- 2026-11-11_ALIGERAR_JUEGO -->
# Revisión actual: Aligerar el juego (11 de noviembre de 2026)


Utilidades tiene una tarjeta nueva, **Aligerar el juego** (`OptimizeGameCard.qml`), debajo de «Compartir o respaldar traducciones» y con su mismo estilo (`PageHeader`, `ThemedButton`, `Theme`). Contiene el selector de compresión con una explicación de cada nivel, tres casillas, el estado de ffmpeg (verde si está listo; ámbar con **Descargar ffmpeg** y **Elegir ffmpeg.exe…** si falta), los botones **Crear copia optimizada**, **Calcular ahorro**, **Detener** y **Abrir copia**, una barra de progreso con la fase en curso y el resultado.

La tarjeta se bloquea mientras se traduce o se genera el MOD (`locked: isTranslating || appBackend.modRunning`). Todos los textos (`opt_*`) están en español, inglés, francés, portugués y ruso. Se comprobó en Qt sin pantalla, con captura, que la tarjeta carga sin avisos QML. Detalle completo: [Aligerar el juego](ALIGERAR_JUEGO.md).

---

# Revisión actual de cobertura y Revisar

La traducción principal separa las copias exentas de los pendientes reales. Aplica una pasada acotada de recuperación y registra las líneas que siguen en la fuente en `translation_pending.json`. Consulta [Cobertura, recuperación e informe](ARREGLO_PORCENTAJE_Y_RECUPERACION.md).

Al pulsar **Detener** en Revisar, el editor finaliza el trabajo, valida las respuestas disponibles y guarda las aceptadas con el respaldo y el control de conflictos existentes. Consulta [Detener en Revisar](ARREGLO_DETENER_REVISAR.md).

---

# INTERFAZ — estado actualizado

Revisión anterior: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

El título de la ventana y el nombre visible de Qt son «Traductor de Ren'Py», para evitar el sufijo duplicado. El borde del cuadro final permanece redondeado; se quitó la franja superior y la clave interna del resumen. El aviso temporal aparece arriba a la derecha durante unos 3,5 segundos. Los avisos de cobertura parcial conservan su significado.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# Interfaz de la prueba

El recorrido principal se mantiene: añadir juego → idioma → Traducir → Jugar. No se añade una confirmación técnica ni un selector de género.

Traducir rechaza pulsaciones duplicadas cuando hay trabajo activo. Los controles existentes de proyecto/idioma permanecen bloqueados durante la traducción. El análisis y la preparación se ejecutan en el worker, no en el hilo de dibujo.

Se añaden las fases de interfaz, preparación y verificación. La fase completed intermedia del traductor principal no se presenta como finalización de toda la operación. El resultado distingue preparado, parcial, detenido y error.

MOD sencillo ofrece el panel opcional; los controles de generación y corrección independiente de traducciones de interfaz solo se muestran en modo avanzado. El panel no se instala automáticamente.

La ventana final usa el título real del resultado. El botón Jugar exige un registro válido para el juego e idioma actuales, y vuelve a verificar las huellas al pulsarlo. Si no existe un lanzador único, el usuario puede seleccionar el ejecutable del juego mediante el selector ya existente; no se elige arbitrariamente entre varios juegos.

Todos los mensajes añadidos están definidos en español, inglés, francés, portugués y ruso. El selector de idioma conserva la corrección de actualización inmediata de sus nombres.
