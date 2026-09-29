"""Genera las carpetas de laboratorio de Abaco: GUIA, CRITERIOS, pistas, referencia."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

E = [
    dict(id="S0", carpeta="S0-bootstrap", nombre="Bootstrap y disciplina de repositorio",
         horas=8, semana="1", modulos="1",
         objetivo="Dejar el repositorio de aprendizaje en condiciones de recibir trabajo de agentes, y entender por que el repositorio de producto es otro.",
         porque=("Aqui hay dos repositorios y la diferencia importa. En el de aprendizaje "
                 "rompes lo que quieras con datos sinteticos. En el de producto hay datos "
                 "reales de tus companeros y se entra por estacion sellada. El limite de "
                 "400 lineas de diff por PR te parecera arbitrario esta semana y lo "
                 "entenderas en la semana 8."),
         tareas=[
             "Crea tu repositorio de aprendizaje a partir de la plantilla y clona en local.",
             "Protege la rama principal: revision obligatoria y pipeline en verde para mergear.",
             "Anade CODEOWNERS marcando labs/, manifiestos/ y .github/ como protegidas.",
             "Anade la plantilla de PR con la checklist de diez puntos.",
             "Configura conventional commits y el gate de tamano de PR.",
             "Lee la seccion de datos personales del contrato de contexto y firma el compromiso de no copiar datos reales al repositorio de aprendizaje.",
             "Abre un PR propio y revisa el de otro miembro de tu escuadra.",
         ],
         entregable="Dos PRs mergeados, uno propio y uno revisado, ambos con la checklist rellena, y el compromiso de datos firmado.",
         aviso=("Ni un solo dato personal real entra en este repositorio. Ni en un test, "
                "ni en un issue, ni en un mensaje de commit, ni en un prompt. Hay un "
                "verificador que lo comprueba y salta en el pipeline."),
         pistas=[
             "Settings, Branches, Add branch protection rule. Busca 'Require a pull request before merging' y 'Require status checks to pass'.",
             "El gate de tamano de PR es un job mas: calcula el diff con `git diff --numstat origin/main...HEAD` y falla si supera el umbral. No hace falta ninguna accion de terceros.",
             "El verificador de datos personales busca patrones de nombre, correo y DNI en el diff. Miralo en labs/S0-bootstrap/verificar.py: saber como se te mide es parte del ejercicio.",
         ]),
    dict(id="S1", carpeta="S1-rebanada-vertical", nombre="Rebanada vertical a mano",
         horas=24, semana="2 a 4", modulos="2, 3, 4",
         objetivo="Construir el alta de demanda y su maquina de estados completa, sin ningun agente.",
         porque=("No se puede revisar lo que no se sabe escribir. Si llegas al modulo 5 sin "
                 "haber escrito un test a mano, aceptaras lo que te proponga el agente "
                 "porque no tendras criterio con el que discrepar. Ademas, el tiempo que "
                 "registres aqui es tu linea base para medir tu propio salto en S2 y S3."),
         tareas=[
             "Implementa la maquina de estados de la demanda con sus ocho estados y las transiciones validas.",
             "Implementa el alta de demanda: endpoint, validacion, persistencia en memoria y tests.",
             "Escribe los tests a mano, incluidos los casos limite de transicion invalida.",
             "Contenedoriza el servicio con una imagen OCI multi-stage.",
             "Monta el pipeline: build, test, cobertura y publicacion de imagen.",
             "Registra el tiempo por tarea en bitacora.md.",
         ],
         entregable="Pipeline verde de extremo a extremo, imagen publicada, maquina de estados completa con tests.",
         pistas=[
             "Empieza por la tabla de transiciones. Si no sabes desde que estado se puede cancelar una demanda, todavia no sabes que estas construyendo.",
             "Los estados terminales son los que mas fallos dan: comprueba explicitamente que cerrada y cancelada no tienen salida.",
             "Para la imagen: etapa de build con dependencias y etapa final solo con runtime y codigo. Si pasa de 200 MB, algo se cuela de la primera etapa.",
         ]),
    dict(id="S2", carpeta="S2-sdd", nombre="Spec-Driven Development",
         horas=26, semana="5 a 6", modulos="6",
         objetivo="Escribir SPEC-002 antes del codigo y derivar de ella la implementacion, con trazabilidad mecanica.",
         porque=("Es el posicionamiento de mercado del AoE. Escribir codigo con un agente lo "
                 "hace cualquiera. Derivar codigo verificable de una especificacion trazable "
                 "es lo que los clientes empiezan a pedir y casi nadie sabe hacer."),
         tareas=[
             "Escribe SPEC-002 completa siguiendo la plantilla, antes de tocar codigo.",
             "Numera los criterios y traducelos a test uno a uno, con la etiqueta `cubre:` en el docstring.",
             "Dirige al agente para que derive la implementacion de la spec, criterio a criterio.",
             "Detecta y resuelve las ambiguedades de la spec de partida ANTES de implementar.",
             "Registra en el apartado de ambiguedades que estaba mal definido y como lo cerraste.",
         ],
         entregable="Spec versionada, implementacion completa, trazabilidad al 100% verificada por el pipeline y registro de ambiguedades.",
         aviso=("La spec de partida contiene dos ambiguedades reales y deliberadas sobre "
                "el calculo de utilizacion. Si no las detectas, el agente producira una "
                "implementacion plausible y equivocada, y tu la aprobaras porque los tests "
                "que escribiste sobre tu suposicion pasaran. Detectarlas es criterio de "
                "evaluacion explicito."),
         pistas=[
             "Lee la spec como si tuvieras que implementarla sin poder preguntar a nadie. Cada vez que tengas que suponer algo, has encontrado una ambiguedad.",
             "Dos preguntas concretas que te van a desbloquear: cuando alguien esta en formacion o en banquillo, esos dias cuentan como capacidad disponible o no. Y cuando alguien esta al 120%, aporta 120 o aporta 100.",
             "Resolucion de la referencia: formacion y banquillo SI cuentan como capacidad, solo se excluyen vacaciones, festivos y bajas. Y la sobreasignacion se corta en 100, reportandose aparte. Lo importante no es coincidir, es haber visto que habia que decidirlo.",
         ]),
    dict(id="S3", carpeta="S3-contexto", nombre="Ingenieria de contexto y operacion de agentes",
         horas=24, semana="6 a 7", modulos="5",
         objetivo="Convertir el repositorio en un entorno donde el agente trabaja bien por diseno, no por suerte en el prompt.",
         porque=("Lo innegociable no se pide en lenguaje natural, se hace determinista. En "
                 "este proyecto ademas hay una linea que ningun agente puede cruzar: los "
                 "datos personales. Eso no se confia a una instruccion."),
         tareas=[
             "Escribe CLAUDE.md con las seis secciones obligatorias.",
             "Declara en la seccion de limites los campos de perfil que ningun agente puede leer.",
             "Configura allowlist y hooks: formato, bloqueo de rutas prohibidas, tests antes de commit.",
             "Define dos subagentes acotados: uno implementa, otro revisa solo el diff.",
             "Resuelve el mismo encargo con Claude Code y con OpenCode y entrega la comparativa razonada.",
             "Ejecuta un ciclo en worktrees paralelos con Orca, patron escritor y revisor.",
         ],
         entregable="Configuracion versionada, cuatro PRs generados con agente y revisados con evidencia, tabla comparativa entregada.",
         aviso=("Se mide tu ratio de diff aceptado sin comentario. Un ratio alto no es "
                "productividad, es aceptacion ciega. Un ratio de cero tampoco es bueno."),
         pistas=[
             "El apartado de invariantes es el que mas rendimiento da. Escribe ahi lo que nunca puede romperse aunque el agente crea que mejora el codigo.",
             "Un hook que bloquea escritura recibe la ruta y devuelve codigo distinto de cero. Pruebalo intentando escribir a proposito en manifiestos/: si no te bloquea, no esta puesto.",
             "Para la comparativa, define tus criterios antes de ejecutar. Si ejecutas primero, escribiras los criterios para justificar la herramienta que ya te gustaba.",
         ]),
    dict(id="S4a", carpeta="S4a-agente-propio", nombre="Servidor MCP y agente de staffing",
         horas=28, semana="8 a 10", modulos="6",
         objetivo="Construir un agente que propone personas para una demanda, y medirlo con metricas separadas de seguridad y utilidad.",
         porque=("Es el corazon del laboratorio y la diferencia con Aula. Alli el agente "
                 "revisaba codigo. Aqui propone personas, y una propuesta equivocada no "
                 "es un bug: es la carrera de alguien."),
         tareas=[
             "Construye el servidor MCP con las seis herramientas del proyecto.",
             "Construye el agente de staffing: recibe una demanda y propone candidatos ordenados con su evidencia.",
             "Incluye siempre las alternativas descartadas y su motivo. Un agente que calla a quien descarto no es explicable.",
             "Mide el agente v0 que trae el repo contra el conjunto de evaluacion y guarda el informe.",
             "Itera hasta cero violaciones de restriccion dura y utilidad por encima de 0,70, y guarda el segundo informe.",
             "Mide la concentracion: cuantas personas distintas propone tu agente sobre el pool.",
             "Explica por escrito que cambiaste entre las dos versiones y por que mejoro.",
         ],
         entregable="Servidor MCP funcionando, agente con propuesta explicable, informe con las dos iteraciones y las tres metricas.",
         aviso=("SEGURIDAD ES TOLERANCIA CERO. Proponer a alguien no disponible, por debajo "
                "de la categoria pedida o sin el nivel de skill exigido es una violacion, y "
                "una sola violacion en la entrega final suspende la dimension completa "
                "aunque tu utilidad sea perfecta. La seguridad no se promedia con nada."),
         pistas=[
             "El nucleo del agente debe ser determinista: filtros, disponibilidad, categoria y aritmetica de ocupacion sin modelo. Si el veredicto cambia entre ejecuciones no lo puedes defender ante la persona que no fue propuesta.",
             "Empieza por las restricciones duras y devuelve TODOS los motivos de descarte, no solo el primero. Con un unico motivo tus explicaciones son pobres y tu metrica de utilidad no mejora.",
             "La categoria que cuenta es la vigente en la fecha de INICIO de la asignacion, no la de hoy. Y la verificacion independiente tiene que usar exactamente la misma dedicacion que la demanda pedia, o produce falsos positivos de sobreasignacion.",
         ]),
    dict(id="S4b", carpeta="S4b-flotilla", nombre="Flotilla multiagente",
         horas=12, semana="10", modulos="6",
         objetivo="Componer tres agentes sobre el mismo contexto y hacer explicito el contrato entre ellos.",
         porque="Es la conversacion que se tiene en cliente cuando se pasa de un piloto a una flota.",
         tareas=[
             "Trabajo de escuadra: componed staffing, deteccion de conflictos de asignacion y alerta de banquillo sobre el mismo servidor MCP.",
             "Ejecutadlos en worktrees aislados y en paralelo.",
             "Documentad el contrato: entradas, salidas, handoff y resolucion de conflicto.",
             "Declarad el nivel de autonomia de cada uno y por que difieren.",
         ],
         entregable="Diagrama de flotilla, contrato validable contra esquema y grabacion de un ciclo completo.",
         aviso=("Los tres agentes no tienen el mismo techo. El de staffing propone personas "
                "y se queda en N2. El de conflictos no propone a nadie y puede llegar a N3. "
                "Justificar esa diferencia es el entregable intelectual de la estacion."),
         pistas=[
             "Un worktree por agente: `git worktree add ../abaco-conflictos rama-conflictos`.",
             "El contrato es un fichero, no una conversacion. Si no se valida contra un esquema, no es un contrato.",
             "Regla de conflicto mas simple que funciona: cada ruta tiene un unico agente con permiso de escritura y los demas proponen.",
         ]),
    dict(id="S5", carpeta="S5-legado", nombre="Modernizacion del legado con agentes",
         horas=22, semana="10 a 11", modulos="5, 6",
         objetivo="Caracterizar, refactorizar y demostrar equivalencia sobre la calculadora de utilizacion heredada.",
         porque=("Es el escenario mas frecuente en cliente real. Y aqui el numero heredado "
                 "alimenta el cuadro de mando que ve direccion, asi que corregirlo tiene "
                 "consecuencias que hay que anunciar antes, no despues."),
         tareas=[
             "Escribe la bateria de caracterizacion que captura el comportamiento actual, incluidos los comportamientos no documentados.",
             "Commitea la caracterizacion ANTES de tocar una linea del legado.",
             "Refactoriza con la red puesta, con la bateria en verde en cada paso.",
             "Ejecuta la equivalencia sobre el corpus completo.",
             "Declara cada desviacion en DESVIACIONES.md con categoria, causa y efecto aguas abajo.",
         ],
         entregable="Caracterizacion completa, refactor entregado, informe de equivalencia sin desviaciones sin justificar.",
         aviso=("REGLA DURA: esta prohibido pedir al agente que refactorice antes de que "
                "exista la caracterizacion. El verificador comprueba el orden en el "
                "historial de git. Suspende la estacion. Es tambien la falta que veras "
                "cometer en cliente."),
         pistas=[
             "Caracterizar no es testear que el codigo sea correcto, es fijar lo que hace hoy, incluso lo que hace mal. Aqui el agente es un acelerador legitimo.",
             "Hay comportamientos que no estan escritos en ninguna parte. Uno tiene que ver con la gente en banquillo, otro con donde se aplica el redondeo y otro con las vacaciones. Ninguno se descubre leyendo el codigo con calma.",
             "El global heredado da 113% de utilizacion. Un numero por encima del 100% deberia haber saltado a la vista de cualquiera, y no salto porque alimentaba un cuadro de mando que nadie recalculaba. Ese es el hallazgo que tienes que reproducir.",
         ]),
    dict(id="S6", carpeta="S6-gobierno", nombre="Gobierno de un agente que decide sobre personas",
         horas=18, semana="11", modulos="7",
         objetivo="Dejar el agente en condiciones de operar sobre datos reales de personas en una organizacion sujeta a normativa.",
         porque=("Es la estacion mas rica de los dos laboratorios. Un agente que propone "
                 "quien trabaja en que afecta a carreras. La conversacion no es con un CTO: "
                 "es con seguridad, con legal y con recursos humanos."),
         tareas=[
             "Escribe el Agent Release Manifest con los seis apartados adicionales: personas afectadas, explicabilidad, via de contestacion, veto humano, vigilancia de concentracion y datos excluidos.",
             "Haz que el pipeline bloquee el merge si falta el manifiesto, si el hash no coincide, si la evaluacion caduco o si el nivel declarado supera N2.",
             "Implementa el control que impide al agente leer los campos excluidos, y pruebalo intentando leerlos.",
             "Mide la concentracion de tus propuestas y comenta el resultado.",
             "Argumenta por escrito por que este agente NO debe llegar a N4, y que control haria falta para que otro agente si pudiera.",
             "Calcula el coste en tokens por propuesta verificada.",
         ],
         entregable="Manifiestos validados por el pipeline, control de campos excluidos probado, informe de concentracion y argumentacion sobre N4.",
         aviso=("El techo de autonomia no lo fija la precision del modelo, lo fija la "
                "reversibilidad del dano. Si llegas al panel defendiendo que tu agente "
                "podria ir en autonomo porque tiene buenas metricas, no has entendido la "
                "estacion, por muy buenas que sean tus metricas."),
         pistas=[
             "Declarar el nivel no basta. Si dices N2 tienes que ensenar que el agente no tiene ninguna ruta de codigo que cree una asignacion. Si la tiene, tu nivel real es otro.",
             "El gate se prueba rompiendolo: abre a proposito un PR con un manifiesto que declare N4 y comprueba que el pipeline lo rechaza.",
             "Para la concentracion: cuenta personas distintas propuestas sobre el pool y la cuota de las cinco mas propuestas. Si tu agente mejora en utilidad y empeora en concentracion, eso no es un fallo tuyo: es el hallazgo de la estacion y hay que contarlo.",
         ]),
    dict(id="S7", carpeta="S7-despliegue", nombre="Despliegue, fallo inducido y MTTR",
         horas=24, semana="12", modulos="3, 4, 7",
         objetivo="Desplegar, romper y medir cuanto se tarda en volver a verde con y sin agente.",
         porque="La comparacion de MTTR es un dato tuyo, no un benchmark de un informe.",
         tareas=[
             "Despliega el servicio con pipeline completo y estrategia de reversion.",
             "Instrumenta observabilidad basica.",
             "Introduce un fallo del catalogo en el entorno de otro miembro de tu escuadra.",
             "Resuelve el que te introduzcan: ronda 1 sin agente, ronda 2 con el agente de triaje.",
             "Registra el MTTR de las dos rondas y escribe la retrospectiva.",
         ],
         entregable="Servicio desplegado, dos rondas resueltas con MTTR registrado y retrospectiva escrita.",
         pistas=[
             "Mide el MTTR desde que el pipeline se pone rojo hasta que vuelve a verde, no desde que te enteras.",
             "Antes de arreglar nada, escribe tu hipotesis. Comparar hipotesis inicial con causa real es lo que ensena a diagnosticar.",
             "En la ronda 2 no le pidas al agente que arregle: pidele que reduzca el espacio de busqueda.",
         ]),
    dict(id="S8", carpeta="S8-defensa", nombre="Defensa ante panel",
         horas=10, semana="12", modulos="8",
         objetivo="Defender lo construido ante Head of AoE, SMEs y el dueno funcional de la herramienta.",
         porque=("Aqui el panel incluye a alguien que va a usar la herramienta de verdad. "
                 "No es una simulacion: es aceptacion."),
         tareas=[
             "Prepara 20 minutos con la estructura fija de la cohorte.",
             "Incluye la defensa del recorte de alcance: por que este subconjunto del PRD y no otro, y por que un monolito modular y no microservicios.",
             "Prepara la seccion de metricas: seguridad, utilidad, concentracion, MTTR y deteccion adversarial.",
             "Prepara la decision de gobierno: por que tu agente se queda en N2.",
             "Prepara una decision tecnica que tomaste y hoy tomarias distinta.",
         ],
         entregable="Demo, cuaderno de decisiones, metricas y defensa oral ante el dueno funcional.",
         aviso=("La defensa del recorte es obligatoria. El PRD pedia 18 modulos, "
                "microservicios y Kafka. Tu has entregado 10 modulos parciales y un "
                "monolito modular. Si no sabes explicar por que eso es lo correcto, has "
                "construido algo que no sabes justificar."),
         pistas=[
             "Estructura: problema, recorte y su justificacion, spec, arquitectura, agente y metricas, gobierno, concentracion, decision que cambiarias.",
             "La defensa del recorte se sostiene en una frase: un junior que monta siete microservicios para un dominio que cabe en un monolito ha aprendido sobreingeniera, que es el fallo mas caro del perfil.",
             "Ensaya con alguien que no haya visto tu proyecto. Si tiene que preguntarte que hace el sistema, tu primer minuto esta mal construido.",
         ]),
]


def escribir(destino, contenido):
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(contenido, encoding="utf-8")


def guia(e):
    p = ["# %s. %s" % (e["id"], e["nombre"]), "", "| | |", "|---|---|",
         "| Semana | %s |" % e["semana"], "| Horas estimadas | %d |" % e["horas"],
         "| Modulos del itinerario | %s |" % e["modulos"], "",
         "## Objetivo", "", e["objetivo"], "",
         "## Por que esta estacion existe", "", e["porque"], ""]
    if e.get("aviso"):
        p += ["## Aviso", "", "> " + e["aviso"], ""]
    p += ["## Que tienes que conseguir", ""]
    p += ["%d. %s" % (i + 1, t) for i, t in enumerate(e["tareas"])]
    p += ["", "Esta guia dice que conseguir, no como. Si pudieras seguirla sin pensar, no",
          "aprenderias nada que sirva cuando cambie el contexto, que es lo que pasa en",
          "cliente el primer dia.", "",
          "## Entregable", "", e["entregable"], "",
          "## Como se cierra", "", "```bash",
          "abaco check %s --prediccion pasa   # declara antes si crees que vas a pasar" % e["id"],
          "abaco cerrar %s                    # sella la estacion y libera la referencia" % e["id"],
          "```", "",
          "Si te atascas: `abaco pista %s`. Si se agota la ventana," % e["id"],
          "`abaco desbloquear %s --motivo \"...\"` te da la referencia como linea base y" % e["id"],
          "te deja continuar. No penaliza las estaciones siguientes.", "",
          "Criterios de superacion en CRITERIOS.md.", ""]
    return "\n".join(p)


def criterios(e):
    return "\n".join([
        "# Criterios de superacion de %s" % e["id"], "",
        "Lo que comprueba `abaco check %s`. Cada criterio es verdadero o falso: si" % e["id"],
        "alguno queda en rojo, la estacion no se sella.", "",
        "El detalle mecanico esta en verificar.py y puedes leerlo. No es un examen",
        "secreto: saber como se te mide es parte de aprender a medir. Lo que no puedes",
        "es modificarlo, porque la ejecucion que sella es la del pipeline y toma el",
        "verificador de la plantilla, no tu copia.", "",
        "## Entregable de la estacion", "", e["entregable"], "",
        "## Pistas disponibles", "",
        "%d escalones: empujon, direccion y fragmento de solucion." % len(e["pistas"]),
        "Cada apertura queda registrada. No penaliza la nota, informa al mentor.", ""])


def main():
    for e in E:
        base = RAIZ / "labs" / e["carpeta"]
        escribir(base / "GUIA.md", guia(e))
        escribir(base / "CRITERIOS.md", criterios(e))
        for nombre, texto in zip(["1-empujon.md", "2-direccion.md", "3-fragmento.md"],
                                 e["pistas"]):
            escribir(base / "pistas" / nombre,
                     "# Pista %s de %s\n\n%s\n" % (nombre[0], e["id"], texto))
        escribir(base / "bitacora.md",
                 "# Bitacora de %s\n\nAnota con `abaco bitacora \"texto\"`.\n"
                 "Que intentaste, que fallo, que harias distinto. Se evalua.\n\n" % e["id"])
        escribir(base / "referencia" / "NOTAS.md",
                 "# Solucion de referencia de %s\n\n"
                 "Se libera al sellar la estacion o al desbloquearla.\n\n"
                 "Comparala con la tuya: donde difieran y por que es la conversacion de la\n"
                 "daily siguiente.\n" % e["id"])
    print("generadas %d estaciones en labs/" % len(E))


if __name__ == "__main__":
    main()
