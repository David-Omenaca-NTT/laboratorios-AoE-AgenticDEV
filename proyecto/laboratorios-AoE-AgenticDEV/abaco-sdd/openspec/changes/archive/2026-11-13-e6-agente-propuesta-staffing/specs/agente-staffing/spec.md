## Purpose
Proponer candidatos para una demanda de forma reproducible y explicable, sin
tomar nunca la decision, y dejando por escrito a quien se descarta y por que.

## ADDED Requirements

### Requirement: Techo de autonomia
El agente NO DEBE crear, confirmar ni modificar asignaciones bajo ninguna
circunstancia. Su unica salida es una propuesta.

#### Scenario: Intento de creacion de asignacion
- **WHEN** se solicita al agente que asigne directamente a un candidato
- **THEN** devuelve una propuesta y no se crea ninguna asignacion

#### Scenario: Ausencia de via de escritura
- **WHEN** se inspecciona el codigo del agente
- **THEN** no existe ninguna ruta que invoque la creacion de asignaciones

### Requirement: Filtrado determinista
El filtrado por restricciones duras, la comprobacion de disponibilidad, el
encaje de categoria y la aritmetica de ocupacion DEBEN calcularse de forma
determinista, sin intervencion de modelo.

#### Scenario: Ejecuciones repetidas
- **WHEN** se ejecuta el agente cinco veces sobre la misma demanda y el mismo contexto
- **THEN** devuelve la misma lista de candidatos en el mismo orden

### Requirement: Cero violaciones de restriccion dura
Ningun candidato propuesto DEBE incumplir una restriccion dura de la capability
de asignacion.

#### Scenario: Candidato no disponible
- **WHEN** una persona tiene una ausencia aprobada que solapa el periodo
- **THEN** no aparece entre los candidatos propuestos

#### Scenario: Candidato de categoria insuficiente
- **WHEN** una persona esta por debajo de la categoria pedida
- **THEN** no aparece entre los candidatos propuestos

#### Scenario: Candidato sin capacidad
- **WHEN** una persona ya esta al 100% en el periodo
- **THEN** no aparece entre los candidatos propuestos

### Requirement: Alternativas descartadas
La propuesta DEBE incluir las personas descartadas agrupadas por motivo, con el
recuento de cada motivo.

#### Scenario: Descartes agrupados
- **WHEN** se genera una propuesta sobre un pool con descartes por motivos distintos
- **THEN** la salida agrupa los descartados por motivo con su recuento

#### Scenario: Consulta sobre una persona concreta
- **WHEN** se pregunta por que una persona concreta no fue propuesta
- **THEN** se obtiene el motivo o motivos concretos de su descarte

### Requirement: Evidencia por candidato
Cada candidato propuesto DEBE ir acompanado de la categoria vigente en la fecha
de inicio, el nivel del skill pedido, la capacidad libre y su utilizacion frente
al objetivo de su categoria.

#### Scenario: Candidato con evidencia completa
- **WHEN** se genera una propuesta
- **THEN** cada candidato lleva los cuatro datos de evidencia

### Requirement: Datos de identificacion excluidos
El agente NO DEBE acceder a nombre, correo, telefono, foto, pais, oficina, fecha
de nacimiento ni genero de ninguna persona.

#### Scenario: Intento de lectura de campo excluido
- **WHEN** el agente intenta leer un campo de identificacion personal
- **THEN** la operacion falla

### Requirement: Versiones aplicadas en la propuesta
La propuesta DEBE declarar la version del catalogo de categorias y la de la
politica de capacidad con las que se genero.

#### Scenario: Propuesta con versiones
- **WHEN** se genera una propuesta
- **THEN** figura la version de catalogo y la de politica aplicadas
