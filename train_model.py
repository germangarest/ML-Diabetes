import numpy as np
import pandas as pd
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split

# Función para cargar y preparar los datos
def load_and_prepare_data(file_path):
    # Cargar el dataset
    diabetes = pd.read_csv(file_path)
    
    # Eliminar duplicados
    diabetes = diabetes.drop_duplicates()
    
    # Crear la variable PreExistingConditions
    diabetes['PreExistingConditions'] = diabetes[['HighBP', 'HighChol', 'HeartDiseaseorAttack', 'Stroke']].sum(axis=1)
    
    # Convertir Diabetes_012 en binario (0: no diabetes, 1: prediabetes o diabetes)
    diabetes['Diabetes_01'] = diabetes['Diabetes_012'].replace(2, 1)
    
    # Eliminar columnas originales que ya no son necesarias
    diabetes.drop(columns=['HighBP', 'HighChol', 'HeartDiseaseorAttack', 'Stroke', 'Diabetes_012'], inplace=True)
    
    # Mezclar los datos
    diabetes = diabetes.sample(frac=1, random_state=42).reset_index(drop=True)
    
    return diabetes

# Función para entrenar el modelo XGBoost
def train_xgboost_model(X_train, y_train):
    # Definir el modelo de XGBoost con parámetros optimizados
    xgb_model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=3,
        learning_rate=0.1,
        eval_metric='logloss',
        random_state=42,
        n_jobs=-1
    )
    
    # Entrenar el modelo
    print("Entrenando el modelo de XGBoost...")
    xgb_model.fit(X_train, y_train)
    print("Modelo de XGBoost entrenado exitosamente.")
    
    return xgb_model

# Función principal
def main():
    # Cargar y preparar los datos
    file_path = 'Diabetes_dataset_1_2.csv'
    diabetes = load_and_prepare_data(file_path)
    
    # Definir un orden específico para las columnas (este es el orden que esperará el modelo)
    expected_features_order = [
        'CholCheck', 'BMI', 'Smoker', 'PhysActivity', 'Fruits', 'Veggies', 
        'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'GenHlth', 
        'MentHlth', 'PhysHlth', 'DiffWalk', 'Sex', 'Age', 'Education', 
        'Income', 'PreExistingConditions'
    ]
    
    # Asegurarse de que todas las columnas esperadas estén presentes
    for column in expected_features_order:
        if column not in diabetes.columns:
            print(f"Error: La columna {column} no está presente en el dataset")
            return
    
    # Separar la matriz de características (X) y la variable objetivo (y)
    X = diabetes[expected_features_order]  # Usar solo las columnas en el orden esperado
    y = diabetes['Diabetes_01']
    
    # División en conjunto de entrenamiento y conjunto de prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Entrenar el modelo
    xgb_model = train_xgboost_model(X_train, y_train)
    
    # Calcular medianas para los valores por defecto
    columns_to_use = [
        'Smoker', 'PhysActivity', 'Fruits', 'Veggies', 'HvyAlcoholConsump',
        'AnyHealthcare', 'NoDocbcCost', 'MentHlth', 'PhysHlth', 'Sex',
        'Age', 'Education', 'Income', 'CholCheck'
    ]
    median_values = diabetes[columns_to_use].median().to_dict()
    
    # Guardar el modelo y las medianas
    import os
    os.makedirs('models', exist_ok=True)
    joblib.dump(xgb_model, 'models/diabetes_xgb_model.pkl')
    joblib.dump(median_values, 'models/median_values.pkl')
    
    print("Modelo y valores medianos guardados exitosamente.")
    
    # Guardar el orden de las características
    with open('models/expected_features_order.txt', 'w') as f:
        f.write(','.join(expected_features_order))
    
    print("Orden de características guardado exitosamente.")

if __name__ == "__main__":
    main()