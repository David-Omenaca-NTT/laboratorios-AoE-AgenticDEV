# Guía de consulta: SDD con OpenSpec

Manual de referencia del laboratorio. No se lee de una vez: se consulta cuando
hace falta. Si buscas cómo empezar, ve al [PLAYBOOK](PLAYBOOK.md).

Verificado contra OpenSpec 1.8.0 el 13 de agosto de 2026. Si tu versión es otra,
comprueba antes de fiarte: la herramienta se mueve rápido.

---

## 1. La regla que gobierna todo

> **El código no se parchea. Se regenera.**

Cuando un test falla, el reflejo de cualquiera es abrir el fichero y arreglarlo.
Aquí eso está prohibido, y es lo único que de verdad tienes que interiorizar.

| Paso | Qué haces |
|------|-----------|
| 1 | Preguntas qué requisito o escenario faltaba, estaba incompleto o admitía dos lecturas. **Un fallo del código es siempre un síntoma de un fallo de la especificación** |
| 2 | Enmiendas la spec delta del cambio activo. Si el fallo revela una intención distinta, abres un cambio nuevo |
| 3 | Regeneras con `/opsx:apply` |
| 4 | Compruebas contra la batería de aceptación externa, que nadie ha tocado |

### La única excepción, y no es una excepción

Puedes escribir a mano en dos sitios, y solo en dos:

- `openspec/` — los requisitos y escenarios. Son la especificación, es tu trabajo.
- `aceptacion/` — la batería externa. Es el examen, y el examinado no lo escribe.

Todo lo demás lo genera el agente.

---

## 2. Los cuatro artefactos de un cambio

Cada cambio vive en `openspec/changes/<nombre>/` y tiene cuatro piezas. Ninguna
es opcional y cada una responde a una pregunta distinta.

| Artefacto | Pregunta que responde | Quién lo revisa |
|-----------|----------------------|-----------------|
| `proposal.md` | Por qué se hace, qué capabilities toca y qué impacto tiene | El humano que aprueba, **antes** de generar nada |
| `specs/<cap>/spec.md` | Qué tiene que cumplir el sistema | Es el contrato. Lo único que genera código |
| `design.md` | Cómo se va a hacer y qué se descartó | Quien vaya a mantenerlo dentro de un año |
| `tasks.md` | Qué pasos hay que ejecutar | El agente, al aplicar |

**El apartado de alternativas descartadas de `design.md` es el que más rendimiento
da a largo plazo.** Dentro de un año nadie recuerda por qué no se hizo de la otra
forma, y sin ese apartado se vuelve a discutir desde cero.

---

## 3. Anatomía de un requisito

```markdown
### Requirement: Corte de la sobreasignación
Al calcular la utilización, la suma de dedicaciones de un día NO DEBE superar el
100%. El exceso se reporta como indicador propio.

#### Scenario: Persona al 150%
- **WHEN** una persona acumula dos asignaciones simultáneas del 100% y del 50%
- **THEN** su utilización es del 100,00% y su sobreasignación del 50,00%

#### Scenario: Persona sin exceso
- **WHEN** la suma de dedicaciones no supera el 100% ningún día
- **THEN** su sobreasignación es 0,00%
```

### Las cuatro reglas de un requisito que sirve

| Regla | Contraejemplo |
|-------|---------------|
| Si no se puede convertir en escenario, no es un requisito, es un deseo | "El sistema debe gestionar correctamente las demandas" |
| DEBE y NO DEBE, no "debería" ni "se recomienda" | "Sería conveniente validar la capacidad" |
| Al menos un escenario que describa el caso que **no** se cumple | Un requisito con solo escenarios felices no protege de nada |
| Números concretos, no adjetivos | "La utilización debe ser razonable" |

### Cuántos escenarios

Entre uno y ocho por requisito. Por debajo no cubre; por encima nadie lo lee, y
una spec que nadie lee no gobierna nada. Lo comprueba `gates_sdd.py densidad`.

---

## 4. Deltas: la parte que distingue a OpenSpec

Un cambio sobre algo que ya existe **no reescribe la capability**. Declara qué
cambia con estas secciones:

| Sección | Cuándo |
|---------|--------|
| `## ADDED Requirements` | Requisitos nuevos |
| `## MODIFIED Requirements` | Requisitos que ya existen y cambian |
| `## REMOVED Requirements` | Requisitos que se eliminan |
| `## RENAMED Requirements` | Requisitos que solo cambian de nombre |

### El error que vas a cometer, y lo sabemos porque lo cometimos

**Un bloque MODIFIED es el estado completo nuevo del requisito, no un parche.**
Todo escenario que no aparezca en el bloque queda eliminado.

