# E4. Motor de asignacion con restricciones duras

> **Nota didactica del laboratorio.** Este fichero no forma parte de OpenSpec.
> Se anade para que el cambio archivado sirva de referencia de consulta. En un
> repositorio real no existe.

La capability con mas reglas del proyecto.

## Que mirar en este cambio

- Fijate en la diferencia entre un requisito y un deseo. 'El sistema debe evitar la sobreasignacion' es un deseo. Lo que hay aqui son limites concretos con su escenario de frontera.
- Cada requisito tiene al menos un escenario que describe el caso que NO se cumple. Un requisito con solo escenarios felices no protege de nada.
- El requisito de traza con origen existe para que auditar al agente no sea opcional.

## Los cuatro artefactos

| Fichero | Que es |
|---------|--------|
| `proposal.md` | Por que se hace y que capabilities toca. Es lo que revisa un humano ANTES de aprobar |
| `specs/` | Los requisitos con sus escenarios. Es el contrato, y lo unico que genera codigo |
| `design.md` | Decisiones tecnicas, alternativas descartadas y riesgos |
| `tasks.md` | La lista que ejecuta `/opsx:apply`. Todas marcadas, porque el cambio esta archivado |

## Como se genero

```bash
/opsx:new e4-motor-asignacion
/opsx:continue          # una vez por artefacto, revisando cada uno
/opsx:apply             # genera el codigo desde tasks.md
/opsx:verify            # comprueba completitud, correccion y coherencia
/opsx:archive           # sincroniza las specs principales y archiva
```
