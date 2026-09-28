# TP 1 — Regresión: predicción de precios de casas

Trabajo práctico de **Aprendizaje Automático 1**, Tecnicatura en Inteligencia Artificial
(FCEIA, UNR).

**Integrantes:** Josías Calabozo · Ismael Darruiz · Sebastián Di Carlo · Sharo Giuntoli

Construcción y comparación de modelos de **regresión lineal múltiple** para predecir `MEDV` (valor
mediano de las viviendas, en miles de dólares) a partir de 13 características del dataset de precios
de casas de Boston.

Todo el trabajo está en un único notebook, [`TP-regresion-AA1.ipynb`](TP-regresion-AA1.ipynb),
que funciona como informe: intercala celdas de código con bloques de texto que desarrollan el
análisis, justifican cada decisión con una métrica o un gráfico, y cierran con las conclusiones.
Las figuras están numeradas para poder referenciarlas desde el texto.

**Contenido del notebook**

1. Análisis descriptivo de las variables: rango, distribución y valores atípicos.
2. Tratamiento de los datos faltantes.
3. Relación entre las variables: correlación con el precio y entre características.
4. Preparación: división en entrenamiento y prueba (80/20), elección del imputador (mediana, media
   o `KNNImputer`) y `Pipeline` de escalado + imputación.
5. Modelado: `LinearRegression`, descenso por gradiente (batch, estocástico y mini-batch) y
   regularización (Ridge, Lasso, Elastic Net).
6. Optimización de hiperparámetros con **validación cruzada de 5 particiones** (`GridSearchCV`),
   comparación de modelos y conclusiones.

**Resultados principales**

- **Imputación:** borrando a propósito valores conocidos, `KNNImputer` los reconstruye con cerca de
  un 40 % menos de error que la mediana o la media, y el mismo experimento elige `k = 5`. Para el
  modelo, en cambio, los tres imputadores resultan equivalentes, porque los faltantes son solo el
  1.6 % de las celdas de entrenamiento.
- `LinearRegression` y los tres métodos de descenso por gradiente convergen a la misma solución,
  porque minimizan la misma función de costo convexa: sus coeficientes no se apartan más de 0.08
  entre sí. Se diferencian en la velocidad de convergencia y en la forma de las curvas de error.
- **Todos los modelos lineales resultan equivalentes** en este dataset. El mejor por validación
  cruzada es Elastic Net con `alpha = 0.1` y `l1_ratio = 0.9` (RMSE 5.925 k\$), pero la mejora sobre
  `LinearRegression` (5.955 k\$) es de 0.030 k\$ contra un desvío entre particiones de 1.2 k\$.
- El caso de **Elastic Net con `alpha = 1`**, que es el mejor en prueba (RMSE 6.47 k\$) y el peor en
  validación cruzada (6.52 k\$), ilustra por qué no hay que elegir modelos mirando el conjunto de
  prueba.

## Estructura

```
TP_1/
├── README.md
├── TP-regresion-AA1.ipynb                    Notebook principal (informe completo)
├── data/
│   └── house-prices-tp.csv                   Dataset
├── src/
│   └── descenso_gradiente.py                 Implementaciones de descenso por gradiente
└── referencia/                               Material de la cátedra (no forma parte del trabajo)
    ├── consigna-TP1.pdf                      Consigna del trabajo práctico
    ├── implementaciones-descenso-gradiente-catedra.ipynb   Notebook de descenso por gradiente
    └── imputacion-datos-catedra.ipynb        Notebook de imputación de datos
```

El módulo `src/descenso_gradiente.py` contiene las implementaciones de **Gradient Descent**,
**Stochastic Gradient Descent** y **Mini-Batch Gradient Descent** tomadas del notebook de la
cátedra, adaptadas para aceptar DataFrames de pandas y devolver el historial de error de
entrenamiento y validación, de modo que los tres métodos se puedan comparar en un mismo gráfico.

El notebook de imputación de la cátedra se usa como referencia metodológica: de ahí sale el
procedimiento de borrar valores conocidos para comparar imputadores. Para ejecutarlo hace falta
instalar `catboost`, que no está en `requirements.txt` porque el trabajo no lo usa.

## Cómo ejecutar

Primero hay que levantar el entorno como se explica en el [README principal](../README.md). Después
se abre `TP-regresion-AA1.ipynb` con el kernel de `.venv`.

El notebook lee `data/house-prices-tp.csv` e importa `src/descenso_gradiente.py` con **rutas
relativas**, así que necesita que el directorio de trabajo sea `TP_1/`. Al abrirlo con Jupyter o
VS Code esto ya ocurre solo, porque el kernel arranca en la carpeta del notebook.

Está configurado con una semilla fija (`SEMILLA = 42`) en todas las divisiones de datos, las
inicializaciones de pesos, el experimento de imputación y los gráficos con componente aleatoria, por
lo que los resultados son reproducibles: con las versiones de bibliotecas fijadas en
[`requirements.txt`](../requirements.txt), ejecutarlo de nuevo devuelve exactamente los mismos
números que figuran en el texto. Los resultados se obtuvieron con Python 3.11.9.
