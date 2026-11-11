# ARREGLO DEEPL Y COMPILACION — estado actualizado

Revisión vigente: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

Se conservaron las correcciones previas de DeepL y el aislamiento de claves de compilación. Sus referencias de configuración y proxies se verificaron con el resto de motores. Los resultados antiguos de esta área son históricos; no representan una nueva llamada con credenciales ni una nueva compilación de Windows. Consultar los registros actuales para las pruebas ejecutadas.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# DeepL visible y compilación sin configuración personal

## Causa confirmada
Los controles de la clave ya estaban implementados, pero la tarjeta del motor medía 135 px y recortaba su contenido. En la reproducción, el campo y los botones empezaban en y=130 y tenían 36 px de alto: quedaban fuera del área visible.

## Corrección mínima
Solo cuando el motor seleccionado es DeepL, la tarjeta adapta su altura al contenido. Las alturas de los demás motores conservan 135/228 px. No se cambió ninguna función Python de traducción, API, guardado, MOD o cancelación, ni los textos existentes. Se añadió un id al layout para medir su altura implícita.

## Uso de la clave
1. Abrir Traducir y elegir DeepL como motor.
2. Debajo de los selectores aparece Clave API de DeepL.
3. Pegar o escribir la clave y pulsar Guardar. Guardar se habilita al introducir texto.
4. Para reemplazarla, pegar otra clave y volver a Guardar.
5. Eliminar se habilita cuando existe una clave guardada y la retira de esa configuración local.

Funciona en modo sencillo y avanzado. La clave completa no vuelve a mostrarse en el campo después de guardarla; se conserva el indicador enmascarado existente.

## Compilación y claves
La API introducida desde la interfaz se guarda en el archivo de configuración local del usuario, no en el código fuente. El BAT compila únicamente el .py y sus dependencias/recursos. No usa --add-data para incorporar carpetas personales ni copia config.json, AppData o .env al ejecutable.

El perfil predeterminado del .py sigue siendo LinguaNova/Prueba_1.5.5. El ejecutable usa ahora LinguaNova/Prueba_1.5.5_Compilado. Por eso no carga automáticamente la clave guardada durante las pruebas del .py, incluso en el mismo equipo. Se verificó esa separación simulando el arranque congelado; no se produjo un .exe Windows aquí.

Guardar en el ejecutable seguirá guardando la clave que introduzca su usuario en su propio perfil local para sesiones posteriores. No es almacenamiento dentro del .exe ni una promesa de almacenamiento cifrado. Un LINGUANOVA_DATA_DIR establecido explícitamente por un usuario avanzado sigue siendo una elección de ese usuario; el BAT lo limpia dentro de su proceso de preparación.

El archivo COMPILAR_PRUEBA.bat se puede usar con solo el .py al lado, sin INICIAR_PRUEBA.bat. Prepara .venv_prueba_155, utiliza un directorio de trabajo propio y genera dist/LinguaNova_155_Prueba. No reutiliza un spec editado que pudiera añadir archivos privados.

## Verificación
- Reproducción del recorte de los tres controles antes del arreglo.
- Controles completos dentro de la tarjeta después del arreglo.
- 20 combinaciones de dos tamaños de ventana, modo sencillo/avanzado y cinco idiomas.
- Guardado, reemplazo y eliminación usando únicamente claves ficticias; persistencia comprobada con una nueva lectura de configuración. Ninguna llamada de validación a la API de DeepL.
- Cinco pruebas de perfiles y del BAT: separación, ausencia de la clave del perfil fuente, conservación de overrides explícitos y compilación únicamente desde el código.
- Regresión completa seleccionada: 481 aprobadas, 1 omitida por falta de una fuente de pruebas.

No se ejecutó el BAT ni PyInstaller en Windows. Las pruebas de interfaz fueron en Qt offscreen/software en Linux. Se mantienen las advertencias preexistentes de implicitWidth de dos diálogos ajenos al arreglo.
