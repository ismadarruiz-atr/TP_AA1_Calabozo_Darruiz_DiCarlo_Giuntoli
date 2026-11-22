"""Predice, a las 23:59 de cada día, si al día siguiente va a llover.

Lee un CSV con las mediciones de un día (una fila por ciudad, con las mismas columnas que el dataset del TP) y escribe
otro con dos columnas más: probabilidad_lluvia y llueve_manana ("Yes" o "No").

Uso:
    python inferencia.py dias.csv predicciones.csv
"""
import json
import sys
from pathlib import Path

# En Windows, TensorFlow tiene que importarse antes que scikit-learn (joblib.load carga scikit-learn)
import tensorflow as tf
import joblib
import numpy as np
import pandas as pd

CARPETA = Path(__file__).parent

# Lo mismo que en la sección 1.9 del notebook: la red tiene que recibir los datos preparados igual que al entrenar
CIUDADES = pd.read_csv(CARPETA / 'ciudades.csv')
RUMBOS = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
NUMERO_RUMBO = {rumbo: i + 1 for i, rumbo in enumerate(RUMBOS)}  # N = 1, ..., NNW = 16
DIRECCIONES = {'WindGustDir': 'WindGustSpeed', 'WindDir9am': 'WindSpeed9am', 'WindDir3pm': 'WindSpeed3pm'}
ASIMETRICAS = ['Rainfall', 'Evaporation']  # las de asimetría mayor a 1 en el entrenamiento


def preparar_columnas(X):
    """Agrega las coordenadas de la ciudad, pasa viento y mes a seno y coseno, y aplica logaritmo a las asimétricas."""
    # Left join por ciudad: cada fila conserva su índice y suma Latitud y Longitud
    X = X.join(CIUDADES.set_index('Location'), on='Location', how='left')
    for direccion, velocidad in DIRECCIONES.items():
        angulo = 2 * np.pi * X[direccion].map(NUMERO_RUMBO) / 16
        X[direccion + '_sin'] = np.sin(angulo)
        X[direccion + '_cos'] = np.cos(angulo)
        # Sin viento no hay dirección: el seno y el coseno quedan en 0
        X.loc[X[velocidad] == 0, [direccion + '_sin', direccion + '_cos']] = 0
    angulo_mes = 2 * np.pi * X['Date'].dt.month / 12
    X['Mes_sin'] = np.sin(angulo_mes)
    X['Mes_cos'] = np.cos(angulo_mes)
    X[ASIMETRICAS] = np.log1p(X[ASIMETRICAS])
    return X.drop(columns=list(DIRECCIONES) + ['Date', 'Location'])


def main(entrada, salida):
    """Predice la lluvia del día siguiente para cada fila de entrada y la guarda en salida."""
    # Lo que aprendió el entrenamiento: el preprocesador ajustado, la red y el umbral elegido en validación
    preprocesador = joblib.load(CARPETA / 'preprocesador.joblib')
    red = tf.keras.models.load_model(CARPETA / 'red.keras')
    umbral = json.loads((CARPETA / 'umbral.json').read_text())['umbral']

    dias = pd.read_csv(entrada)

    X = dias.copy()
    try:
        X['Date'] = pd.to_datetime(X['Date'])
        # Mismas columnas y en el mismo orden que al entrenar; las que sobran quedan afuera
        X = preparar_columnas(X)[list(preprocesador.feature_names_in_)]
    except KeyError as error:
        sys.exit(f'Error: a {entrada} le falta una columna: {error}')

    # Una ciudad que no está en ciudades.csv queda sin coordenadas, y el imputador se las inventaría
    desconocidas = sorted(set(dias.loc[X['Latitud'].isna(), 'Location'].astype(str)))
    if desconocidas:
        sys.exit(f'Error: estas ciudades no están en ciudades.csv: {", ".join(desconocidas)}')

    # transform y predict, nunca fit: lo aprendido viene en los archivos
    prob = red.predict(preprocesador.transform(X), verbose=0).ravel()

    dias['probabilidad_lluvia'] = prob.round(3)
    dias['llueve_manana'] = np.where(prob >= umbral, 'Yes', 'No')
    dias.to_csv(salida, index=False)
    print(f'{len(dias)} días predichos en {salida}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Uso: python inferencia.py <dias.csv> <predicciones.csv>')
    main(sys.argv[1], sys.argv[2])
