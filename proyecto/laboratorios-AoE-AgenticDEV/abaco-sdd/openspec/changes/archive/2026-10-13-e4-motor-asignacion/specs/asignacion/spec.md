## Purpose
Decidir de forma reproducible y explicable si una persona puede ser asignada a
una posicion, aplicando la normativa vigente en la fecha de inicio.

## ADDED Requirements

### Requirement: Limite de capacidad
La suma de dedicaciones de una persona en cualquier punto del periodo NO DEBE
superar el 100%. El solape se comprueba sobre el intervalo completo y no
unicamente sobre la fecha de inicio.

#### Scenario: Persona libre
- **WHEN** se evalua a una persona sin asignaciones que solapen el periodo
- **THEN** la restriccion de capacidad no la rechaza

#### Scenario: Solape parcial por el final
- **WHEN** una asignacion previa empieza antes del periodo y termina dentro de el
- **THEN** cuenta como solape y su dedicacion consume capacidad

#### Scenario: Asignacion anterior sin solape
- **WHEN** una asignacion previa termina antes de que empiece el periodo
- **THEN** no consume capacidad en ese periodo

### Requirement: Sobreasignacion bajo aprobacion
Una dedicacion total superior al 100% SOLO DEBE admitirse si esta dentro de la
tolerancia de la politica vigente y existe aprobacion explicita registrada.

#### Scenario: Sobreasignacion dentro de tolerancia y aprobada
- **WHEN** el total queda dentro de la tolerancia y hay aprobacion registrada
- **THEN** el candidato es apto

#### Scenario: Sobreasignacion dentro de tolerancia sin aprobacion
- **WHEN** el total queda dentro de la tolerancia y no hay aprobacion
- **THEN** el candidato se rechaza por sobreasignacion no aprobada

#### Scenario: Sobreasignacion por encima de la tolerancia
- **WHEN** el total supera la tolerancia de la politica
- **THEN** el candidato se rechaza aunque exista aprobacion

### Requirement: Encaje de categoria y skill
El candidato DEBE igualar o superar en orden de seniority la categoria pedida y
alcanzar el nivel minimo del skill exigido.

#### Scenario: Categoria por debajo
- **WHEN** se evalua a alguien de categoria inferior a la pedida
- **THEN** se rechaza indicando categoria insuficiente

#### Scenario: Categoria superior
- **WHEN** se evalua a alguien de categoria superior a la pedida
- **THEN** la restriccion de categoria no lo rechaza

#### Scenario: Nivel de skill insuficiente
- **WHEN** el candidato tiene el skill pedido por debajo del nivel minimo
- **THEN** se rechaza indicando nivel insuficiente

### Requirement: Categoria vigente en la fecha de inicio
La asignacion DEBE registrar la categoria que la persona tenia vigente en la
fecha de inicio de la asignacion, no la que tenga en el momento del calculo.

#### Scenario: Persona promocionada despues del inicio
- **WHEN** una persona asciende despues de la fecha de inicio de una asignacion
- **THEN** esa asignacion sigue registrando la categoria anterior

#### Scenario: Sin categoria vigente en la fecha
- **WHEN** la persona no tiene ninguna vigencia de categoria que cubra la fecha de inicio
- **THEN** el candidato se rechaza

### Requirement: Disponibilidad
Una ausencia aprobada que solape el periodo, o una persona no activa, DEBEN
impedir la asignacion.

#### Scenario: Ausencia aprobada solapada
- **WHEN** el candidato tiene vacaciones aprobadas dentro del periodo
- **THEN** se rechaza por ausencia

#### Scenario: Ausencia no aprobada
- **WHEN** la ausencia que solapa no esta aprobada
- **THEN** no bloquea la asignacion

#### Scenario: Persona de baja antes del periodo
- **WHEN** la fecha de baja de la persona es anterior al inicio del periodo
- **THEN** se rechaza por persona no activa

### Requirement: Veredicto completo
El veredicto DEBE incluir todos los motivos de rechazo aplicables y no
unicamente el primero encontrado.

#### Scenario: Varios incumplimientos a la vez
- **WHEN** un candidato incumple a la vez categoria y nivel de skill
- **THEN** el veredicto recoge los dos motivos

### Requirement: Traza de decision con origen
Toda creacion de asignacion DEBE escribir traza con la version de politica, la
version de catalogo y el origen de la decision.

#### Scenario: Decision tomada por una persona
- **WHEN** un resource manager crea una asignacion
- **THEN** la traza recoge origen api con las dos versiones aplicadas

#### Scenario: Decision tomada por un agente
- **WHEN** la asignacion llega por la via del agente
- **THEN** la traza recoge origen agente con las mismas versiones

#### Scenario: Origen no declarado
- **WHEN** se intenta registrar una decision con un origen que no esta en la lista
- **THEN** el registro se rechaza
