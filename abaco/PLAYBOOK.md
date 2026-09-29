<!-- version: v1.0 | estado: para entregar | audiencia: students de la cohorte | fuente: diseño del laboratorio Ábaco v0.2 -->

# Playbook del laboratorio

**Proyecto Ábaco | AI Engineering Talent Factory | AoE Agentic DevOps**
196 horas | 10 estaciones | 12 semanas

---

## Lo primero, y va en serio

No vas a construir un ejercicio. Vas a construir **una herramienta interna que el
área va a usar, con datos reales de tus compañeros**.

Eso cambia dos cosas respecto de cualquier práctica que hayas hecho antes.

La primera: lo que entregues lo va a usar alguien con nombre y apellidos, que se
va a enfadar si no funciona y te lo va a decir. No hay nota de consolación.

La segunda, y más importante: **vas a construir un agente que propone quién
trabaja en qué proyecto**. Si se equivoca, no es un bug. Es que a una persona no
la propusieron para un proyecto que le habría venido bien, y no se entera nunca.

Todo el laboratorio está diseñado alrededor de esa diferencia.

---

## 1. Los dos repositorios

Esto es lo primero que hay que entender y lo que más gente confunde.

| | Repositorio de aprendizaje | Repositorio de producto |
|---|---|---|
| Cuántos | **Uno tuyo** | **Uno para toda la cohorte** |
| Datos | Sintéticos, generados | **Reales, de tus compañeros** |
| Para qué | Estaciones, verificadores, pistas, desbloqueo, tu evaluación | La herramienta que se va a usar |
| Puedes romperlo | Sí, todo lo que quieras | No |
| Desbloqueo | Disponible siempre | No existe |
| Rondas adversariales | Aquí | Nunca |

**El acceso al repositorio de producto se gana.** Entras a tocar el producto
cuando has sellado la estación equivalente en tu repositorio de aprendizaje. No
es una metáfora ni una norma escrita: es un gate técnico.

No es burocracia. Nadie toca producción el primer día en ningún cliente, y la
razón por la que no se toca es exactamente esta: hasta que no has demostrado en
un entorno seguro que sabes lo que haces, el riesgo de que rompas algo es mayor
que el valor que aportas.

### La regla que no se negocia

**Ningún dato personal real entra en el repositorio de aprendizaje.** Ni en un
test, ni en un fichero de datos, ni en un issue, ni en un mensaje de commit, ni
en un prompt que le pases a un agente.

Hay un verificador que escanea el repositorio buscando correos, DNIs y teléfonos,
y salta en el pipeline. Si salta, el PR no entra.

No es desconfianza. Es que el error se comete sin querer, copiando un caso real
para depurar algo, y una vez está en el historial de git ya no se quita.

---

## 2. Qué vas a construir

**Proyecto Ábaco**: el núcleo de capacidad, demanda y asignación de personas a
proyectos.

Viene de un PRD de 18 módulos que pedía microservicios, Kafka, apps nativas y un
gestor de recursos autónomo. **Hemos recortado a diez módulos parciales y un
monolito modular**, y una de tus obligaciones en la defensa final es saber
explicar por qué ese recorte es lo correcto.

Adelanto el argumento porque te va a servir en cliente: un junior que monta siete
microservicios para un dominio que cabe en un monolito ha aprendido
sobreingeniería, que es el fallo más caro y más frecuente del perfil junior. La
arquitectura se justifica por la restricción real, no por lo que pone en el
documento.

### El dominio en una tabla

| Pieza | Qué hace |
|-------|----------|
| Motor de asignación | Decide si alguien puede entrar en una posición: capacidad, categoría, skill, disponibilidad |
| Cálculo de ocupación | Utilización real frente al objetivo de cada categoría, sobreasignación, banquillo |
| Ciclo de vida de la demanda | Ocho estados, del PRD tal cual |
| Categorías profesionales | Configurables y versionadas por vigencia |
| Módulo heredado | Una calculadora de utilización antigua que vas a caracterizar y modernizar |
| Servidor MCP | El contexto del proyecto expuesto como herramientas para agentes |
| Agente de staffing | El que propone personas. Tu entregable central |

