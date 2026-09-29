<!-- version: v0.1 | estado: borrador | documento fuente: plan de capacitación students v0.12 | audiencia: student de la cohorte | pendiente: [nombre de tu mentor y grupo de mentoría, fechas exactas de cohorte, URL del SharePoint del programa, calendario de sesiones técnicas SME] | destino: entrega el día 1 a cada student -->

# Manual del student

**AI Engineering Talent Factory | AoE Agentic DevOps | Digital Architecture**
Cohorte septiembre 2026 | 6 meses

---

## Tu misión

**En 4 meses debes tener autonomía suficiente para integrarte en un equipo real de desarrollo de un cliente y desempeñar un rol junior con solvencia.**

Ese es el objetivo del programa y la vara con la que se mide todo lo que hagas. No estás aquí para acumular cursos ni para coleccionar diplomas: estás aquí para que, cuando llegues a un squad de cliente, aportes desde la primera semana.

Por qué existe este programa: nuestros clientes de banca y seguros están pidiendo perfiles que sepan trabajar con agentes de IA dentro del ciclo de desarrollo (SDD, GitHub, DevOps, automatización avanzada) y ni nosotros ni el mercado tenemos suficiente gente que sepa hacerlo. Tú vas a ser esa gente. Es una capacidad escasa y por eso el programa concentra tanto tiempo en ella.

## Qué sabrás hacer al terminar

- Trabajar en un repositorio compartido con soltura: ramas, pull requests, revisión de código, resolución de conflictos.
- Entender la arquitectura cloud de un cliente y moverte en ella sin depender de otro.
- Empaquetar una aplicación en contenedores y desplegarla en Kubernetes.
- Construir y mantener un pipeline de CI/CD con quality gates y security gates.
- Desarrollar con agentes de IA aplicando criterio: elegir la herramienta adecuada, revisar lo que produce y justificar cada aceptación o rechazo.
- Aplicar Spec-Driven Development y diseñar, orquestar y evaluar agentes dentro de un SDLC gobernado.
- Defender técnicamente tu trabajo ante alguien que no te conoce.

## Cómo se organiza tu recorrido

| Fase | Cuándo | Qué haces | Cómo sabes que la has cerrado |
|------|--------|-----------|-------------------------------|
| Fase 1: onboarding y fundamentos | Septiembre (mes 1) | Incorporación, evaluación inicial de tu nivel, módulos 0 a 2 | Tus OKRs de fase 1 pactados y en verde |
| Fase 2: formación intensiva | Octubre y noviembre (meses 2 y 3) | Módulos 3 a 8, el grueso del programa | Proyecto vertebrador completo y panel de asignación superado |
| Fase 3: asignación a cliente | Diciembre a febrero (meses 4 a 6) | Incorporación a un squad real con acompañamiento senior | Feedback del squad en el mes 5 y cierre del programa |

La formación intensiva son 17 semanas efectivas. Los módulos 0 a 2 arrancan ya en septiembre, solapados con el onboarding.

---

## Tu itinerario

| # | Módulo | Semanas | Qué sabrás hacer | Qué entregas |
|---|--------|---------|------------------|--------------|
| 0 | Onboarding y contexto de negocio | 0,5 | Situar quién es NTT DATA, qué son las torres, qué hace el AoE Agentic DevOps y para qué clientes trabajamos | Evaluación inicial de skills completada |
| 1 | Git y flujos de colaboración | 1 | Operar un flujo de PR completo sin bloquear a nadie: ramas, rebase, merge, review, conventional commits | PRs mergeadas como evidencia y una review cruzada con checklist |
| 2 | Fundamentos cloud | 1,5 | Tener modelo mental de cloud (identidad, red, almacenamiento, cómputo, costes) con foco en Azure | Primer despliegue del proyecto sobre servicios gestionados |
| 3 | Contenedores y Kubernetes | 2 | Construir imágenes, desplegar en Kubernetes y depurar un workload que falla | Proyecto contenedorizado y corriendo en AKS o kind |
| 4 | CI/CD y DevOps | 1,5 | Montar un pipeline de build, test y deploy con GitHub Actions e infraestructura como código | Pipeline verde de extremo a extremo y un ejercicio de MTTR |
| 5 | SDLC asistido por IA e IDEs agénticos | 4 | Desarrollar con Claude Code, OpenCode, Orca y Copilot, y justificar cuál eliges y cuándo no usar IA | Tabla comparativa razonada, configuración versionada (CLAUDE.md, allowlist, hooks) |
| 6 | Agentes y SDD | 4 | Aplicar Spec-Driven Development, construir agentes y skills, integrar MCP, gestionar memoria y evaluar agentes | Una fase del SDLC automatizada con un agente gobernado |
| 7 | Gobierno, seguridad y calidad | 1,5 | Trabajar con los estándares que exige banca y seguros: secretos, SAST/DAST, uso responsable de IA, trazabilidad | Quality gates y security gates activos en tu pipeline |
| 8 | Preparación cliente | 1 | Contar y defender tu trabajo, y funcionar dentro de un squad | Dos simulacros de entrevista y la presentación ante el panel final |

