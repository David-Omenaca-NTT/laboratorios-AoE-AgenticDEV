# Flotilla de agentes sobre el contexto de Ábaco

```
                    ┌──────────────────────┐
                    │  MCP abaco-contexto  │
                    │  specs, trazas,      │
                    │  catálogo, política  │
                    └──────────┬───────────┘
             ┌─────────────────┼──────────────────┐
             │                 │                  │
     ┌───────▼──────┐  ┌───────▼───────┐  ┌───────▼───────┐
     │  staffing    │  │  conflictos   │  │   banquillo   │
     │     N2       │  │      N3       │  │      N2       │
     │ propone      │  │ detecta       │  │ alerta        │
     └───────┬──────┘  └───────┬───────┘  └───────┬───────┘
             │                 │                  │
             └─────────── decisión humana ────────┘
```

## Por qué los tres no tienen el mismo techo

Es el entregable intelectual de la estación.

| Agente | Techo | Motivo |
|--------|-------|--------|
| conflictos | N3 | Detecta hechos verificables (solapes, sobreasignaciones). No nombra a nadie como candidato ni condiciona ninguna decisión sobre una persona. Puede abrir PR en rama aislada porque el peor caso es un PR que se rechaza |
| staffing | N2 | Propone personas. El peor caso no es un PR malo: es que alguien no entre en un proyecto que le habría venido bien |
| banquillo | N2 | No propone, pero señala personas por su nombre. Una lista de "gente sin asignación" leída sin contexto se convierte en una lista de gente prescindible |

La regla que resume las tres filas: **el techo lo fija el radio de daño, no la
precisión**.

## Handoff

| De | A | Cuándo | Qué pasa |
|----|---|--------|----------|
| conflictos | staffing | Detecta sobreasignación | Persona y periodo, para excluirla de propuestas |
| banquillo | staffing | Hay demanda abierta compatible | Persona y skills |

## Resolución de conflicto

Cada ruta tiene un único agente con permiso de escritura. `src/abaco/reglas/` no
lo escribe ningún agente: solo humano. Si dos agentes necesitan la misma ruta, se
para la ejecución y decide la persona.
