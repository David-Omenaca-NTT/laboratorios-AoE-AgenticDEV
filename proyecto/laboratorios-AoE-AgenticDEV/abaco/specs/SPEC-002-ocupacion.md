# SPEC-002: utilización y ocupación

Versión: v1.2.0 | Estado: activa
Autor: referencia del laboratorio | Revisor: SME de plataforma

> Esta es la spec que contiene la ambigüedad plantada del laboratorio. En el
> repo de aprendizaje que recibe el student, el apartado de ambigüedades está
> **vacío** y los criterios CA-01 y CA-05 están redactados de forma ambigua a
> propósito. Lo que sigue es la versión de referencia, ya resuelta.

## Propósito

Calcular la ocupación real de las personas y del área: utilización individual,
desviación sobre el objetivo de su categoría, sobreasignación, utilización
agregada y cobertura de demanda.

De estos números salen conversaciones de desempeño sobre personas con nombre y
apellidos y el cuadro de mando mensual de dirección. La reproducibilidad exacta
del número es un requisito, no un detalle.

## Entradas y salidas

| Elemento | Tipo | Restricciones |
|----------|------|---------------|
| Persona | Con histórico de categoría | |
| Asignaciones | Con dedicación y periodo | |
| Ausencias | Con tipo y aprobación | El tipo determina si computa como capacidad |
| Catálogo | Versionado | Aporta el objetivo de utilización por categoría |
| Utilización | Decimal | Porcentaje con exactamente dos decimales, redondeo half-up |

## Invariantes

- INV-01: el redondeo se aplica una sola vez y al final. Nunca por persona ni por mes antes de agregar. El agregado suma numerador y denominador, no promedia porcentajes ya redondeados.
- INV-02: aritmética decimal, nunca coma flotante binaria.
- INV-03: el resultado es determinista y no depende del orden de las asignaciones.

## Criterios de aceptación

- CA-01: dado un periodo, cuando se calcula la utilización, entonces es días equivalentes asignados entre capacidad disponible. La capacidad disponible son los días laborables del periodo menos las ausencias no trabajables aprobadas. **La formación y el banquillo sí computan como capacidad disponible; solo se excluyen vacaciones, festivos y bajas.**
- CA-02: dada una persona, cuando se evalúa su utilización, entonces se compara contra el objetivo de utilización de su categoría, nunca contra un objetivo único de compañía.
- CA-03: dada una asignación que cubre parcialmente el periodo, cuando se calcula, entonces prorratea por días laborables efectivos del solape, no por días naturales ni por mes completo.
- CA-04: dada una demanda, cuando se calcula su cobertura, entonces es la proporción de posiciones cubiertas por una asignación cuya categoría registrada iguala o supera la pedida.
- CA-05: dada una persona sobreasignada, cuando se calcula su utilización, entonces la suma de dedicaciones **se corta en el 100% en cada día**. Una persona al 150% tiene una utilización del 100%.
- CA-06: dada una persona sobreasignada, cuando se calcula la sobreasignación, entonces se reporta como indicador propio: días equivalentes por encima del 100% sobre la capacidad del periodo.
- CA-07: dada una persona sin ninguna asignación en el periodo y con capacidad disponible, cuando se evalúa, entonces está en banquillo. Sin capacidad disponible no se considera banquillo.
- CA-08: dada una asignación que solapa una ausencia no trabajable aprobada, cuando se calculan los días asignados, entonces esos días no computan. Numerador y denominador excluyen exactamente los mismos días.

## Casos límite

| Caso | Resultado esperado |
|------|--------------------|
| Persona de vacaciones todo el mes | Capacidad 0, utilización 0,00 sin error, no cuenta como banquillo |
| Persona asignada al 100% con tres semanas de vacaciones | Utilización 100%, no 287% |
| Dos asignaciones al 100% y al 50% simultáneas | Utilización 100%, sobreasignación 50% |
| Agregado con una persona en banquillo | Su capacidad entra en el denominador y baja el número global |
| Persona con capacidad 0 en el agregado | Se excluye del agregado, no divide por cero |

## Fuera de alcance

Rutas: src/abaco/reglas/ocupacion.py, tests/test_ocupacion.py, specs/SPEC-002-ocupacion.md

- Coste, ingreso, tarifa y margen: fuera del sistema por minimización de datos.
- Forecast y proyección de ocupación futura.
- Imputación real de horas: aquí se calcula sobre asignación, no sobre timesheet.
- Objetivos individuales negociados que se aparten del objetivo de su categoría.

## Ambigüedades detectadas y resolución

| # | Ambigüedad | Resolución adoptada | Alternativa descartada y por qué |
|---|-----------|---------------------|----------------------------------|
| A-01 | No estaba definido si la formación y el banquillo entran en el denominador de la utilización | Sí entran: son capacidad que existía y no se facturó | Excluirlos sube la utilización del área sin que nadie haya trabajado más. Es exactamente lo que hace el módulo heredado y por eso su número no cuadra con la realidad |
| A-02 | No estaba definido si una sobreasignación al 120% aporta 120 o se corta en 100 | Se corta en 100, y el exceso se reporta como indicador propio | Dejar que aporte 120 hace que un equipo quemado parezca un equipo eficiente, y esconde justo lo que hay que vigilar |
| A-03 | No estaba definido qué pasa con una asignación que solapa vacaciones aprobadas | No computa esos días. Numerador y denominador excluyen los mismos días | Contarlos produce utilizaciones por encima del 100% sin que nadie haya trabajado de más. Recogido en CA-08 |

La resolución de A-01 y A-02 es deliberadamente distinta del comportamiento del
módulo heredado. Esa diferencia es la que aparece en el informe de equivalencia
de S5 y debe declararse como corrección intencionada en `legado/DESVIACIONES.md`.
