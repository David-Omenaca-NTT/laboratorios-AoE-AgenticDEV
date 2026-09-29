# Crítica del proyecto formativo Aula

**Versión:** v0.1  
**Fecha de análisis:** 2026-08-14  
**Alcance:** ejercicio, diseño pedagógico, enfoque de IA generativa/agentes y controles operativos del repositorio `aula`.

## Dictamen ejecutivo

Aula presenta un itinerario formativo sólido y bien contextualizado para incorporar perfiles junior a equipos que desarrollan con IA generativa. Sus mejores decisiones son empezar por una implementación manual, entrenar revisión adversarial y trazabilidad, usar un agente cuyo núcleo de decisión es determinista, y tratar legado, gobierno y operación como partes del mismo trabajo de ingeniería.

La principal debilidad es la distancia entre la narrativa de controles y su aplicación efectiva. El programa enseña que los gates, los verificadores y la evidencia deben ser reales; sin embargo, el agente de conformidad no revisa PRs reales ni bloquea según su veredicto, el despliegue de CI es un `echo`, los controles de manifiesto y de rutas son principalmente textuales o convencionales, y varios verificadores de estaciones validan presencia de archivos o palabras en vez de comportamiento ejecutado.

La recomendación es mantener la estructura y el dominio, pero **cerrar los P0 antes de una nueva cohorte**: convertir la conformidad en gate real, endurecer el manifiesto, implementar despliegue/reversión verificables y separar las barreras pedagógicas de los controles técnicos de seguridad.

## 1. Evaluación del ejercicio y del programa

### Aciertos

1. **Secuencia pedagógica adecuada.** Las estaciones avanzan desde fundamentos y rebanada vertical manual hasta SDD, contexto, MCP, agentes, legado, gobierno, operación y defensa. Evita que la generación de código sustituya la comprensión de código y pruebas (`aula/PLAYBOOK.md:174-187`, `aula/PLAYBOOK.md:201-213`, `aula/PLAYBOOK.md:279-326`).
2. **Dominio accesible con transferencia real.** Matrícula y expediente son comprensibles para la audiencia, pero permiten trabajar reglas versionadas, precisión decimal, trazabilidad y auditoría aplicables a dominios regulados (`aula/PLAYBOOK.md:27-44`).
3. **Revisión como competencia central.** Las rondas adversariales, la checklist de PR y el mensaje “no dejar pasar código mal generado” entrenan una habilidad crítica para trabajar con IA generativa (`aula/PLAYBOOK.md:330-366`, `aula/PLAYBOOK.md:486-495`).
4. **Invariantes de dominio explícitas.** `Decimal`, redondeo final, auditoría de cada decisión y trazabilidad de criterio a test son restricciones correctas y didácticamente valiosas (`aula/CLAUDE.md:18-31`).
5. **Andamiaje y autonomía razonables.** Verificadores transparentes, pistas escalonadas, bitácora y desbloqueo reducen el bloqueo sin eliminar responsabilidad sobre el aprendizaje (`aula/PLAYBOOK.md:80-99`, `aula/PLAYBOOK.md:152-170`, `aula/PLAYBOOK.md:370-394`).
6. **El agente se plantea como sistema evaluable.** S4a parte de una línea base, exige dos iteraciones y recomienda que cobertura, alcance y riesgo se calculen determinísticamente; el modelo solo redacta (`aula/PLAYBOOK.md:246-270`).
7. **El legado y el gobierno no son anexos.** Exigir caracterización antes de refactorizar y probar que un gate rechaza cambios enseña prácticas que suelen faltar en laboratorios de IA (`aula/PLAYBOOK.md:279-307`).

### Riesgos pedagógicos

1. **Sobrecarga de competencias en 196 horas.** El programa combina Python, Git, CI/CD, contenedores, dominio académico, pruebas, SDD, MCP, agentes, evaluación, legacy, seguridad y defensa. La vía con andamiaje en S4a es positiva, pero conviene formalizar diagnóstico de entrada, nivelación y capacidad de mentoría por competencia.
2. **La calibración puede convertirse en señal punitiva.** Predecir el resultado antes de verificar es una práctica formativa útil, pero requiere política clara: quién accede a la métrica, qué decisiones permite, cómo se corrigen sesgos y que no sea un sustituto opaco de evaluación (`aula/PLAYBOOK.md:117-127`).
3. **Los porcentajes no definen una rúbrica completa.** Precisión, detección adversarial, trazabilidad y costes son útiles, pero hay que publicar cómo se combinan con evidencia cualitativa, revisión humana, trabajo colaborativo y criterios de recuperación (`aula/PLAYBOOK.md:398-430`).
4. **La flotilla puede terminar como diagrama.** S4b explica bien contratos e interferencias, pero si triaje y modernización no son ejecutables, el alumno practica documentación de coordinación más que coordinación real. Debe declararse explícitamente como diseño o implementarse de extremo a extremo (`aula/PLAYBOOK.md:272-277`).
5. **La referencia visible debilita el desbloqueo como mecanismo.** El programa afirma que las referencias se liberan al sellar o desbloquear, pero la referencia resuelta las contiene. Para la plantilla student deben estar fuera del árbol accesible o servirse desde un flujo protegido (`aula/README.md:54-66`).

