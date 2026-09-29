# E1. Comprobacion de salud del servicio

> **Nota didactica del laboratorio.** Este fichero no forma parte de OpenSpec.
> Se anade para que el cambio archivado sirva de referencia de consulta. En un
> repositorio real no existe.

El cambio mas pequeno posible, y por eso el primero. Sirve para recorrer el ciclo entero sin que el dominio distraiga.

## Que mirar en este cambio

- Hasta un endpoint trivial tiene tres escenarios, y uno de ellos es negativo.
- La propuesta ya declara el impacto: endpoint publico sin autenticacion. Un cambio sin impacto declarado no se aprueba.

## Los cuatro artefactos

| Fichero | Que es |
|---------|--------|
| `proposal.md` | Por que se hace y que capabilities toca. Es lo que revisa un humano ANTES de aprobar |
| `specs/` | Los requisitos con sus escenarios. Es el contrato, y lo unico que genera codigo |
| `design.md` | Decisiones tecnicas, alternativas descartadas y riesgos |
| `tasks.md` | La lista que ejecuta `/opsx:apply`. Todas marcadas, porque el cambio esta archivado |

## Como se genero

```bash
/opsx:new e1-salud-servicio
/opsx:continue          # una vez por artefacto, revisando cada uno
/opsx:apply             # genera el codigo desde tasks.md
/opsx:verify            # comprueba completitud, correccion y coherencia
/opsx:archive           # sincroniza las specs principales y archiva
```
