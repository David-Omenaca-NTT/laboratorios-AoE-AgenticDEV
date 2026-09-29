# Comparativa de motores de agente: Claude Code frente a OpenCode

Criterios definidos ANTES de ejecutar, para no escribirlos después justificando
la herramienta que ya me gustaba.

Encargo idéntico: implementar CA-06 de SPEC-002 (sobreasignación como indicador
propio) con su test, sin tocar nada fuera del alcance de la spec.

| Criterio | Claude Code | OpenCode | Peso |
|----------|-------------|----------|------|
| Control de permisos por ruta | Allowlist y hooks nativos, deniega por defecto | Configurable, menos granular | Alto |
| Bloqueo de campos de perfil prohibidos | Se puede forzar por hook determinista | Requiere convención propia | **Crítico en este proyecto** |
| Calidad del primer diff | Respetó el alcance y propuso el caso del corte al 100% | Correcto, no propuso el caso límite | Alto |
| Portabilidad de modelo | Ligada al proveedor | Multi-modelo, cambia con una variable | Medio |
| Trazabilidad de lo ejecutado | Registro de comandos y ediciones | Menor detalle | Alto |

## Criterio de elección defendible

En este proyecto manda una restricción por encima de las demás: hay datos de
personas y hay campos que ningún agente puede leer. Eso empuja a Claude Code,
porque el bloqueo se hace determinista con un hook y no depende de que el agente
respete una instrucción.

Si el proyecto no tuviera datos personales, la elección se decidiría por coste y
portabilidad, y ahí OpenCode gana. Lo que se vende no es la herramienta: es saber
qué restricción del cliente manda.
