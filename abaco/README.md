# Proyecto Ábaco

Núcleo de capacidad, demanda y asignación de personas a proyectos. Es el segundo
proyecto vertebrador del laboratorio del AoE Agentic DevOps, derivado del PRD de
la plataforma PPM.

**Este repositorio es la referencia resuelta del repositorio de aprendizaje.** El
que recibe el student trae la spec ambigua sin resolver, el agente en su versión
v0 y las estaciones sin completar. El repositorio de producto, con datos reales,
es otro y no se deriva de este.

- Si eres student: empieza por [PLAYBOOK.md](PLAYBOOK.md).
- Si eres mentor o Lead: sigue leyendo.

## Arranque

```bash
pip install -r requirements.txt
python3 herramientas/generar_corpus.py    # corpus sintético determinista
make test                                 # 75 tests
python3 -m abaco_cli estado               # progreso del laboratorio
python3 -m agentes.staffing.evaluar       # seguridad, utilidad y concentración
```

## Diferencia con Aula

| Dimensión | Aula | Ábaco |
|-----------|------|-------|
| Objeto del agente | El SDLC: conformidad de un PR con su spec | El dominio: propuesta de staffing |
| Si se equivoca, daña | Código | La carrera de una persona |
| Techo de autonomía | N3 | **N2 permanente, forzado por el gate** |
| Métrica del agente | Precisión y recall | Seguridad, utilidad y concentración, separadas |
| Datos | Sintéticos | Sintéticos en aprendizaje, **reales en producto** |
| Conversación de gobierno | Con un CTO | Con seguridad, legal y personas |

## Estructura

| Ruta | Contenido |
|------|-----------|
| `src/abaco/dominio/` | Modelos y máquina de estados de la demanda (8 estados del PRD) |
| `src/abaco/reglas/motor.py` | Motor de asignación: capacidad, categoría, skill, disponibilidad |
| `src/abaco/reglas/ocupacion.py` | Utilización, sobreasignación, cobertura, banquillo |
| `src/abaco/reglas/politicas.py` | Catálogos de categorías y políticas versionados por vigencia |
| `src/abaco/legado/` | Calculadora heredada con comportamientos ocultos, más `DESVIACIONES.md` |
| `src/abaco/auditoria.py` | Traza con campo `origen`: las decisiones del agente se auditan igual |
| `politicas/categorias/` | CAT-2024 y CAT-2026. Dos versiones para que el versionado sea real |
| `specs/` | SPEC-001 asignación, SPEC-002 ocupación, SPEC-003 demanda |
| `agentes/mcp_abaco/` | Servidor MCP en stdlib puro, 6 herramientas |
| `agentes/staffing/` | Agente de propuesta, su v0 y el evaluador de tres métricas |
| `evals/dorado_ejemplo/` | 15 demandas con la elección humana etiquetada |
| `manifiestos/` | Agent Release Manifest con los 6 apartados de gobierno sobre personas |
| `labs/` | 10 estaciones: guía, criterios, verificador, 3 pistas, referencia |
| `abaco_cli/` | CLI y biblioteca de verificación, reutilizados de Aula sin cambios |

## Estado verificado de la referencia

| Comprobación | Resultado |
|--------------|-----------|
| Suite de tests | 75 en verde |
| Trazabilidad SPEC-001 / 002 / 003 | 100% de criterios cubiertos |
| Verificadores de estación | **79 criterios automáticos, todos en verde** |
| Mutación sobre `reglas/ocupacion.py` | 3 mutaciones aplicadas, 3 detectadas |
| Equivalencia legado | 180 personas, 0 desviaciones sin justificar |
| Utilización global: legado vs motor nuevo | **113,09% frente a 56,31%** |
| Agente v0 | 43 violaciones de seguridad, utilidad 0,154 |
| Agente final | **0 violaciones, utilidad 1,000** |
| Concentración v0 vs final | 33 personas distintas vs **20** de un pool de 180 |

## Hallazgos que conviene que el mentor conozca

1. **El legado dice 113% de utilización.** Un número por encima del 100% que
   nadie detectó porque alimentaba un cuadro de mando que nadie recalculaba. Es
   la lección de S5 en una cifra.
2. **El agente final es más seguro, más útil y más concentrado.** Propone la
   mitad de personas distintas que la versión ingenua. No es un fallo: es la
   consecuencia de optimizar por encaje sin contrapartida de reparto. Está
   documentado en `labs/S6-gobierno/concentracion.md` y es el mejor material de
   conversación del laboratorio.
3. **El verificador independiente usaba una dedicación fija** en lugar de la
   pedida por cada demanda, y producía tres falsos positivos de sobreasignación.
   Está corregido y documentado en la lámina de defensa: el verificador tiene que
   usar exactamente los mismos parámetros que lo verificado.
4. **Un test encontró un fallo real de modelado**: una asignación no debe computar
   durante una ausencia no trabajable. Numerador y denominador tienen que excluir
   los mismos días. Dio lugar a CA-08 de SPEC-002.

## Cómo se deriva el repo de aprendizaje del student

| Paso | Acción |
|------|--------|
| 1 | Vaciar el apartado de ambigüedades de SPEC-002 y reescribir CA-01 y CA-05 en su forma ambigua |
| 2 | Sustituir `agentes/staffing/agente.py` por `agente_v0.py`, dejando el final en `labs/S4a-agente-propio/referencia/` |
| 3 | Mover `evals/dorado_ejemplo/` a un flujo reutilizable de la organización: el student recibe métricas, nunca etiquetas |
| 4 | Vaciar `tests/`, salvo `conftest.py` y `utilidades.py` |
| 5 | Vaciar los artefactos de estación: comparativa, flotilla, concentración, coste, n4, mttr, reversión, defensa |
| 6 | Mover cada solución a `labs/<estación>/referencia/` |
| 7 | Conservar íntegros: legado, generador de corpus, specs sin resolver, CLAUDE.md, workflows, verificadores y CLI |

Los verificadores, el generador de corpus y los catálogos de categorías **no se
tocan**: son la vara de medir.

## Y lo que hay que decidir antes de arrancar

Dos cosas siguen sin dueño y son bloqueantes:

1. **Dueño funcional de la herramienta**: un resource manager que decida qué entra
   y qué no, y que acepte o rechace cada módulo. Sin esa figura la herramienta la
   diseña la cohorte por consenso y no la usa nadie.
2. **Quién mantiene la herramienta cuando la cohorte termine.** Si la respuesta es
   nadie, conviene saberlo antes de que el área empiece a depender de ella.

Y una tercera que no es decisión sino requisito: la base jurídica, la
minimización y la transparencia hacia las personas cuyos datos entran en el
repositorio de producto, más la verificación del encaje en el EU AI Act. Antes de
septiembre, no en noviembre.
