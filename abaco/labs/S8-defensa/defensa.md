# Guion de defensa ante panel

20 minutos, más 15 de preguntas. El panel incluye al dueño funcional de la
herramienta, que la va a usar de verdad.

| # | Apartado | Min | Contenido |
|---|----------|-----|-----------|
| 1 | El problema | 2 | Qué resuelve Ábaco y por qué el número tiene que ser exacto |
| 2 | El recorte de alcance | 3 | Por qué 10 módulos parciales del PRD y no 18, y por qué un **monolito modular** y no microservicios |
| 3 | La spec | 2 | SPEC-002, las dos ambigüedades que encontré y cómo las resolví |
| 4 | La arquitectura | 2 | Dominio, políticas versionadas, categoría como pivote, auditoría con origen |
| 5 | El agente y sus métricas | 4 | De 43 violaciones y 0,154 de utilidad en v0 a 0 violaciones y 1,0 en la final |
| 6 | Gobierno | 3 | Por qué N2 permanente, manifiesto con contestación y veto, gate que rechaza N4 |
| 7 | Concentración | 2 | El hallazgo: más seguro y más útil, y a la vez más concentrado |
| 8 | Lo que hoy haría distinto | 2 | Ver abajo |

## Lámina 2: por qué este recorte

El PRD pedía 18 módulos, microservicios, Kafka y CQRS. He entregado 10 módulos
parciales y un monolito modular con un almacén relacional.

El argumento en una frase: un junior que monta siete microservicios y un bus de
eventos para un dominio que cabe en un monolito ha aprendido sobreingeniería, que
es el fallo más caro del perfil junior en cliente. La arquitectura se justifica
por la restricción real, no por lo que pone en el documento.

Lo que sí conservé del PRD son las piezas que tenían reglas duras y superficie de
auditoría, que es donde está la dificultad real.

## Lámina 8: la decisión que hoy tomaría distinta

Construí la verificación independiente del agente con una dedicación fija del
100% en lugar de la que pedía cada demanda. Durante dos iteraciones estuve
persiguiendo tres violaciones de sobreasignación que el agente no había cometido:
las producía mi propio verificador.

La lección no es el bug. Es que **el verificador tiene que usar exactamente los
mismos parámetros que lo verificado**, y que estuve a punto de "arreglar" un
agente que estaba bien. Si hubiera tocado el agente para hacer callar al
verificador, habría roto algo que funcionaba para satisfacer a algo que estaba
mal.
