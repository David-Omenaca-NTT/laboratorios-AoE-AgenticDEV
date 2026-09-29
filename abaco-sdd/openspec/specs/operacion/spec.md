# operacion Specification

## Purpose
Permitir diagnosticar un fallo en produccion y volver a un estado bueno conocido
en menos de diez minutos.
## Requirements
### Requirement: Registro de decisiones de negocio
Las rutas que toman decisiones de dominio DEBEN registrar la entrada relevante y
el resultado, sin incluir ningun dato de identificacion personal.

#### Scenario: Alta de demanda registrada
- **WHEN** se da de alta una demanda
- **THEN** queda registro con el identificador y el numero de posiciones

#### Scenario: Registro sin datos personales
- **WHEN** se inspecciona cualquier linea de registro
- **THEN** no contiene nombre, correo ni telefono de ninguna persona

### Requirement: Comprobacion de configuracion al arranque
El servicio DEBE fallar al arrancar si la configuracion normativa referenciada no
existe, en lugar de fallar mas tarde al atender una peticion.

#### Scenario: Version de catalogo inexistente
- **WHEN** la configuracion apunta a una version de catalogo que no existe
- **THEN** el servicio no llega a aceptar peticiones y el error nombra la version

### Requirement: Objetivo de recuperacion
El procedimiento de reversion DEBE permitir volver a la version anterior en
menos de diez minutos, y DEBE haberse ensayado antes del despliegue.

#### Scenario: Reversion ensayada
- **WHEN** se despliega una version nueva
- **THEN** existe constancia de que la reversion se ensayo con esa version

