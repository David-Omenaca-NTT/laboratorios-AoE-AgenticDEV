# Crítica del proyecto formativo Ábaco

**Versión:** v0.1  
**Fecha de análisis:** 2026-08-14  
**Alcance:** ejercicio, enfoque pedagógico, diseño operativo y mecanismos de evaluación del repositorio `abaco`.

## Dictamen ejecutivo

Ábaco es una propuesta formativa ambiciosa y, en lo conceptual, mejor orientada que la mayoría de itinerarios de desarrollo con IA generativa: parte de fundamentos manuales, exige trazabilidad y pruebas, y sitúa el uso de agentes en un caso de alto impacto sobre personas. Sus mejores decisiones son separar seguridad, utilidad y concentración; imponer supervisión humana N2; y enseñar que las restricciones relevantes deben hacerse deterministas.

Sin embargo, existe una brecha importante entre el discurso del programa y su implementación como laboratorio. Varios elementos que el alumnado debe aprender a confiar —comandos de operación, imagen desplegable, sellado de estaciones, protección de verificadores, escaneo de datos personales y gates de gobierno— no están alineados o no se ejecutan en CI. Esta incoherencia es especialmente perjudicial en una formación cuyo objetivo es desarrollar criterio de ingeniería: puede enseñar a validar documentación y patrones textuales en lugar de evidencia ejecutable.

La recomendación es **corregir los defectos P0 antes de impartir una nueva cohorte** y después fortalecer la evaluación conductual de los controles de gobierno.

## 1. Evaluación del ejercicio

### Aciertos

1. **Caso de uso realista y éticamente relevante.** El agente recomienda personas para proyectos, un dominio en el que los errores pueden afectar oportunidades profesionales. El programa no reduce la IA generativa a generación de código y obliga a tratar explicabilidad, exclusiones de datos, supervisión y posibilidad de contestación (`abaco/PLAYBOOK.md:20-24`, `abaco/PLAYBOOK.md:219-268`, `abaco/PLAYBOOK.md:289-313`).
2. **Aprendizaje progresivo y con transferencia.** S1 exige construir una rebanada vertical sin agente antes de S2–S4; la secuencia SDD → contexto → agente → legado → gobierno → operación evita presentar el agente como sustituto de los fundamentos (`abaco/PLAYBOOK.md:158-203`, `abaco/PLAYBOOK.md:270-319`).
3. **Restricciones de decisión bien formuladas.** Separar violaciones duras, utilidad y concentración evita que una métrica agregada oculte daños graves. La exigencia de cero violaciones duras es apropiada para el caso (`abaco/PLAYBOOK.md:229-239`).
4. **Uso pedagógico adecuado del legado.** La caracterización obligatoria antes del refactor y la diferencia entre el 113% heredado y el 56,31% esperado entrenan la prudencia necesaria para intervenir sistemas en producción (`abaco/PLAYBOOK.md:270-287`).
5. **Andamiaje transparente.** Verificadores consultables, tres niveles de pistas, bitácora y desbloqueo permiten avanzar sin convertir el atasco en una penalización permanente (`abaco/PLAYBOOK.md:112-154`, `abaco/PLAYBOOK.md:345-358`).
6. **Principio técnico correcto para sistemas agénticos.** El laboratorio expresa con claridad que los límites críticos se deben hacer deterministas, no dejarse a instrucciones en lenguaje natural (`abaco/PLAYBOOK.md:205-217`; `abaco/CLAUDE.md:22-39`).

### Riesgos pedagógicos

