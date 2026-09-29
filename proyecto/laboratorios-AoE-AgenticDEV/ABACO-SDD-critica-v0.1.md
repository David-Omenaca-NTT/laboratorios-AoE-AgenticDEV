# Crítica del proyecto formativo Ábaco — modalidad SDD estricta

**Versión:** v0.1  
**Fecha de análisis:** 2026-08-14  
**Alcance:** ejercicio, enfoque pedagógico de Spec-Driven Development (SDD), uso de IA generativa/agentes y mecanismos operativos del repositorio `abaco-sdd`.

## Dictamen ejecutivo

Ábaco-SDD plantea una experiencia formativa poco habitual y valiosa: desplaza el trabajo desde escribir implementación hacia expresar intención verificable, mantener cambios como artefactos revisables y demostrar que una especificación ambigua automatiza el error con más rapidez. La secuencia de diez etapas, el uso explícito de deltas, la aceptación externa y la caracterización previa al cambio de legado construyen un mensaje pedagógico coherente y relevante para desarrollo asistido por IA.

No obstante, la modalidad se anuncia como **SDD estricta**, pero varios controles que deberían impedir los atajos son declarativos o incompletos. La CI principal aún utiliza la estructura heredada de Ábaco (`tests/`, `SPEC-*`) en vez de `aceptacion/` y OpenSpec; el gate de procedencia solo cubre `src/`, no el agente; la integridad de aceptación depende de que el commit se autodeclare generado; y el propio agente deserializa atributos que su especificación prohíbe leer. Además, la imagen OCI no arranca Ábaco.

La recomendación es conservar la propuesta didáctica, pero **corregir los P0 antes de impartirla**. De lo contrario, el laboratorio enseña correctamente que las garantías de SDD deben ser verificables mientras sus propias puertas permiten esquivarlas.

## 1. Evaluación del ejercicio y del programa

### Aciertos

1. **Progresión con sentido de ingeniería.** E0–E9 recorren bootstrap, cambio mínimo, capability, deltas, reglas duras, cálculos numéricos, agente, legado, gobierno y operación. La dificultad crece a la vez que el impacto de las decisiones (`abaco-sdd/PLAYBOOK.md:100-113`).
2. **Propósito central adecuado a la IA generativa.** Obligar a formular requisitos y escenarios antes de generar código combate uno de los riesgos más frecuentes del desarrollo agéntico: aceptar una implementación plausible sin haber concretado la intención (`abaco-sdd/PLAYBOOK.md:10-31`, `abaco-sdd/GUIA-SDD.md:54-82`).
3. **El laboratorio enseña límites, no promesas de herramienta.** Que `validate` no detecte todos los problemas y que `archive` rechace un delta incompleto son lecciones especialmente valiosas: validación sintáctica no equivale a corrección (`abaco-sdd/PLAYBOOK.md:115-125`, `abaco-sdd/GUIA-SDD.md:98-119`).
4. **Aceptación y escenarios frontera bien orientados.** La batería externa cubre aritmética decimal, invariantes, ausencias, transiciones y comportamiento heredado, evitando un ejercicio reducido a “generar verde” (`abaco-sdd/aceptacion/test_ocupacion.py`, `abaco-sdd/aceptacion/test_motor_asignacion.py`, `abaco-sdd/aceptacion/test_caracterizacion_legado.py`).
5. **Legado tratado con responsabilidad.** Separar caracterización y corrección hace visible el coste organizativo de modificar un indicador histórico, no solo la corrección técnica (`abaco-sdd/PLAYBOOK.md:154-162`).
6. **Gobierno de un caso sensible.** N2, veto humano, explicabilidad, exclusión de atributos y métricas separadas de seguridad, utilidad y concentración son decisiones apropiadas para un sistema de recomendación de staffing (`abaco-sdd/openspec/specs/agente-staffing/spec.md:3-79`; `abaco-sdd/labs/E6-agente/GUIA.md:8-21`).
7. **Control de privacidad de herramientas de aprendizaje.** Fijar la versión de OpenSpec y desactivar telemetría expresan una preocupación correcta por reproducibilidad y tratamiento de información (`abaco-sdd/README.md:13-25`, `abaco-sdd/GUIA-SDD.md:280-290`).