### La categoría profesional, que es el pivote

No hay coste de personal, ni tarifas, ni márgenes en este sistema. Se quitaron a
propósito: la retribución es el dato más sensible del expediente de alguien, y
sacarlo elimina la mayor parte del riesgo.

Su lugar lo ocupa la **categoría profesional**, y atraviesa el dominio entero:

- La **demanda** pide categoría más skill: "dos Java senior" es categoría Senior
  y skill Java nivel 4 o más.
- La **asignación** registra la categoría vigente **en su fecha de inicio**.
- La **utilización** se compara contra el objetivo de cada categoría, no contra
  un número único de compañía.

Esa segunda es la que más gente falla. Una persona asciende, y **todas sus
asignaciones pasadas tienen que seguir diciendo la categoría que tenía
entonces**. Si tu código coge la categoría de hoy, has reescrito el histórico.

---

## 3. Cómo funciona el laboratorio

### Tú puedes saber si has terminado bien

Cada estación tiene un verificador que ejecutas cuando quieras y que te dice,
criterio a criterio, qué está en verde y qué no, y por qué.

El mentor no está para decirte "está bien". Está para preguntarte "por qué lo has
hecho así", que es una conversación mucho más útil y para la que hay tiempo
precisamente porque la primera no hace falta.

### Nunca te quedas bloqueado

Tres escalones de pista. Y si se acaba la ventana de la estación, `abaco
desbloquear`: recibes la solución de referencia como nueva línea base y
**continúas con la estación siguiente**.

No se deniega nunca y no penaliza las estaciones posteriores. Preferimos que
llegues a S8 habiendo desbloqueado S4 a que te quedes clavado en S4 y te pierdas
donde está la mitad del valor. Lo que sí se evalúa es tu bitácora: qué intentaste
antes de desbloquear.

### Los comandos

```bash
abaco estado                         # dónde estás y qué te falta
abaco guia                           # qué tienes que conseguir ahora
abaco check --prediccion pasa        # verifica, tras declarar si crees que pasas
abaco pista                          # siguiente escalón de ayuda
abaco bitacora "lo que sea"          # anota en tu cuaderno
abaco cerrar                         # sella la estación y libera la referencia
abaco desbloquear --motivo "..."     # toma la referencia y continúa
```

### Sobre `--prediccion`

Antes de verificar, declaras si crees que vas a pasar. El sistema compara tu
predicción con el resultado y calcula tu **calibración**.

Mide si sabes lo que sabes, y resulta ser el mejor predictor de si vas a aprobar
por error algo defectuoso cuando estés en cliente. Si tu calibración es mala, tu
mentor lo verá y hablaréis de ello. No es un castigo: es la señal más útil que
tenemos antes de la primera ronda adversarial.

---

## 4. Las diez estaciones

| ID | Estación | Semanas | Horas | Qué demuestras |
|----|----------|---------|-------|----------------|
| S0 | Bootstrap y disciplina | 1 | 8 | Sabes montar un repo donde se pueda gobernar el trabajo |
| S1 | Rebanada vertical a mano | 2 a 4 | 24 | Sabes escribir, no solo revisar |
| S2 | Spec-Driven Development | 5 a 6 | 26 | Sabes derivar código verificable de una especificación |
| S3 | Ingeniería de contexto | 6 a 7 | 24 | Sabes preparar un repo para que un agente trabaje bien |
| S4a | MCP y agente de staffing | 8 a 10 | 28 | Sabes construir un agente que decide sobre personas, y medirlo |
| S4b | Flotilla multiagente | 10 | 12 | Sabes por qué tres agentes no tienen el mismo techo |
| S5 | Modernización del legado | 10 a 11 | 22 | Sabes tocar código heredado sin romperlo |
| S6 | Gobierno sobre personas | 11 | 18 | Sabes poner en producción un agente que afecta a carreras |
| S7 | Despliegue, fallo y MTTR | 12 | 24 | Sabes desplegar, romper y recuperar |
| S8 | Defensa ante panel | 12 | 10 | Sabes contarlo y defender el recorte |

