# S0. Bootstrap y disciplina de repositorio

| | |
|---|---|
| Semana | 1 |
| Horas estimadas | 8 |
| Modulos del itinerario | 1 |

## Objetivo

Dejar el repositorio de aprendizaje en condiciones de recibir trabajo de agentes, y entender por que el repositorio de producto es otro.

## Por que esta estacion existe

Aqui hay dos repositorios y la diferencia importa. En el de aprendizaje rompes lo que quieras con datos sinteticos. En el de producto hay datos reales de tus companeros y se entra por estacion sellada. El limite de 400 lineas de diff por PR te parecera arbitrario esta semana y lo entenderas en la semana 8.

## Aviso

> Ni un solo dato personal real entra en este repositorio. Ni en un test, ni en un issue, ni en un mensaje de commit, ni en un prompt. Hay un verificador que lo comprueba y salta en el pipeline.

## Que tienes que conseguir

1. Crea tu repositorio de aprendizaje a partir de la plantilla y clona en local.
2. Protege la rama principal: revision obligatoria y pipeline en verde para mergear.
3. Anade CODEOWNERS marcando labs/, manifiestos/ y .github/ como protegidas.
4. Anade la plantilla de PR con la checklist de diez puntos.
5. Configura conventional commits y el gate de tamano de PR.
6. Lee la seccion de datos personales del contrato de contexto y firma el compromiso de no copiar datos reales al repositorio de aprendizaje.
7. Abre un PR propio y revisa el de otro miembro de tu escuadra.

Esta guia dice que conseguir, no como. Si pudieras seguirla sin pensar, no
aprenderias nada que sirva cuando cambie el contexto, que es lo que pasa en
cliente el primer dia.

## Entregable

Dos PRs mergeados, uno propio y uno revisado, ambos con la checklist rellena, y el compromiso de datos firmado.

## Como se cierra

```bash
abaco check S0 --prediccion pasa   # declara antes si crees que vas a pasar
abaco cerrar S0                    # sella la estacion y libera la referencia
```

Si te atascas: `abaco pista S0`. Si se agota la ventana,
`abaco desbloquear S0 --motivo "..."` te da la referencia como linea base y
te deja continuar. No penaliza las estaciones siguientes.

Criterios de superacion en CRITERIOS.md.
