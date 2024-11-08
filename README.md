# **Predicción de Diabetes con Machine Learning**

Este proyecto de Machine Learning tiene como objetivo predecir si un paciente tiene prediabetes, diabetes, o no tiene diabetes en función de diversos factores. Se emplean técnicas de clasificación con un enfoque en limpieza, análisis y visualización de datos, junto con el uso del modelo RandomForest.

---

## **Tabla de Contenidos**
- [**Introducción**](#introducción)
- [**Dataset**](#dataset)
- [**Objetivo**](#objetivo)
- [**Preparación de Datos**](#preparación-de-datos)
- [**Entrenamiento del Modelo**](#entrenamiento-del-modelo)
- [**Evaluación**](#evaluación)
- [**Conclusiones**](#conclusiones)
- [**Requisitos**](#requisitos)
- [**Ejecución**](#ejecución)

---

## **Introducción**
En este proyecto, se busca una clasificación efectiva de los tipos de diabetes, con un enfoque en los factores que permiten una distinción precisa. La clasificación se realiza utilizando el algoritmo RandomForest, adecuado para problemas de clasificación.

---

## **Dataset**
El dataset incluye variables que abarcan aspectos clínicos y demográficos de las pacientes. Estos factores se han recolectado y limpiado para maximizar la precisión y relevancia del modelo predictivo.

---

## **Objetivo**
El objetivo de este proyecto es desarrollar un modelo que pueda predecir el tipo de diabetes en pacientes (tipo 1, tipo 2 o no diabetes) y explorar qué variables tienen mayor impacto en la clasificación.

---

## **Preparación de Datos**
### **Limpieza**
- Se identificaron y gestionaron valores nulos.
- Se eliminó ruido en las variables categóricas y numéricas.
- Se realizó escalado de variables, y codificación de variables categóricas para adaptarlas al modelo.

### **Análisis Exploratorio**
Se analizaron las características del dataset para identificar patrones en los datos, con visualizaciones específicas para:
- Distribución de cada clase de diabetes.
- Correlaciones entre variables.

---

## **Entrenamiento del Modelo**
### **Selección del Modelo**
Se seleccionó el algoritmo **RandomForest** para la predicción de diabetes debido a su capacidad para manejar datasets grandes y complejos sin sobreajustarse.

### **Entrenamiento**
Se dividió el dataset en conjuntos de entrenamiento y prueba en una proporción 80-20. Se entrenó el modelo con el conjunto de entrenamiento y se validaron sus parámetros para optimizar el rendimiento.

### **Parámetros del Modelo**
- Número de árboles (n_estimators): 100
- Profundidad máxima (max_depth): sin límite
- Número de características (max_features): 'sqrt'

---

## **Evaluación**
Se utilizó el conjunto de prueba para evaluar el modelo mediante las siguientes métricas:
- **Precisión**: La tasa de predicciones correctas.
- **Recall**: Evaluación de falsos negativos.
- **F1-score**: Métrica combinada que balancea precisión y recall.

### **Resultados**
Los resultados obtenidos mostraron que el modelo tiene un alto grado de precisión y recall, lo que indica su fiabilidad en la predicción del tipo de diabetes.

---

## **Conclusiones**
Este modelo es útil en el ámbito clínico, proporcionando una herramienta adicional para la clasificación y detección de diabetes en pacientes. Las variables más significativas pueden ayudar a entender mejor los factores que influyen en la diabetes y permitir la prevención temprana.

---

## **Requisitos**
Este proyecto requiere los siguientes paquetes:
```plaintext
- pandas
- numpy
- matplotlib
- scikit-learn
