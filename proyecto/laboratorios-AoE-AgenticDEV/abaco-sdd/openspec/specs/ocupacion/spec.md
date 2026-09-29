# ocupacion Specification

## Purpose
Calcular la ocupacion real de las personas y del area de forma exacta,
reproducible y comparable contra el objetivo de cada categoria.
## Requirements
### Requirement: Capacidad disponible
La capacidad disponible de una persona en un periodo SON los dias laborables del
periodo menos las ausencias no trabajables aprobadas. La formacion y el
banquillo SI computan como capacidad disponible; solo se excluyen vacaciones,
festivos y bajas.

#### Scenario: Persona sin ausencias
- **WHEN** se calcula la capacidad de una persona sin ausencias en el periodo
- **THEN** es igual al numero de dias laborables del periodo

#### Scenario: Formacion dentro del periodo
- **WHEN** la persona tiene una semana de formacion en el periodo
- **THEN** esos dias siguen contando como capacidad disponible

#### Scenario: Banquillo dentro del periodo
- **WHEN** la persona figura en banquillo durante parte del periodo
- **THEN** esos dias siguen contando como capacidad disponible

#### Scenario: Vacaciones dentro del periodo
- **WHEN** la persona tiene vacaciones aprobadas durante parte del periodo
- **THEN** esos dias laborables se restan de la capacidad

### Requirement: Utilizacion
La utilizacion es la proporcion entre dias equivalentes asignados y capacidad
disponible, expresada en porcentaje con dos decimales.

#### Scenario: Dedicacion completa
- **WHEN** una persona esta asignada al 100% durante todo el periodo y sin ausencias
- **THEN** su utilizacion es del 100,00%

#### Scenario: Media dedicacion
- **WHEN** una persona esta asignada al 50% durante todo el periodo
- **THEN** su utilizacion es del 50,00%

#### Scenario: Sin capacidad disponible
- **WHEN** la persona esta de vacaciones todo el periodo
- **THEN** su utilizacion es 0,00% y el calculo no falla

### Requirement: Corte de la sobreasignacion
Al calcular la utilizacion, la suma de dedicaciones de un dia NO DEBE superar el
100%. El exceso se reporta como indicador propio y no se diluye dentro de la
utilizacion.

#### Scenario: Persona al 150%
- **WHEN** una persona acumula dos asignaciones simultaneas del 100% y del 50%
- **THEN** su utilizacion es del 100,00% y su sobreasignacion del 50,00%

#### Scenario: Persona sin exceso
- **WHEN** la suma de dedicaciones no supera el 100% ningun dia
- **THEN** su sobreasignacion es 0,00%

### Requirement: Exclusion simetrica de dias no trabajables
Una asignacion NO DEBE computar durante una ausencia no trabajable aprobada.
Numerador y denominador excluyen exactamente los mismos dias.

#### Scenario: Asignacion que solapa vacaciones
- **WHEN** una persona asignada al 100% tiene tres semanas de vacaciones dentro del periodo
- **THEN** su utilizacion es del 100,00% y no superior

### Requirement: Comparacion contra el objetivo de la categoria
La utilizacion de una persona DEBE compararse contra el objetivo de utilizacion
de su categoria, nunca contra un objetivo unico de compania.

#### Scenario: Mismo numero, lectura distinta
- **WHEN** dos personas de categorias con objetivos distintos alcanzan la misma utilizacion
- **THEN** la desviacion sobre objetivo es distinta para cada una

### Requirement: Agregacion del area
La utilizacion agregada DEBE calcularse sumando numeradores y denominadores de
todas las personas y redondeando una sola vez al final. NO DEBE promediarse
porcentajes individuales ya redondeados, ni excluirse a las personas en
banquillo.

#### Scenario: Personas con capacidad distinta
- **WHEN** se agrega la utilizacion de personas con capacidades disponibles distintas
- **THEN** el resultado difiere del promedio de sus porcentajes individuales

#### Scenario: Persona en banquillo dentro del agregado
- **WHEN** una de las personas del area no tiene ninguna asignacion en el periodo
- **THEN** su capacidad entra en el denominador y baja el resultado agregado

### Requirement: Prorrateo por dias laborables efectivos
Una asignacion que cubre parcialmente el periodo DEBE prorratearse por los dias
laborables del solape, no por dias naturales ni por mes completo.

#### Scenario: Asignacion de medio mes
- **WHEN** una asignacion al 100% cubre poco mas de la mitad de los dias laborables del mes
- **THEN** aporta exactamente esos dias laborables y no el mes entero

### Requirement: Aritmetica decimal y redondeo unico
El calculo DEBE usar aritmetica decimal y aplicar el redondeo una sola vez, al
final. El resultado NO DEBE depender del orden de las asignaciones.

#### Scenario: Orden alterado
- **WHEN** se calcula la utilizacion con las asignaciones en orden inverso
- **THEN** el resultado es identico

### Requirement: Cobertura de demanda
La cobertura de una demanda es la proporcion de posiciones cubiertas por una
asignacion cuya categoria registrada iguala o supera la pedida.

#### Scenario: Media demanda cubierta
- **WHEN** una demanda de dos posiciones tiene una cubierta con categoria suficiente
- **THEN** su cobertura es del 50,00%

#### Scenario: Cubierta con categoria insuficiente
- **WHEN** la unica asignacion tiene categoria por debajo de la pedida
- **THEN** la posicion no cuenta como cubierta

### Requirement: Deteccion de banquillo
Una persona esta en banquillo cuando tiene capacidad disponible en el periodo y
ninguna asignacion que lo solape.

#### Scenario: Sin asignaciones y con capacidad
- **WHEN** una persona activa no tiene ninguna asignacion en el periodo
- **THEN** figura en banquillo

#### Scenario: Sin capacidad disponible
- **WHEN** una persona esta de baja todo el periodo
- **THEN** no figura en banquillo