## 2. Evaluación del enfoque de IA generativa y agentes

### Aciertos

- El agente de conformidad reserva el veredicto para análisis de spec, diff y tests y limita el LLM a la explicación; es el patrón apropiado para una barrera de calidad (`aula/PLAYBOOK.md:261-265`).
- El servidor MCP es reducido y, por diseño, se orienta a exponer contexto de proyecto antes que a automatizar escrituras de alto riesgo (`aula/README.md:30-38`).
- La evaluación con línea base y métricas de precisión/recall hace visible la mejora y evita valorar el agente solo por lo convincente de su texto (`aula/README.md:41-52`, `aula/PLAYBOOK.md:256-259`).
- Los límites de contexto en `CLAUDE.md` expresan correctamente que workflows, verificadores, manifiestos y datasets de evaluación no deben ser modificables por el sistema vigilado (`aula/CLAUDE.md:57-67`).

### Carencias y mejoras

1. **El agente no es un gate de PR real.** CI ejecuta una evaluación estática del dorado, pero no obtiene el diff del PR, no ejecuta `agente.py --pr`, no publica el veredicto y no bloquea por `NO_CONFORME` (`aula/.github/workflows/ci.yml:69-79`; `aula/agentes/conformidad/agente.py`). Esto reduce S4a a evaluación offline. Debe integrarse contra el PR real, con evidencia adjunta y check obligatorio.
2. **Cobertura declarativa no equivale a cobertura efectiva.** Una etiqueta `cubre:` puede no representar aserciones útiles, relación con el cambio o ejecución del test. El agente debe derivar criterios afectados desde el diff y la spec, ejecutar pruebas pertinentes y usar AST/mutaciones/contraejemplos para detectar tests decorativos.
3. **La evaluación F1=1,0 no demuestra robustez suficiente.** Un conjunto de 15 PRs es útil para aprendizaje, pero no acredita generalización. Se necesita conjunto holdout custodiado, versionado de datos, pruebas adversariales, FPR/FNR, regresiones y evaluación posterior a merge (`aula/README.md:35`, `aula/README.md:51-52`).
4. **MCP debe limitar ejecución de tests.** Si acepta rutas arbitrarias para pytest, debe resolver y restringir targets bajo `tests/`, definir timeouts/límites de salida y aislar procesos. El hecho de no usar shell no sustituye una allowlist.
5. **Faltan amenazas específicas de agentes.** Añadir inyección de instrucciones mediante archivos de repo, abuso de herramientas, cambios de políticas, evasión de contexto, contaminación de datos de evaluación y salidas no deterministas daría profundidad a S3, S4 y S6.

## 3. Coherencia de controles y operación

| Prioridad | Hallazgo | Evidencia | Impacto |
|---|---|---|---|
| P0 | El agente se evalúa contra el dorado, pero no revisa ni bloquea PRs reales. | `aula/.github/workflows/ci.yml:69-79`; `aula/PLAYBOOK.md:246-265` | La principal pieza de S4a no funciona como control de entrega. |
| P0 | El despliegue de CI es solo un `echo`; no existe destino, publicación, smoke test ni rollback ejecutado. | `aula/.github/workflows/ci.yml:91-99` | Contradice S7: despliegue, fallo y MTTR dejan de ser evidencia operativa. |
| P0 | El gate de manifiesto se activa solo para `agentes/**` y `manifiestos/**`; no cubre MCP, permisos, dependencias, evaluador, workflows ni contexto. | `aula/.github/workflows/gate-manifiesto.yml:6-10` | Cambios que alteran riesgo o comportamiento pueden eludir re-evaluación y gobierno. |
| P0 | El manifiesto se valida por texto/regex y hash opcional truncado de un único agente. | `aula/.github/workflows/gate-manifiesto.yml:27-65` | No se valida semántica YAML, relación con el agente afectado ni autenticidad de la evidencia. |
| P0 | El manifiesto indica revertir `conformidad.yml`, workflow inexistente. | `aula/manifiestos/conformidad-spec.yaml:56-59`; `aula/.github/workflows/` | El procedimiento de reversión no es ejecutable ni confiable. |
| P1 | Las restricciones de rutas en configuración y hook son convenciones del cliente, no barreras para shell, Git, scripts u otros agentes. | `aula/.claude/settings.json`; `aula/herramientas/hook_rutas.py` | Un control pedagógico puede confundirse con aislamiento de seguridad. |
| P1 | S3 y S6 comprueban en parte texto/presencia, no la ejecución del hook o del workflow. | `aula/labs/S3-contexto/verificar.py`; `aula/labs/S6-gobierno/verificar.py` | Se puede aprobar con artefactos inoperantes. |
| P1 | El progreso y desbloqueo son locales y no están firmados ni validados remotamente. | `aula/aula_cli/__main__.py`; `aula/.aula/progreso.json` | El sellado no constituye evidencia independiente de superación. |
| P1 | CODEOWNERS no demuestra que haya protección de rama efectiva. | `aula/.github/CODEOWNERS`; `aula/labs/S0-bootstrap/verificar.py` | La seguridad depende de configuración externa no comprobada. |
| P2 | CI pide solo 60% de cobertura general, insuficiente para las invariantes anunciadas. | `aula/.github/workflows/ci.yml:38-41`; `aula/README.md:41-52` | La cobertura puede crecer por código trivial sin proteger decisiones sensibles. |
| P2 | Dependencias e imagen no están bloqueadas por lockfile o digest. | `aula/requirements.txt`; `aula/Containerfile:4-9` | El entorno no ofrece la reproducibilidad que se exige al alumnado. |
| P2 | Varios verificadores validan presencia documental en vez de una prueba reproducible. | `aula/labs/S4b-flotilla/verificar.py`; `aula/labs/S7-despliegue/verificar.py`; `aula/labs/S8-defensa/verificar.py` | Incentiva cumplir patrones de texto en lugar de demostrar propiedades. |

