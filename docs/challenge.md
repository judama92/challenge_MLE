# Análisis de datos inicial

Los gráficos de distribución de los datos se **optimizaron para una mejor compresión**, por ejemplo en algunos casos se ordenó los resultados de mayor a menor para ver las cantidades de vuelos por por aerolinea, cantidad de vuelos por destino, etc.

Se obvió la **función sns.set() que está obsoleta**, en su lugar **me enfoqué a ordenar los resultados** y utilizar colores que permitan visualizar de mejor manera los gráficos.


# Generación de features

### Función get_period_day
Se identificó que la función **get_period_day no consideraba las horas de los rangos**, por ejemplo, cuando se validaba si la hora es mayor a 05:00, si por casualidad se evaluaba una hora 05:00 no entraba en la condición y asinaba como valor None.
Este problema se solucionó agregando a las condiciones "mayor o igual" o "menor o igual" para que las condiciones consideren las horas los extremos de los rangos horarios.

### Función is_high_season
Tal y como estaba implementada la función, **no asignaba el valor de 1 a las fechas del 31-Dec**, se tuvo que hacer una reingeniería de la función.
La solución que propongo es validar las fechas en base a rangos de fecha, por ejemplo, un rango es ((12, 15), (12, 31)) esto permitirá validar si una fecha se encuentra entre el 15-Dic y el 31-Dic.

# Análisis posterior de los datos

**Se ordenaron los datos de los gráficos** para un mejor entendimiento de las tendencias de los datos, por ejemplo para el mostrar el resultado del Delay rate by destination se ordenaron los datos por paises de mayor a menos para visualizar los paises donde con mayor frecuencia ocurren los Delays.

Suponiendo que este sería un trabajo real, sugeriría que se preste mucha atención al proceso de validación de las variables calculadas porque habían muchos registros que no se clasificaban, por ejemplo, al calcular el periodo al cual pertenecen los registros como "mañana", "tarde" y "noche", algunos registros no entraban en ninguna condición, esto podría inducir al error al entrenar el modelo con datos sesgados y obtener modelos de no tanto provecho para el negocio.

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

# Ejecución de Pruebas

Las pruebas fueron claves para validar que las funcionalidades desarrolladas cumplan con su objetivo contemplando distintos escenarios previo a su despliegue a producción.

**Las pruebas del modelo, api y stress fueron satisfactorias**, cumpliendo con los estándares de calidad exigas en esta prueba.

# Integración y Entrega continua

### Integración Continua

Para el proceso de Integración continua, consideré la validación del código que el científico quiere guardar en alguna rama, para esto me apoyé de los **procesos de pruebas unitarias (tests)**. A través de la **implementación de un proceso automático**, cada vez que el científico pase a otra rama su código fuente, **se activarán los test de model y api**.

Con esto **garantizamos que el código fuente cumpla con los requisitos mínimos de calidad** que se requiere para migrar el código.

**Sugiero que para un proceso productivo o real**, se implementen pruebas de validación del código en cuestión de formato, sintaxis, identación, **buenas practicas de desarrollo**, etc. **Dependiendo de las políticas actuales de la empresa** en cuestión de como deben estar los entregables se puede hace uso de herramientas que nos ayude a validar todo el set de buenas prácticas que los científicos deben cumplir.
**Esto permite que se tenga un código bajo un estándar y patrones de diseño** que todo el equipo tenga conoce y sea más sencillo interpretar y entender el objetivo de lo desarrollado.

Si en la empresa existe un equipo de Data Quality Assurance con muchas más facilidad el equipo de desarrollo tendrá a su alcance material para realizar un mejor trabajo y entregar **desarrollos de alta calidad y sobre todo facilitar el mantenimiento del código** para futuros upgrates de los desarrollos.

### Entrega Continua

**Actualmente una de las nubes con la que mas vengo trabajando es GCP**, para el proceso de entrega continua consideré dos servicios que permiten disponer de modelos como servicio, **Artifac Registry y Cloud Run**.
A través de **un proceso automático se construye la imagen Docker** y se **despliega** dicha imagen en el componente **Artifact Registry de GCP**, de esta manera en GCP **versionamos las imagenes de los modelos** y los tenemos en un entorno seguro y de fácil integración con otros componentes para su exposición como servicio.

**Implementé un proceso automático** que permite desplegar en Cloud Run un contenedor con la imagen Docker que previamente se registró en Artifact Registry, **con esto logramos exponer el modelo como un servicio**, listo para su consumo desde otros sistemas.
Configuré el servicio de contenedores de Cloud Run con los recursos mínimos dado que esto es un proceso de prueba. **Sin embargo para un caso productivo, se debe calcular el sizing requerido para el consumo del modelo.**

Para no tener inconvenientes con las versiones de las librerías de Python, **planteo que se implemente una gestión de imagenes Docker** para los distintos casos de uso que el equipo de científicos aborda en su día a día. Entiendo que hay diferentes frameworks que permite a los científicos construir distintos modelos, mi objetivo es mantener un inventario y set de librerías **que permita una mejor gestión en los depliegues de los modelos.** 

**A nivel de configuración sugiero tener cuidado con las claves** de las cuentas de servicio en el IAM que permiten la conexión entre los servicios de GCP. **Como buena práctica siempre es mejor manejar estos accesos a través de Secrets** para prevenir vulnerabilidades como hackeos.

**Sugiero también que si se va a manejar información confidencial de los clientes,** plantear desde el inicio junto con el equipo de **Ciberseguridad** de la empresa una arquitectura tecnológica que permita **mantener esos datos de forma segura en nube**, por ejemplo podemos manejar **llaves de encriptación con KMS**, hacer uso de **canales seguros de transferencia de datos via VPN** y de ser el caso implementar una VPC para tener un acceso restringido a los proyectos en GCP desde la red de la empresa. **Con esto evitamos robo de información** y vulnerabilidades de externos.