Al construir el cambio de referencia E3 reformulamos el requisito de transiciones
y dejamos fuera, sin querer, un escenario que ya existía. OpenSpec lo rechazó al
archivar con este mensaje:

```
demanda MODIFIED failed for header "### Requirement: Transiciones permitidas"
- current spec contains scenario(s) not present in the modified block:
  "Cancelacion de demanda ya asignada".
  Refresh the change spec before archiving to avoid dropping scenarios.
```

Dos cosas que aprender de ahí:

1. Cuando modifiques un requisito, **copia sus escenarios actuales y edita sobre
   ellos**. No lo reescribas de memoria.
2. **`openspec validate` no detecta esto. Solo lo detecta `archive`.** Que algo
   valide no significa que esté bien.

Lo tienes documentado en `openspec/changes/archive/2026-09-29-e3-.../LEEME.md`.

---

## 5. El ciclo, comando a comando

```bash
/opsx:explore                # opcional: pensar antes de comprometerse
/opsx:new <nombre-del-cambio>
/opsx:continue               # un artefacto cada vez, revisando
/opsx:apply                  # genera el código desde tasks.md
/opsx:verify                 # completitud, corrección y coherencia
/opsx:archive                # sincroniza specs principales y archiva
```

| Comando | Qué hace de verdad |
|---------|--------------------|
| `/opsx:explore` | Conversación sin artefactos. Investiga el código y compara opciones. Úsalo cuando no tengas claro qué quieres |
| `/opsx:new` | Crea la carpeta y el `.openspec.yaml`. No genera contenido |
| `/opsx:continue` | Crea el siguiente artefacto en orden de dependencia. **Prefiérelo a `/opsx:ff`**: revisas cada pieza antes de que la siguiente se apoye en ella |
| `/opsx:ff` | Crea todos los artefactos de golpe. Rápido y peligroso: si la propuesta está mal, todo lo demás hereda el error |
| `/opsx:apply` | Ejecuta `tasks.md` y marca las casillas |
| `/opsx:update` | Revisa artefactos de planificación y los reconcilia. **Nunca toca código** |
| `/opsx:verify` | Comprueba tres dimensiones. Ojo: **no bloquea el archivado** |
| `/opsx:sync` | Funde los deltas en las specs principales sin archivar |
| `/opsx:archive` | Sincroniza si hace falta y mueve a `archive/AAAA-MM-DD-nombre/` |

### Comandos de terminal

```bash
openspec list                      # cambios activos
openspec list --specs              # capabilities
openspec validate --all            # valida cambios y specs
openspec show <cambio|spec>        # ver un elemento
openspec status --change <nombre>  # estado de artefactos de un cambio
openspec view                      # panel interactivo
openspec doctor                    # salud de relaciones
openspec archive <cambio> -y       # archivar sin confirmación
```

### Dos advertencias sobre `/opsx:verify`

1. **No bloquea.** Reporta críticos, advertencias y sugerencias, y te deja
   archivar igual. En este laboratorio el pipeline sí bloquea, y por eso existe.
2. **Es un agente comprobando trabajo de agente.** Sirve para detectar
   incoherencias evidentes, no como garantía. La garantía es `aceptacion/`.

---

## 6. Las cuatro puertas del laboratorio

```bash
python3 -m herramientas.gates_sdd todos
```

| Puerta | Qué detecta | Por qué existe |
|--------|-------------|----------------|
| `procedencia` | Commits sobre `src/` sin `Change-Id`, o con uno que no existe | Es la que detecta el parcheo silencioso, la infracción que define la modalidad |
| `aceptacion` | Commits marcados como generados que tocan `aceptacion/` | Si el generador puede modificar su propio examen, no hay examen |
| `deriva` | Capabilities sin código y código sin capability | El código que nadie pidió es el que nadie revisará |
| `densidad` | Escenarios por requisito fuera de rango | Una spec que nadie lee no gobierna nada |

### Formato de commit obligatorio

```
feat(ocupacion): genera la capability desde su especificacion

Change-Id: e5-ocupacion-utilizacion
Generated-By: claude-code / opsx:apply
```

`Change-Id` tiene que existir como carpeta activa o archivada. El pipeline lo
comprueba contra el sistema de ficheros, no se fía del texto.

---

## 7. Mapa del repositorio

| Ruta | Qué es | ¿Lo toca el agente? |
|------|--------|---------------------|
| `openspec/specs/` | Especificaciones principales, el estado actual del sistema | Solo vía `sync` y `archive` |
| `openspec/changes/` | Cambios en curso | Sí, es su sitio |
| `openspec/changes/archive/` | **La referencia por etapa del curso.** Diez cambios completos | No |
| `openspec/trazabilidad.md` | Qué módulo implementa cada capability | **No. Lo mantiene una persona** |
| `src/` | Código generado | Sí, solo por generación |
| `aceptacion/` | Batería externa escrita a mano | **Nunca** |
| `herramientas/gates_sdd.py` | Las cuatro puertas | No |
| `labs/` | Guías, criterios y verificadores por etapa | No |
| `politicas/` | Catálogos y políticas versionados por vigencia | No |

