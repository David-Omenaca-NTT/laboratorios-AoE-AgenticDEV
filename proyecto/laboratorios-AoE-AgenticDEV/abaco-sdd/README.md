# Proyecto Ábaco, modalidad SDD estricta

Núcleo de capacidad, demanda y asignación de personas a proyectos, construido
**sin escribir implementación a mano**. Todo el código se deriva de
especificaciones con [OpenSpec](https://github.com/Fission-AI/OpenSpec).

Es la tercera modalidad del laboratorio del AoE Agentic DevOps. Mismo dominio
que Ábaco, disciplina radicalmente distinta.

- Si eres student: empieza por [PLAYBOOK.md](PLAYBOOK.md) y ten a mano [GUIA-SDD.md](GUIA-SDD.md).
- Si buscas la referencia de una etapa: `openspec/changes/archive/`.

## Arranque

```bash
npm install -g @fission-ai/openspec@1.8.0     # versión fijada a propósito
pip install -r requirements.txt
export OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1    # política, no preferencia

python3 herramientas/generar_corpus.py
openspec list --specs                          # las capabilities
openspec validate --all                        # 8 specs válidas
python3 -m pytest aceptacion/ -q               # 72 tests
python3 -m herramientas.gates_sdd todos        # 4 puertas
```

## La regla

> **El código no se parchea. Se regenera.**

Si un test falla, no se abre el fichero de implementación: se busca qué requisito
faltaba, se enmienda la especificación y se vuelve a generar.

Se escribe a mano en dos sitios y solo en dos:

| Ruta | Qué es |
|------|--------|
| `openspec/` | Los requisitos y escenarios. Es la especificación, es el trabajo |
| `aceptacion/` | La batería externa. Es el examen, y el examinado no lo escribe |

## La referencia por etapa

Es para lo que existe este repositorio. Diez cambios archivados, uno por etapa
del curso, cada uno con sus cuatro artefactos completos y una nota didáctica.

| Etapa | Cambio archivado | Qué enseña |
|-------|------------------|------------|
| E1 | `2026-09-08-e1-salud-servicio` | El cambio mínimo bien hecho |
| E2 | `2026-09-18-e2-ciclo-vida-demanda` | Una máquina de estados como escenarios |
| E3 | `2026-09-29-e3-cancelacion-demanda-asignada` | Deltas, y **un error real que la herramienta detectó** |
| E4 | `2026-10-13-e4-motor-asignacion` | Restricciones duras con escenarios de frontera |
| E5 | `2026-10-27-e5-ocupacion-utilizacion` | **La ambigüedad del curso, resuelta y documentada** |
| E6 | `2026-11-13-e6-agente-propuesta-staffing` | Un agente y su techo de autonomía, especificados |
| E7 | `2026-11-24-e7-caracterizacion-legado` | Describir un sistema heredado antes de tocarlo |
| E7b | `2026-11-27-e7b-correccion-utilizacion-heredada` | Corregirlo avisando del impacto |
| E8 | `2026-12-04-e8-gobierno-agente` | Gobierno como puertas automáticas |
| E9 | `2026-12-11-e9-reversion-y-observabilidad` | Operación y reversión |

```bash
cat openspec/changes/archive/2026-10-27-e5-ocupacion-utilizacion/LEEME.md
```

## Estado verificado

Todo lo de abajo se ha ejecutado en este repositorio, no es aspiracional.

| Comprobación | Resultado |
|--------------|-----------|
| OpenSpec | 1.8.0, instalado y ejecutado de verdad |
| `openspec validate --all` | 8 capabilities válidas |
| Cambios archivados | 10, archivados con `openspec archive` |
| Capabilities generadas por la herramienta | `salud`, `demanda`, `asignacion`, `ocupacion`, `ocupacion-heredada`, `agente-staffing`, `gobierno-agentes`, `operacion` |
| Requisitos y escenarios | 46 requisitos, 85 escenarios |
| Batería de aceptación externa | 72 tests en verde |
| Puerta de procedencia | En verde sobre el historial real |
| Puerta de aceptación | En verde |
| Puerta de deriva | 0,0% (umbral 5%) |
| Puerta de densidad | Media de 1,8 escenarios por requisito |

## Las cuatro puertas

```bash
python3 -m herramientas.gates_sdd todos
```

| Puerta | Qué detecta |
|--------|-------------|
| `procedencia` | Commits sobre `src/` sin `Change-Id` válido. Es la que detecta el parcheo silencioso |
| `aceptacion` | Commits generados que tocan `aceptacion/`. Sostiene toda la modalidad |
| `deriva` | Capabilities sin código y código sin capability |
| `densidad` | Escenarios por requisito fuera de rango |

## Hallazgos que el mentor debe conocer

1. **La herramienta detectó un error real al construir E3.** El bloque MODIFIED
   dejaba fuera un escenario existente, y `archive` lo rechazó con un mensaje
   explícito. Está documentado en el `LEEME.md` de ese cambio y es la mejor
   lección sobre deltas del repositorio. Nota importante: **`openspec validate`
   no lo detecta, solo `archive`**.
2. **`/opsx:verify` no bloquea el archivado.** Lo dice la documentación oficial.
   Por eso existe la batería de aceptación externa y por eso el pipeline sí
   bloquea.
3. **La telemetría de OpenSpec va desactivada por política.** Está en el
   devcontainer, en el pipeline y declarada en `AGENTS.md`.
4. **La versión está fijada en 1.8.0.** La herramienta cambió su flujo hace poco
   y va por versiones cada pocas semanas. Un cambio de comandos a mitad de
   cohorte descarrila el laboratorio.

## Cómo se deriva el repo del student

| Paso | Acción |
|------|--------|
| 1 | Vaciar `openspec/specs/` y `openspec/changes/`, conservando el archivo como referencia de consulta |
| 2 | Reescribir los requisitos de E5 en su forma ambigua y vaciar su apartado de decisiones |
| 3 | Vaciar `src/`, `agentes/` y `aceptacion/` |
| 4 | Conservar íntegros: `politicas/`, generador de corpus, módulo heredado, gates, labs, guía y CLI |
| 5 | Dejar el archivo de cambios accesible pero en solo lectura |

El archivo de cambios **no se toca**: es la referencia por etapa y es la razón de
ser de este repositorio.

## Lo que esta modalidad no enseña

Escribir implementación desde cero, y depurar con un depurador. Se compensa con
los ejercicios de arqueología de E4 y E7.

Y la advertencia principal, que el student comprueba en E5:

> SDD no protege de una especificación equivocada. La ejecuta más rápido y de
> forma más coherente.