1. **Sobrecarga y dependencia de prerrequisitos.** Diez estaciones, 196 horas y un dominio que mezcla Python, CI/CD, contenedores, MCP, pruebas, arquitectura, legado, evaluación de IA y gobierno requieren una prueba inicial de competencias o rutas de refuerzo. La progresión es buena, pero no se especifican prerrequisitos, tiempo tutorizado ni criterios de recuperación por competencia.
2. **Caso de producto demasiado cercano a la producción para una incorporación inicial.** El playbook presenta el uso de datos reales de compañeros y acceso progresivo al repositorio de producto (`abaco/PLAYBOOK.md:28-60`). Aunque el mensaje de minimización es valioso, utilizar perfiles reales durante formación necesita una evaluación de impacto, base jurídica, roles de acceso, retención, proceso de derechos y un entorno segregado documentados antes del inicio. El propio README identifica que la base jurídica, minimización, transparencia y encaje regulatorio siguen pendientes (`abaco/README.md:102-115`). No debe presentarse como producto utilizable mientras esos puntos estén abiertos.
3. **Métrica de concentración sin una decisión operativa asociada.** Se mide y comenta correctamente, pero no se define umbral, protocolo de investigación ni acción correctiva. Esto puede convertir una señal de equidad en un artefacto narrativo (`abaco/PLAYBOOK.md:249-268`). Debe existir una política: segmentación por disponibilidad y perfiles, revisión humana, análisis de impacto y criterio explícito para rechazar o recalibrar una versión.
4. **Éxito descrito con cifras demasiado cerradas.** Mostrar la evolución esperada de v0 a final es didáctico, pero puede inducir optimización hacia el resultado conocido —aunque las etiquetas estén ocultas— y reducir la exploración de alternativas. Conviene evaluar también conjuntos de escenarios no divulgados, estabilidad entre ejecuciones, casos límite y justificaciones cualitativas.
5. **Calibración con riesgo de uso punitivo.** La predicción previa al check es una práctica formativa útil (`abaco/PLAYBOOK.md:146-154`), pero debe estar explícitamente separada de la evaluación sumativa salvo que se publique su fiabilidad, sesgos y protocolo de acompañamiento. La transparencia debe incluir qué ve el mentor y para qué puede emplearlo.

## 2. Evaluación del enfoque de IA generativa y agentes

### Aciertos

- El agente se orienta a **recomendar**, no a decidir: el techo N2 y el veto humano son la respuesta correcta para un sistema que puede afectar carreras (`abaco/PLAYBOOK.md:297-313`).
- El diseño favorece un núcleo determinista para elegibilidad y aritmética, reservando la IA para tareas donde aporta valor explicativo o de interacción (`abaco/PLAYBOOK.md:244-247`).
- Exigir motivos de inclusión y descarte es un buen punto de partida para trazabilidad y posibilidad de impugnación (`abaco/PLAYBOOK.md:223-227`).
- La exclusión de atributos personales y la auditoría con origen son principios de minimización y rendición de cuentas coherentes (`abaco/CLAUDE.md:33-35`, `abaco/CLAUDE.md:75-85`).

### Carencias y recomendaciones

1. **Definir qué componente es realmente generativo.** La arquitectura descrita parece deliberadamente determinista; es una decisión razonable, pero el programa debería separar con precisión: reglas, ranking, explicación generada, herramientas MCP y posible LLM. De otro modo, el estudiante puede asociar “agente” a una orquestación de reglas sin aprender límites de contexto, fallos de herramientas, inyección de instrucciones, no determinismo ni evaluación de salidas generativas.
2. **Añadir amenazas específicas de IA agéntica.** Faltan ejercicios explícitos de prompt injection a través de artefactos del repositorio, abuso de herramientas, exfiltración de contexto, confusión de autoridad, degradación por cambio de políticas y ataques a evaluaciones. S3 y las rondas adversariales son el lugar natural para introducirlos.
3. **Evaluar explicaciones, no solo selecciones.** Explicar por qué se descarta a alguien es requisito, pero no aparece una rúbrica que evalúe fidelidad, suficiencia, lenguaje no discriminatorio, trazabilidad a regla/política y ausencia de revelación de atributos excluidos. Una explicación convincente pero falsa es un riesgo central.
4. **Ampliar evaluación de equidad y daño.** La concentración es útil pero insuficiente. Deben incorporarse pruebas de consistencia contrafactual sobre atributos no permitidos, análisis de cobertura de oportunidades, revisión de grupos definidos legalmente solo cuando la gobernanza lo permita, y simulaciones de error de datos.
5. **Formalizar el rol humano.** “Humano decide” no basta. El entregable debe describir quién decide, qué evidencia recibe, cómo se registra la aceptación/rechazo, cuándo debe escalar, cómo se comunica una recomendación y cómo se corrigen datos o decisiones.

