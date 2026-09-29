## Qué cambia y por qué

<!-- Dos frases. Si necesitas más, probablemente el PR es demasiado grande. -->

## Spec y criterios que implementa

- Spec: SPEC-nnn
- Criterios: CA-nn, CA-nn

## Checklist de revisión

El revisor no marca conforme sin haber respondido las nueve. Esta misma
checklist se usa en las rondas adversariales.

- [ ] 1. ¿Cada criterio de aceptación tocado tiene test que lo referencia?
- [ ] 2. ¿Los tests fallan si rompo la implementación a propósito?
- [ ] 3. ¿Hay algún test omitido, marcado o con aserción vacía?
- [ ] 4. ¿El diff contiene algo fuera del alcance declarado en la spec?
- [ ] 5. ¿Alguna dependencia nueva existe, se mantiene y era necesaria?
- [ ] 6. ¿Se conserva la precisión decimal y el redondeo se aplica una sola vez, al final?
- [ ] 6b. ¿Numerador y denominador de la utilización excluyen exactamente los mismos días?
- [ ] 7. ¿La traza de auditoría, con versión de política, de catálogo y **origen**, se escribe en todas las ramas del código nuevo, incluida la del agente?
- [ ] 8. ¿La cobertura sube porque se cubre lógica o porque se añadió código trivial?
- [ ] 9. ¿Entiendo lo suficiente este cambio como para defenderlo ante el cliente?

> La novena no es retórica. Si la respuesta es no, el PR no se aprueba, con
> independencia de que el pipeline esté verde.

## Datos personales

- [ ] Confirmo que este PR no introduce ningún dato personal real en el repositorio de aprendizaje

## Evidencia

<!-- Pega la salida de los tests y de `aula check`. No basta con decir que funciona. -->

## Intervención de agente en este PR

- [ ] Ninguna
- [ ] Asistida (nivel N1 o N2)
- [ ] Generado por agente en rama aislada (N3)

Coste en tokens de la rama: ___