### Riesgos pedagógicos

1. **La regla “no abrir código” es demasiado rígida.** Impedir la edición manual es coherente con la modalidad; impedir la inspección del código ante un fallo reduce aprendizaje de depuración, seguridad y comprensión de sistemas generados. Además, la propia guía propone arqueología de código como compensación (`abaco-sdd/PLAYBOOK.md:12-21`, `abaco-sdd/PLAYBOOK.md:231-242`; `abaco-sdd/GUIA-SDD.md:294-302`). Debe prohibirse editar sin regenerar, no leer; conviene exigir primero hipótesis en la spec, después inspección o instrumentación registrada y finalmente regeneración.
2. **La aceptación tiene un rol contradictorio.** README, Playbook y guía indican que `aceptacion/` se escribe a mano, pero a la vez se define como examen que el examinado no escribe (`abaco-sdd/README.md:34-39`; `abaco-sdd/PLAYBOOK.md:23-31`; `abaco-sdd/GUIA-SDD.md:25-32`). Hay que separar pruebas de diseño del estudiante de aceptación custodiada por mentor/CI, con permisos y procedencia distintos.
3. **El ejercicio requiere prerrequisitos elevados.** En 206 horas combina Git, CI, Python, contenedores, OpenSpec, modelado de dominio, testing, evaluación de agentes, legado y gobierno. Debe existir diagnóstico inicial, ruta de nivelación y capacidad de mentoría explícita; de otro modo la herramienta y la sintaxis desplazarán la reflexión sobre especificación.
4. **La densidad de escenarios no mide calidad.** El rango de 1–8 escenarios permite que un requisito con solo un caso feliz pase, aunque la guía exige escenarios negativos (`abaco-sdd/herramientas/gates_sdd.py:199-225`; `abaco-sdd/GUIA-SDD.md:70-82`). Un lint mínimo de negatividad, límites e invariantes y una revisión docente por muestreo aportarían señal real.
5. **Fechas futuras afectan la credibilidad de la evidencia.** Con la fecha de análisis, los cambios de referencia están fechados entre septiembre y diciembre de 2026, mientras README afirma que ya se ejecutaron (`abaco-sdd/README.md:43-77`; `abaco-sdd/GUIA-SDD.md:6`). Usar fechas reales, etiquetas de cohorte o declarar que son simuladas evitaría confusión.

## 2. Evaluación del enfoque de IA generativa y agentes

### Aciertos

- La arquitectura reserva las restricciones duras y el ranking a lógica determinista y limita el modelo a explicar resultados ya calculados (`abaco-sdd/agentes/staffing/agente.py:10-20`, `abaco-sdd/agentes/staffing/agente.py:271-292`).
- La especificación exige reproducibilidad, alternativas descartadas, evidencia por candidato y versiones de política/catálogo (`abaco-sdd/openspec/specs/agente-staffing/spec.md:19-79`).
- El techo N2 se fundamenta en reversibilidad del daño, no en una métrica de precisión; es el marco correcto para recomendaciones que afectan trayectorias profesionales (`abaco-sdd/agentes/staffing/agente.py:22-24`; `abaco-sdd/openspec/specs/agente-staffing/spec.md:7-18`).
- E6 obliga a corregir el requisito ausente cuando falla seguridad, no a parchear el resultado (`abaco-sdd/labs/E6-agente/GUIA.md:12-26`).

### Carencias y mejoras

