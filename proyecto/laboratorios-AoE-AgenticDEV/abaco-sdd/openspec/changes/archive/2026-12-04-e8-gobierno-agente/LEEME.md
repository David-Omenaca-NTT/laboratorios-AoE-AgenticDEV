# E8. Gobierno del agente y trazabilidad

> **Nota didactica del laboratorio.** Este fichero no forma parte de OpenSpec.
> Se anade para que el cambio archivado sirva de referencia de consulta. En un
> repositorio real no existe.

Gobierno expresado como requisitos verificables en lugar de como politica escrita.

## Que mirar en este cambio

- Si la exigencia de auditar al agente igual que a una persona no es un escenario, no se cumple sola.
- El requisito de integridad de la bateria de aceptacion es el que sostiene toda la modalidad: si el generador puede modificar el examen que lo evalua, no hay evaluacion.
- El techo de autonomia se deduce de si el manifiesto declara personas afectadas, no de una lista mantenida a mano que se desactualiza en silencio.

## Los cuatro artefactos

| Fichero | Que es |
|---------|--------|
| `proposal.md` | Por que se hace y que capabilities toca. Es lo que revisa un humano ANTES de aprobar |
| `specs/` | Los requisitos con sus escenarios. Es el contrato, y lo unico que genera codigo |
| `design.md` | Decisiones tecnicas, alternativas descartadas y riesgos |
| `tasks.md` | La lista que ejecuta `/opsx:apply`. Todas marcadas, porque el cambio esta archivado |

## Como se genero

```bash
/opsx:new e8-gobierno-agente
/opsx:continue          # una vez por artefacto, revisando cada uno
/opsx:apply             # genera el codigo desde tasks.md
/opsx:verify            # comprueba completitud, correccion y coherencia
/opsx:archive           # sincroniza las specs principales y archiva
```
