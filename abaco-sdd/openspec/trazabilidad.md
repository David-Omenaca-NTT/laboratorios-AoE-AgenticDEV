# Trazabilidad entre capabilities y módulos

Este fichero asocia cada capability de `openspec/specs/` con los módulos que la
implementan. Lo mantiene una **persona**, nunca el agente: si lo generase el
mismo motor que produce el código, la comprobación de deriva no valdría nada.

Lo consume `herramientas/gates_sdd.py deriva`.

| Capability | Módulos que la implementan |
|------------|----------------------------|
| `salud` | `src/abaco/api/app.py` |
| `demanda` | `src/abaco/dominio/estados.py`, `src/abaco/dominio/modelos.py` |
| `asignacion` | `src/abaco/reglas/motor.py`, `src/abaco/auditoria.py` |
| `ocupacion` | `src/abaco/reglas/ocupacion.py`, `src/abaco/reglas/politicas.py` |
| `ocupacion-heredada` | `src/abaco/legado/calculadora_utilizacion_v1.py` |
| `agente-staffing` | `agentes/staffing/agente.py`, `agentes/staffing/agente_v0.py`, `agentes/staffing/evaluar.py`, `agentes/mcp_abaco/servidor.py` |
| `gobierno-agentes` | `herramientas/gates_sdd.py`, `.github/workflows/gate-manifiesto.yml` |
| `operacion` | `src/abaco/api/app.py` |

## Cómo se lee una desviación

| Síntoma | Qué significa |
|---------|---------------|
| Capability sin módulo | Hay requisitos escritos que nadie implementó. O sobra la spec, o falta el código |
| Módulo sin capability | Hay código que ningún requisito justifica. Es la deriva más peligrosa: nadie lo pidió y nadie lo revisará |

El umbral está en el 5%. Por encima, el pipeline bloquea.
