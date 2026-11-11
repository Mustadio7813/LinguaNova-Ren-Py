# Revisión actual de cobertura y Revisar

La recuperación posterior al lote principal consulta el cooldown del motor. Su política de respaldo es independiente de la del MOD. Consulta [Cobertura, recuperación e informe](ARREGLO_PORCENTAJE_Y_RECUPERACION.md).

---

# CORRECCION MOD Y MOTORES — estado actualizado

Revisión anterior: **2026-11-05_MODv5**. Paquete: **LinguaNova_Desarrollador.zip**. Título: **Traductor de Ren'Py**. Runtime del MOD: **v5**.

## Información vigente

El intercambio de argumentos de Bing se corrigió pasando configuración y proxies por nombre. Los seis motores se comprobaron con referencias correctas y respuestas simuladas. La protección común detecta errores internos directos o encapsulados y conserva los reintentos temporales. La recursión del juego se corrigió por separado en el runtime v5: no era una cuota ni otro fallo de Bing.

La [guía completa](GUIA_COMPLETA.md), el [historial](HISTORIAL_CAMBIOS.md) y los [resultados actuales](RESULTADOS_PRUEBAS.md) son las referencias de esta entrega.

## Antecedente conservado

El contenido siguiente describe revisiones anteriores. Las rutas, nombres y mediciones antiguos no sustituyen la información vigente de arriba.

---

# Revisión del MOD y sus motores — 5 de noviembre de 2026

## Causa del error recibido

Bing llamaba al constructor común con dos argumentos posicionales. El constructor común espera primero la clave de API, después el gestor de proxies y por último la configuración. Como resultado, Bing guardaba el objeto ConfigManager como gestor de proxies y fallaba al llamar a get_next_proxy().

El registro repetía el mismo error al procesar lotes y al reintentar sus textos individualmente. El contador de textos pendientes no significa que el motor esté recuperándose de ese error.

## Cambios

- Bing transmite proxy_manager y config_manager mediante sus nombres correctos.
- El constructor compartido comprueba que el gestor de proxies tenga el método esperado antes de iniciar solicitudes. La comprobación cubre todos los motores que lo heredan.
- El gestor de traducción distingue errores internos de los fallos transitorios de transporte. Un AttributeError/TypeError interno, o su equivalente dentro de un resultado fallido, se propaga y no se convierte en cientos de solicitudes individuales.
- El MOD conserva esa distinción en sus reintentos y muestra un mensaje localizado con la causa técnica. Las tareas pendientes se cancelan y se espera su cierre al detener el trabajo por un error.
- Se mantienen los reintentos existentes para fallos temporales de red y la validación de traducciones.
- Se conservaron las correcciones anteriores del cuadro final, la notificación temporal y los botones Quit/Exit → Salir.

## Revisión de motores

| Motor | Configuración y proxies | Integración del MOD |
| --- | --- | --- |
| Google | Referencias verificadas | Registro separado y manejo común verificados |
| Bing | Constructor corregido y referencias verificadas | Respaldo Google verificado; solicitud y generación probadas |
| DeepL | Referencias verificadas | Registro separado y manejo común verificados |
| OpenAI | Referencias verificadas | Registro separado y manejo común verificados |
| DeepSeek | Referencias verificadas | Variante de OpenAI verificada |
| Gemini | Referencias verificadas | Respaldo Google y registro separado verificados |

## Validación

Las pruebas usan claves ficticias y respuestas simuladas: no consumen servicios de pago ni verifican credenciales reales. Se ejercitaron los constructores reales y la fábrica del MOD para los seis motores, los errores directos y los errores encapsulados en resultados, los reintentos transitorios, la cancelación de tareas y los mensajes en los cinco idiomas de la aplicación.

Se generó un MOD con 451 textos mediante el escáner real, el adaptador de Bing y el gestor de traducción, con una sesión HTTP simulada. Se comprobó que un error interno posterior detuviera el proceso, conservara el archivo del MOD anterior y no modificara screens.rpy. Se verificó la sintaxis Python y que los cambios se limitaran a los motores, su gestión de errores y la integración del MOD.

No se ejecutó el juego del usuario: solo se recibió su registro de errores.

## Uso de esta revisión

Cierra la ejecución anterior del traductor, extrae esta revisión y vuelve a iniciarla con INICIAR.bat. Después vuelve a generar el MOD del juego. Los cambios de código no se aplican a una ejecución que ya estaba abierta.
