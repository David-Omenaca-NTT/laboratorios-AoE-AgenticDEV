<!-- version: v1.0 | estado: para entregar | audiencia: students de la vía SDD estricta -->

# Playbook del laboratorio, vía SDD estricta

**Proyecto Ábaco sobre OpenSpec | AI Engineering Talent Factory | AoE Agentic DevOps**
206 horas | 10 etapas | 12 semanas

---

## Lo primero, y es distinto de lo que esperas

**No vas a escribir código.**

Ni una línea de implementación en doce semanas. Si un test falla, no puedes
abrir el fichero y arreglarlo. Tienes que averiguar qué requisito faltaba,
corregir la especificación y volver a generar.

Sabemos que suena a limitación arbitraria. No lo es: es la disciplina que los
clientes están empezando a pedir y que casi nadie sabe ejecutar. Tu trabajo deja
de ser producir código y pasa a ser producir **intención verificable**, que es lo
que el mercado va a pagar los próximos años.

Dos cosas sí las escribes tú, a mano, y son las importantes:

| Ruta | Qué es |
|------|--------|
| `openspec/` | Los requisitos y escenarios. Es la especificación: es tu trabajo |
| `aceptacion/` | La batería externa. Es el examen, y el examinado no lo escribe |

Esa segunda es la que hace seguro todo lo demás. Si el agente escribiera la spec,
el código y los tests, no habría nadie fuera del bucle comprobando nada.

---

## 1. Qué vas a construir

**Proyecto Ábaco**: el núcleo de capacidad, demanda y asignación de personas a
proyectos. Quién puede entrar en qué proyecto, cuánta ocupación real tiene cada
persona y cuánta el área.

Al terminar tendrás ocho capabilities especificadas, el código generado de todas
ellas, un agente que propone candidatos, un módulo heredado caracterizado y
corregido, y un archivo de cambios que documenta por qué el sistema hace cada
cosa que hace.

Nada de eso lo habrás escrito a mano. Todo lo habrás especificado.

---

## 2. El ciclo, que se repite diez veces

```bash
/opsx:explore                # si no tienes claro qué quieres
/opsx:new <nombre>           # crea la carpeta del cambio
/opsx:continue               # un artefacto cada vez, revisando
/opsx:apply                  # genera el código
/opsx:verify                 # comprueba coherencia
/opsx:archive                # sincroniza specs y archiva
```

**Usa `/opsx:continue` y no `/opsx:ff`.** Crear los cuatro artefactos de golpe es
más rápido y es exactamente donde se cuelan los errores: si la propuesta está
mal, la spec, el diseño y las tareas heredan el error y tú no lo ves hasta que el
código ya está generado.

### Los cuatro artefactos

| Artefacto | Pregunta que responde |
|-----------|----------------------|
| `proposal.md` | Por qué se hace y qué impacto tiene. Lo revisa un humano **antes** de generar |
| `specs/` | Qué tiene que cumplir el sistema. Es el contrato y lo único que genera código |
| `design.md` | Cómo se hace y **qué se descartó** |
| `tasks.md` | Los pasos que ejecuta el agente |

---

## 3. Cómo se escribe un requisito que sirve

```markdown
### Requirement: Corte de la sobreasignación
Al calcular la utilización, la suma de dedicaciones de un día NO DEBE superar el
100%. El exceso se reporta como indicador propio.

#### Scenario: Persona al 150%
- **WHEN** una persona acumula dos asignaciones simultáneas del 100% y del 50%
- **THEN** su utilización es del 100,00% y su sobreasignación del 50,00%
```

Cuatro reglas, y las cuatro se comprueban:

| Regla | Contraejemplo que te van a devolver |
|-------|-------------------------------------|
| Si no se puede convertir en escenario, es un deseo | "El sistema debe gestionar correctamente las demandas" |
| DEBE y NO DEBE, no "debería" | "Sería conveniente validar la capacidad" |
| Al menos un escenario del caso que **no** se cumple | Un requisito con solo escenarios felices no protege de nada |
| Números concretos, no adjetivos | "La utilización debe ser razonable" |

---

## 4. Las etapas

| ID | Etapa | Semanas | Horas |
|----|-------|---------|-------|
| E0 | Bootstrap y contrato SDD | 1 | 8 |
| E1 | El ciclo completo en pequeño | 2 | 16 |
| E2 | Primera capability: ciclo de vida de la demanda | 2 a 3 | 20 |
| E3 | Deltas sobre lo existente | 4 | 18 |
| E4 | Capability de reglas duras: motor de asignación | 5 a 6 | 26 |
| E5 | Capability numérica: ocupación | 6 a 7 | 26 |
| E6 | El agente, especificado y generado | 8 a 10 | 28 |
| E7 | Brownfield real: el legado | 10 a 11 | 22 |
| E8 | Gobierno de especificaciones y de agentes | 11 | 18 |
| E9 | Despliegue, deriva y defensa | 12 | 24 |

### E3, donde vas a tropezar la primera vez

Modificar algo que ya existe. **Un bloque MODIFIED es el estado completo nuevo
del requisito, no un parche.** Todo escenario que no aparezca queda eliminado.

