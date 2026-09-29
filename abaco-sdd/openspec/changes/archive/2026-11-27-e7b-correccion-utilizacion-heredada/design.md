## Context

Este cambio es el par del anterior. La capability heredada existe unicamente
para ser corregida aqui, dejando las dos versiones en el archivo.

## Goals / Non-Goals

**Goals:**
- Que el numero publicado sea el correcto y que quede escrito por que cambio

**Non-Goals:**
- Recalcular el historico publicado: es una decision de negocio, no tecnica

## Decisions

**Se MODIFICAN los requisitos en lugar de eliminar la capability.**
Asi el archivo conserva que el defecto existio, desde cuando y con que efecto.
Si se borrase, dentro de un ano el 113% no tendria explicacion.

**El aviso precede al despliegue.**
Alternativa descartada: desplegar y explicar despues. Se descarto porque el
primer cuadro de mando con el numero nuevo genera una conversacion que conviene
tener antes y con datos, no despues y a la defensiva.

## Risks / Trade-offs

Riesgo principal: que se lea como un empeoramiento del area. Se mitiga
publicando el desglose que compone el numero nuevo junto al agregado, y el
detalle de las cuatro causas de la diferencia.
