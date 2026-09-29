# E5. Calculo de utilizacion y ocupacion

> **Nota didactica del laboratorio.** Este fichero no forma parte de OpenSpec.
> Se anade para que el cambio archivado sirva de referencia de consulta. En un
> repositorio real no existe.

AQUI ESTA LA AMBIGUEDAD DEL CURSO. Esta es la version resuelta.

## Que mirar en este cambio

- El que tu recibiste tenia los requisitos de capacidad disponible y de corte de la sobreasignacion redactados de forma que admitian dos lecturas, y no lo decia.
- Las dos lecturas producen un sistema que funciona, pasa sus tests y da numeros distintos. Esa es la leccion central de la modalidad: SDD no protege de una especificacion equivocada, la ejecuta mas rapido.
- El apartado de decisiones del diseno lleva las dos alternativas descartadas con su motivo. Es el artefacto que te van a pedir en cliente cuando pregunten por que el numero cambio.

## Los cuatro artefactos

| Fichero | Que es |
|---------|--------|
| `proposal.md` | Por que se hace y que capabilities toca. Es lo que revisa un humano ANTES de aprobar |
| `specs/` | Los requisitos con sus escenarios. Es el contrato, y lo unico que genera codigo |
| `design.md` | Decisiones tecnicas, alternativas descartadas y riesgos |
| `tasks.md` | La lista que ejecuta `/opsx:apply`. Todas marcadas, porque el cambio esta archivado |

## Como se genero

```bash
/opsx:new e5-ocupacion-utilizacion
/opsx:continue          # una vez por artefacto, revisando cada uno
/opsx:apply             # genera el codigo desde tasks.md
/opsx:verify            # comprueba completitud, correccion y coherencia
/opsx:archive           # sincroniza las specs principales y archiva
```
