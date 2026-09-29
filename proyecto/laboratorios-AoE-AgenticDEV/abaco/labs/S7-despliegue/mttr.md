# Fallo inducido: dos rondas

Fallo recibido: la variable de entorno del catálogo de categorías apunta a una
versión que no existe. El healthcheck sigue en verde y solo falla el endpoint de
evaluación de candidatos.

## Ronda 1, sin asistencia de agente

| Momento | Evento |
|---------|--------|
| 00:00 | Pipeline en rojo tras el despliegue |
| 00:05 | Hipótesis inicial: fallo en la carga del corpus |
| 00:22 | Hipótesis descartada: el corpus carga bien |
| 00:34 | Causa real: versión de catálogo inexistente en la variable de entorno |
| 00:41 | Corregido y verde |

**MTTR ronda 1: 41 minutos.** La hipótesis inicial fue incorrecta y costó 22.

## Ronda 2, con el agente de triaje

| Momento | Evento |
|---------|--------|
| 00:00 | Pipeline en rojo |
| 00:03 | El agente clasifica como fallo de configuración, no de código: fallan los tests que cargan catálogo y pasan los de la máquina de estados |
| 00:07 | Hipótesis dirigida a configuración, confirmada |
| 00:15 | Corregido y verde |

**MTTR ronda 2: 15 minutos.**

## Lo que aprendí

El agente no escribió una línea del parche. Redujo el espacio de búsqueda en los
tres primeros minutos. Mi error en la ronda 1 fue empezar a probar antes de leer
qué tests fallaban y cuáles seguían pasando, que era la información que separaba
código de configuración desde el minuto uno.
