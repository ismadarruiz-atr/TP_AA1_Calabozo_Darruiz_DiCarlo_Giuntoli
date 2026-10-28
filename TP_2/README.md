# TP 2 — Clasificación: predicción de lluvia en Australia

Trabajo práctico de **Aprendizaje Automático 1**, Tecnicatura en Inteligencia Artificial (FCEIA, UNR).

**Integrantes:** Josías Calabozo · Ismael Darruiz · Sebastián Di Carlo · Sharo Giuntoli

Predicción, a las 23:59 de cada día, de si al día siguiente va a llover (`RainTomorrow`), a partir de las
mediciones climáticas de ese día en 49 ciudades de Australia. Todo el desarrollo está en
[`TP-clasificacion-AA1.ipynb`](TP-clasificacion-AA1.ipynb), con los mismos ítems de la
[consigna](referencia/consigna-TP2.pdf).

## Avance

| Ítem | Contenido | Entrega | Estado |
|---|---|---|---|
| 1 | Análisis descriptivo y preparación de los datos | 30/10 | Hecho |
| 2 | Regresión logística: métricas, curva ROC y umbral | 30/10 | Hecho |
| 3 | Modelos base | 30/10 | Hecho |
| 4 | Optimización de hiperparámetros | 13/11 | Pendiente |
| 5 | Explicabilidad | 13/11 | Pendiente |
| 6 | AutoML con PyCaret | 13/11 | Pendiente |
| 7 | Red neuronal | 27/11 | Pendiente |
| 8 | Comparación de modelos | 27/11 | Pendiente |
| 9 | MLOps con Docker | 27/11 | Pendiente |
| 10 | Conclusión | 27/11 | Pendiente |

## Decisiones que valen para todo el TP

- **División por fecha**, porque los datos están ordenados en el tiempo: entrenamiento hasta junio de 2015,
  validación de julio de 2015 a junio de 2016 y prueba de julio de 2016 a junio de 2017. La validación se usa
  para decidir y la prueba, solo para medir el resultado final de cada modelo.
- `RainfallTomorrow` se descarta porque es información del día siguiente (fuga de datos).
- **Preparación de los datos** (sección 1.8 del notebook, siguiendo el apunte de la Unidad 0):
  - Con pandas, igual en los tres conjuntos, porque son fórmulas fijas: codificación cíclica (seno y coseno) de
    las direcciones del viento y del mes, y logaritmo de las variables con asimetría mayor a 1 (`Rainfall` y
    `Evaporation`).
  - En el `ColumnTransformer` `preprocesador`, ajustado solo con entrenamiento: `StandardScaler` y `KNNImputer`
    (k = 5) para las numéricas, y moda y one-hot para `Location` (con todas sus columnas, por si aparece una
    ciudad nueva) y `RainToday` (una sola columna 0/1). Se ajusta una sola vez, porque KNN tarda varios
    minutos (se guarda en `data/preprocesado.joblib`), y los modelos se entrenan con los datos ya
    transformados.
- **Modelo:** regresión logística con `class_weight='balanced'`.
- **Métrica principal: F1 de la clase "llueve".** El umbral de decisión se elige en validación, donde se cruzan
  la precisión y el recall.

Para el ítem 9: la codificación cíclica y el logaritmo se hacen con pandas, así que el script de inferencia tiene
que repetirlos antes de usar `preprocesador` y el modelo. Lo que se aprende de los datos ya está en
`preprocesador`. El umbral de decisión también hay que guardarlo.

## Entorno

El TP2 usa su propio entorno, distinto del de la raíz del repositorio, porque tiene que servir para todos los
ítems en un mismo notebook:

- PyCaret 3.3.2, la última versión, solo funciona con Python 3.9 a 3.11, y fija versiones viejas de numpy,
  pandas y scikit-learn (1.4.2).
- TensorFlow no tiene versión para Python 3.14.
- SHAP 0.49.1 es la última versión compatible con esas versiones de numpy.

Por eso usa **Python 3.11** (de python.org) y las versiones de [`requirements.txt`](requirements.txt). Desde
`TP_2/`, en Git Bash:

```bash
py -3.11 -m venv .venv                 # en Linux o macOS: python3.11 -m venv .venv
source .venv/Scripts/activate          # en Linux o macOS: source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name aa1-tp2 --display-name "Python 3.11 (AA1 TP2)"
```

La última línea registra el entorno como kernel de Jupyter. El notebook lo pide por ese nombre, y en VS Code
aparece en **Select Kernel → Jupyter Kernel…**, aunque la carpeta abierta no sea `TP_2/`.

El entorno ocupa unos 2.6 GB, sobre todo por TensorFlow. Si falta Python 3.11, en Windows se instala con
`winget install Python.Python.3.11`.

En Windows, TensorFlow tiene que importarse antes que scikit-learn. scikit-learn 1.4.2 trae su propia copia de
una biblioteca de Visual C++ (`msvcp140.dll`), más vieja que la que necesita TensorFlow 2.21: si se carga
primero, TensorFlow falla con `DLL load failed`. Por eso, cuando se use la red neuronal (ítem 7),
`import tensorflow` va al principio de la celda de configuración.

## Cómo ejecutar

Abrir el notebook con el kernel **Python 3.11 (AA1 TP2)**. Lee `data/weatherAUS_2026C2.csv` con una ruta relativa, así que
necesita que la carpeta de trabajo sea `TP_2/`, algo que Jupyter y VS Code hacen solos.

La primera ejecución tarda unos 15 minutos, casi todo por `KNNImputer`. El preprocesador ajustado y los datos
preparados se guardan en `data/preprocesado.joblib`, que no se versiona, y las ejecuciones siguientes los cargan
de ahí y tardan menos de un minuto. **Si se cambia algo de la preparación de los datos (sección 1.8 o
anteriores), hay que borrar ese archivo** para que se vuelva a calcular.

## Estructura

```
TP_2/
├── README.md
├── requirements.txt                Dependencias de Python del TP2
├── TP-clasificacion-AA1.ipynb      Notebook con todo el desarrollo
├── data/
│   ├── weatherAUS_2026C2.csv       Dataset
│   └── preprocesado.joblib         Datos preparados que guarda el notebook (no se versiona)
└── referencia/
    └── consigna-TP2.pdf            Consigna
```
