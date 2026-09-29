"""Construye el archivo de cambios de referencia, uno por etapa del curso.

Es el corazon de este repositorio: un student atascado en E5 abre el cambio
archivado de E5 y ve exactamente que aspecto tiene una propuesta, una spec
delta, un diseno y una lista de tareas bien hechos en ese punto del curso.

Formato verificado contra las plantillas del esquema spec-driven de OpenSpec
1.8.0 y validado con `openspec validate`.
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
ARCHIVO = RAIZ / "openspec" / "changes" / "archive"

CAMBIOS = [
    dict(
        id="e1-salud-servicio", fecha="2026-09-08", etapa="E1",
        titulo="Comprobacion de salud del servicio",
        nota_didactica=(
            "El cambio mas pequeno posible, y por eso el primero. Sirve para "
            "recorrer el ciclo entero sin que el dominio distraiga. Fijate en "
            "que hasta un endpoint trivial tiene tres escenarios, y en que uno "
            "de ellos es negativo."),
    ),
    dict(
        id="e2-ciclo-vida-demanda", fecha="2026-09-18", etapa="E2",
        titulo="Ciclo de vida de la demanda",
        nota_didactica=(
            "Primera capability de dominio. Ocho estados que se expresan como "
            "escenarios casi sin traducir. Fijate en que los escenarios "
            "negativos (una transicion que NO se permite) son mas numerosos "
            "que los positivos: ahi esta la mayor parte del valor."),
    ),
    dict(
        id="e3-cancelacion-demanda-asignada", fecha="2026-09-29", etapa="E3",
        titulo="Cancelacion excepcional de demanda asignada",
        nota_didactica=(
            "Primer delta sobre algo que ya existia. No se reescribe la "
            "capability: se declara MODIFIED sobre un requisito concreto y se "
            "anade uno nuevo. Compara el fichero delta con la spec principal "
            "despues de sincronizar y veras que se fusiono y que se conservo."),
    ),
    dict(
        id="e4-motor-asignacion", fecha="2026-10-13", etapa="E4",
        titulo="Motor de asignacion con restricciones duras",
        nota_didactica=(
            "La capability con mas reglas del proyecto. Fijate en la diferencia "
            "entre un requisito y una regla: 'el sistema debe evitar la "
            "sobreasignacion' no es un requisito, es un deseo. Lo que hay aqui "
            "son limites concretos con su escenario de frontera."),
    ),
    dict(
        id="e5-ocupacion-utilizacion", fecha="2026-10-27", etapa="E5",
        titulo="Calculo de utilizacion y ocupacion",
        nota_didactica=(
            "AQUI ESTA LA AMBIGUEDAD DEL CURSO. Este cambio es la version "
            "resuelta. El que tu recibiste tenia los requisitos de denominador "
            "y de corte al 100% redactados de forma que admitian dos lecturas. "
            "Compara los dos y mira cuanto cambia el resultado."),
    ),
    dict(
        id="e6-agente-propuesta-staffing", fecha="2026-11-13", etapa="E6",
        titulo="Agente de propuesta de staffing",
        nota_didactica=(
            "El agente tambien se especifica y se genera. Fijate en que el "
            "techo de autonomia N2 no es una nota en el diseno: es un requisito "
            "con su escenario, verificable, y por tanto algo que el generador "
            "tiene que respetar."),
    ),
    dict(
        id="e7-caracterizacion-legado", fecha="2026-11-24", etapa="E7",
        titulo="Caracterizacion del calculo heredado",
        nota_didactica=(
            "El unico cambio del curso cuyos requisitos describen un defecto "
            "como si fuera correcto. Es deliberado: primero se especifica lo "
            "que el sistema HACE, sin juzgarlo. La correccion viene en el "
            "cambio siguiente y asi queda por escrito que se cambio y por que."),
    ),
    dict(
        id="e7b-correccion-utilizacion-heredada", fecha="2026-11-27", etapa="E7",
        titulo="Correccion del calculo heredado de utilizacion",
        nota_didactica=(
            "El par del anterior. Aqui se MODIFICAN los requisitos que "
            "describian el defecto. La propuesta declara el impacto aguas "
            "abajo, que es la conversacion incomoda: el numero que ve direccion "
            "se mueve 57 puntos."),
    ),
    dict(
        id="e8-gobierno-agente", fecha="2026-12-04", etapa="E8",
        titulo="Gobierno del agente y trazabilidad de decisiones",
        nota_didactica=(
            "Gobierno expresado como requisitos verificables en lugar de como "
            "politica escrita. Si la exigencia de auditar al agente igual que a "
            "una persona no es un escenario, no se cumple sola."),
    ),
    dict(
        id="e9-reversion-y-observabilidad", fecha="2026-12-11", etapa="E9",
        titulo="Reversion y observabilidad del despliegue",
        nota_didactica=(
            "Ultimo cambio del curso. Es tambien el que se usa en el ejercicio "
            "de fallo inducido: cuando algo se rompe en produccion, la "
            "correccion tambien pasa por aqui, no por un parche."),
    ),
]


def escribir(ruta: Path, contenido: str):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(contenido.lstrip("\n"), encoding="utf-8")


def carpeta(c) -> Path:
    return ARCHIVO / ("%s-%s" % (c["fecha"], c["id"]))


def escribir_lectura(c):
    escribir(carpeta(c) / "LEEME.md", """
# %s. %s

> **Nota didactica, no forma parte de OpenSpec.** Este fichero lo anade el
> laboratorio para que este cambio archivado sirva de referencia. En un
> repositorio real no existe.

%s

## Que mirar en este cambio

| Fichero | Para que sirve |
|---------|----------------|
| `proposal.md` | Por que se hace y que capabilities toca. Es lo que revisa un humano antes de aprobar |
| `specs/` | Los requisitos con sus escenarios. Es el contrato |
| `design.md` | Decisiones tecnicas y alternativas descartadas |
| `tasks.md` | La lista que ejecuta `/opsx:apply`. Todas marcadas, porque el cambio esta archivado |

## Como se genero

```bash
/opsx:new %s
/opsx:continue          # una vez por artefacto, revisando cada uno
/opsx:apply
/opsx:verify
/opsx:archive
```
""" % (c["etapa"], c["titulo"], c["nota_didactica"], c["id"]))


def main():
    for c in CAMBIOS:
        escribir_lectura(c)
    print("LEEME generado para %d cambios" % len(CAMBIOS))


if __name__ == "__main__":
    main()
