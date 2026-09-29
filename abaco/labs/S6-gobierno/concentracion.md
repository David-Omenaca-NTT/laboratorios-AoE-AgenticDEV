# Informe de concentración de propuestas

## Medición

| Métrica | Agente v0 | Versión final |
|---------|-----------|---------------|
| Pool disponible | 180 personas | 180 personas |
| Personas distintas propuestas | 33 | **20** |
| Cobertura del pool | 18,3% | **11,1%** |
| Cuota de las cinco más propuestas | 26,7% | **40,6%** |
| Violaciones de restricción dura | 43 | 0 |
| Utilidad (top 3) | 0,154 | 1,000 |

## El hallazgo

**La versión final es más segura y más útil que la v0, y a la vez más
concentrada.** Propone la mitad de personas distintas y las cinco más propuestas
acumulan el 40,6% de las propuestas frente al 26,7% de la versión ingenua.

No es un fallo del agente. Es la consecuencia directa de optimizar por encaje sin
ninguna contrapartida de reparto. Cuando el agente empieza a filtrar bien por
categoría, nivel de skill y disponibilidad real, el conjunto de personas que
cumplen todo se estrecha, y dentro de ese conjunto la puntuación siempre premia a
los mismos: quienes tienen el nivel más alto y más hueco.

En un área real esas personas ya están al 110%.

## Por qué importa que lo haya medido yo

Si nadie mide esto, el agente parece un éxito: cero violaciones y acierto
perfecto. La concentración no aparece en ninguna de las dos métricas de la
estación y solo se ve si se busca a propósito.

Es la primera vez en el programa que mido un sesgo de un sistema que he
construido yo, y el sesgo no viene de los datos ni del modelo: viene de mi
función de puntuación.

## Qué haría en la siguiente iteración

| Palanca | Efecto esperado | Riesgo |
|---------|-----------------|--------|
| Penalizar en la puntuación a quien ya ha sido propuesto varias veces en la ventana | Reparte, sube cobertura del pool | Puede proponer peores encajes |
| Bonificar tiempo en banquillo | Saca gente del banquillo antes | Puede favorecer a quien lleva parado por un motivo |
| Fijar un umbral de revisión en la cuota del top 5 | Convierte el sesgo en una alerta, no en una regla | No lo corrige, solo lo hace visible |

Recomendación: la tercera. Las dos primeras meten un criterio de reparto dentro
de una decisión que debe tomar un humano, y eso es exactamente lo que este agente
no debe hacer. El agente informa del sesgo; el resource manager decide qué hacer
con él.