## 4. Plan de mejora priorizado

### P0 — Antes de impartir una nueva cohorte

1. **Convertir conformidad en required check real.** Extraer el diff y metadatos del PR, derivar criterios afectados, ejecutar el agente sobre ese input, publicar el informe y bloquear el merge ante no conformidad. La evaluación dorada debe mantenerse como regresión separada.
2. **Implementar despliegue o retirar la promesa.** Publicar imagen inmutable por digest, desplegar a entorno aislado, ejecutar smoke/readiness tests y ejercicio de reversión; almacenar evidencia de MTTR. Un `echo` no es un despliegue.
3. **Sustituir gate textual por validación estructurada.** Parsear manifiestos YAML contra un esquema, exigir hash SHA-256 completo, asociar un manifiesto a cada agente ejecutable y activar el gate ante cambios de código, evaluaciones, MCP, permisos, dependencias y políticas relevantes.
4. **Corregir el procedimiento de reversión.** Referenciar workflows y mecanismos existentes, priorizar deshabilitar capacidad o revertir versión desplegada antes que desactivar controles de gobierno, y probar el procedimiento regularmente.

### P1 — Hacer reales los límites y la evidencia

5. **Separar instrucción de seguridad.** Mantener `CLAUDE.md` y hooks como aprendizaje, pero aplicar en servidor reglas de rama, CODEOWNERS efectivos, permisos mínimos, tokens sin secretos, entornos con aprobadores y CI independiente.
6. **Reemplazar verificaciones textuales por integración.** Usar repositorios temporales o fixtures para intentar escrituras prohibidas, disparar hooks/workflows y demostrar rechazos; mutar manifiestos y probar que los gates fallan.
7. **Fortalecer el agente y sus pruebas.** Matching seguro de rutas, alcance obligatorio, análisis AST de tests, ejecución selectiva de pruebas, mutaciones, casos límite y evaluación holdout.
8. **Proteger el mecanismo de progreso.** Registrar cierres/desbloqueos en CI o plataforma de cohorte, requerir bitácora y validación mentor donde proceda, y entregar referencias desde una ubicación no accesible hasta el hito correspondiente.
9. **Aislar MCP.** Aplicar allowlist de herramientas y rutas, límites de recursos, resolución de paths, timeouts y un modelo explícito de autenticación/origen si deja el entorno local.

### P2 — Sostenibilidad y profundidad técnica

10. **Fijar entorno y cadena de suministro.** Lockfiles con hashes, imágenes por digest, SBOM, escaneo de vulnerabilidades, firma/provenance de artefactos y política de actualización.
11. **Completar S4b.** Implementar triaje y modernización con permisos, worktrees, handoffs y conflictos reproducibles; alternativamente, renombrar la estación como diseño de contrato y no como flotilla operativa.
12. **Proteger auditoría y API.** Añadir autenticación/autorización, persistencia, idempotencia, validación de entradas, manejo de fallos y auditoría append-only con retención, integridad y seudonimización.
13. **Hacer la evaluación de estaciones híbrida y explícita.** Distinguir controles automáticos, pruebas de integración, evidencia humana y defensa; no presentar una búsqueda textual como prueba de seguridad u operación.

## 5. Conclusión

Aula tiene un núcleo pedagógico muy fuerte: coloca el criterio de revisión por encima de la velocidad de generación, enseña que la especificación, los tests y la auditoría son activos de ingeniería, y sitúa gobierno y operación dentro del ciclo de vida de un agente. Es una base excelente para formación en desarrollo con IA generativa.

La siguiente mejora no es añadir más temas, sino lograr que el propio laboratorio cumpla su tesis: cada control que se declara debe ejecutarse, cada evidencia debe ser verificable y cada puerta debe ser difícil de eludir. Con los P0 resueltos, Aula puede convertirse en un programa formativo especialmente defendible para contextos de ingeniería y regulación exigentes.
