# E6. Agente de propuesta de staffing

> **Nota didactica del laboratorio.** Este fichero no forma parte de OpenSpec.
> Se anade para que el cambio archivado sirva de referencia de consulta. En un
> repositorio real no existe.

El agente tambien se especifica y se genera. Ni una linea escrita a mano.

## Que mirar en este cambio

- El techo de autonomia N2 no es una nota en el diseno: es un requisito con dos escenarios, uno de ellos sobre la ausencia de una via de escritura en el codigo. Como escenario, es verificable. Como nota, seria decorativo.
- El requisito de alternativas descartadas es lo que convierte la propuesta en algo contestable por la persona que no fue propuesta.
- La concentracion se mide y se publica, pero no se corrige sola. Meter un criterio de reparto dentro del agente seria devolverle una decision que es del resource manager.

## Los cuatro artefactos

| Fichero | Que es |
|---------|--------|
| `proposal.md` | Por que se hace y que capabilities toca. Es lo que revisa un humano ANTES de aprobar |
| `specs/` | Los requisitos con sus escenarios. Es el contrato, y lo unico que genera codigo |
| `design.md` | Decisiones tecnicas, alternativas descartadas y riesgos |
| `tasks.md` | La lista que ejecuta `/opsx:apply`. Todas marcadas, porque el cambio esta archivado |

## Como se genero

```bash
/opsx:new e6-agente-propuesta-staffing
/opsx:continue          # una vez por artefacto, revisando cada uno
/opsx:apply             # genera el codigo desde tasks.md
/opsx:verify            # comprueba completitud, correccion y coherencia
/opsx:archive           # sincroniza las specs principales y archiva
```