**130 de las 196 horas están en S2 a S6.** Ahí está el diferencial.

### S1. Rebanada vertical a mano (24 h)

Construyes el alta de demanda y su máquina de estados completa **sin usar ningún
agente**.

Sabemos que es contraintuitivo en un programa de desarrollo agéntico. La razón es
simple: no se puede revisar lo que no se sabe escribir. Si llegas a S4 sin haber
escrito nunca un test a mano, aceptarás lo que te proponga el agente porque no
tendrás criterio con el que discrepar.

Apunta tus tiempos. Es tu línea base para medir tu propio salto en S2 y S3, con
datos tuyos y no con la cifra de un informe.

### S2. Spec-Driven Development (26 h)

Escribes la spec antes que el código, numeras los criterios y cada uno tiene que
tener un test que lo referencie. El pipeline lo comprueba.

**Aviso**: la spec de partida contiene dos ambigüedades reales y puestas a
propósito, sobre el cálculo de utilización. Si no las detectas, el agente
producirá una implementación perfectamente plausible y equivocada, y tú la
aprobarás porque los tests que escribiste sobre tu suposición pasarán.

Las dos preguntas que te van a desbloquear: cuando alguien está en formación o en
banquillo, ¿esos días cuentan como capacidad disponible? Y cuando alguien está al
120%, ¿aporta 120 o aporta 100?

Piénsalo antes de mirar la pista. Las dos tienen consecuencias en el número que
alguien va a usar para hablar de tu desempeño algún día.

### S3. Ingeniería de contexto (24 h)

Conviertes el repo en un sitio donde el agente trabaja bien por diseño:
`CLAUDE.md` con invariantes y límites, allowlist, hooks deterministas, subagentes
acotados.

La idea central: **lo innegociable no se pide en lenguaje natural, se hace
determinista**. En este proyecto hay una línea que ningún agente puede cruzar,
que son los campos de perfil prohibidos, y esa no se confía a una instrucción: se
hace con un hook.

Se mide tu **ratio de diff aceptado sin comentario**. Alto no es productividad,
es aceptación ciega. Cero tampoco es bueno: significa que no usas la herramienta.

### S4a. Servidor MCP y agente de staffing (28 h)

**Es el corazón del laboratorio.**

Construyes el servidor MCP y el agente que, dada una demanda, propone candidatos
ordenados con la evidencia de por qué cada uno entra y **por qué cada descartado
no entra**. Ese segundo campo no es opcional: un agente que dice a quién proponer
y calla a quién descartó no es explicable, y una recomendación que no se puede
explicar no se puede defender ante la persona que no fue propuesta.

Y lo mides con **dos métricas separadas**, que es la lección de la estación:

| Métrica | Umbral | Por qué |
|---------|--------|---------|
| **Seguridad**: violaciones de restricción dura | **0. Tolerancia cero** | Proponer a alguien no disponible, por debajo de la categoría pedida o sin el nivel exigido |
| **Utilidad**: la elección humana está en tu top 3 | ≥ 0,70 | Un agente seguro pero inútil se apaga a la semana |
| **Concentración**: personas distintas propuestas | Se mide y se comenta | Ver abajo |

**No se promedian.** Son obligaciones distintas y una no compensa a la otra. Una
sola violación de seguridad en la entrega final suspende la dimensión completa
aunque tu utilidad sea perfecta.

Dos iteraciones medidas es requisito. La versión ingenua que trae el repo comete
**43 violaciones y acierta el 15%**. Ese es tu punto de partida real.