---

## 8. Cómo usar el archivo como referencia

Es para lo que existe. Si estás en E5 y no sabes qué aspecto debe tener tu
cambio, abre el de E5 y míralo.

```bash
ls openspec/changes/archive/
cat openspec/changes/archive/2026-10-27-e5-ocupacion-utilizacion/LEEME.md
```

Cada carpeta lleva un `LEEME.md` con la nota didáctica de esa etapa, y los cuatro
artefactos completos.

| Si te preguntas | Abre |
|-----------------|------|
| Qué aspecto tiene un cambio mínimo bien hecho | E1 |
| Cómo se expresa una máquina de estados como escenarios | E2 |
| Cómo se modifica algo que ya existe sin romperlo | **E3, y lee su LEEME: contiene un error real** |
| Cómo se especifican restricciones duras | E4 |
| Cómo se resuelve una ambigüedad y se deja constancia | **E5, el cambio central del curso** |
| Cómo se especifica un agente y su techo de autonomía | E6 |
| Cómo se describe un sistema heredado antes de tocarlo | E7 |
| Cómo se corrige un defecto avisando del impacto | E7b |
| Cómo se convierte el gobierno en puertas automáticas | E8 |
| Cómo se especifica la operación y la reversión | E9 |

---

## 9. Errores frecuentes

| Síntoma | Causa casi siempre | Qué hacer |
|---------|--------------------|-----------|
| El código generado no hace lo que esperabas | Tu escenario admitía dos lecturas | No toques el código. Reescribe el escenario y regenera |
| `archive` se queja de escenarios que faltan | Reescribiste un bloque MODIFIED de memoria | Copia los escenarios actuales de la spec principal y edita sobre ellos |
| `validate` pasa y `archive` falla | Son comprobaciones distintas | Ejecuta siempre los dos antes de dar nada por cerrado |
| La puerta de procedencia bloquea tu PR | Falta `Change-Id` o apunta a algo inexistente | Rehaz el commit con el pie correcto |
| La puerta de deriva se queja de un módulo huérfano | Se generó código que ningún requisito pide | O sobra el código, o falta el requisito. Decide cuál |
| Un cambio no tiene ninguna capability que tocar | Es puro refactor, tooling o documentación | Marca `skip_specs: true` en su `.openspec.yaml`. **No inventes un requisito para que valide** |
| El agente genera specs larguísimas | Le diste una descripción vaga | Escribe tú el primer requisito a mano y deja que siga el patrón |

---

## 10. Configuración del proyecto

`openspec/config.yaml` acepta contexto de proyecto y reglas por artefacto. El
contexto se le enseña al agente cada vez que crea un artefacto, así que es la
palanca más barata para subir la calidad de lo que genera.

```yaml
schema: spec-driven

context: |
  Núcleo de capacidad, demanda y asignación de personas a proyectos.
  Python con FastAPI. Aritmética decimal obligatoria en todo cálculo.
  Sin coste, tarifa ni margen: fuera del sistema por minimización de datos.
  De estos números salen conversaciones sobre personas concretas.

rules:
  proposal:
    - Declara siempre el impacto aguas abajo, incluido el de comunicación
  specs:
    - Todo requisito lleva al menos un escenario negativo
    - Números concretos, nunca adjetivos
  design:
    - Toda decisión lleva su alternativa descartada y el motivo
```

### Telemetría

OpenSpec envía estadísticas anónimas de uso. **En este laboratorio va
desactivada por política**, no por preferencia:

```bash
export OPENSPEC_TELEMETRY=0
export DO_NOT_TRACK=1
```

Está en el devcontainer y en el pipeline. No lo quites.

---

## 11. Lo que esta modalidad no te va a enseñar

Conviene saberlo para compensarlo por tu cuenta.

| No lo aprendes aquí | Cómo lo compensas |
|---------------------|-------------------|
| Escribir implementación desde cero | Los ejercicios de arqueología de E4 y E7: te dan código generado y buscas el requisito que lo originó |
| Depurar con un depurador | La batería de aceptación te dice qué falla, no por qué. Pídele al agente que instrumente, y lee |
| Intuición de rendimiento | Fuera de alcance de la cohorte |

Y la advertencia principal, que vas a comprobar en E5:

> **SDD no te protege de una especificación equivocada. La ejecuta más rápido y
> de forma más coherente.** Toda la disciplina existe para que la especificación
> sea correcta, porque después ya no hay ninguna fricción que te avise.