Los módulos 5 y 6 ocupan 8 de las 17 semanas. No es un desajuste: los fundamentos son requisito de entrada pero los tiene cualquiera, y lo que te hace diferente en el mercado es saber operar agentes dentro de un ciclo de desarrollo gobernado.

## El proyecto vertebrador

Desde el módulo 3, todos tus labs contribuyen a un mismo proyecto: una aplicación contenedorizada, desplegada, con pipeline completo y evolucionada con agentes. No son ejercicios sueltos, es una sola cosa que crece contigo.

Ese proyecto es tu portfolio. Es lo que enseñas en el panel de asignación y lo que un cliente mira cuando pregunta qué sabes hacer. Trátalo como código de producción desde el primer commit: repositorio limpio, historia de commits legible, README que explique cómo se levanta, y evidencia de que funciona.

---

## Cómo se trabaja aquí

Siete reglas que rigen todo el programa. Si tienes dudas sobre cómo abordar algo, la respuesta suele estar en una de ellas.

1. **Se aprende haciendo.** El ratio objetivo es 30% contenido y 70% laboratorio. La teoría aparece cuando el gesto la necesita, no antes.
2. **Se sube de nivel por fluidez, no por tiempo.** Un módulo está cerrado cuando el gesto te sale sin consultar, no cuando has visto todos los vídeos.
3. **La habilidad central es revisar, no prompear.** Lo importante no es escribir el prompt perfecto, es leer bien lo que el agente propone antes de aceptarlo. Quien acepta a ciegas hereda todos los errores. En los labs tendrás que justificar por qué aceptas o rechazas cada diff.
4. **Pide evidencia, no aserciones.** "Funciona" no vale. Los tests en verde sí. Todo entregable va acompañado de su evidencia, y eso incluye lo que le exiges al agente y lo que reportas a tu mentor.
5. **El contexto es un recurso escaso.** La ventana de contexto se administra a propósito: limpiar entre tareas, compactar dirigido, apuntar a lo concreto.
6. **Lo innegociable no se confía a un prompt.** Lo que tiene que pasar siempre se hace determinista (hooks, gates de pipeline), no se pide en lenguaje natural.
7. **El material caduca, el método no.** Las herramientas cambian cada pocos meses. Aprende dónde está la documentación oficial, cómo comprobar la versión que usas y cómo contrastar, en lugar de memorizar listas de comandos.

---

## Tu día a día

### Estructura tipo de una jornada

| Bloque | Duración orientativa | Qué es |
|--------|----------------------|--------|
| Daily de mentoría | 15 min | Con tu mentor y los 2 o 3 students de tu grupo. Qué hiciste, qué vas a hacer, qué te bloquea |
| Formación autodirigida | 2 a 2,5 h | Cursos y material del módulo en curso, según el catálogo de abajo |
| Labs y proyecto | 3 a 3,5 h | El bloque principal. Es donde se aprende de verdad |
| Revisión de tu trabajo | Asíncrona | Tu mentor comenta tus PRs y labs a lo largo del día. Léelos y respóndelos el mismo día |

### Ritmo semanal y mensual

