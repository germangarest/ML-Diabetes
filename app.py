import os
import numpy as np
import pandas as pd
import joblib
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, session

# Cargar el modelo y los valores medianos globalmente
model = None
median_values = None
expected_features_order = None

# Crear la aplicación Flask
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Cargar el modelo al inicio
def load_model_and_data():
    global model, median_values, expected_features_order
    try:
        model = joblib.load('models/diabetes_xgb_model.pkl')
        median_values = joblib.load('models/median_values.pkl')
        
        # Definir el orden esperado de las características
        expected_features_order = [
            'CholCheck', 'BMI', 'Smoker', 'PhysActivity', 'Fruits', 'Veggies', 
            'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'GenHlth', 
            'MentHlth', 'PhysHlth', 'DiffWalk', 'Sex', 'Age', 'Education', 
            'Income', 'PreExistingConditions'
        ]
        
        print("Modelo y valores medianos cargados exitosamente.")
    except Exception as e:
        print(f"Error al cargar el modelo o los valores medianos: {e}")

# Cargar el modelo al inicio de la aplicación
load_model_and_data()

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plan-prevencion')
def plan_prevencion():
    return render_template('plan_prevencion.html')

@app.route('/consejos-alimentacion')
def consejos_alimentacion():
    return render_template('consejos_alimentacion.html')

# Función para obtener la categoría de IMC
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Bajo peso"
    elif bmi < 25:
        return "Peso normal"
    elif bmi < 30:
        return "Sobrepeso"
    else:
        return "Obesidad"

# Función para obtener consejos de salud personalizados
def get_health_advice(prediction, probability, bmi, gen_hlth, pre_existing_conditions):
    advice = []
    
    # Consejos basados en la predicción
    if prediction == 1:
        advice.append("Consulta con un médico especialista para evaluar tu riesgo de diabetes.")
        advice.append("Considera realizarte pruebas de glucosa en sangre para un diagnóstico preciso.")
    
    # Consejos basados en el IMC
    if bmi >= 25:
        advice.append("Intenta reducir tu IMC mediante una dieta equilibrada y ejercicio regular.")
    
    # Consejos basados en salud general
    if gen_hlth >= 3:
        advice.append("Trabaja en mejorar tu salud general a través de hábitos saludables.")
    
    # Consejos basados en condiciones previas
    if pre_existing_conditions > 0:
        advice.append("Mantén un control regular de tus condiciones de salud preexistentes.")
    
    # Consejos generales
    advice.append("Mantén una dieta equilibrada rica en frutas, verduras y granos integrales.")
    advice.append("Realiza al menos 150 minutos de actividad física moderada cada semana.")
    advice.append("Limita el consumo de alcohol y evita el tabaco.")
    
    return advice

# Función para evaluar factores de riesgo
def get_risk_factors(pre_existing_conditions, gen_hlth, bmi, age, diff_walk):
    risk_factors = []
    
    if pre_existing_conditions > 0:
        risk_factors.append(("Condiciones preexistentes", "Alto" if pre_existing_conditions > 2 else "Moderado"))
    
    if gen_hlth > 3:
        risk_factors.append(("Salud general", "Alto" if gen_hlth > 4 else "Moderado"))
    
    if bmi >= 25:
        risk_factors.append(("IMC", "Alto" if bmi >= 30 else "Moderado"))
    
    if age >= 7:  # Aproximadamente edad > 50
        risk_factors.append(("Edad", "Alto" if age >= 10 else "Moderado"))
    
    if diff_walk == 1:
        risk_factors.append(("Dificultad al caminar", "Alto"))
    
    return risk_factors

