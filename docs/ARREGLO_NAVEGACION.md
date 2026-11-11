# ARREGLO NAVEGACION — estado actualizado

Revisión vigente: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

Se conserva la navegación entre Traducción y MOD y el comportamiento previo del modo avanzado. La revisión actual modifica el título visible y el runtime generado; no sustituye esa lógica. Los resultados antiguos de navegación se conservan como antecedentes y se distinguen de la carga completa actual de la interfaz en Linux.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# Regreso a Traducción durante una operación

## Causa
La regla de navegación de Main.qml habilitaba únicamente MOD (página 6) durante una traducción. Al abrir MOD, Traducción (página 0) quedaba deshabilitada y no se podía regresar a su seguimiento ni al botón Detener.

## Cambio único de comportamiento
Se sustituyó la condición completa del botón de navegación:

```qml
// Antes
enabled: !isTranslating || pageIndex === 6
// Ahora
enabled: !isTranslating || pageIndex === 0 || pageIndex === 6
```

Traducción y MOD permanecen accesibles durante el trabajo. Cambiar entre ambas páginas no inicia, detiene ni reinicia la operación. Los selectores de juego, idioma y motor conservan sus bloqueos propios; las demás páginas conservan el bloqueo durante la traducción. Desde Traducción se puede consultar el progreso y pulsar Detener con el comportamiento de cancelación anterior.

No se modificaron definiciones Python, motores, traducciones de la interfaz, opciones de MOD, guardado de claves, cancelación ni compiladores. AUDITORIA_NAVEGACION.json registra la comparación AST de todas las definiciones Python y la comparación de los recursos integrados: únicamente cambia la condición anterior y su comentario explicativo en Main.qml.

## Verificación
Dos casos nuevos cargan la interfaz QML real con sus backends, en modo sencillo y avanzado. Cada caso simula una traducción activa sin red, realiza tres recorridos Traducción → MOD → Traducción, comprueba que sigue siendo la misma operación y que los demás bloqueos se mantienen. Después pulsa el botón Detener real, comprueba una sola solicitud de cancelación y la recuperación de controles al finalizar.

La batería acumulada termina con 483 pruebas aprobadas y 1 omitida. Se conserva sintaxis compatible con Python 3.10 y cero importaciones de archivos propios. Los comentarios INICIO/FIN, sus índices, el manifiesto y las huellas de los originales se validaron de nuevo.

Entorno: Python 3.12/Linux, Qt offscreen. La actividad del trabajador se simula para probar la navegación; no se enviaron traducciones a proveedores. No se ejecutó un juego completo ni un .exe en Windows. Ver PRUEBAS_NAVEGACION_CODIGO.md y REGISTRO_PRUEBAS.txt.