1. **La minimización de datos está incumplida por la implementación de referencia.** La spec prohíbe leer nombre, correo, teléfono, foto, país, oficina, fecha de nacimiento y género, pero `_persona()` lee `nombre`, `pais` y `oficina` y los inserta en el modelo (`abaco-sdd/openspec/specs/agente-staffing/spec.md:65-71`; `abaco-sdd/agentes/staffing/agente.py:51-54`, `abaco-sdd/agentes/staffing/agente.py:109-121`). Debe usarse un DTO/proyección permitida que no deserialice esos campos, y pruebas negativas estáticas y dinámicas que demuestren ausencia de acceso.
2. **Explicabilidad necesita una rúbrica de fidelidad.** El sistema pide explicar, pero no define cómo comprobar que la explicación generativa no añade motivos, no altera orden, no revela atributos y es trazable a las reglas. Se requieren casos adversariales y evaluación humana basada en evidencia, no solo una instrucción al modelo.
3. **El evaluador del agente no es completamente independiente.** Si reutiliza el mismo motor que determina aptitud, un fallo compartido puede declarar “cero violaciones”. Debe existir un oráculo de aceptación independiente, casos ocultos del docente y ejecución también en `main` y antes del despliegue.
4. **Faltan amenazas específicas de agentes.** Incorporar en E6/E8/E9 escenarios de prompt injection a través de artefactos, abuso de herramientas, exfiltración de contexto, cambios de políticas, salida no determinista y degradación de evaluación daría al itinerario una cobertura más completa de Agentic DevOps.
5. **Precisar la semántica del agente.** La documentación generada afirma que el agente “PROPONE y decide una persona”, aunque la spec dice que nunca decide (`abaco-sdd/agentes/staffing/agente.py:22-24`; `abaco-sdd/openspec/specs/agente-staffing/spec.md:3-9`). Debe decir que recomienda sobre personas y que la decisión corresponde al resource manager.

## 3. Coherencia operativa y controles SDD

| Prioridad | Hallazgo | Evidencia | Impacto |
|---|---|---|---|
| P0 | La CI principal ejecuta `tests/` y trazabilidad `SPEC-*`, pero el laboratorio usa `aceptacion/` y `openspec/specs/`. | `abaco-sdd/.github/workflows/ci.yml:30-67`; `abaco-sdd/README.md:20-25` | CI puede fallar o validar una estructura heredada; contradice el flujo que aprende el estudiante. |
| P0 | La procedencia inspecciona solo `src/`; deja fuera `agentes/` y devuelve verde si no hay Git. | `abaco-sdd/herramientas/gates_sdd.py:21`, `abaco-sdd/herramientas/gates_sdd.py:65-99` | Se puede parchear manualmente el agente o ejecutar puertas sin historial sin incumplimiento. |
| P0 | La integridad de aceptación solo bloquea commits que se declaran mediante `Generated-By:`. | `abaco-sdd/herramientas/gates_sdd.py:104-132` | Basta omitir un trailer para modificar el examen sin detección; contradice `AGENTS.md`. |
| P0 | El contenedor arranca `aula.api.app:app`, no el paquete `abaco`. | `abaco-sdd/Containerfile:1-19` | La imagen construida no prueba que el servicio sea desplegable; E9 pierde evidencia operativa. |
| P1 | El gate de deriva comprueba capability→módulo, no requisito/escenario→aceptación/código; no inventaría agentes y excluye legado. | `abaco-sdd/herramientas/gates_sdd.py:137-194`; `abaco-sdd/openspec/trazabilidad.md` | La cifra de deriva no representa cobertura semántica y puede ocultar módulos o requisitos huérfanos. |
| P1 | El gate de manifiesto usa coincidencias textuales, hash opcional y no vincula el manifiesto al agente/políticas alterados. | `abaco-sdd/.github/workflows/gate-manifiesto.yml:31-80` | El control de gobierno es evadible con texto, comentarios o manifiestos no relacionados. |
| P1 | Las puertas no verifican una generación reproducible. `Change-Id` y `Generated-By` son declaraciones en commits, no una prueba de procedencia. | `abaco-sdd/GUIA-SDD.md:125-166`; `abaco-sdd/herramientas/gates_sdd.py:89-96` | “Todo código se deriva” no queda demostrado y la modalidad puede premiar documentación de un parche. |
| P2 | Dependencias Python y base OCI no están fijadas por lockfile/digest, a diferencia de OpenSpec. | `abaco-sdd/requirements.txt`; `abaco-sdd/Containerfile:4-9`; `abaco-sdd/README.md:15-16` | La reproducibilidad que se exige al alumno no se mantiene en el entorno. |

