<!-- 2026-11-11_ALIGERAR_JUEGO -->
# Revisión actual: Aligerar el juego (11 de noviembre de 2026)


- [x] Código nuevo en módulos propios, sin parches sobre funciones existentes; anclajes de inserción únicos.
- [x] Misma modificación en las dos ediciones; las diferencias entre ediciones son las mismas que antes.
- [x] Tarjeta cargada en Qt sin pantalla, sin avisos QML, en los cinco idiomas.
- [x] Flujo completo probado: estimar, crear copia, detener sin dejar copias a medias, original intacto.
- [x] Descarga de ffmpeg probada con servidor local (huella correcta e incorrecta).
- [x] Avisos de terceros y modificaciones GPL actualizados.
- [ ] Compilar con los dos BAT en Windows y probar: procesos `spawn` en el EXE portable, carpeta `ffmpeg` en la versión en carpeta y descarga real desde gyan.dev.
- [ ] Probar una copia optimizada con un juego Ren'Py real (Ren'Py 7 y 8).

---

# Revisión actual de cobertura y Revisar

Para esta revisión, consulta [Resultados de las pruebas](RESULTADOS_PRUEBAS.md) antes de citar pruebas de Windows, Qt o Ren’Py.

---

# RELEASE CHECKLIST — estado actualizado

Revisión anterior: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

Antes de distribuir, comprobar el manifiesto, los JSON, la sintaxis de fuente y pruebas, el título exacto y el registro de pruebas actual. Las pruebas del SDK 7.4.4 en Linux se separan de las comprobaciones pendientes en el juego completo y Windows nativo. Conservar avisos de licencia y excluir datos privados. No presentar antecedentes históricos como pruebas recién ejecutadas.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# Comprobación de la entrega Prueba

- [x] Trabajo realizado en una copia; originales verificados por SHA-256.
- [x] Un único .py sin imports de archivos propios.
- [x] Sustituciones activas únicas, sin wrappers que deleguen en versiones antiguas.
- [x] QML y diccionarios de los cinco idiomas integrados.
- [x] Interfaz cargada desde una carpeta que contiene únicamente el .py.
- [x] Pruebas automáticas de regresión y del flujo nuevo; ver RESULTADOS_PRUEBAS.md.
- [x] Reproducción del duplicado Click to play the video.
- [x] Respaldos fuera de game/ y protección frente a rutas/enlaces inseguros.
- [x] Diario de operación separado de la caché de traducción.
- [x] Comprobación de lanzamiento después de cambios en archivos y fuentes.
- [ ] Ejecutar la aplicación con el juego Valley_Awakening completo proporcionado por el usuario; aquí solo se dispone del traceback.
- [ ] Ejecutar compilación PyInstaller y pruebas de .exe en Windows.
- [ ] Verificar visualmente en Ren’Py real el encadenamiento de callbacks en distintas versiones y los menús particulares de cada juego.
- [ ] Pruebas de usabilidad con usuarios nuevos.

Las casillas pendientes son límites de validación, no comprobaciones que se declaren aprobadas.
