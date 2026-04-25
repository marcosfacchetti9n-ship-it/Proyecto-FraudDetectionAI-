# ==========================================
# SERVIDOR WEB (API) DEL DETECTOR DE FRAUDE
# ==========================================

# Importar Flask para crear el servidor web
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # Para permitir que el navegador hable con el servidor

# Importar librerías de datos y ML
import joblib  # Para cargar el modelo entrenado
import pandas as pd  # Para manipular datos
import numpy as np  # Para matemática
import os  # Para trabajar con archivos

# Crear la aplicación Flask
app = Flask(__name__, static_folder='.')
# Permitir que el frontend acceda al backend
CORS(app)

print("=" * 50)
print("CARGANDO MODELO ENTRENADO...")
print("=" * 50)

# CARGAR MODELOS GUARDADOS PREVIAMENTE
# =====================================
try:
    # Cargar el modelo de IA entrenado
    modelo = joblib.load('fraud_model.pkl')
    print("✓ Modelo cargado correctamente")
    
    # Cargar el normalizador (scaler)
    scaler = joblib.load('scaler.pkl')
    print("✓ Scaler cargado correctamente")
    
    # Cargar el codificador de categorías
    label_encoder = joblib.load('label_encoder.pkl')
    print("✓ Label Encoder cargado correctamente")
    
except Exception as e:
    print(f"✗ Error al cargar modelos: {e}")
    print("Por favor ejecuta: python train_model.py")

print("=" * 50)

# RUTA PARA VERIFICAR QUE EL SERVIDOR FUNCIONA
# =============================================
@app.route('/', methods=['GET'])
def inicio():
    """
    Esta función devuelve la interfaz web principal
    """
    return send_from_directory('.', 'index_fraud.html')

# RUTA PARA VERIFICAR ESTADO (API)
# =================================
@app.route('/status', methods=['GET'])
def status():
    """
    Esta función devuelve un mensaje simple cuando accedes a /status
    Es útil para verificar que el servidor está corriendo
    """
    return jsonify({
        'status': 'OK',
        'mensaje': 'Servidor de Detector de Fraude funcionando correctamente'
    })

# RUTA PARA PREDECIR FRAUDE
# ==========================
@app.route('/predict', methods=['POST'])
def predecir_fraude():
    """
    ESTA ES LA FUNCIÓN MÁS IMPORTANTE
    
    Recibe datos de una transacción desde el navegador y predice si es fraude o no
    
    Entrada (JSON):
    {
        'amount': 100,           # Monto de la transacción
        'hour': 14,              # Hora del día (0-23)
        'merchant_category': 'groceries',  # Tipo de comercio
        'distance_from_home': 2,           # Distancia en km
        'days_since_last_transaction': 5,  # Días desde última compra
        'num_transactions_today': 1        # Transacciones hoy
    }
    """
    try:
        # Obtener los datos enviados por el navegador
        data = request.json
        print(f"\n📨 Nueva solicitud recibida:")
        print(f"   Datos: {data}")
        
        # PASO 1: VALIDAR QUE TODOS LOS DATOS ESTÉN PRESENTES
        # ====================================================
        campos_requeridos = [
            'amount', 'hour', 'merchant_category',
            'distance_from_home', 'days_since_last_transaction',
            'num_transactions_today'
        ]
        
        for campo in campos_requeridos:
            if campo not in data:
                return jsonify({'error': f'Falta el campo: {campo}'}), 400
        
        # PASO 2: PREPARAR LOS DATOS PARA EL MODELO
        # ==========================================
        # Crear un DataFrame (tabla) con los datos
        entrada = pd.DataFrame([{
            'amount': float(data['amount']),
            'hour': int(data['hour']),
            'merchant_category': str(data['merchant_category']),
            'distance_from_home': float(data['distance_from_home']),
            'days_since_last_transaction': int(data['days_since_last_transaction']),
            'num_transactions_today': int(data['num_transactions_today'])
        }])
        
        print(f"   Datos convertidos correctamente")
        
        # PASO 3: CODIFICAR LA CATEGORÍA (texto a número)
        # ===============================================
        # El modelo solo entiende números, así que convertimos:
        # 'groceries' → 0, 'shopping' → 1, etc.
        entrada['merchant_category'] = label_encoder.transform(entrada['merchant_category'])
        print(f"   Categoría codificada: {entrada['merchant_category'].values[0]}")
        
        # PASO 4: NORMALIZAR LOS DATOS
        # =============================
        # Aplicar la misma transformación que usamos en entrenamiento
        entrada_normalizada = scaler.transform(entrada)
        print(f"   Datos normalizados")
        
        # PASO 5: HACER LA PREDICCIÓN
        # ============================
        # Aquí el modelo PREDICE si es fraude (1) o no (0)
        prediccion = modelo.predict(entrada_normalizada)[0]
        
        # Obtener la probabilidad de fraude (0.0 a 1.0)
        probabilidades = modelo.predict_proba(entrada_normalizada)[0]
        confianza_fraude = probabilidades[1] * 100  # Convertir a porcentaje
        confianza_legitimo = probabilidades[0] * 100
        
        print(f"   🔍 Predicción: {'FRAUDE' if prediccion == 1 else 'LEGÍTIMO'}")
        print(f"   📊 Confianza de fraude: {confianza_fraude:.2f}%")
        
        # PASO 6: PREPARAR LA RESPUESTA
        # =============================
        respuesta = {
            'prediccion': 'FRAUDE' if prediccion == 1 else 'LEGÍTIMO',
            'es_fraude': int(prediccion),
            'confianza_fraude': round(confianza_fraude, 2),
            'confianza_legitimo': round(confianza_legitimo, 2),
            'transaccion': {
                'monto': data['amount'],
                'hora': data['hour'],
                'categoria': data['merchant_category'],
                'distancia': data['distance_from_home'],
                'días_desde_última': data['days_since_last_transaction'],
                'transacciones_hoy': data['num_transactions_today']
            }
        }
        
        print(f"   ✓ Respuesta enviada")
        return jsonify(respuesta)
        
    except Exception as e:
        # Si algo va mal, devolver error
        print(f"   ✗ Error: {e}")
        return jsonify({'error': str(e)}), 500

# RUTA PARA OBTENER INFORMACIÓN DEL MODELO
# ==========================================
@app.route('/info', methods=['GET'])
def obtener_info():
    """
    Devuelve información sobre el modelo entrenado
    """
    return jsonify({
        'nombre': 'Detector de Fraude Financiero',
        'version': '1.0',
        'descripcion': 'Modelo que predice si una transacción es fraude o legítima',
        'features': [
            'amount', 'hour', 'merchant_category',
            'distance_from_home', 'days_since_last_transaction',
            'num_transactions_today'
        ],
        'categorias_disponibles': list(label_encoder.classes_)
    })

# RUTAS PARA SERVIR ARCHIVOS ESTÁTICOS
# =====================================
@app.route('/<path:filename>')
def serve_static(filename):
    """
    Sirve archivos estáticos (CSS, JS, imágenes, etc.)
    """
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print("\n🚀 INICIANDO SERVIDOR...")
    print("=" * 50)
    print("Abierto en: http://localhost:5000")
    print("Interfaz web: http://localhost:5000")
    print("Estado API: http://localhost:5000/status")
    print("Presiona CTRL+C para detener el servidor")
    print("=" * 50)
    
    # Iniciar el servidor web
    # debug=True: recarga automáticamente si hay cambios
    app.run(debug=True, port=5000)
