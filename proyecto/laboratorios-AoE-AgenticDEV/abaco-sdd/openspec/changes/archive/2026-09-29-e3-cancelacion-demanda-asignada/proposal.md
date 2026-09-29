## Why

Operaciones ha planteado un caso que el ciclo actual no cubre: cuando un cliente
cancela el proyecto entero, quedan demandas en estado asignada que hoy solo se
pueden cerrar, y cerrarlas da a entender que se cubrieron. El dato de cobertura
del area sale falseado hacia arriba.

## What Changes

Se permite cancelar una demanda asignada, pero solo con motivo declarado y
dejando constancia de que las asignaciones vinculadas quedan sin demanda que las
justifique. El requisito que lo prohibia se modifica en lugar de eliminarse.

## Capabilities

### New Capabilities

### Modified Capabilities
- `demanda`: el requisito de transiciones permitidas pasa a admitir la cancelacion desde asignada bajo condicion, y se anade un requisito de motivo obligatorio

## Impact

Cambia el calculo de cobertura del area: demandas que antes se cerraban ahora se
cancelan y dejan de contar como cubiertas. Hay que avisar a quien lee el cuadro
de mando antes de desplegarlo.