Un consejo que te ahorra horas: **haz el núcleo determinista**. Filtros,
disponibilidad, categoría y aritmética sin modelo. Si dejas que el modelo decida a
quién se propone, el mismo caso te dará resultados distintos entre ejecuciones, y
eso no lo puedes defender ante nadie.

### La métrica de concentración, que es donde está lo interesante

Mides cuántas personas distintas propone tu agente sobre el pool total.

Te adelanto lo que va a pasar, porque pasó en la referencia: **tu versión final
será más segura y más útil que la v0, y a la vez más concentrada**. La referencia
pasó de proponer 33 personas distintas a proponer 20, y las cinco más propuestas
pasaron del 26,7% al 40,6% de todas las propuestas.

No es un fallo. Es la consecuencia directa de optimizar por encaje sin ninguna
contrapartida de reparto: cuando filtras bien, el conjunto que cumple todo se
estrecha, y dentro de él la puntuación premia siempre a los mismos. En un área
real esas personas ya están al 110%.

Si nadie mide esto, el agente parece un éxito perfecto. La concentración no
aparece en ninguna de las otras dos métricas y solo se ve si la buscas.

Es la primera vez en el programa que vas a medir un sesgo de un sistema que has
construido tú, y el sesgo no viene de los datos ni del modelo: **viene de tu
función de puntuación**.

### S5. Modernización del legado (22 h)

Te dan una calculadora de utilización heredada, sin tests, con números mágicos y
código muerto. Y con comportamientos que no están documentados en ninguna parte y
de los que depende el cuadro de mando que ve dirección.

**REGLA DURA: está prohibido pedirle al agente que refactorice antes de que
exista la caracterización.** El verificador comprueba el orden en tu historial de
git. Suspende la estación.

Un anticipo de lo que vas a encontrar: el número heredado dice que la utilización
del área es del **113%**. Un número por encima del 100% debería haber saltado a la
vista de cualquiera, y no saltó porque alimentaba un cuadro de mando que nadie
recalculaba. El valor correcto es 56,31%.

Esa diferencia de 57 puntos es la lección de la estación, y es la conversación
más incómoda del laboratorio: cuando corrijas el cálculo, el número que dirección
lleva años viendo se va a mover. Eso hay que anunciarlo antes, no después.

### S6. Gobierno de un agente que decide sobre personas (18 h)

La estación más rica del programa.

Escribes el Agent Release Manifest, que aquí tiene seis apartados que no existen
en un agente que revisa código: personas afectadas, explicabilidad, vía de
contestación, veto humano, vigilancia de concentración y datos excluidos.

Y haces que el pipeline bloquee el merge si el manifiesto falta, si el hash no
coincide, si la evaluación caducó **o si el nivel declarado supera N2**.

**Tu agente de staffing tiene techo permanente N2. Propone; decide un humano.**

Y aquí está la idea que quiero que te lleves del programa entero:

> El techo de autonomía no lo fija la precisión del modelo. Lo fija la
> reversibilidad del daño.

Un agente que revisa código puede equivocarse mil veces y el daño es ruido en un
PR. Un agente que asigna personas puede equivocarse una vez y el daño es un mes
de la carrera de alguien que no se recupera.

Si llegas al panel defendiendo que tu agente podría ir en autónomo porque tiene
buenas métricas, no has entendido la estación, por muy buenas que sean tus
métricas.

### S7 y S8

Despliegas, alguien de tu escuadra rompe tu entorno y tú el suyo. Dos rondas de
diagnóstico, sin agente y con agente, con MTTR medido. Y defiendes ante un panel
que incluye al dueño funcional de la herramienta: alguien que la va a usar.

---

## 5. Las rondas adversariales

Tres veces, tu mentor mete en tu rama un PR generado con agente que contiene
**exactamente un defecto**. Tienes 45 minutos para emitir veredicto.

| Ronda | Semana | Qué esperar |
|-------|--------|-------------|
| R1 | 6 | Visible leyendo con atención |
| R2 | 9 | Solo aparece si ejecutas y compruebas |
| R3 | 11 | Requiere razonar sobre el dominio |