| Cuándo | Qué | Duración | Qué se espera de ti |
|--------|-----|----------|---------------------|
| Diario | Daily de mentoría | 15 min | Puntualidad y honestidad con los bloqueos. Un bloqueo escondido cuesta días |
| Semanal | Sesión técnica con un SME | 1,5 h | Cohorte completa. Queda grabada, pero asiste en vivo: es donde puedes preguntar |
| Viernes | Feedback semanal con tu mentor | 10 min | Llegas con tus evidencias de la semana. Sale registrado en tu ficha |
| Viernes | Actualización de tu ficha en SharePoint | 15 min | Autoevaluación y enlaces a lo que has producido. Es responsabilidad tuya, no del mentor |
| Mensual | Retro de cohorte | 1 h | Aquí se cambia el programa. Si algo no funciona, este es el sitio |
| Mensual | Medición de tus KRs | Sin reunión | Tu mentor actualiza tu semáforo. Lo ves en el panel de cohorte |
| Fin de fase 2 | Panel de asignación | 2 h | Presentas tu proyecto ante el Head of AoE, SMEs y responsables de torre |

### Qué hacer cuando te bloqueas

1. Intenta resolverlo por tu cuenta un máximo de 30 minutos y documenta lo que has probado.
2. Pregunta en el canal de tu grupo de mentoría con esa documentación delante. La mitad de los bloqueos se resuelven aquí.
3. Si sigue abierto, llévalo al daily siguiente o escríbele a tu mentor sin esperar al daily si te está parando por completo.
4. Los bloqueos relevantes se anotan en tu ficha. No es un registro de fallos, es cómo el programa detecta si un contenido está mal calibrado.

Regla práctica: bloquearte es normal, quedarte bloqueado en silencio no lo es.

---

## Tu mentor

Tienes un mentor asignado durante todo el programa, con 3 o 4 students a su cargo. La asignación es estable a propósito: la confianza y una evaluación justa necesitan continuidad.

**Qué hace tu mentor:** te desbloquea, revisa tu trabajo, te reta y te da contexto real de cliente. Te da feedback escrito cada semana y evalúa tus KRs.

**Qué no hace:** dar clase. Las sesiones formativas son de los SMEs y del material del catálogo. Tu mentor trabaja sobre lo que tú produces.

**Qué espera de ti:** que llegues al daily con trabajo hecho, que respondas sus comentarios en PRs el mismo día, que le enseñes evidencias y no impresiones, y que le avises pronto cuando algo no va.

---

## Cómo se te evalúa

### OKRs por fase

Al inicio de cada fase pactas con tu mentor un objetivo y un máximo de 4 KRs, calibrados sobre tu punto de partida en la evaluación inicial. No hay listón único: se te compara contigo mismo y con el estándar de un junior solvente, no con el resto de la cohorte. Los KRs miden capacidad demostrada, nunca cursos consumidos.

**Fase 1. Dominar los fundamentos del SDLC moderno**
- Completas el itinerario de Git y operas un flujo de PR con review sin asistencia.
- Superas el assessment de fundamentos cloud con 80% o más.
- Completas las rutas de GitHub Skills del módulo 1, con PRs mergeadas como evidencia.

**Fase 2. Construir y operar un pipeline completo con IA**
- Proyecto vertebrador contenedorizado y desplegado con pipeline CI/CD funcional.
- Resuelves un lab de debugging de Kubernetes sin ayuda y en tiempo objetivo.
- Completas la ruta oficial de Microsoft Learn para AZ-900 con todos los módulos superados.
- Demuestras un flujo de desarrollo asistido con Claude Code o Copilot con criterio de revisión, evaluado por un SME.

**Fase 3. Operar con autonomía en un squad real**
- Te incorporas a un squad de cliente con acompañamiento senior.
- El feedback del squad en el mes 5 alcanza al menos "cumple expectativas de su nivel".
- Realizas una intervención autónoma documentada en el SDLC del cliente: una PR mergeada, un pipeline mejorado o equivalente según el contexto.

### Semáforo

Cada mes tu mentor actualiza tu estado por KR: verde, ámbar o rojo. Es visible en el panel de cohorte.

El ámbar no es un castigo, es el mecanismo que dispara ayuda: material de refuerzo específico, más tiempo de mentoría o replanificación. Un ámbar sostenido activa un plan de refuerzo antes de decidir tu asignación. Lo que no funciona es llegar al final de una fase en rojo sin haberlo dicho antes.

### Criterio de éxito individual

Se cumple con tres cosas a la vez:

1. Certificaciones obligatorias obtenidas (las tres son gratuitas para ti).
2. KRs de fases 1 y 2 en verde.
3. Evaluación positiva en el panel de asignación.

Las certificaciones recomendadas no son requisito para graduarte, pero suman en la priorización de asignación.

---

## Certificaciones

