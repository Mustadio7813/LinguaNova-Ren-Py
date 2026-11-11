# CASO DUPLICADOS RENPY — estado actualizado

Revisión vigente: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

Hay dos problemas diferentes: las traducciones nativas duplicadas y los callbacks de dos archivos del MOD. Se mantiene la protección de las tablas nativas; el runtime v5 añade aislamiento, unión de idiomas y protección de reentrada. La publicación retira scripts y bytecode propios obsoletos, con respaldo fuera de game. Se ha probado el caso de dos hooks y la mezcla v4/v5 en el SDK 7.4.4.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# Caso reportado: Valley_Awakening 0.91.05F-hotfix / Ren’Py 8.5

## Evidencia del usuario
`game/tl/spanish/common.rpy:6` intenta registrar `Click to play the video.` y el motor informa que ya está en `game/tl/spanish/_engine/common/000statements.rpy:6`.

La causa inmediata es la duplicación del mismo old para el mismo idioma. El traceback no establece qué proceso creó cada archivo. No se atribuye sin evidencia al juego o a la conversión plana.

## Reparación en la copia
1. Tras adquirir el bloqueo y respaldar los resultados existentes, analizar las declaraciones en scripts fuente sueltos del juego.
2. Agrupar por idioma y cadena original exacta. Se conservan los marcadores de contexto, por ejemplo `{#state}`.
3. No reescribir fuentes originales fuera de tl/<idioma>. Si una traducción del autor fuera de esa carpeta ya define la cadena, conserva su autoridad.
4. Entre declaraciones editables, preferir traducción no vacía y distinta del original; después la ruta fuera de _engine; después ruta/línea determinista.
5. Respaldar los archivos que cambiarán y sus compilados asociados fuera del juego.
6. Comentar únicamente los pares duplicados. Si un bloque queda vacío, comentar también su cabecera para no dejar un bloque inválido. No borrar common.rpy completo.
7. Retirar únicamente el .rpyc/.rpymc asociado al fuente que se acaba de reparar; así el motor recompila el fuente actualizado.
8. Repetir el análisis después de la generación y antes del resultado final. La reparación repetida sin cambios no hace nuevas modificaciones.

Si las traducciones duplicadas son diferentes, registrar el conflicto y marcar el resultado como parcial. No declarar resuelta una ambigüedad lingüística por haber resuelto el error técnico.

Un archivo corregido y protegido no se sobrescribe: si contiene un conflicto que requiere editarlo, se bloquea la preparación y se registra el motivo.

## Límites
La reparación automática se aplica a declaraciones fuente .rpy/.rpym sueltas. No reescribe AST compilados sin fuente, paquetes RPA ni archivos del motor instalado. Las comprobaciones previas existentes de traducciones ajenas siguen funcionando, pero no se afirma una detección exhaustiva dentro de paquetes de terceros. No se ha ejecutado el juego completo del usuario en este entorno.

Referencia técnica: https://www.renpy.org/doc/html/translation.html

Las traducciones compiladas sin fuente de la carpeta de destino se inspeccionan como propietarios de solo lectura. Un conflicto detectado o un archivo no verificable bloquea la preparación; no se borra ese compilado. La restauración avanzada respalda y retira los compilados asociados a fuentes que restaura o elimina, para no dejar registros huérfanos activos.
