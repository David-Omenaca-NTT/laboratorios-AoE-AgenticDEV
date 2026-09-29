# salud Specification

## Purpose
Permitir que el pipeline y la sonda de plataforma comprueben en una sola llamada
si el servicio esta operativo y con que configuracion normativa arranco.
## Requirements
### Requirement: Comprobacion de salud
El servicio DEBE exponer un endpoint que informe de su disponibilidad sin
requerir autenticacion y sin consultar datos de personas.

#### Scenario: Servicio operativo
- **WHEN** se consulta el endpoint de salud y el servicio esta operativo
- **THEN** responde con estado correcto y el momento de la respuesta

#### Scenario: Version de catalogo cargada
- **WHEN** se consulta el endpoint de salud
- **THEN** informa de la version del catalogo de categorias que tiene cargada

#### Scenario: Sin acceso a datos personales
- **WHEN** se consulta el endpoint de salud
- **THEN** la respuesta no contiene ningun dato de ninguna persona

