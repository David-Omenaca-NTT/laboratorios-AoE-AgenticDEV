## Purpose
Gobernar el ciclo de vida de una peticion de recursos para que en todo momento
se sepa en que punto esta, quien tiene la pelota y si admite asignaciones.

## ADDED Requirements

### Requirement: Estados de la demanda
Una demanda DEBE encontrarse siempre en uno de estos ocho estados: solicitada,
aprobada, buscando, candidato propuesto, aceptada, asignada, cerrada o
cancelada.

#### Scenario: Estado inicial
- **WHEN** se da de alta una demanda
- **THEN** queda en estado solicitada

#### Scenario: Recorrido completo
- **WHEN** una demanda avanza por todas sus fases sin incidencias
- **THEN** recorre solicitada, aprobada, buscando, candidato propuesto, aceptada, asignada y cerrada, en ese orden

### Requirement: Transiciones permitidas
El sistema DEBE rechazar cualquier transicion de estado que no este declarada
como valida, indicando el estado de origen y el de destino.

#### Scenario: Transicion no declarada
- **WHEN** se intenta pasar una demanda de solicitada directamente a asignada
- **THEN** la transicion se rechaza con un error que nombra origen y destino

#### Scenario: Cancelacion desde estado no terminal
- **WHEN** se cancela una demanda que esta en solicitada, aprobada, buscando, candidato propuesto o aceptada
- **THEN** la transicion se acepta y la demanda queda cancelada

#### Scenario: Cancelacion de demanda ya asignada
- **WHEN** se intenta cancelar una demanda en estado asignada
- **THEN** la transicion se rechaza, porque cancelarla dejaria asignaciones sin demanda que las justifique

### Requirement: Rechazo de candidato
Cuando el solicitante rechaza al candidato propuesto, la demanda DEBE volver a
busqueda y no quedar bloqueada ni cancelada.

#### Scenario: Rechazo desde candidato propuesto
- **WHEN** el solicitante rechaza al candidato de una demanda en estado candidato propuesto
- **THEN** la demanda vuelve al estado buscando

#### Scenario: Rechazo desde aceptada
- **WHEN** el candidato aceptado cae antes de formalizarse la asignacion
- **THEN** la demanda vuelve al estado buscando

#### Scenario: Rechazo desde un estado que no lo admite
- **WHEN** se intenta devolver a busqueda una demanda en estado solicitada
- **THEN** la operacion se rechaza

### Requirement: Estados terminales
Una demanda cerrada o cancelada NO DEBE admitir asignaciones nuevas ni
transiciones de salida.

#### Scenario: Asignacion sobre demanda cancelada
- **WHEN** llega una asignacion tardia para una demanda cancelada
- **THEN** se rechaza indicando el estado de la demanda

#### Scenario: Sin salida desde terminal
- **WHEN** se consultan las transiciones validas de una demanda cerrada
- **THEN** no hay ninguna disponible
