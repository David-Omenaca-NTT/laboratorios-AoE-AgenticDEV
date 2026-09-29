## Purpose
Fijar por escrito lo que el calculo heredado hace hoy, sin juzgarlo, para poder
modificarlo despues sin romper nada por accidente.

## ADDED Requirements

### Requirement: Exclusion del banquillo del calculo global
El calculo heredado excluye del agregado a toda persona sin ninguna asignacion en
el periodo, no solo del numerador. Este comportamiento NO esta documentado en el
modulo y procede de un parche de 2021.

#### Scenario: Una persona ocupada y cuatro en banquillo
- **WHEN** se calcula el agregado con una persona al 100% y cuatro sin asignacion
- **THEN** el resultado heredado es del 100%

### Requirement: Promedio de porcentajes redondeados
El calculo heredado promedia utilizaciones individuales ya redondeadas en lugar
de agregar numeradores y denominadores.

#### Scenario: Personas con capacidad distinta
- **WHEN** se agregan personas con capacidades disponibles distintas
- **THEN** el resultado heredado coincide con el promedio de sus porcentajes y no con la agregacion

### Requirement: Asignacion computada durante ausencia
El calculo heredado cuenta como asignados los dias en que la persona estaba de
vacaciones, mientras los descuenta de la capacidad.

#### Scenario: Asignada al 100% con tres semanas de vacaciones
- **WHEN** se calcula la utilizacion individual de esa persona
- **THEN** el resultado heredado supera el 100%

### Requirement: Sobreasignacion sin corte
El calculo heredado permite que la utilizacion individual supere el 100% cuando
hay asignaciones simultaneas.

#### Scenario: Persona al 150%
- **WHEN** una persona acumula dedicaciones del 100% y del 50%
- **THEN** el resultado heredado es del 150%

### Requirement: Cache por periodo
El calculo heredado cachea el resultado por periodo y no por conjunto de datos,
de modo que dos escenarios distintos del mismo mes devuelven el primero
calculado.

#### Scenario: Dos conjuntos distintos del mismo mes
- **WHEN** se calculan dos conjuntos de datos distintos para el mismo periodo
- **THEN** el segundo devuelve el resultado del primero
