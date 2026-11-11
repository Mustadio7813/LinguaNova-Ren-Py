# GLOSARIO — estado actualizado

Revisión vigente: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

El glosario sigue separado por juego y por idioma. Esta revisión conserva sus rutas y prioridades. Las correcciones manuales y los términos explícitos se respetan; el uso de un nombre de paquete distinto no convierte el glosario en global. La migración de scripts del MOD no elimina sus JSON.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# Glosario por juego y por idioma (5 de noviembre de 2026)

## Dónde se guarda

Cada juego y cada idioma de destino tienen su propio glosario, dentro del juego:

```
game/zz_linguanova/glossary/spanish.json
game/zz_linguanova/glossary/french.json
```

No se guarda en `game/tl/`: Ren'Py convierte cada carpeta de `tl/` en un idioma del
menú del juego, aunque solo tenga un `.json`. Un glosario de la entrega anterior en
`tl/<idioma>/linguanova_glossary.json` se lee, se pasa aquí y se borra (y su carpeta, si
queda vacía).

Así un término del español nunca aparece en el francés, y los términos de un juego
nunca pasan a otro. El archivo viaja en el paquete para compartir (dentro de `zz_linguanova`).
El traductor y el MOD usan el mismo archivo; si un juego todavía tiene el archivo
antiguo del MOD (`linguanova_mod_glossary.json`), se lee y el siguiente guardado
crea el nuevo.

El glosario único de antes (`glossary.json` en la carpeta de datos de LinguaNova) ya
no se lee ni se escribe. Si tenías términos ahí, elige el juego y el idioma y usa
«Importar» en la página del glosario para pasarlos al glosario de ese juego e idioma.

Formato:

```json
{
  "schema": 1,
  "help": "...",
  "language": "spanish",
  "terms": {
    "Eileen": "Eileen",
    "Shadow Sword": "Espada Sombría",
    "Mana": ""
  }
}
```

- igual en los dos lados: se conserva sin traducir (nombres);
- con traducción: se usa siempre esa traducción;
- vacío: término pendiente; se guarda, pero no se aplica hasta que lo rellenes.

## Cómo se usa

1. Elige el juego (`.exe`) y el idioma de destino. La cabecera de la página del
   glosario dice cuál estás editando, por ejemplo «Glosario de MiJuego · Español».
2. Al elegir el juego, LinguaNova analiza el juego completo: los `.rpy`, los `.rpyc`
   sin fuente y lo que hay dentro de los `.rpa`. El resultado (nombres de personajes y
   términos con mayúscula que se repiten) queda **solo en memoria** mientras el
   programa está abierto. No se escribe nada en disco.
3. Al traducir, los nombres de ese análisis se conservan siempre sin traducir, aunque
   no los hayas añadido al glosario.
4. «Extraer del proyecto» añade al glosario de ese juego e idioma los nombres (ya
   rellenados) y los términos frecuentes (vacíos, para que decidas su traducción).
5. Cambia el idioma de destino y verás otro glosario, vacío al principio.

Cada traducción carga el glosario de su juego y su idioma. Si se traducen varios
idiomas seguidos, cada uno usa el suyo.

## Comprobación

- Juego de prueba compilado con el SDK de Ren'Py 8.3.7; el personaje «Marcus» solo
  existe dentro de un `.rpa`, como `.rpyc` sin fuente. El análisis lo encontró (la
  versión anterior solo leía `.rpy` y no lo veía) y no escribió nada en disco.
- Glosario español `Shadow Sword → Espada Sombría` y francés
  `Shadow Sword → Épée de l'Ombre`. Se tradujo con el pipeline real (la consola) a
  ambos idiomas con un motor simulado: el español salió con «Espada Sombría», el
  francés con «Épée de l'Ombre», ninguno con el término del otro, y el motor nunca
  recibió «Eileen» ni «Marcus» sin proteger.
- En la interfaz real: el término añadido con el español no aparece al cambiar a
  francés, cada idioma guarda su archivo y al volver al español sigue ahí; no se crea
  ninguna carpeta en `game/tl/`.
- El MOD lee el archivo antiguo, conserva los términos pendientes y no los aplica.

No se usaron motores de traducción reales.