## 4. Plan de mejora priorizado

### P0 — Antes de impartir una cohorte

1. **Unificar el pipeline en torno a OpenSpec.** Sustituir referencias a `tests/`, `specs/` y `SPEC-*` por `aceptacion/`, `openspec/specs/` y trazabilidad de requisitos/escenarios. Ejecutar corpus, OpenSpec, aceptación, cuatro puertas, evaluación del agente, construcción OCI y prueba de salud en un camino coherente.
2. **Endurecer procedencia e integridad.** Aplicar gate a todo código generado, incluidos `agentes/`; fallar fuera de Git y comprobar el diff de PR; impedir cambios de `aceptacion/` por reglas de repositorio, CODEOWNERS efectivos y fuente de pruebas custodiada. No usar un trailer autodeclarado como frontera de confianza.
3. **Reparar y probar el contenedor.** Cambiar el punto de entrada a `abaco.api.app:app`, usar nombres coherentes y añadir un smoke test que construya, arranque y consulte `/salud`.
4. **Corregir minimización de datos.** Eliminar deserialización de atributos prohibidos, crear una proyección de contexto permitida y añadir casos de aceptación adversariales que fallen ante lectura o propagación de esos campos.

### P1 — Convertir controles en evidencia verificable

5. **Reformular el gate de deriva.** Mapear requisitos/escenarios a aceptación y módulos; validar que cada módulo declarado existe; incluir agentes, herramientas y workflows cuando implementen una capability; diferenciar exclusiones justificadas de omisiones.
6. **Hacer estructurado el Agent Release Manifest.** Parsear YAML con esquema; exigir hash, fechas y asociación con ruta exacta de agente; disparar gate ante cambios en agente, dominio, políticas, evaluación y herramientas; fijar N2 según tipo de sistema, no por presencia textual.
7. **Registrar generación y reproducibilidad.** Guardar versiones de herramienta/modelo, prompts o plantillas aprobadas, hashes de specs y outputs; reproducir o verificar la generación en CI; exigir revisión humana del diff generado.
8. **Separar pruebas del estudiante y evaluación independiente.** Mantener tests que el alumno diseña para explorar requisitos, pero ejecutar aceptación oculta o protegida por el docente/CI. Añadir mutaciones y casos adversariales que el generador no pueda acomodar.

### P2 — Fortalecer el aprendizaje y sostenibilidad

9. **Permitir lectura disciplinada del código.** Mantener prohibición de edición manual, pero establecer protocolo de diagnóstico: hipótesis en spec, inspección/instrumentación, decisión documentada y regeneración.
10. **Añadir rúbrica de calidad de specs.** Evaluar escenarios negativos, límites, invariantes, ambigüedades resueltas, criterios cuantitativos y alternativas descartadas; la densidad debe ser solo una señal auxiliar.
11. **Definir gobierno operativo del agente.** Establecer umbrales de concentración, revisión de explicaciones, dueño de decisión, registro de aceptación/rechazo, vía de impugnación, monitorización y retirada.
12. **Mejorar reproducibilidad del entorno.** Introducir lockfile con hashes, imágenes OCI por digest y validación periódica de la versión fijada de OpenSpec; declarar explícitamente qué evidencias son simuladas y cuáles ejecutadas.

## 5. Conclusión

Ábaco-SDD destaca porque convierte una intuición importante en práctica: con IA generativa, el activo escaso deja de ser solo escribir código y pasa a ser formular, revisar y gobernar intención verificable. La estructura de cambios, las lecciones de deltas, el legado y el caso de staffing son materiales formativos de alto valor.

Para ser una modalidad estricta y defendible, sus puertas deben proteger de verdad las fronteras que el curso proclama: código generado, aceptación independiente, procedencia, privacidad, despliegue y gobierno. Al alinear CI, controles y documentación, el laboratorio dejará de explicar SDD de calidad y empezará a demostrarlo end-to-end.
