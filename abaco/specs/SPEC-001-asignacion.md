# SPEC-001: motor de asignación

Versión: v1.4.0 | Estado: activa
Autor: referencia del laboratorio | Revisor: SME de plataforma

## Propósito

Decidir si una persona puede ser asignada a una posición de una demanda en un
periodo dado, aplicando las reglas duras de capacidad, categoría, skill y
disponibilidad vigentes en la fecha de inicio de la asignación. La decisión debe
quedar auditada con la versión de política y de catálogo aplicadas, y con el
origen de la decisión.

## Entradas y salidas

| Elemento | Tipo | Restricciones |
|----------|------|---------------|
| Persona | Identidad, histórico de categoría, skills | Sin datos retributivos: quedan fuera del sistema |
| Posición | Rol, categoría, skill, nivel mínimo, dedicación | La dedicación debe ser válida en la política vigente |
| Periodo | Desde y hasta | Intervalo cerrado en ambos extremos |
| Catálogo de categorías | Versionado por vigencia | El aplicable es el vigente en la fecha de inicio |
| Política de capacidad | Versionada | Fija tolerancia de sobreasignación y dedicaciones válidas |
| Salida | Veredicto con todos los motivos de rechazo | Nunca un único motivo: el agente necesita explicar |

## Invariantes

- INV-01: toda decisión de asignación escribe una entrada de auditoría con versión de política, versión de catálogo y **origen** (api, agente, carga o corrección manual). Las decisiones del agente se auditan igual que las de una persona.
- INV-02: una asignación confirmada no cambia de categoría registrada en silencio. Exige versión de catálogo nueva y deja traza.
- INV-03: el veredicto de un candidato es reproducible: los mismos datos producen el mismo resultado y los mismos motivos.

## Criterios de aceptación

- CA-01: dada una persona con asignaciones que solapan el periodo, cuando se evalúa un candidato, entonces la suma de dedicaciones no puede superar el 100%. El solape se comprueba sobre el intervalo completo, no solo sobre la fecha de inicio.
- CA-02: dada una sobreasignación dentro de la tolerancia de la política vigente, cuando se evalúa el candidato, entonces se admite solo con aprobación explícita registrada. Por encima de la tolerancia se rechaza siempre.
- CA-03: dada una posición que pide categoría y skill con nivel mínimo, cuando se evalúa un candidato, entonces su categoría debe igualar o superar la pedida en orden de seniority y su nivel de skill debe alcanzar el mínimo.
- CA-04: dada una ausencia aprobada que solapa el periodo, o una persona no activa, cuando se evalúa el candidato, entonces se rechaza. Una ausencia no aprobada no bloquea.
- CA-05: dada una asignación, cuando se crea, entonces registra la categoría vigente de la persona **en su fecha de inicio**, nunca la actual. Una promoción posterior no reescribe el histórico.
- CA-06: dada una dedicación, cuando se crea la asignación en modalidad porcentual, entonces debe ser una de las declaradas válidas en la política. La modalidad horaria no está sujeta a esa lista.
- CA-07: dadas varias demandas concurrentes, cuando se ordenan para asignar, entonces se ordenan por prioridad declarada y, a igualdad, por momento de solicitud ascendente.

## Casos límite

| Caso | Resultado esperado |
|------|--------------------|
| Asignación que empieza antes del periodo y termina dentro | Solapa. Es el caso que detecta el error de comprobar solo la fecha de inicio |
| Persona sin categoría vigente en la fecha de inicio | Rechazo por categoría, no excepción |
| Candidato que incumple categoría y skill a la vez | El veredicto devuelve los dos motivos, no solo el primero |
| Sobreasignación exactamente en el límite de tolerancia | Admitida con aprobación explícita |
| Persona de baja el día anterior al inicio | No activa |

## Fuera de alcance

Rutas: src/abaco/reglas/motor.py, src/abaco/dominio/, tests/test_motor_asignacion.py, specs/SPEC-001-asignacion.md

- Cálculo de utilización, que es objeto de SPEC-002.
- Transiciones de la demanda, que son objeto de SPEC-003.
- Coste, tarifa y margen: fuera del sistema por decisión de minimización de datos.
- Reserva de plazas y gestión de lista de espera a lo largo del proyecto.
- Aprobación multinivel de la sobreasignación: aquí solo se consume el hecho de que exista aprobación.

## Ambigüedades detectadas y resolución

| # | Ambigüedad | Resolución | Fecha |
|---|-----------|------------|-------|
| A-01 | No estaba definido si el solape se comprueba sobre la fecha de inicio o sobre el intervalo completo | Sobre el intervalo completo. Recogido en CA-01 y con test específico | 2026-08 |
| A-02 | No estaba definido qué categoría aplica cuando la persona ha promocionado entre la solicitud y el inicio | La vigente en la fecha de inicio. Recogido en CA-05 | 2026-08 |
| A-03 | El veredicto devolvía solo el primer motivo de rechazo, lo que producía explicaciones pobres del agente | Devuelve todos los motivos | 2026-08 |
