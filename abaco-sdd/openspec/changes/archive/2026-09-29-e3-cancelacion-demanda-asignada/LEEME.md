# E3. Cancelacion excepcional de demanda asignada

> **Nota didactica del laboratorio.** Este fichero no forma parte de OpenSpec.
> Se anade para que el cambio archivado sirva de referencia de consulta. En un
> repositorio real no existe.

Primer delta sobre algo que ya existia. No se reescribe la capability: se declara MODIFIED sobre un requisito concreto y se anade otro.

## Que mirar en este cambio

- ESTE CAMBIO CONTIENE UN ERROR REAL QUE LA HERRAMIENTA DETECTO. La primera version del delta reformulaba el requisito y dejaba fuera, sin querer, el escenario 'Cancelacion de demanda ya asignada'. Al archivar, OpenSpec lo rechazo: 'current spec contains scenario(s) not present in the modified block'.
- La leccion: un bloque MODIFIED es el estado COMPLETO nuevo del requisito, no un parche. Todo escenario que no aparezca se elimina. La herramienta lo detecta, pero solo al archivar, no al validar.
- Compara este delta con la spec principal despues de sincronizar y veras que se fusiono y que se conservo.

## Los cuatro artefactos

| Fichero | Que es |
|---------|--------|
| `proposal.md` | Por que se hace y que capabilities toca. Es lo que revisa un humano ANTES de aprobar |
| `specs/` | Los requisitos con sus escenarios. Es el contrato, y lo unico que genera codigo |
| `design.md` | Decisiones tecnicas, alternativas descartadas y riesgos |
| `tasks.md` | La lista que ejecuta `/opsx:apply`. Todas marcadas, porque el cambio esta archivado |

## Como se genero

```bash
/opsx:new e3-cancelacion-demanda-asignada
/opsx:continue          # una vez por artefacto, revisando cada uno
/opsx:apply             # genera el codigo desde tasks.md
/opsx:verify            # comprueba completitud, correccion y coherencia
/opsx:archive           # sincroniza las specs principales y archiva
```
