# Optimización en el análisis de datos inicial

Los gráficos de distribución de los datos se **optimizaron para una mejor compresión**, por ejemplo en algunos casos se ordenó los resultados de mayor a menor para ver las cantidades de vuelos por por aerolinea, cantidad de vuelos por destino, etc.

Se obvió la **función sns.set() que está obsoleta**, en su lugar **me enfoqué a ordenar los resultados** y utilizar colores que permitan visualizar de mejor manera los gráficos.


# Optimización en la generación de features

### Función get_period_day
Se identificó que la función **get_period_day no consideraba las horas de los rangos**, por ejemplo, cuando se validaba si la hora es mayor a 05:00, si por casualidad se evaluaba una hora 05:00 no entraba en la condición y asinaba como valor None.
Este problema se solucionó agregando a las condiciones "mayor o igual" o "menor o igual" para que las condiciones consideren las horas los extremos de los rangos horarios.

### Función is_high_season
Tal y como estaba implementada la función, **no asignaba el valor de 1 a las fechas del 31-Dec**, se tuvo que hacer una reingeniería de la función.
La solución que propongo es validar las fechas en base a rangos de fecha, por ejemplo, un rango es ((12, 15), (12, 31)) esto permitirá validar si una fecha se encuentra entre el 15-Dic y el 31-Dic.

# Optimización en el análisis posterior de los datos

**Se ordenaron los datos de los gráficos** para un mejor entendimiento de las tendencias de los datos, por ejemplo para el mostrar el resultado del Delay rate by destination se ordenaron los datos por paises de mayor a menos para visualizar los paises donde con mayor frecuencia ocurren los Delays.

# Elección del modelo Ganador

Revisé los 6 entrenamientos, los modelos entrenados con XGBoost y Regresion Logistica con el top 10 de variables y con balanceo serían los modelos ganadores, para elegir entre uno de ellos lo hice en base a los sigueintes criterios.
1. **Métricas**: Ambos modelos han obtenido un puntaje 0.69 en Recall y 0.25 de Precisión, lo cual es un indicador que se debe realizar una ventana de testeo y validación mas amplia.
2. **Simplicidad de interpretación e implementación**: Si nos enfocamos en que el modelo debe ser fácil de interpretar y desarollar, la opcion ganadora sería Regresión Logística.
3. **Capacidad de computo**: El entorno donde se vaya a ejecutar el modelo, suponiendo que se va a consultar de forma masiva el modelo y en paralelo, si elegimos XGBoost debemos considerar un entorno más dedicado que para Regresión Logística, con GPU y RAM, en cambio con Regresión podría bastar un entorno solo de CPU.
4. **Robutez y Confianza**: El agoritmo XGBoost es la mejor opción debido a esta ligeramente mejor en su mejor F1-Score y porque tienen una mejor capacidad para manejar datos desbalanceados a comparación de Regresión Logística.
5. **El valor al negocio**: Este es uno de los principale puntos a evaluar. A veces es necesario invertir para lograr mas ingresos o reducir costos. Por esta razón, viendo la necesidad del negocio en su toma de decisiones, si el proceso es realmente crítico, me inclinaría por XGBoost por su robustez y confianza, a pesar de requerir mayor capacidad de computo y sea más complejo de interpretar.

**Por las razones 1, 4 y 5 la mejor opción sería XGBoost con selección del top 10 de variables y balanceo.**


Tabla compartiva de métricas
| Modelo                                      | Precisión | Recall (Clase 1) | F1-Score |
|---------------------------------------------|-----------|------------------|----------|
| XGBoost (Todas, sin balanceo)              | 0.00      | 0.00             | 0.00     |
| XGBoost (Top 10, sin balanceo)             | 0.76      | 0.01             | 0.01     |
|**XGBoost (Top 10, con balanceo)**           | **0.25**      | **0.69**             | **0.37**     |
| Logistic Regression (Todas, sin balanceo)  | 0.56      | 0.03             | 0.06     |
| Logistic Regression (Top 10, sin balanceo) | 0.53      | 0.01             | 0.03     |
| **Logistic Regression (Top 10, con balanceo)** | **0.25**      | **0.69**             | **0.36**     |


# Creación de API local

Esta etapa fue clave para **validar en el entorno de desarrollo** la disponibilidad del **modelo como un servicio**, a través de este proceso nos preparamos para un siguiente etapa de disponiblizar el modelo en Cloud para el consumo de los usuarios o sistemas.

Entre los puntos validado, está en definir la **forma de invocar el modelo**, el formato del **input y del output del modelo**.

# Creación de API GCP

Previo al despliegue del modelo en GCP como un endpoint, **construí la imagen Docker** alineada a las caraterísticas del modelo, por ejemplo, la verisón de Python y librerías requeridas para ejecución y consumo.
Se desplegó la imagen Docker en **Artifact Registry**, para luego estar disponible como servicio desde el **servicio de Cloud Run**. 

Configuré el servicio de contenedores de Cloud Run con los recursos mínimos dado que es una especie de POC este proyecto. **Sin embargo para un caso productivo, se debe calcular el sizing requerido para el consumo del modelo.**

# Ejecución de Pruebas

Las pruebas fueron claves para validar que las funcionalidades desarrolladas cumplan con su objetivo contemplando escenarios críticos previo a su despliegue a producción.

**Las pruebas del modelo, api y stress fueron satisfactorias**, cumpliendo con los estándares de calidad exigas en esta prueba.
