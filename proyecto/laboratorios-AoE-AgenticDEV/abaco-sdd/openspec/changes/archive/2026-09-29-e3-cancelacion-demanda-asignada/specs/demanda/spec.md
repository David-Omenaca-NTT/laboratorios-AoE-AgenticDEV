## MODIFIED Requirements

### Requirement: Transiciones permitidas
El sistema DEBE rechazar cualquier transicion de estado que no este declarada
como valida, indicando el estado de origen y el de destino. La cancelacion desde
el estado asignada SE PERMITE unicamente cuando se aporta motivo de cancelacion.

#### Scenario: Transicion no declarada
- **WHEN** se intenta pasar una demanda de solicitada directamente a asignada
- **THEN** la transicion se rechaza con un error que nombra origen y destino

#### Scenario: Cancelacion desde estado no terminal
- **WHEN** se cancela una demanda que esta en solicitada, aprobada, buscando, candidato propuesto o aceptada
- **THEN** la transicion se acepta y la demanda queda cancelada

#### Scenario: Cancelacion de demanda ya asignada
- **WHEN** se intenta cancelar una demanda en estado asignada sin aportar motivo
- **THEN** la transicion se rechaza, porque cancelarla dejaria asignaciones sin demanda que las justifique

#### Scenario: Cancelacion de demanda asignada con motivo
- **WHEN** se cancela una demanda en estado asignada aportando motivo
- **THEN** la transicion se acepta y la demanda queda cancelada

## ADDED Requirements

### Requirement: Constancia de asignaciones afectadas
Al cancelar una demanda asignada, el sistema DEBE registrar en la traza cuantas
asignaciones quedan sin demanda que las justifique.

#### Scenario: Registro de asignaciones huerfanas
- **WHEN** se cancela una demanda asignada que tenia dos asignaciones vinculadas
- **THEN** la traza recoge el motivo y el numero de asignaciones afectadas

#### Scenario: Cancelacion sin asignaciones vinculadas
- **WHEN** se cancela una demanda asignada que no llego a tener asignaciones
- **THEN** la traza recoge el motivo y cero asignaciones afectadas
