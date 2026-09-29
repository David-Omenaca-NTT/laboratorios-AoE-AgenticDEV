# E7. Caracterizacion del calculo heredado

> **Nota didactica del laboratorio.** Este fichero no forma parte de OpenSpec.
> Se anade para que el cambio archivado sirva de referencia de consulta. En un
> repositorio real no existe.

El unico cambio del curso cuyos requisitos describen un defecto como si fuera una regla. Es deliberado.

## Que mirar en este cambio

- Primero se especifica lo que el sistema HACE, sin juzgarlo. La correccion viene en el cambio siguiente, y asi el archivo conserva las dos versiones y la fecha en que se paso de una a otra.
- Si caracterizas despues de refactorizar, tus requisitos describen el codigo nuevo y no tienes forma de saber si rompiste algo.
- El gate de procedencia comprueba en el historial que este cambio precede al siguiente.

## Los cuatro artefactos

| Fichero | Que es |
|---------|--------|
| `proposal.md` | Por que se hace y que capabilities toca. Es lo que revisa un humano ANTES de aprobar |
| `specs/` | Los requisitos con sus escenarios. Es el contrato, y lo unico que genera codigo |
| `design.md` | Decisiones tecnicas, alternativas descartadas y riesgos |
| `tasks.md` | La lista que ejecuta `/opsx:apply`. Todas marcadas, porque el cambio esta archivado |

## Como se genero

```bash
/opsx:new e7-caracterizacion-legado
/opsx:continue          # una vez por artefacto, revisando cada uno
/opsx:apply             # genera el codigo desde tasks.md
/opsx:verify            # comprueba completitud, correccion y coherencia
/opsx:archive           # sincroniza las specs principales y archiva
```
