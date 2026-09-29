# SPEC-003: ciclo de vida de la demanda

Versión: v1.0.0 | Estado: activa

## Propósito

Gobernar el ciclo de vida de una demanda de recursos desde que un manager la
solicita hasta que se cierra o se cancela, con los ocho estados del PRD.

## Invariantes

- INV-01: una demanda en estado terminal, cerrada o cancelada, no admite asignaciones nuevas.
- INV-02: los estados terminales no tienen transición de salida. No se reabre una demanda: se crea otra.

## Criterios de aceptación

- CA-01: dada una demanda nueva, cuando recorre el camino completo, entonces pasa por solicitada, aprobada, buscando, candidato propuesto, aceptada, asignada y cerrada.
- CA-02: dada una transición no declarada en el modelo, cuando se intenta, entonces se rechaza con error explícito.
- CA-03: dada una demanda en cualquier estado no terminal salvo asignada, cuando se cancela, entonces la transición es válida. Una demanda ya asignada no se cancela: se cierra.
- CA-04: dado un candidato rechazado por el solicitante, cuando se procesa el rechazo, entonces la demanda vuelve a buscando, no se cancela ni queda bloqueada.

## Casos límite

| Caso | Resultado esperado |
|------|--------------------|
| Cancelar una demanda ya asignada | Rechazado. Se cierra, no se cancela: cancelarla dejaría asignaciones huérfanas |
| Rechazar al candidato estando en aceptada | Vuelve a buscando, no a candidato propuesto |
| Transición de un estado terminal a cualquier otro | Rechazado. Los terminales no tienen salida |
| Demanda cancelada a la que llega una asignación tardía | Rechazado por INV-01, con error explícito |

## Fuera de alcance

Rutas: src/abaco/dominio/estados.py, tests/test_estados_demanda.py, specs/SPEC-003-demanda.md

- Aprobación multinivel configurable.
- Notificaciones y escalados asociados a los cambios de estado.
- Reapertura de demandas cerradas.

## Ambigüedades detectadas y resolución

| # | Ambigüedad | Resolución |
|---|-----------|------------|
| A-01 | El PRD no aclara qué pasa cuando el solicitante rechaza al candidato propuesto | Vuelve a buscando. Recogido en CA-04 |
| A-02 | El PRD no aclara si una demanda asignada puede cancelarse | No. Se cierra. Cancelar una demanda con gente ya asignada dejaría asignaciones huérfanas |
