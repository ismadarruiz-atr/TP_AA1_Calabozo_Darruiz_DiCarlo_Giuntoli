# Predicción de lluvia con Docker

Imagen que recibe un CSV con las mediciones de un día en una o más ciudades y devuelve, para cada fila, la
probabilidad de que llueva al día siguiente y la predicción. Usa la red con Optuna del ítem 7 del notebook, el mejor
modelo del ítem 8.

## Contenido

- `inferencia.py`: prepara los datos igual que el notebook, aplica el preprocesador y la red, y compara la
  probabilidad con el umbral. No entrena nada.
- `preprocesador.joblib`: el escalado, la imputación con KNN y el one-hot de `RainToday`, ajustados con el
  entrenamiento.
- `red.keras`: la red entrenada.
- `umbral.json`: el umbral de decisión, elegido en validación.
- `ciudades.csv`: la latitud y la longitud de cada ciudad.
- `requirements.txt`: las librerías para predecir, con las mismas versiones del entrenamiento.
- `Dockerfile`: cómo se arma la imagen.
- `dias_ejemplo.csv`: 10 días del conjunto de prueba, para probar la imagen.

Los binarios, `ciudades.csv` y `dias_ejemplo.csv` los genera la sección 9 del notebook.

## Construir la imagen

Con Docker abierto, desde esta carpeta:

```bash
docker build -t lluvia-australia .
```

La primera vez tarda varios minutos, porque descarga Python y TensorFlow.

## Correr la inferencia

El contenedor solo ve las carpetas que se le montan. Se monta la carpeta actual como `/datos` y se le pasan la
entrada y la salida con esa ruta. En Linux o macOS:

```bash
docker run --rm -v "$(pwd)":/datos lluvia-australia /datos/dias_ejemplo.csv /datos/predicciones.csv
```

En Windows, con Git Bash, hay que agregar `MSYS_NO_PATHCONV=1` adelante, porque si no Git Bash cambia las rutas que
empiezan con `/`:

```bash
MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd)":/datos lluvia-australia /datos/dias_ejemplo.csv /datos/predicciones.csv
```

Y con PowerShell:

```powershell
docker run --rm -v "${PWD}:/datos" lluvia-australia /datos/dias_ejemplo.csv /datos/predicciones.csv
```

Imprime `10 días predichos en /datos/predicciones.csv` y deja `predicciones.csv` en esta carpeta. `--rm` borra el
contenedor al terminar. Para `dias_ejemplo.csv`, las probabilidades y las predicciones tienen que ser las de la última
tabla del notebook.

## Formato de entrada y salida

Entrada: un CSV con una fila por ciudad y por día, con las columnas del dataset: `Date` (AAAA-MM-DD), `Location`,
`MinTemp`, `MaxTemp`, `Rainfall`, `Evaporation`, `Sunshine`, `WindGustDir`, `WindGustSpeed`, `WindDir9am`,
`WindDir3pm`, `WindSpeed9am`, `WindSpeed3pm`, `Humidity9am`, `Humidity3pm`, `Pressure9am`, `Pressure3pm`,
`Cloud9am`, `Cloud3pm`, `Temp9am`, `Temp3pm` y `RainToday`. Las celdas vacías se imputan con lo aprendido en el
entrenamiento. Las columnas que sobran no se usan y pasan tal cual a la salida. Si falta una columna, o si una ciudad
no está en `ciudades.csv`, el script termina con un error que dice cuál.

Salida: el mismo CSV con dos columnas más: `probabilidad_lluvia`, redondeada a tres decimales, y `llueve_manana`, que
es `Yes` si la probabilidad llega al umbral y `No` si no.
