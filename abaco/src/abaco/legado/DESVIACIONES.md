# Desviaciones declaradas entre la calculadora heredada y el motor nuevo

Toda diferencia de resultado entre `legado/calculadora_utilizacion_v1.py` y
`reglas/ocupacion.py` sobre el corpus debe estar clasificada en una de estas
categorías. Una desviación sin categoría hace fallar el test de equivalencia y
bloquea la estación S5.

**Resultado agregado sobre el corpus (180 personas, julio de 2026):**

| Métrica | Legado | Motor nuevo | Diferencia |
|---------|--------|-------------|------------|
| Utilización global | 113,09% | 56,31% | 56,78 puntos |
| Personas coincidentes | 115 de 180 | | |
| Desviaciones justificadas | D-03: 11, D-04: 54 | | |
| Desviaciones sin justificar | 0 | | |

Que el número heredado esté por encima del 100% debería haber saltado a la vista
de cualquiera. No saltó porque alimentaba un cuadro de mando que nadie
recalculaba. Es la lección de la estación en una cifra.

## D-01: el banquillo se excluye entero del cálculo global

| Campo | Contenido |
|-------|-----------|
| Comportamiento heredado | A quien no tiene ninguna asignación se le saca del cálculo global, no solo del numerador |
| Comportamiento nuevo | Su capacidad entra en el denominador y baja el número, que es lo que corresponde |
| Origen | "Ajuste banquillo" de febrero de 2021, sin ticket asociado |
| Efecto | La utilización del área sube sin que nadie haya trabajado más. Con 1 persona ocupada y 4 en banquillo, el legado sigue diciendo 100% |
| Naturaleza | Corrección deliberada, resuelta en SPEC-002/A-01 |
| Efecto aguas abajo | El cuadro de mando mensual de dirección cambia de forma visible. Requiere aviso y recálculo del histórico antes de sustituir el motor |

## D-02: promedio de porcentajes ya redondeados

| Campo | Contenido |
|-------|-----------|
| Comportamiento heredado | El global promedia utilizaciones individuales redondeadas, en lugar de agregar numerador y denominador |
| Comportamiento nuevo | Agrega y redondea una sola vez, al final |
| Origen | Petición de reporting de septiembre de 2022 |
| Efecto | Con capacidades distintas entre personas los dos caminos dan números distintos. Una persona con poca capacidad pesa lo mismo que una a jornada completa |
| Naturaleza | Corrección deliberada, resuelta en SPEC-002/INV-01 |

## D-03: la asignación computa durante ausencia no trabajable

| Campo | Contenido |
|-------|-----------|
| Comportamiento heredado | Cuenta como asignados días en los que la persona estaba de vacaciones o de baja |
| Comportamiento nuevo | Numerador y denominador excluyen exactamente los mismos días |
| Efecto | Utilizaciones individuales por encima del 100% sin que nadie haya trabajado de más. Afecta a 11 personas del corpus |
| Naturaleza | Corrección deliberada, resuelta en SPEC-002/CA-08 y A-03 |
| Efecto aguas abajo | Cualquier conversación de desempeño basada en el número individual estaba usando un dato inflado |

## D-04: la sobreasignación no se corta en el 100%

| Campo | Contenido |
|-------|-----------|
| Comportamiento heredado | Una persona al 150% aporta 150% a la utilización |
| Comportamiento nuevo | Se corta en 100% y el exceso se reporta como indicador propio de sobreasignación |
| Efecto | Afecta a 54 personas del corpus. Un equipo quemado parece un equipo eficiente y el problema queda escondido dentro del número que se presume bueno |
| Naturaleza | Corrección deliberada, resuelta en SPEC-002/A-02 |
| Efecto aguas abajo | Aparece un indicador nuevo, sobreasignación, que antes no existía y que va a incomodar. Ese es justamente su propósito |

## Cómo se lee esto en cliente

Las cuatro desviaciones son el mismo patrón que aparece en cualquier motor de
cálculo heredado: reglas que nadie recuerda haber pedido, un redondeo colocado
donde no debía y una métrica que se optimizó para parecer buena. Ninguna se
descubre leyendo el código. Todas se descubren caracterizando y contrastando
contra un corpus.
