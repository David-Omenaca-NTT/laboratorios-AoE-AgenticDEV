# E7. Correccion del calculo heredado

> **Nota didactica del laboratorio.** Este fichero no forma parte de OpenSpec.
> Se anade para que el cambio archivado sirva de referencia de consulta. En un
> repositorio real no existe.

El par del anterior. Aqui se MODIFICAN los requisitos que describian el defecto.

## Que mirar en este cambio

- La propuesta declara el impacto aguas abajo, que es la conversacion incomoda: el numero que ve direccion pasa de 113,09% a 56,31%.
- Un indicador por encima del 100% llevaba anos publicandose. No salto porque alimentaba un cuadro de mando que nadie recalculaba.
- Fijate en que la tarea 3 es de comunicacion, no de codigo. Un cambio que mueve un indicador de direccion sin avisar antes es un incidente, no una entrega.

## Los cuatro artefactos

| Fichero | Que es |
|---------|--------|
| `proposal.md` | Por que se hace y que capabilities toca. Es lo que revisa un humano ANTES de aprobar |
| `specs/` | Los requisitos con sus escenarios. Es el contrato, y lo unico que genera codigo |
| `design.md` | Decisiones tecnicas, alternativas descartadas y riesgos |
| `tasks.md` | La lista que ejecuta `/opsx:apply`. Todas marcadas, porque el cambio esta archivado |

## Como se genero

```bash
/opsx:new e7b-correccion-utilizacion-heredada
/opsx:continue          # una vez por artefacto, revisando cada uno
/opsx:apply             # genera el codigo desde tasks.md
/opsx:verify            # comprueba completitud, correccion y coherencia
/opsx:archive           # sincroniza las specs principales y archiva
```
