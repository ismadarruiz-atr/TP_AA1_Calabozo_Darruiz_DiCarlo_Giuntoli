# TP Aprendizaje Automático 1

Trabajos prácticos de **Aprendizaje Automático 1**, Tecnicatura en Inteligencia Artificial (FCEIA, UNR).

**Integrantes:** Josías Calabozo · Ismael Darruiz · Sebastián Di Carlo · Sharo Giuntoli

## Contenido

| Carpeta          | Trabajo práctico                                 | Estado   |
| ---------------- | ------------------------------------------------ | -------- |
| [`TP_1/`](TP_1/) | Regresión: predicción de precios de casas        | Completo |
| [`TP_2/`](TP_2/) | Clasificación: predicción de lluvia en Australia | En curso |

Cada trabajo práctico está en su propia carpeta, con un README que explica su contenido.

## Estructura del repositorio

```
.
├── README.md
├── requirements.txt                 Dependencias de Python (TP1)
├── TP_1/                            TP de regresión (ver TP_1/README.md)
│   ├── README.md
│   ├── TP-regresion-AA1.ipynb       Notebook principal (informe completo)
│   ├── data/                        Dataset
│   ├── src/                         Implementaciones de descenso por gradiente
│   └── referencia/                  Consigna y notebooks de la cátedra
└── TP_2/                            TP de clasificación (ver TP_2/README.md)
    ├── README.md
    ├── requirements.txt             Dependencias de Python del TP2
    ├── TP-clasificacion-AA1.ipynb   Notebook principal
    ├── data/                        Dataset (weatherAUS_2026C2.csv)
    └── referencia/                  Consigna
```

## Entorno

Requiere Python 3.11 o superior (probado con 3.14). Desde la raíz del repositorio, en Git Bash:

```bash
py -3.14 -m venv .venv                 # en Linux o macOS: python3 -m venv .venv
source .venv/Scripts/activate          # en Linux o macOS: source .venv/bin/activate
pip install -r requirements.txt
```

Después se abren los notebooks con el kernel de `.venv`, desde VS Code o Jupyter.

El TP2 tiene su propio entorno, con Python 3.11, porque PyCaret no funciona en versiones más nuevas. Se arma
desde `TP_2/`, como se explica en su [README](TP_2/README.md#entorno).
