# AUDITORIA CAMBIOS — estado actualizado

Revisión vigente: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

Este documento se ha revisado en el contexto de la fuente actual: título «Traductor de Ren'Py», correcciones previas conservadas, runtime del MOD v5 y migración transaccional de scripts propios. Sus afirmaciones antiguas de pruebas, rutas o estructura se conservan como antecedentes identificados, no como evidencia de esta entrega. El estado completo y las limitaciones están en la guía y los resultados actuales.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# Auditoría de la copia

El archivo de referencia plano y los ZIP originales no se reemplazan. Ver ORIGINALES_SHA256.json. Esta entrega utiliza como base lógica el mismo código integrado y conserva las correcciones previas de compilación/idioma.

## Política de sustitución
Cada función afectada tiene una única implementación activa. La coordinación run, inicio/finalización, cancelación, fases, arranque del juego, selección de ejecutable y generador de interfaz se sustituyen en su totalidad. No hay aliases a versiones antiguas, funciones *_old ni monkey patches de la aplicación en ejecución. Los analizadores, motores y validadores especializados no afectados se conservan; no se reescriben innecesariamente.

## Evidencias
- CAMBIOS_FUNCIONES.json: 38 definiciones nuevas o cambiadas, incluidas funciones anidadas; huellas AST antes/después.
- DIFERENCIAS_IMPLEMENTACION.diff: diferencias de implementación contra la base modular equivalente. También contiene cambios de formato de la reconstrucción AST; no toda línea de este diff representa una nueva función.
- INDICE_DEFINICIONES.json: líneas de las definiciones globales en el .py final.
- MANIFIESTO_PRUEBA.json: tamaños y SHA-256 de los archivos de esta entrega.
- RESULTADOS_PRUEBAS.md y registros: resultados y límites de validación.

El código nuevo de coordinación, diario y reparación aparece directamente en el .py bajo los prefijos LN_src_core_trial_workflow y LN_src_core_trial_integrity. Los prefijos conservan trazabilidad de procedencia, sin crear módulos propios en ejecución.

## Documentación heredada
Los documentos de uso, interfaz, mapa y checklist se recrearon para esta edición. Los documentos históricos de publicación/procedencia se conservan marcados como referencia. ORIGEN_ARCHIVOS.json se identifica como inventario histórico modular, no como inventario del paquete de prueba.

## Adenda: cancelación con un clic

La auditoría inicial conserva el inventario de la primera entrega Prueba. El ajuste posterior se detalla en ARREGLO_CANCELACION.md y CAMBIOS_CANCELACION.json: siete definiciones existentes afectadas, once definiciones auxiliares nuevas y ningún cambio en las demás definiciones existentes. El índice y el manifiesto se recalcularon para el archivo final.

## Adenda: DeepL y perfil del compilado

El ajuste posterior se documenta en ARREGLO_DEEPL_Y_COMPILACION.md y AUDITORIA_DEEPL.json. Todas las definiciones Python existentes se conservaron sin cambios; se corrigió la altura de la tarjeta DeepL y el perfil predeterminado al ejecutar un compilado. COMPILAR_PRUEBA.bat se recreó para trabajar directamente junto al .py y excluir configuración personal.

## Adenda: regreso desde MOD durante una traducción

Se sustituyó únicamente la condición de habilitación de la navegación en Main.qml para permitir Traducción (página 0), además de MOD (página 6), durante el trabajo. Todas las definiciones Python, los demás recursos QML y los valores de los idiomas se conservaron. La evidencia, los dos casos nuevos y sus límites están en ARREGLO_NAVEGACION.md, AUDITORIA_NAVEGACION.json y PRUEBAS_NAVEGACION_CODIGO.md. Se actualizaron el registro de pruebas, la validación, los índices y el manifiesto. Los archivos originales y los BAT permanecen intactos.
