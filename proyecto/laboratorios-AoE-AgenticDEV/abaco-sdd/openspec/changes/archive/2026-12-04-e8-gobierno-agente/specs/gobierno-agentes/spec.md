## Purpose
Convertir el gobierno de un agente que decide sobre personas en controles
mecanicos que fallan solos, en lugar de politicas escritas que alguien deberia
recordar.

## ADDED Requirements

### Requirement: Manifiesto obligatorio
Todo agente DEBE tener un manifiesto versionado que declare proposito,
propietario humano, herramientas, datos accesibles, datos prohibidos, nivel de
autonomia, evaluacion con fecha, coste y procedimiento de reversion.

#### Scenario: Cambio sobre un agente sin manifiesto
- **WHEN** se propone un cambio que toca el codigo de un agente y no existe manifiesto
- **THEN** el pipeline bloquea el merge

#### Scenario: Manifiesto incompleto
- **WHEN** el manifiesto omite alguno de los apartados obligatorios
- **THEN** el pipeline bloquea el merge indicando cual falta

### Requirement: Apartados propios de decisiones sobre personas
El manifiesto de un agente que afecta a personas DEBE declarar ademas las
personas afectadas, la explicabilidad, la via de contestacion, el veto humano y
la vigilancia de concentracion.

#### Scenario: Manifiesto de agente sobre personas sin via de contestacion
- **WHEN** el manifiesto declara personas afectadas pero no via de contestacion
- **THEN** el pipeline bloquea el merge

### Requirement: Techo de autonomia por radio de dano
Un agente cuyo manifiesto declare personas afectadas NO DEBE declarar un nivel
de autonomia superior a N2.

#### Scenario: Agente sobre personas que declara N3
- **WHEN** un manifiesto con personas afectadas declara nivel N3
- **THEN** el pipeline bloquea el merge indicando que el techo lo fija la reversibilidad del dano

#### Scenario: Agente sin personas afectadas que declara N3
- **WHEN** un agente que solo detecta hechos verificables declara nivel N3
- **THEN** el pipeline lo admite

### Requirement: Alineacion entre manifiesto y codigo
El manifiesto DEBE declarar la huella del codigo del agente, y el pipeline DEBE
rechazar el merge si no coincide con el codigo presente.

#### Scenario: Codigo modificado sin actualizar el manifiesto
- **WHEN** cambia el codigo del agente y el manifiesto conserva la huella anterior
- **THEN** el pipeline bloquea el merge

### Requirement: Vigencia de la evaluacion
La evaluacion referenciada en el manifiesto NO DEBE tener mas de treinta dias.

#### Scenario: Evaluacion caducada
- **WHEN** la fecha de evaluacion declarada supera los treinta dias
- **THEN** el pipeline bloquea el merge

### Requirement: Deriva entre especificacion y codigo
El sistema DEBE medir los requisitos sin codigo que los implemente y el codigo
sin requisito que lo justifique, y bloquear cuando la deriva supere el umbral.

#### Scenario: Codigo sin requisito
- **WHEN** aparece un modulo generado que ningun requisito justifica
- **THEN** la medicion de deriva lo detecta y el pipeline avisa

#### Scenario: Requisito sin implementar
- **WHEN** una capability contiene un requisito sin ninguna implementacion asociada
- **THEN** la medicion de deriva lo detecta

### Requirement: Procedencia del codigo generado
Todo commit que toque codigo generado DEBE referenciar el cambio que lo origina,
y ese cambio DEBE existir como carpeta activa o archivada.

#### Scenario: Commit sin referencia de cambio
- **WHEN** un commit modifica codigo generado sin declarar el cambio de origen
- **THEN** el pipeline bloquea el merge

#### Scenario: Referencia a un cambio inexistente
- **WHEN** el commit referencia un cambio que no existe ni activo ni archivado
- **THEN** el pipeline bloquea el merge

### Requirement: Integridad de la bateria de aceptacion
La bateria de aceptacion externa NO DEBE ser modificada por ningun commit
marcado como generado.

#### Scenario: Commit generado que toca la bateria
- **WHEN** un commit con marca de generacion modifica la bateria de aceptacion
- **THEN** el pipeline bloquea el merge
