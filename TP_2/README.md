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
| 1 | Análisis descriptivo y preparación de los datos | 30/10 | Pendiente |
| 2 | Regresión logística: métricas, curva ROC y umbral | 30/10 | Pendiente |
| 3 | Modelos base | 30/10 | Pendiente |
| 4 | Optimización de hiperparámetros | 13/11 | Pendiente |
| 5 | Explicabilidad | 13/11 | Pendiente |
| 6 | AutoML con PyCaret | 13/11 | Pendiente |
| 7 | Red neuronal | 27/11 | Pendiente |
| 8 | Comparación de modelos | 27/11 | Pendiente |
| 9 | MLOps con Docker | 27/11 | Pendiente |
| 10 | Conclusión | 27/11 | Pendiente |

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
```

El entorno ocupa unos 2.6 GB, sobre todo por TensorFlow. Si falta Python 3.11, en Windows se instala con
`winget install Python.Python.3.11`.

En Windows, TensorFlow tiene que importarse antes que scikit-learn. scikit-learn 1.4.2 trae su propia copia de
una biblioteca de Visual C++ (`msvcp140.dll`), más vieja que la que necesita TensorFlow 2.21: si se carga
primero, TensorFlow falla con `DLL load failed`. Por eso, cuando se use la red neuronal (ítem 7),
`import tensorflow` va al principio de la celda de configuración.

## Cómo ejecutar

Abrir el notebook con el kernel de `TP_2/.venv`. Lee `data/weatherAUS_2026C2.csv` con una ruta relativa, así que
necesita que la carpeta de trabajo sea `TP_2/`, algo que Jupyter y VS Code hacen solos.

## Estructura

```
TP_2/
├── README.md
├── requirements.txt                Dependencias de Python del TP2
├── TP-clasificacion-AA1.ipynb      Notebook con todo el desarrollo
├── data/
│   └── weatherAUS_2026C2.csv       Dataset
└── referencia/
    └── consigna-TP2.pdf            Consigna
```
