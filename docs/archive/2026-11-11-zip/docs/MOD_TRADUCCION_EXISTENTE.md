# MOD TRADUCCION EXISTENTE — estado actualizado

Revisión vigente: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

El runtime v5 registra cadenas en la tabla nativa respetando las traducciones existentes. Cada instalación usa un ámbito privado y un registro que reúne idiomas y conserva el callback previo de forma estable. La regeneración migra copias propias antiguas y sus compilados con respaldo y restauración transaccional. Actualizar el ZIP del traductor requiere regenerar el MOD del juego para aplicar ese cambio.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# El MOD sobre una traducción que no hizo LinguaNova (5 de noviembre de 2026)

## Regla fija

**El MOD nunca toca `game/tl/`.** Ninguna traducción que esté ahí se modifica ni recibe
archivos nuevos, la haya hecho el desarrollador, otra herramienta o el propio traductor de
LinguaNova. Los datos del MOD viven en `game/zz_linguanova/mod/<idioma>/`
(`linguanova_mod_hook_data.json`, `linguanova_mod_manual.json`, informe y copias de
seguridad). Si una versión anterior los dejó en `game/tl/<idioma>/`, se trasladan; si esa
carpeta la había creado el MOD y queda vacía, se borra.

**El idioma del juego manda, también en el futuro.** Cada vez que el juego arranca, el MOD
mira si el juego tiene un idioma con nombre igual o parecido al suyo (`spanish`, `espanol`,
`Español`, `castellano`…) que tenga traducción propia. Si lo hay, el MOD rellena ESE idioma
y retira el suyo del menú. Sirve aunque ese idioma llegue después, con una actualización
del juego o una traducción de fans instalada más tarde, sin volver a generar el MOD. Un
jugador que tenía elegido el idioma del MOD pasa automáticamente al del juego.

Objetivo: que el jugador vea **un único idioma, completo**, como si el juego se hubiera
hecho en él desde el primer día. Si el juego ya trae una traducción (oficial, de fans o
de otra herramienta), el MOD la completa; nunca crea un segundo «Español».

## Cómo encuentra la traducción existente

Busca en `game/tl/` la carpeta que ya contiene el idioma elegido:

1. por el nombre de la carpeta o por el nombre que declara en `translate <idioma>`, con
   todos los nombres que el catálogo conoce, sin mayúsculas ni tildes
   (`spanish`, `es`, `espanol`, `Español`, `castellano`…);
2. si ninguno coincide, por el texto traducido que contiene: el detector sin conexión
   reconoce el idioma (por ejemplo, una carpeta `traduccion_fan`). Una carpeta con el
   nombre de otro idioma (`french`, `chinese`…) nunca se toma por este idioma, aunque
   tenga líneas sin traducir.

Si hay varias, gana la que guarda una traducción real (no solo datos del MOD).

## Qué hace con ella

- Reutiliza sus traducciones (textos de interfaz y diálogo) sin pasarlas por el motor.
- Registra sus propias traducciones con el **mismo nombre de idioma** que usa la
  traducción del juego, así Ren'Py muestra un único idioma.
- En el juego, la traducción existente manda: el MOD solo rellena lo que le falta
  (textos nuevos, pantallas, diálogos sin traducir, textos con variables como
  «Oro: [gold]»).
- Nunca modifica los archivos de esa traducción ni le añade archivos.
- Si un MOD anterior había creado otra carpeta del mismo idioma con solo sus datos (un
  «Español» duplicado en el menú), esa carpeta se mueve a
  `.linguanova_backups/mod_duplicate_languages/` (fuera del juego).

## Nombre en el menú de idiomas

El menú muestra el idioma con su propio nombre («Español»), también cuando la carpeta
se llama de otra forma: una carpeta `traduccion_fan` escrita en español aparece como
«Español», nunca como «Traduccion Fan» (comprobado con Ren'Py 8.3.7).

## Glosario fuera de `tl/`

Ren'Py convierte en idioma del menú **cualquier** carpeta de `game/tl/`, aunque solo
tenga un archivo `.json`. Por eso el glosario vive en
`game/zz_linguanova/glossary/<idioma>.json`. Un glosario guardado en
`tl/<idioma>/linguanova_glossary.json` (entrega anterior) se lee, se pasa a la nueva
ubicación y se borra; si su carpeta queda vacía, también se borra.

## Paquete para compartir

Si la traducción de una carpeta la hizo otra persona y LinguaNova solo dejó ahí los
datos del MOD, el paquete lleva solo los archivos de LinguaNova, no la traducción ajena.

## Comprobación con Ren'Py 8.3.7 real

Juego «The Question» del SDK con su traducción oficial al español (hecha por el equipo
de Ren'Py), más contenido nuevo que esa traducción no cubre: dos líneas de diálogo y una
pantalla de inventario. Motor simulado; el juego se ejecutó de verdad (Xvfb) y se leyó
lo que muestra en español. Cinco casos, en las dos versiones:

| Caso | Traducción existente | Resultado |
|---|---|---|
| normal | `tl/spanish`, `translate spanish` | 9/9 |
| renombrada | `tl/espanol`, `translate espanol` | 9/9 |
| nombre desconocido | `tl/traduccion_fan`, `translate traduccion_fan` | 9/9 |
| carpeta distinta | `tl/es_fan`, `translate spanish` | 9/9 |
| duplicado de un MOD anterior | `tl/espanol` + `tl/spanish` con solo datos del MOD | 10/10 |
| conflictos (copias sin traducir, líneas vacías, corrección manual) | `tl/spanish` alterada | 10/10 |
| actualización futura | el juego no tenía español; se genera el MOD; después el desarrollador añade `tl/espanol` | 11/11 |

En todos los casos se comprobó además que la carpeta de la traducción existente queda
idéntica (ni cambios ni archivos nuevos) y que el MOD no crea ninguna carpeta en
`game/tl/`. En la actualización futura, sin regenerar el MOD: un solo idioma («espanol»),
la preferencia del jugador pasó de «spanish» a «espanol», «Start» mostró la traducción del
desarrollador («Comenzar») y el MOD completó lo que faltaba («Inventario», el diálogo nuevo).

En todos: el MOD reutilizó 146 textos de la traducción existente y tradujo 5; no añadió
ningún idioma al juego; «Start» siguió como «Comenzar» (traducción oficial); «Inventory»
pasó a «Inventario», «Gold: [gold]» a «Oro: [gold]» y la línea nueva de diálogo quedó en
español; el diálogo oficial siguió intacto; ningún archivo de la traducción oficial
cambió; el paquete para compartir no incluyó la traducción oficial.

Antes de este cambio, con la carpeta `tl/espanol` el MOD no veía la traducción oficial,
enviaba 193 textos al motor en lugar de 48 y el juego quedaba con dos idiomas:
«espanol» (oficial, incompleto) y «spanish» (MOD, sin la traducción oficial).