## 3. Coherencia del programa y operación del laboratorio

### Hallazgos críticos

| Prioridad | Hallazgo | Evidencia | Impacto |
|---|---|---|---|
| P0 | El Makefile conserva referencias a Aula: cobertura sobre `src/aula`, comandos `aula_cli`, evaluador de conformidad y MCP de Aula. | `abaco/Makefile:13-26` | Los comandos recomendados no ejercitan Ábaco; se rompe el recorrido de aprendizaje y la confianza en la automatización. |
| P0 | La imagen OCI también conserva Aula: usuario `aula`, etiqueta Aula y comando `aula.api.app:app`. | `abaco/Containerfile:1-19` | La imagen no arranca el servicio Ábaco; S7 y CI no validan el despliegue que se enseña. |
| P0 | El sellado no se ejecuta desde una fuente protegida. La CLI carga `verificar.py` local y CI no ejecuta verificadores de estaciones. | `abaco/abaco_cli/__main__.py`; `abaco/.github/workflows/ci.yml:30-99`; `abaco/labs/S4a-agente-propio/CRITERIOS.md:3-9` | Contradice la afirmación de que el pipeline usa una vara de medir no modificable. Se puede aprender a pasar el check local, no a cumplir el objetivo. |
| P0 | El escaneo de PII se declara como gate de pipeline pero su verificación está limitada a S0 local, rutas/extensiones parciales. | `abaco/PLAYBOOK.md:50-60`; `abaco/labs/S0-bootstrap/verificar.py`; `abaco/.github/workflows/ci.yml:30-99` | La principal salvaguarda pedagógica de datos reales no está implementada de extremo a extremo. |
| P1 | El gate de manifiesto depende de rutas limitadas y no vincula de forma robusta manifiesto, código, políticas y evaluación. | `abaco/.github/workflows/gate-manifiesto.yml`; `abaco/manifiestos/staffing-propuesta.yaml` | Cambios de dominio o política que alteren recomendaciones pueden no requerir nueva evidencia de gobierno. |
| P1 | S6 y S7 verifican en parte presencia de texto/artefactos en lugar de comportamiento ejecutado. | `abaco/labs/S6-gobierno/verificar.py`; `abaco/labs/S7-despliegue/verificar.py` | Favorece soluciones que satisfacen el patrón del verificador sin demostrar la propiedad de seguridad u operación. |

### Incoherencias adicionales

- README declara 75 tests y 79 criterios automáticos, pero CI no valida integralmente ese inventario ni ejecuta los verificadores del laboratorio (`abaco/README.md:55-67`; `abaco/.github/workflows/ci.yml:30-99`).
- S0 solicita dos PR mergeados y compromiso de datos; S7 un servicio desplegado; S8 defensa ante dueño funcional. Los criterios consultados describen los entregables, pero no explicitan qué prueba el sistema y qué evalúa el mentor/panel (`abaco/labs/S0-bootstrap/GUIA.md:21-48`; `abaco/labs/S7-despliegue/CRITERIOS.md:11-18`; `abaco/labs/S8-defensa/CRITERIOS.md:11-18`).
- El README reconoce que faltan dueño funcional y responsable de mantenimiento (`abaco/README.md:102-110`). Son condiciones de viabilidad, no tareas que puedan quedar abiertas al comenzar la cohorte.

## 4. Plan de mejora priorizado

### P0 — Antes de impartir o reutilizar el laboratorio

