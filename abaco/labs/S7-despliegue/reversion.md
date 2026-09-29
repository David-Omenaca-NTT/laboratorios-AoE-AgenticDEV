# Procedimiento de reversión

| Paso | Acción | Tiempo objetivo |
|------|--------|-----------------|
| 1 | Detectar: alerta de healthcheck o pipeline en rojo tras el despliegue | < 2 min |
| 2 | Decidir: revertir primero, diagnosticar después. No se depura en producción | < 1 min |
| 3 | Ejecutar: redesplegar la etiqueta de imagen anterior | < 3 min |
| 4 | Verificar: healthcheck en verde y prueba de humo del alta de demanda | < 2 min |
| 5 | Registrar: entrada en bitácora con hora de detección y de recuperación | posterior |

Objetivo de recuperación: 8 minutos. Probado el día del despliegue, no el día del
incidente. Una reversión que no se ha ensayado no existe.

Nota propia de este sistema: como el agente de staffing no crea asignaciones, una
reversión nunca deja datos inconsistentes de asignación. Es una consecuencia
directa del techo N2 que no había previsto al ponerlo.
