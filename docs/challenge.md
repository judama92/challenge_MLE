## Optimización en el análisis de datos inicial

Los gráficos de distribución de los datos se optimizaron para una mejor compresión, por ejemplo en algunos casos se ordenó los resultados de mayor a menor para ver las cantidades de vuelos por por aerolinea, cantidad de vuelos por destino, etc.

Se obvió la función sns.set() que está obsoleta, en su lugar me enfoqué a ordenar los resultados y utilizar colores que permitan visualizar de mejor manera los gráficos.


## Optimización en la generación de features

### Función get_period_day
Se identificó que la función get_period_day no consideraba las horas de los rangos, por ejemplo, cuando se validaba si la hora es mayor a 05:00, si por casualidad se evaluaba una hora 05:00 no entraba en la condición y asinaba como valor None.
Este problema se solucionó agregando a las condiciones "mayor o igual" o "menor o igual" para que las condiciones consideren las horas los extremos de los rangos horarios.

### Función is_high_season
Tal y como estaba implementada la función, no asignaba el valor de 1 a las fechas del 31-Dec, se tuvo que hacer una reingeniería de la función.
La solución que propongo es validar las fechas en base a rangos de fecha, por ejemplo, un rango es ((12, 15), (12, 31)) esto permitirá validar si una fecha se encuentra entre el 15-Dic y el 31-Dic.

## Optimización en el análisis posterior de los datos

Se ordenaron los datos de los gráficos para un mejor entendimiento de las tendencias de los datos, por ejemplo para el mostrar el resultado del Delay rate by destination se ordenaron los datos por paises de mayor a menos para visualizar los paises donde con mayor frecuencia ocurren los Delays.
