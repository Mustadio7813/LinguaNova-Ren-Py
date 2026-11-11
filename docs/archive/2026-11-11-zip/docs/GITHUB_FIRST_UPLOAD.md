# GITHUB FIRST UPLOAD — estado actualizado

Revisión vigente: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

La fuente actual es el archivo integrado, con sus recursos, BAT y licencias. Publicar únicamente los archivos que corresponden al proyecto, excluyendo claves, perfiles, entornos y respaldos de juegos. Las rutas, hashes y resultados actuales se consultan en el manifiesto y en los resultados de esta revisión; las instrucciones anteriores de una estructura modular se conservan solo como antecedentes.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

> Referencia heredada del proyecto modular 1.5.5. Para esta copia de prueba, prevalecen `LEEME_PRUEBA.md`, `MAPA_DEL_PROYECTO.md` y `AUDITORIA_CAMBIOS.md`. Las rutas src/ y recetas de publicación de este documento no describen el paquete plano.

# Primera publicación de LinguaNova en GitHub

Este documento está pensado para crear un repositorio **nuevo** llamado `LinguaNova`, no un fork visible de GitHub.

La procedencia de RenLocalizer se conserva explícitamente mediante `README.md`, `NOTICE.md`, `UPSTREAM.md`, `LICENSE`, `COPYING` y el registro de modificaciones.

## 1. Crear el repositorio

En GitHub:

1. pulsa **New repository**;
2. nombre: `LinguaNova`;
3. elige la visibilidad deseada;
4. **no marques** “Add a README”;
5. **no añadas** una licencia desde el asistente;
6. **no añadas** un `.gitignore` desde el asistente;
7. crea el repositorio vacío.

Este paquete ya contiene esos archivos y evita que GitHub genere versiones diferentes.

## 2. Subir este árbol completo

La forma más sencilla para un proyecto de este tamaño es GitHub Desktop o Git.

No subas únicamente el `.exe`: el repositorio debe contener el código fuente.

## 3. Primer commit recomendado

Mensaje:

`Initial LinguaNova publication with upstream attribution and GPL notices`

## 4. Antes de hacerlo público

Ejecuta:

```bash
python scripts/check_repository_compliance.py
```

y revisa `docs/RELEASE_CHECKLIST.md`.

## 5. Configuración recomendada de GitHub

En Settings:

- habilita Issues;
- habilita Discussions solo si realmente se usarán;
- habilita Dependabot alerts cuando estén disponibles;
- habilita Secret scanning / Push protection cuando tu plan/repositorio lo permita;
- habilita Private vulnerability reporting;
- configura la rama principal y protección de rama cuando el flujo esté estable.

## 6. No activar todavía el actualizador público

Esta revisión conserva la fuente pública de actualizaciones sin configurar.

No apuntes temporalmente a RenLocalizer.

Cuando exista el repositorio oficial y se haya probado el sistema de actualización, configura exclusivamente el canal de LinguaNova.

## 7. Primera Release

No publiques una Release binaria hasta terminar:
- compilación;
- auditoría de dependencias empaquetadas;
- pruebas del instalador/portable;
- código fuente correspondiente;
- sumas SHA-256.

Consulta `docs/RELEASE_CHECKLIST.md`.
