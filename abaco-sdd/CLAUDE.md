# AGENTS.md

Instrucciones para cualquier asistente que trabaje en este repositorio.

## La regla que gobierna todo

**El codigo no se parchea. Se regenera.**

Si un test falla, no abras el fichero de implementacion. Busca que requisito o
escenario faltaba, estaba incompleto o admitia dos lecturas, enmienda la
especificacion y vuelve a generar.

## Rutas prohibidas

No escribas nunca en estas rutas, bajo ninguna circunstancia:

| Ruta | Motivo |
|------|--------|
| `aceptacion/` | Es la bateria de aceptacion externa. Si el generador puede modificar el examen que lo evalua, no hay evaluacion |
| `openspec/trazabilidad.md` | Lo mantiene una persona. Si lo generas tu, la comprobacion de deriva no vale nada |
| `herramientas/gates_sdd.py` | Son las puertas del laboratorio |
| `labs/*/verificar.py` | Es la vara de medir |
| `.github/workflows/` | Un agente que puede desactivar el gate que lo controla no esta controlado |

## Datos personales

Este es el repositorio de aprendizaje y trabaja con datos sinteticos. **Ningun
dato personal real entra aqui**: ni en un test, ni en un fichero de datos, ni en
un issue, ni en un mensaje de commit, ni en un prompt.

El agente de staffing ademas no puede leer nombre, correo, telefono, foto, pais,
oficina, fecha de nacimiento ni genero de ninguna persona.

## Formato de commit

Todo commit que toque codigo generado lleva:

```
feat(<capability>): <que se genero>

Change-Id: <nombre-del-cambio-en-openspec>
Generated-By: <herramienta> / opsx:apply
```

El `Change-Id` debe existir como carpeta activa o archivada en
`openspec/changes/`. El pipeline lo comprueba.

## Verificacion

Antes de dar por terminado cualquier trabajo, ejecuta y muestra la salida:

```bash
openspec validate --all
python3 -m pytest aceptacion/ -q
python3 -m herramientas.gates_sdd todos
```

No digas que algo funciona. Ensena la salida en verde.

## Ante una ambiguedad

Pregunta, no asumas. Una implementacion plausible derivada de una suposicion no
declarada es el defecto mas caro de este proyecto, porque en SDD se genera mas
rapido y con mas coherencia que si la escribiera una persona, y nada avisa.

Escribe la ambiguedad en el apartado correspondiente del cambio antes de generar.