Uno de los defectos de R3 es el mejor del programa y te lo describo sin decirte
en qué ronda cae: **el sistema deja de auditar lo que hace el agente, y sigue
auditando lo que hacen las personas**. Ningún test funcional lo detecta. Todo
sigue verde. Y el día que alguien pregunte por qué se tomó una decisión, la
respuesta existe si la tomó un humano y no existe si la tomó el agente.

Declarar conforme un PR defectuoso es el fallo grave del ejercicio. No porque
queramos pillarte, sino porque es exactamente lo que va a pasar en cliente.

---

## 6. Cuando te atascas

| Tiempo | Qué haces |
|--------|-----------|
| 0 a 15 min | Relees `CRITERIOS.md` y ejecutas `abaco check` para ver qué criterio falla exactamente, no el síntoma |
| 15 min | `abaco pista`, escalón 1 |
| 30 min | `abaco pista`, escalón 2, y documentación oficial |
| 45 min | Publicas en el canal con el formato de tres líneas |
| 90 min sin respuesta | Mentor |
| Fin de ventana | `abaco desbloquear` y sigues. Sin negociación |

**Formato de tres líneas**: qué intento, qué obtengo (la salida exacta, no tu
resumen), qué he probado. En un porcentaje alto de casos lo resolverás mientras
lo escribes.

---

## 7. Cómo se te evalúa

| Dimensión | Peso |
|-----------|:----:|
| Agente propio, MCP y evaluación | 25% |
| SDD y trazabilidad | 20% |
| Ingeniería de contexto y operación | 20% |
| Gobierno, evidencia y coste | 15% |
| Criterio de revisión | 10% |
| Fundamentos SDLC | 10% |

**Condición de suspenso específica de este laboratorio**: una violación de
restricción dura sin detectar en la entrega final de S4a suspende la dimensión
completa, con independencia del resto de métricas. Es la traducción a la rúbrica
del principio de que la seguridad no se promedia con nada.

**Nivel destacado**: tu agente o tu spec entra en el repositorio de activos del
AoE con tu nombre. Varios de los activos que usan hoy los equipos salieron de
trabajo de alguien que empezó donde estás tú.

---

## 8. Reglas del juego

**Lo que se espera de ti**

- Que uses agentes en todo salvo S1, y criterio en todo.
- Que escribas la bitácora en caliente, no el resumen del viernes.
- Que preguntes cuando una spec sea ambigua, en lugar de suponer.
- Que trates los datos de tus compañeros como querrías que trataran los tuyos.

**Lo que no**

- No copies ni un dato real al repositorio de aprendizaje. Ni para depurar.
- No modifiques los verificadores. Además de inútil, porque la ejecución que
  sella es la del pipeline, te llevará a suspender R3 y la defensa.
- No optimices contra el conjunto de evaluación. No ves sus etiquetas, y aunque
  las vieras estarías entrenándote para aprobar un examen.
- No aceptes un diff que no entiendes. En cliente el error lleva tu nombre en el
  historial de git.

---

## 9. Arranque

```bash
git clone <tu-repositorio-de-aprendizaje> && cd abaco
pip install -r requirements.txt
python3 herramientas/generar_corpus.py    # corpus sintético determinista
make ayuda
abaco estado
abaco guia
```

Si algo del entorno no arranca, no pierdas la mañana: el contenedor de desarrollo
está en `.devcontainer/` y levanta todo preinstalado.

---

## Y una última cosa

En algún momento de la semana 9 vas a tener delante una propuesta que tu agente
ha generado, con tres nombres ordenados y una explicación convincente.

La pregunta que decide si este programa ha servido de algo no es si el agente
acertó. Es si, antes de pasarle esa propuesta a alguien, comprobaste por qué
estaba el tercero y no el cuarto.

Eso es lo que vamos a entrenar durante doce semanas.
