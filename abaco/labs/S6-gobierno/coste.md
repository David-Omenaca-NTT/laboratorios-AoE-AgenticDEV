# Coste por unidad de resultado

| Concepto | Valor |
|----------|-------|
| Coste en tokens de la rama (S2 a S6) | 3,10 USD |
| Propuestas de staffing verificadas | 15 |
| **Coste por propuesta verificada** | **0,21 USD** |
| Coste por ejecución del agente | 0,00 USD (núcleo determinista) |
| Latencia media por propuesta | 13 ms |

## Por qué el agente cuesta cero

El núcleo es determinista: filtros, disponibilidad, categoría y aritmética de
ocupación se calculan sin modelo. El coste en tokens de la rama corresponde al
trabajo de desarrollo asistido, no a la ejecución del agente.

Activando el juez de modelo para redactar la explicación, el coste por ejecución
sube a unos 0,012 USD y el veredicto no cambia, porque el veredicto no lo decide
el modelo. Conclusión propia: el juez se queda desactivado por defecto.

## La cifra que se lleva a una conversación de negocio

"Hemos gastado 3,10 dólares en tokens" no significa nada. "Cada propuesta de
staffing con sus restricciones verificadas y su explicación cuesta 0,21 dólares"
se puede comparar con los 20 minutos que tarda un resource manager en hacer la
misma búsqueda a mano, y esa es la conversación de coste atribuible del AoE.
