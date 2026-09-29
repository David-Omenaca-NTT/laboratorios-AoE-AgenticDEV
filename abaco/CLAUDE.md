# CLAUDE.md

Contrato de contexto del proyecto Ábaco. No es documentación: es la
configuración que hace que un agente trabaje bien en este repositorio por diseño
y no por suerte en el prompt. Se versiona y se revisa como código.

## Propósito

Ábaco es el núcleo de capacidad, demanda y asignación de personas a proyectos.
Decide si alguien puede ser asignado a una posición aplicando reglas de
capacidad, categoría, skill y disponibilidad, y calcula la ocupación real de las
personas y del área.

De sus números salen conversaciones de desempeño sobre personas con nombre y
apellidos, y el cuadro de mando mensual de dirección. La reproducibilidad exacta
del número es un requisito, no un detalle.

**Este es el repositorio de aprendizaje.** Trabaja con datos sintéticos. El
repositorio de producto es otro, contiene datos reales de empleados y se accede
por estación sellada.

## Invariantes

Estas seis cosas no se rompen nunca, aunque parezca que el código mejora:

1. **Ningún dato personal real entra en este repositorio.** Ni en un test, ni en
   un fichero de datos, ni en un issue, ni en un mensaje de commit, ni en un
   prompt. Hay un verificador que lo comprueba y salta en el pipeline.
2. El redondeo se aplica **una sola vez y al final**. El agregado suma numerador
   y denominador; nunca promedia porcentajes ya redondeados.
3. Numerador y denominador de la utilización excluyen exactamente los mismos
   días. Si no, el cociente no significa nada.
4. Toda decisión de asignación escribe traza de auditoría con versión de
   política, versión de catálogo y **origen**. Las decisiones del agente se
   auditan igual que las de una persona.
5. Una asignación registra la categoría vigente **en su fecha de inicio**. Una
   promoción posterior no reescribe el histórico.
6. Todo criterio de aceptación de una spec activa tiene al menos un test que lo
   referencia con la etiqueta `cubre:`.

## Verificación

Antes de dar por terminado cualquier cambio, ejecuta y muestra la salida:

```bash
python3 -m pytest tests/ -q                      # suite completa
python3 -m abaco_cli check                       # verificador de la estación activa
python3 -m agentes.staffing.evaluar              # seguridad, utilidad y concentración
```

No digas que algo funciona. Enseña la salida en verde. Una afirmación no es
evidencia.

## Convenciones

- Conventional commits: `feat:`, `fix:`, `test:`, `refactor:`, `docs:`, `chore:`.
- Máximo 400 líneas de diff por PR. Límite duro del pipeline. Si no cabe, se parte.
- Un test por criterio, con `cubre: SPEC-nnn/CA-nn` en el docstring.
- Español en documentación y nombres de dominio.
- Sin dependencias nuevas sin justificarlas en el PR.
- Sin coste, tarifa ni margen en el modelo: quedaron fuera por minimización de datos.

## Límites

Rutas que **no puedes modificar** sin aprobación humana explícita:

| Ruta | Motivo |
|------|--------|
| `src/abaco/legado/` | Solo se toca en S5, y solo después de que exista la caracterización |
| `manifiestos/` | Es el gobierno de los agentes. Que el vigilado escriba su propio permiso no es gobierno |
| `.github/workflows/` | Son los gates. Un agente que puede desactivar el gate que lo controla no está controlado |
| `labs/*/verificar.py` | Es la vara de medir |
| `evals/dorado*/` | Optimizar contra el conjunto de evaluación en lugar de contra el problema es el fallo clásico |

### Campos de perfil que ningún agente puede leer

Declarados como `CAMPOS_PROHIBIDOS` en el agente y comprobados por prueba
negativa en el verificador de S6:

`nombre`, `correo`, `teléfono`, `foto`, `país`, `oficina`, `fecha de nacimiento`,
`género`.

Un agente que propone personas no necesita saber cómo se llaman ni de dónde son.
Todo lo que necesita es categoría, skill, nivel y disponibilidad. Cuanto menos
ve, menos puede sesgar y menos hay que auditar.

## Escalado

Ante una ambigüedad de la especificación: **pregunta, no asumas**. Una
implementación plausible derivada de una suposición no declarada es el defecto
más caro de este proyecto, porque pasa los tests que tú mismo escribiste sobre
esa suposición.

Cuando encuentres una ambigüedad, escríbela en el apartado de ambigüedades de la
spec correspondiente antes de implementar nada.
