# E2. Ciclo de vida de la demanda

> **Nota didactica del laboratorio.** Este fichero no forma parte de OpenSpec.
> Se anade para que el cambio archivado sirva de referencia de consulta. En un
> repositorio real no existe.

Primera capability de dominio. Ocho estados que se expresan como escenarios casi sin traducir.

## Que mirar en este cambio

- Los escenarios negativos, los que declaran lo que NO se permite, son mas numerosos que los positivos. Ahi esta la mayor parte del valor.
- El apartado de decisiones del diseno registra una alternativa descartada y por que. Dentro de un ano eso es lo unico que evitara volver a discutirlo.

## Los cuatro artefactos

| Fichero | Que es |
|---------|--------|
| `proposal.md` | Por que se hace y que capabilities toca. Es lo que revisa un humano ANTES de aprobar |
| `specs/` | Los requisitos con sus escenarios. Es el contrato, y lo unico que genera codigo |
| `design.md` | Decisiones tecnicas, alternativas descartadas y riesgos |
| `tasks.md` | La lista que ejecuta `/opsx:apply`. Todas marcadas, porque el cambio esta archivado |

## Como se genero

```bash
/opsx:new e2-ciclo-vida-demanda
/opsx:continue          # una vez por artefacto, revisando cada uno
/opsx:apply             # genera el codigo desde tasks.md
/opsx:verify            # comprueba completitud, correccion y coherencia
/opsx:archive           # sincroniza las specs principales y archiva
```
