# E9. Reversion y observabilidad

> **Nota didactica del laboratorio.** Este fichero no forma parte de OpenSpec.
> Se anade para que el cambio archivado sirva de referencia de consulta. En un
> repositorio real no existe.

Ultimo cambio del curso, y el que se usa en el ejercicio de fallo inducido.

## Que mirar en este cambio

- Cuando algo se rompe en produccion, la correccion tambien pasa por aqui, no por un parche directo. Ese es el ejercicio.
- El requisito de fallar al arranque si la configuracion no resuelve viene de un incidente real de la fase de pruebas: el healthcheck seguia verde y solo fallaba un endpoint.

## Los cuatro artefactos

| Fichero | Que es |
|---------|--------|
| `proposal.md` | Por que se hace y que capabilities toca. Es lo que revisa un humano ANTES de aprobar |
| `specs/` | Los requisitos con sus escenarios. Es el contrato, y lo unico que genera codigo |
| `design.md` | Decisiones tecnicas, alternativas descartadas y riesgos |
| `tasks.md` | La lista que ejecuta `/opsx:apply`. Todas marcadas, porque el cambio esta archivado |

## Como se genero

```bash
/opsx:new e9-reversion-y-observabilidad
/opsx:continue          # una vez por artefacto, revisando cada uno
/opsx:apply             # genera el codigo desde tasks.md
/opsx:verify            # comprueba completitud, correccion y coherencia
/opsx:archive           # sincroniza las specs principales y archiva
```
