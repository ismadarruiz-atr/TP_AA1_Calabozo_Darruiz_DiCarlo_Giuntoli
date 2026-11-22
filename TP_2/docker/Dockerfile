# La misma versión de Python con la que se entrenó; la variante slim trae solo lo básico
FROM python:3.11-slim

# Sin los mensajes informativos que TensorFlow muestra al arrancar
ENV TF_CPP_MIN_LOG_LEVEL=2

WORKDIR /app

# Primero las librerías: si después cambia el código o el modelo, Docker reutiliza esta capa y no las reinstala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# El script, lo que aprendió el entrenamiento y las coordenadas de cada ciudad
COPY inferencia.py preprocesador.joblib red.keras umbral.json ciudades.csv ./

# Al correr el contenedor se ejecuta el script; lo que se pase a docker run son sus argumentos
ENTRYPOINT ["python", "inferencia.py"]
