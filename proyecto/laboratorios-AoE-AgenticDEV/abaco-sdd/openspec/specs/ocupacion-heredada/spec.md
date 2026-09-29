# ocupacion-heredada Specification

## Purpose
Fijar por escrito lo que el calculo heredado hace hoy, sin juzgarlo, para poder
modificarlo despues sin romper nada por accidente.
## Requirements
### Requirement: Exclusion del banquillo del calculo global
El calculo NO DEBE excluir del agregado a las personas sin asignacion. Su
capacidad disponible entra en el denominador.

#### Scenario: Una persona ocupada y cuatro en banquillo
- **WHEN** se calcula el agregado con una persona al 100% y cuatro sin asignacion
- **THEN** el resultado refleja la capacidad de las cinco y es muy inferior al 100%

### Requirement: Promedio de porcentajes redondeados
El calculo DEBE agregar numeradores y denominadores y redondear una sola vez al
final, en lugar de promediar porcentajes ya redondeados.

#### Scenario: Personas con capacidad distinta
- **WHEN** se agregan personas con capacidades disponibles distintas
- **THEN** el resultado corresponde a la agregacion y no al promedio de porcentajes

### Requirement: Asignacion computada durante ausencia
El calculo NO DEBE contar como asignados los dias cubiertos por una ausencia no
trabajable aprobada. Numerador y denominador excluyen los mismos dias.

#### Scenario: Asignada al 100% con tres semanas de vacaciones
- **WHEN** se calcula la utilizacion individual de esa persona
- **THEN** el resultado es del 100,00% y no superior

### Requirement: Sobreasignacion sin corte
El calculo DEBE cortar la suma de dedicaciones diarias en el 100% y reportar el
exceso como indicador de sobreasignacion.

#### Scenario: Persona al 150%
- **WHEN** una persona acumula dedicaciones del 100% y del 50%
- **THEN** su utilizacion es del 100,00% y su sobreasignacion del 50,00%

### Requirement: Cache por periodo
El calculo heredado cachea el resultado por periodo y no por conjunto de datos,
de modo que dos escenarios distintos del mismo mes devuelven el primero
calculado.

#### Scenario: Dos conjuntos distintos del mismo mes
- **WHEN** se calculan dos conjuntos de datos distintos para el mismo periodo
- **THEN** el segundo devuelve el resultado del primero