# Ruta para procesar la predicción
@app.route('/predict', methods=['POST'])
def predict():
    # Verificar que el modelo está cargado
    if model is None or median_values is None or expected_features_order is None:
        flash('Error: El modelo de predicción no está disponible en este momento.')
        return redirect(url_for('index'))
        
    try:
        # Obtener datos del formulario
        pre_existing_conditions = int(request.form['pre_existing_conditions'])
        gen_hlth = int(request.form['gen_hlth'])
        bmi = float(request.form['bmi'])
        age = int(request.form['age'])
        diff_walk = int(request.form['diff_walk'])
        
        # Validar entradas
        if not (0 <= pre_existing_conditions <= 4):
            flash('El número de condiciones previas debe estar entre 0 y 4')
            return redirect(url_for('index'))
        
        if not (1 <= gen_hlth <= 5):
            flash('La salud general debe estar entre 1 y 5')
            return redirect(url_for('index'))
        
        if not (10 <= bmi <= 100):
            flash('El IMC debe estar entre 10 y 100')
            return redirect(url_for('index'))
        
        if not (1 <= age <= 13):
            flash('La edad debe estar entre 1 y 13')
            return redirect(url_for('index'))
        
        if diff_walk not in [0, 1]:
            flash('La dificultad para caminar debe ser 0 o 1')
            return redirect(url_for('index'))
        
        # Crear el diccionario con todos los valores (usando medianas para los que no se solicitan)
        data = {
            'CholCheck': median_values.get('CholCheck', 0.0),
            'BMI': bmi,
            'Smoker': median_values.get('Smoker', 0.0),
            'PhysActivity': median_values.get('PhysActivity', 1.0),
            'Fruits': median_values.get('Fruits', 1.0),
            'Veggies': median_values.get('Veggies', 1.0),
            'HvyAlcoholConsump': median_values.get('HvyAlcoholConsump', 0.0),
            'AnyHealthcare': median_values.get('AnyHealthcare', 1.0),
            'NoDocbcCost': median_values.get('NoDocbcCost', 0.0),
            'GenHlth': gen_hlth,
            'MentHlth': median_values.get('MentHlth', 0.0),
            'PhysHlth': median_values.get('PhysHlth', 0.0),
            'DiffWalk': diff_walk,
            'Sex': median_values.get('Sex', 0.0),
            'Age': age,
            'Education': median_values.get('Education', 5.0),
            'Income': median_values.get('Income', 6.0),
            'PreExistingConditions': pre_existing_conditions
        }
        
        # Asegurarse de que todas las características estén presentes en el orden correcto
        input_data = pd.DataFrame([data])[expected_features_order]
        
        # Realizar la predicción
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1] * 100  # Probabilidad de clase positiva
        
        # Guardar los datos de entrada en la sesión para referencia futura
        session['input_data'] = {
            'bmi': bmi,
            'gen_hlth': gen_hlth,
            'diff_walk': diff_walk,
            'age': age,
            'pre_existing_conditions': pre_existing_conditions
        }
        
        # Preparar los resultados para la plantilla
        result = {
            'prediction': int(prediction),
            'probability': probability,
            'bmi_category': get_bmi_category(bmi),
            'health_advice': get_health_advice(prediction, probability, bmi, gen_hlth, pre_existing_conditions),
            'risk_factors': get_risk_factors(pre_existing_conditions, gen_hlth, bmi, age, diff_walk)
        }
        
        return render_template('result.html', result=result)
    
    except Exception as e:
        flash(f'Error: {str(e)}')
        return redirect(url_for('index'))

# Ruta API para evaluación rápida
@app.route('/api/evaluate', methods=['POST'])
def api_evaluate():
    # Verificar que el modelo está cargado
    if model is None or median_values is None or expected_features_order is None:
        return jsonify({'error': 'El modelo de predicción no está disponible'}), 503
        
    try:
        data = request.json
        
        # Asegurarse de que todas las características estén presentes
        for feature in expected_features_order:
            if feature not in data:
                data[feature] = median_values.get(feature, 0.0)
        
        # Crear un DataFrame con los datos y ordenar columnas
        input_data = pd.DataFrame([data])[expected_features_order]
        
        # Realizar la predicción
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1] * 100
        
        return jsonify({
            'prediction': int(prediction),
            'probability': probability,
            'risk_level': 'Alto' if probability > 70 else 'Moderado' if probability > 30 else 'Bajo',
            'bmi_category': get_bmi_category(data['BMI']) if 'BMI' in data else None
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)