| Certificación | Módulo | Cuándo | Carácter |
|---------------|--------|--------|----------|
| [Claude Code 101](https://anthropic.skilljar.com/claude-code-101) y [Claude Code in Action](https://anthropic.skilljar.com/claude-code-in-action) de Anthropic Academy, certificados de finalización | 5 | Mes 3 | Obligatoria, gratuita |
| [Claude Certified Associate, Foundations](https://www.pearsonvue.com/us/en/anthropic.html) | 5 | Mes 3 | Obligatoria, gratuita por acuerdo de partner |
| [Claude Certified Developer, Foundations](https://www.pearsonvue.com/us/en/anthropic.html) | 5 y 6 | Mes 4 o 5 | Obligatoria, gratuita por acuerdo de partner |
| [GitHub Foundations](https://learn.github.com/certification/GHF) | 1 y 4 | Mes 2 | Recomendada |
| [Microsoft AZ-900, Azure Fundamentals](https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/) | 2 | Mes 2 o 3 | Recomendada |
| [GitHub Actions](https://learn.github.com/certification/ACTIONS) | 4 | Mes 3 o 4 | Recomendada |
| [KCNA, Kubernetes and Cloud Native Associate](https://www.cncf.io/training/certification/kcna/) | 3 | Mes 3 o 4 | Recomendada |
| [GitHub Copilot](https://learn.github.com/certification/COPILOT) | 5 | Mes 4 | Recomendada |
| [GitHub Certified: Agentic AI Developer, GH-600](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-600) | 5 y 6 | Mes 4 o 5 | Recomendada, sujeta a confirmar disponibilidad |
| [HashiCorp Terraform Associate](https://developer.hashicorp.com/certifications/infrastructure-automation) | 4 | Mes 5 o 6, ya en cliente | Opcional |

Las certificaciones de Anthropic son gratuitas para ti porque NTT DATA pertenece al Claude Partner Network. Consulta con el Lead del programa el mecanismo de registro antes de agendar examen. Para las recomendadas, habla con tu mentor antes de inscribirte: el orden importa, no tiene sentido presentarse a una certificación de un módulo que aún no has cerrado.

Formato de los exámenes de Anthropic: 120 minutos, proctorizado, se aprueba con 720 sobre una escala de 100 a 1.000. Descarga siempre la guía de examen vigente antes de agendar, porque cambia por versiones.

---

## Tu catálogo de recursos

Todo lo que necesitas está aquí. Los códigos C01 a C57 son los que verás en el calendario y en los labs. Los recursos marcados como internos viven en el SharePoint del programa.

### Módulo 0: onboarding y contexto de negocio

| ID | Recurso | Formato | Duración | Qué produces |
|----|---------|---------|----------|--------------|
| C01 | Sesión de bienvenida DA y AoE Agentic DevOps | Sesión en vivo | 2 h | Mapa de torres y clientes comentado |
| C02 | Assessment inicial de skills | Evaluación | 2 h | Tu baseline, sobre el que se pactan tus OKRs |
| C03 | [AI Capabilities and Limitations](https://anthropic.skilljar.com/ai-capabilities-and-limitations) | Autoservicio | 1 h | Ejercicios guiados de límites del modelo |
| C04 | Código de conducta y uso responsable de IA | Autoservicio | 1 h | Obligatorio antes de acceder a herramientas con IA |

### Módulo 1: Git y flujos de colaboración

| ID | Recurso | Formato | Duración | Qué produces |
|----|---------|---------|----------|--------------|
| C05 | GitHub Skills: [Introduction to GitHub](https://github.com/skills/introduction-to-github), [Review Pull Requests](https://github.com/skills/review-pull-requests), [Communicate Using Markdown](https://github.com/skills/communicate-using-markdown) | Interactivo | 6 h | PRs mergeadas en repos reales, evidencia de KR |
| C06 | [Learn Git Branching](https://learngitbranching.js.org/) | Simulador | 3 h | Escenarios de rebase y merge resueltos |
| C07 | Lab: conflicto provocado a tres bandas | Laboratorio | 2 h | Resolución guiada de un conflicto real con otros dos students |
| C08 | Lab: ciclo de PR con review cruzada | Laboratorio | 3 h | Revisas el PR de un compañero con checklist estándar |
| C09 | [Pro Git](https://git-scm.com/book) y [Conventional Commits](https://www.conventionalcommits.org/) | Referencia | Consulta | Consulta puntual, no lectura lineal |

### Módulo 2: fundamentos cloud

| ID | Recurso | Formato | Duración | Qué produces |
|----|---------|---------|----------|--------------|
| C10 | [Microsoft Learn, ruta AZ-900](https://learn.microsoft.com/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/) | Autoservicio | 10 h | Módulos superados, evidencia de KR de fase 2 |
| C11 | [Microsoft Learn Sandbox](https://learn.microsoft.com/training/) | Entorno de práctica | Integrado | Entorno Azure real sin suscripción propia |
| C12 | Lab: despliegue de app con servicios gestionados | Laboratorio | 6 h | Primer contacto con tu proyecto vertebrador, desplegado y accesible |

### Módulo 3: contenedores y Kubernetes

| ID | Recurso | Formato | Duración | Qué produces |
|----|---------|---------|----------|--------------|
| C13 | [Docker, guía oficial y buenas prácticas](https://docs.docker.com/get-started/) | Autoservicio | 5 h | Imágenes multi-stage y optimización de tamaño |
| C14 | [Play with Docker](https://labs.play-with-docker.com/) | Entorno efímero | 3 h | Práctica en navegador, sin instalación |
| C15 | [Kubernetes, tutoriales oficiales](https://kubernetes.io/docs/tutorials/) | Autoservicio | 8 h | Despliegues guiados paso a paso |
| C16 | Killercoda: [Pod Intro](https://killercoda.com/kubernetes/scenario/pod-intro), [Deployment Basics](https://killercoda.com/kubernetes/scenario/deployment-basics), [Playground](https://killercoda.com/kubernetes/scenario/playground) | Interactivo | 8 h | Manifiestos y salida de rollout como evidencia |
| C17 | Lab: contenedorizar y desplegar el proyecto vertebrador | Laboratorio | 10 h | Entregable evaluable: tu proyecto corriendo en AKS o kind |

### Módulo 4: CI/CD y DevOps

| ID | Recurso | Formato | Duración | Qué produces |
|----|---------|---------|----------|--------------|
| C18 | GitHub Skills: [Hello GitHub Actions](https://github.com/skills/hello-github-actions) y [Test with Actions](https://github.com/skills/test-with-actions) | Interactivo | 6 h | Workflow con trigger sobre PR, tests y cobertura en matriz |
| C19 | [HashiCorp Learn, ruta Terraform](https://developer.hashicorp.com/terraform/tutorials) | Autoservicio | 6 h | Provisión real de infraestructura |
| C20 | [OpenTelemetry, guía de conceptos](https://opentelemetry.io/docs/concepts/) | Referencia | 2 h | Instrumentación de tu proyecto |
| C21 | Lab: pipeline completo build, test, deploy | Laboratorio | 8 h | Entregable evaluable: pipeline verde de extremo a extremo |
| C22 | Lab: introducir un fallo y medir el MTTR | Laboratorio | 4 h | Medición propia del tiempo de recuperación |

### Módulo 5: SDLC asistido por IA e IDEs agénticos

El objetivo de este módulo no es que domines una herramienta, es que construyas criterio para elegir. Claude Code como motor de referencia, OpenCode para demostrar que el patrón es portable entre proveedores, Orca para trabajar en paralelo y disciplinar la revisión de diffs. Al salir debes poder justificar ante un cliente por qué eliges una u otra, no solo operarlas.

| ID | Recurso | Formato | Duración | Qué produces |
|----|---------|---------|----------|--------------|
| C23 | [Claude Code 101](https://anthropic.skilljar.com/claude-code-101) | Autoservicio | 2 h | Certificado de finalización, obligatorio |
| C24 | [Claude Code in Action](https://anthropic.skilljar.com/claude-code-in-action) | Autoservicio | 4 h | Certificado de finalización, obligatorio. Requiere soltura con CLI |
| C25 | [Claude Platform 101](https://anthropic.skilljar.com/claude-platform-101) | Autoservicio | 2 h | Recorrido por el ecosistema completo |
| C26 | [Aprendiendo Claude Code](https://www.iaparagentecuriosa.686f6c61.dev/aprende-con-teo/claude-code/) | Curso práctico en español | 12 h | Guía de laboratorio principal del módulo, con checkpoint por nivel |
| C27 | [Documentación oficial de Claude Code](https://docs.claude.com/en/docs/claude-code/overview) | Referencia | Consulta | Tu fuente de verdad durante los labs: hooks, subagentes, skills, settings |
| C28 | [OpenCode](https://opencode.ai/) | Referencia y práctica | 4 h | Instalación y uso real como alternativa multi-modelo |
| C29 | [Orca, ADE](https://github.com/stablyai/orca) | Herramienta | 4 h | Agentes en paralelo sobre git worktrees aislados |
| C30 | [GitHub Copilot, docs y ruta](https://docs.github.com/copilot) | Autoservicio | 3 h | Copilot en IDE frente a agente en terminal |
| C31 | Lab: mismo encargo con Claude Code y con OpenCode | Laboratorio | 8 h | Entregable: tabla comparativa con criterio de elección razonado |
| C32 | Lab: worktrees paralelos en Orca, patrón escritor y revisor | Laboratorio | 6 h | Un agente implementa, otro revisa solo el diff |
| C33 | Lab: CLAUDE.md, allowlist y hook de formato | Laboratorio | 6 h | Entregable: configuración versionada en el repo de tu proyecto |

### Módulo 6: agentes y SDD

El módulo de mayor peso junto al 5. Combina el framework propio del AoE, que no tiene equivalente público, con el ecosistema abierto de agentes. Todos los recursos externos terminan en un agente funcionando y evaluado, no en un vídeo visto.

| ID | Recurso | Formato | Duración | Qué produces |
|----|---------|---------|----------|--------------|
| C34 | Framework SDD del AoE | Material propio | 8 h | El activo diferencial del área, aplicado a tu proyecto |
| C35 | Agent Release Manifest y autonomía progresiva | Material propio | 4 h | Patrones de gobierno aplicados a tu proyecto |
| C36 | [Introduction to agent skills](https://anthropic.skilljar.com/introduction-to-agent-skills) | Autoservicio | 2 h | Skills reutilizables construidas por ti |
| C37 | [Introduction to Model Context Protocol](https://anthropic.skilljar.com/introduction-to-model-context-protocol) | Autoservicio | 2 h | Conexión de herramientas externas |
| C38 | [MCP: Advanced Topics](https://anthropic.skilljar.com/model-context-protocol-advanced-topics) | Autoservicio | 3 h | Servidores MCP propios |
| C39 | [Introduction to subagents](https://anthropic.skilljar.com/introduction-to-subagents) | Autoservicio | 2 h | Orquestación de subagentes |
| C40 | [Building with the Claude API](https://anthropic.skilljar.com/claude-with-the-anthropic-api) | Autoservicio | 4 h | Agentes dentro de un programa propio, con el Agent SDK |
| C41 | [AI Agents Course](https://huggingface.co/learn/agents-course) | Curso con proyecto | 20 h | El más práctico del catálogo: smolagents, LlamaIndex y LangGraph sobre el mismo problema, agente evaluado contra benchmark público. Dos certificados gratuitos |
| C42 | [Ambient Agents with LangGraph](https://academy.langchain.com/courses/ambient-agents) | Curso con proyecto | 8 h | Asistente de email construido desde cero y evaluado con LangSmith |
| C43 | [Deep Research with LangGraph](https://academy.langchain.com/courses/deep-research-with-langgraph) | Curso con proyecto | 8 h | Sistema multiagente de investigación evaluado con LangSmith |
| C44 | [Long-Term Agentic Memory with LangGraph](https://www.deeplearning.ai/courses/long-term-agentic-memory-with-langgraph/) | Curso corto | 1,5 h | Memoria semántica, episódica y procedural con LangMem |
| C45 | [Introduction to Deep Agents](https://academy.langchain.com/courses/foundation-introduction-to-deepagents) | Autoservicio | 4 h | Agentes de larga duración sobre harness open source |
| C46 | Lab: automatizar una fase del SDLC con agente gobernado | Laboratorio | 12 h | Entregable principal del módulo, sobre tu proyecto vertebrador |

### Módulo 7: gobierno, seguridad y calidad

| ID | Recurso | Formato | Duración | Qué produces |
|----|---------|---------|----------|--------------|
| C47 | Marco de velocidad gobernada del AoE | Material propio | 3 h | Intención verificable, ejecución autorizada, evidencia observable, coste atribuible |
| C48 | [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) | Referencia | 3 h | Checklist aplicado a tu proyecto |
| C49 | [GitHub Advanced Security](https://docs.github.com/code-security) | Autoservicio | 3 h | Secret scanning y code scanning activos en tu repo |
| C50 | [Monitoring Production Agents](https://academy.langchain.com/collections) y [Building Reliable Agents](https://academy.langchain.com/collections) | Autoservicio | 6 h | Observabilidad, coste, calidad y latencia de agentes con LangSmith |
| C51 | Formación interna de seguridad y compliance | Autoservicio | 2 h | Obligatoria por política |
| C52 | Lab: quality gates y security gates en el pipeline | Laboratorio | 6 h | Entregable evaluable sobre tu proyecto |

### Módulo 8: preparación cliente

| ID | Recurso | Formato | Duración | Qué produces |
|----|---------|---------|----------|--------------|
| C53 | Simulacro de entrevista técnica con tu mentor | Simulacro | 3 h | Dos rondas con feedback escrito |
| C54 | Simulacro con un SME que no te conoce | Simulacro | 2 h | Evaluación más realista, sin sesgo de familiaridad |
| C55 | Preparación de la presentación de tu proyecto | Taller | 4 h | Presentación sobre plantilla única |
| C56 | Taller de comunicación en squad | Taller | 3 h | Daily, estimación y escalado de bloqueos |
| C57 | Panel final ante Head of AoE, SMEs y torres | Evaluación | 2 h | Tu hito de salida de fase 2 |

### Material adicional bajo demanda

Existe un banco de recursos verificados que no está asignado por defecto y que tu mentor puede activarte por un motivo concreto: reforzar algo que se te resiste, acelerar si vas por delante del calendario, o especializarte en el stack del cliente al que te asignen. Tres reglas:

- Nada de ese banco es obligatorio ni evaluable. No entra en tus KRs ni en el panel de asignación.
- Solo puedes tener un recurso adicional activo a la vez. Acumular refuerzos es la forma más rápida de saturarte.
- Nunca desplaza a un lab del itinerario. Si vas justo de tiempo, se recorta lo adicional, nunca el núcleo.

Si crees que necesitas algo, pídelo en el feedback semanal. Tu mentor lo registra en tu ficha con el motivo.

---

## SharePoint: qué hay y qué mantienes tú

El SharePoint del programa es la única fuente de verdad. No hay versiones paralelas ni información importante circulando solo por chat.

| Área | Qué encuentras | Quién escribe |
|------|----------------|---------------|
| Panel de cohorte | Semáforo de OKRs, certificaciones y fase actual de toda la cohorte | Lead del programa |
| Tu ficha individual | Tus OKRs, el feedback semanal de tu mentor, tu autoevaluación, tus evidencias y certificaciones | Tu mentor y tú |
| Itinerario y materiales | Módulos, calendario, enlaces, labs y grabaciones de las sesiones | Lead y SMEs |
| Repositorio de proyecto | Enlaces a los repos de los proyectos vertebradores de la cohorte | Los students |

Tus responsabilidades directas: mantener tu ficha al día cada viernes, enlazar tus evidencias en lugar de describirlas, y usar las plantillas estándar. No inventes formato propio, porque la homogeneidad es lo que permite que la evaluación sea comparable y justa.

Tu ficha la ven tu mentor, el Lead, el director del programa y People. Escríbela sabiéndolo, con criterio profesional y sin adornos.

---

## Cinco cosas que conviene tener claras desde el día 1

1. **Tu nivel de entrada no determina tu resultado.** Los OKRs se calibran sobre tu baseline. Lo que se mide es tu progresión y si llegas al estándar de un junior solvente, no si empezaste sabiendo más o menos que otro.
2. **Los fundamentos no son relleno.** Un junior que no domina Git bloquea a todo su squad. Las tres primeras semanas parecen menos brillantes que los agentes, pero son la condición de entrada.
3. **La IA no sustituye entender lo que haces.** Nadie opera agentes sobre un SDLC que no comprende. Si aceptas código que no sabrías explicar, has creado un problema, no lo has resuelto.
4. **Todo lo que produzcas puede terminar delante de un cliente.** El proyecto, el pipeline, la configuración: trátalos con ese estándar desde el principio.
5. **Trabajamos para banca y seguros.** Seguridad, trazabilidad y uso responsable no son un módulo aparte, son la licencia para operar en estos clientes.
