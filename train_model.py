# ==========================================
# DETECTOR DE FRAUDE FINANCIERO
# Script para entrenar el modelo de IA
# ==========================================

# Importar librerías necesarias
import pandas as pd  # Para leer y manipular datos en tablas
from sklearn.model_selection import train_test_split  # Para dividir datos en entrenamiento y prueba
from sklearn.preprocessing import StandardScaler, LabelEncoder  # Para preparar los datos
from sklearn.ensemble import RandomForestClassifier  # El modelo de IA que aprenderá
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score  # Para medir qué tan bien funciona
import joblib  # Para guardar el modelo entrenado
import numpy as np  # Para matemática

print("=" * 50)
print("INICIANDO ENTRENAMIENTO DEL MODELO")
print("=" * 50)

# PASO 1: CARGAR LOS DATOS
# ========================
print("\n1. Cargando datos de transacciones...")
# Leer el archivo CSV que contiene las transacciones
datos = pd.read_csv('transactions.csv')
print(f"   ✓ Datos cargados: {len(datos)} transacciones")
print(f"   Columnas: {list(datos.columns)}")

# PASO 2: PREPARAR LOS DATOS
# ==========================
print("\n2. Preparando datos para el modelo...")

# Separar características (X) de lo que queremos predecir (y)
# X = Son los datos de entrada (monto, hora, categoría, etc)
# y = Es lo que queremos predecir (fraude o no fraude)
X = datos.drop('is_fraud', axis=1)  # Todo excepto la columna "is_fraud"
y = datos['is_fraud']  # Solo la columna "is_fraud" (0=legítimo, 1=fraude)

print(f"   ✓ Características de entrada (X): {X.shape}")
print(f"   ✓ Variable objetivo (y): {y.shape}")

# Codificar texto a números (el modelo solo entiende números)
# Por ejemplo: 'groceries' → 0, 'shopping' → 1, etc
print("\n3. Convirtiendo texto a números...")
label_encoder = LabelEncoder()
X['merchant_category'] = label_encoder.fit_transform(X['merchant_category'])
print(f"   ✓ Categorías de comercio codificadas")
print(f"   Ejemplo: {dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))}")

# PASO 3: DIVIDIR LOS DATOS
# ==========================
print("\n4. Dividiendo datos en entrenamiento y prueba...")
# 80% para entrenar, 20% para probar
# random_state=42 asegura que siempre sea igual (reproducible)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"   ✓ Datos de entrenamiento: {X_train.shape[0]} transacciones")
print(f"   ✓ Datos de prueba: {X_test.shape[0]} transacciones")

# PASO 4: NORMALIZAR LOS DATOS
# ==============================
print("\n5. Normalizando datos (escala 0-1)...")
# Esto es importante porque los números tienen rangos muy diferentes
# Por ejemplo: amount (100-9000) vs hour (1-24)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print(f"   ✓ Datos normalizados correctamente")

# PASO 5: ENTRENAR EL MODELO
# ===========================
print("\n6. Entrenando el modelo de Inteligencia Artificial...")
# Random Forest = Bosque de árboles de decisión
# Es como preguntar a 100 expertos y ver qué dice la mayoría
modelo = RandomForestClassifier(
    n_estimators=100,  # 100 árboles de decisión
    random_state=42,
    n_jobs=-1  # Usar todos los núcleos del procesador
)
modelo.fit(X_train_scaled, y_train)  # ¡Aquí el modelo APRENDE!
print(f"   ✓ Modelo entrenado exitosamente")

# PASO 6: EVALUAR EL MODELO
# ==========================
print("\n7. Evaluando el modelo en datos de prueba...")
# Hacer predicciones con los datos de prueba
predicciones = modelo.predict(X_test_scaled)

# Calcular métricas de rendimiento
accuracy = accuracy_score(y_test, predicciones)
precision = precision_score(y_test, predicciones, zero_division=0)
recall = recall_score(y_test, predicciones, zero_division=0)
f1 = f1_score(y_test, predicciones, zero_division=0)

print(f"   ✓ Accuracy (precisión general): {accuracy:.2%}")
print(f"   ✓ Precision (de los fraudes detectados, cuántos son reales): {precision:.2%}")
print(f"   ✓ Recall (de los fraudes reales, cuántos detectamos): {recall:.2%}")
print(f"   ✓ F1-Score (promedio de precision y recall): {f1:.2%}")

# PASO 7: GUARDAR EL MODELO Y SCALER
# ====================================
print("\n8. Guardando modelo y datos de normalización...")
# Guardar el modelo entrenado para usarlo después
joblib.dump(modelo, 'fraud_model.pkl')
print(f"   ✓ Modelo guardado en: fraud_model.pkl")

# Guardar el scaler (normalizador) también
joblib.dump(scaler, 'scaler.pkl')
print(f"   ✓ Scaler guardado en: scaler.pkl")

# Guardar el label encoder para categorías
joblib.dump(label_encoder, 'label_encoder.pkl')
print(f"   ✓ Label Encoder guardado en: label_encoder.pkl")

print("\n" + "=" * 50)
print("¡ENTRENAMIENTO COMPLETADO EXITOSAMENTE!")
print("=" * 50)
print("\nAhora puedes ejecutar: python app.py")
print("Y abrir http://localhost:5000 en tu navegador")