Nosotros cometimos ese error construyendo la referencia y la herramienta lo
cazó al archivar. Está el mensaje exacto en el `LEEME.md` de ese cambio. Léelo
antes de empezar E3, no después.

Y un detalle que importa: **`openspec validate` no detecta ese error. Solo lo
detecta `archive`.** Que algo valide no significa que esté bien.

### E5, la etapa que justifica el laboratorio

Especificas el cálculo de utilización. La spec de partida tiene dos decisiones
sin tomar y no te lo dice.

Cuando encuentres una diferencia entre lo que esperabas y lo que salió, la
tentación va a ser mirar el código. No lo hagas. Mira tu escenario.

Lo que vas a aprender ahí, y es lo más valioso de las doce semanas:

> **SDD no te protege de una especificación equivocada. La ejecuta más rápido y
> de forma más coherente.**

En un laboratorio normal, escribir el código a mano te habría hecho tropezar con
la ambigüedad. Aquí no hay ninguna fricción que te avise. El único punto de
control es tu batería de aceptación y tu propia atención al escribir la spec.

### E6, tu agente

Especificas y generas un agente que propone candidatos para una demanda.

Cuando la métrica de seguridad no llegue a cero, **está prohibido tocar el
agente**. Tienes que encontrar qué restricción dura no habías especificado.

Vas a descubrir que casi todos los fallos de tu agente eran fallos de tu
especificación. Ese descubrimiento es el entregable real de la etapa.

### E7, el legado

Un módulo heredado que dice que la utilización del área es del **113%**. Un
número por encima del 100% llevaba años publicándose sin que nadie lo
recalculara.

Primero escribes la especificación de lo que **hace**, incluidos los defectos,
sin juzgarlos. Después, en un cambio aparte, los corriges. Así el archivo
conserva las dos versiones y la fecha en que se pasó de una a la otra.

---

## 5. Las cuatro puertas

```bash
python3 -m herramientas.gates_sdd todos
```

| Puerta | Qué te va a bloquear |
|--------|---------------------|
| `procedencia` | Un commit sobre `src/` sin `Change-Id`, o con uno que no existe |
| `aceptacion` | Un commit generado que toca tu batería externa |
| `deriva` | Código que ningún requisito pide, o requisitos que nadie implementó |
| `densidad` | Requisitos con demasiados escenarios o con ninguno |

Formato de commit obligatorio:

```
feat(ocupacion): genera la capability desde su especificacion

Change-Id: e5-ocupacion-utilizacion
Generated-By: claude-code / opsx:apply
```

La primera semana la puerta de procedencia te va a bloquear varias veces. Es el
precio de que la disciplina sea real y no una frase en un documento.

---

## 6. La referencia por etapa

Es la razón de ser de este repositorio. Si estás en E5 y no sabes qué aspecto
debe tener tu cambio, abre el de E5 y míralo.

```bash
ls openspec/changes/archive/
cat openspec/changes/archive/2026-10-27-e5-ocupacion-utilizacion/LEEME.md
```

Cada carpeta tiene los cuatro artefactos completos y una nota didáctica con lo
que hay que mirar en esa etapa.

Y para todo lo demás, [GUIA-SDD.md](GUIA-SDD.md) es el manual de consulta:
comandos, formato de deltas, errores frecuentes y qué hacer cuando algo falla.

---

## 7. Cómo se te evalúa

Las métricas del agente son las mismas que en las otras vías. Estas seis son
propias de esta modalidad.

| Métrica | Umbral |
|---------|--------|
| Procedencia: commits con `Change-Id` válido | 100% |
| **Tasa de parcheo: ediciones humanas de implementación** | **0. Es la infracción que define la vía** |
| Deriva entre especificación y código | Menos del 5% |
| Vacuidad: mutaciones que tu batería no detecta | 0 |
| Densidad: escenarios por requisito | Entre 1 y 8 |
| Coste por requisito entregado | Registrado, con tendencia a la baja |

La de vacuidad es la que sostiene todo. Si el agente genera código y tests, y
romper el código a propósito no rompe ningún test, tienes una fábrica de verde
que no verifica nada.

---

## 8. Lo que esta vía no te va a enseñar

Conviene que lo sepas para compensarlo.

No vas a aprender a escribir implementación desde cero ni a depurar con un
depurador. Se compensa con los ejercicios de arqueología de E4 y E7: te damos
código generado y tienes que localizar el requisito que lo originó, y encontrar
el que falta.

Pero sé honesto contigo mismo sobre esto en la defensa final. Una de las láminas
que te vamos a pedir es **en qué contextos no recomendarías esta disciplina**, y
la respuesta tiene que ser algo más que "en ninguno".

---

## 9. Arranque

```bash
git clone <tu-repositorio> && cd abaco-sdd
npm install -g @fission-ai/openspec@1.8.0
pip install -r requirements.txt
export OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1

python3 herramientas/generar_corpus.py
openspec list --specs
abaco estado
abaco guia
```

---

## Y una última cosa

En la semana 6 vas a tener delante una especificación que te parecerá clara, y un
código generado a partir de ella que hará algo distinto de lo que esperabas.

La pregunta que decide si este programa te ha servido no es si el agente acertó.
Es si, en ese momento, tu primer impulso fue abrir el código o abrir la spec.