1. **Reparar el camino de ejecución completo.** Corregir Makefile, Containerfile, devcontainer, scripts y documentación para utilizar exclusivamente `abaco`, `abaco_cli`, `agentes.staffing` y `agentes.mcp_abaco`. Añadir pruebas de humo para `make estado`, `make check`, `make eval`, `make mcp`, construcción OCI y endpoint `/salud`.
2. **Centralizar la evaluación que sella estaciones.** Ejecutar verificadores desde una plantilla, paquete o workflow protegidos; guardar evidencias firmadas o inmutables; impedir que una copia local alterada determine el sellado.
3. **Convertir la protección de datos en control efectivo de CI.** Analizar el diff completo y rutas/tipos relevantes; revisar mensajes de commit si forman parte de la regla; documentar falsos positivos y excepciones aprobadas; impedir el acceso accidental de agentes a datos reales.
4. **Bloquear el uso de datos reales hasta cerrar gobierno.** Nombrar dueño funcional y responsable de mantenimiento; documentar DPIA/evaluación de impacto, base jurídica, matriz de acceso, retención, transparencia, revisión legal y mecanismo de reclamación.

### P1 — Fortalecer la evidencia de gobierno y calidad

5. **Endurecer el Agent Release Manifest.** Parsear YAML estructurado; exigir hash y fecha; asociar manifiesto al agente, políticas, evaluador y contratos MCP relevantes; disparar gate ante cambios del dominio o de catálogos; aplicar N2 como restricción tipada, no por coincidencia textual.
6. **Sustituir comprobaciones de presencia por pruebas conductuales.** Mutar un manifiesto a N3/N4 y exigir fallo; introducir atributos prohibidos y demostrar que no se leen ni se propagan; arrancar contenedor, comprobar salud, simular fallo y validar reversión/observabilidad.
7. **Publicar una rúbrica dual.** Diferenciar claramente criterios automáticos, evidencias revisadas por mentor y desempeño ante panel. Asignar ejemplos de evidencia válida y niveles de logro, sin revelar soluciones.
8. **Operativizar concentración y explicabilidad.** Definir umbrales de alerta, métricas de distribución, investigación obligatoria, estrategia de mitigación y evaluación humana de fidelidad de las explicaciones.

### P2 — Mejorar la experiencia y sostenibilidad pedagógica

9. **Diagnóstico de entrada y rutas de nivelación.** Medir Python, Git, testing, contenedores y lectura de especificaciones antes de S0; ofrecer cápsulas previas para evitar que la complejidad técnica eclipse los objetivos de IA agéntica.
10. **Añadir evaluación transversal de seguridad agéntica.** Crear escenarios de inyección, herramientas maliciosas, archivos con instrucciones conflictivas, cambios de políticas y degradación del modelo; evaluar detección, contención y explicación.
11. **Instrumentar resultados de aprendizaje.** Recoger tiempos, calibración, calidad de revisión, uso de pistas, fallos recurrentes y desempeño posterior sin convertir telemetría en vigilancia punitiva. Revisar el programa al cierre de cada cohorte.
12. **Mantener una versión operativa y una versión de referencia claramente separadas.** Automatizar la derivación de la plantilla student desde la referencia y probarla en CI, para que los residuos de otros proyectos no lleguen a la cohorte.

## 5. Conclusión

El núcleo didáctico de Ábaco es sólido: enseña que desarrollar con IA generativa no consiste en aceptar código más rápido, sino en diseñar contexto, controles, evaluación y responsabilidad humana alrededor de un sistema con impacto. Su mayor oportunidad no es añadir más contenido, sino asegurar que sus propias protecciones son reales, ejecutables y coherentes.

Cuando un laboratorio de Agentic DevOps afirma que un gate protege datos, que un contenedor despliega un servicio o que una estación está sellada por una evaluación independiente, esas afirmaciones deben verificarse de extremo a extremo. Corregir esa brecha convertirá un programa conceptualmente excelente en un activo formativo defendible y reproducible.
