# 🔍 Detector de Fraude Financiero - Proyecto de IA

## 📚 Descripción

Este es un proyecto educativo que implementa un **Detector de Fraude Financiero** usando **Machine Learning**.

El sistema usa una **Red de Árboles de Decisión (Random Forest)** para analizar transacciones y predecir si son fraudulentas o legítimas.

### ¿Por qué es importante estudiar este código?

- ✅ Aprenderás cómo funciona el **Machine Learning en práctica**
- ✅ Entenderás el flujo completo: datos → modelo → predicción
- ✅ Verás cómo integrar **Python + JavaScript** en una aplicación
- ✅ Descubrirás técnicas reales usadas en **empresas financieras**

---

## 🏗️ Estructura del Proyecto

```
Proyecto_3/
├── train_model.py           # ⭐ Script para ENTRENAR el modelo
├── app.py                   # ⭐ Servidor backend (API)
├── index_fraud.html         # Interfaz web
├── style_fraud.css          # Estilos
├── app_fraud.js             # Lógica del navegador
├── transactions.csv         # Dataset de ejemplo
├── requirements.txt         # Dependencias
└── README.md                # Este archivo
```

---

## 🚀 Cómo Ejecutar

### PASO 1: Instalar dependencias

```bash
pip install -r requirements.txt
```

Esto instala:
- **Flask**: Servidor web
- **scikit-learn**: Machine Learning
- **pandas**: Manipulación de datos
- **numpy**: Matemática

### PASO 2: Entrenar el modelo

```bash
python train_model.py
```

**¿Qué hace?**
1. Lee los datos de `transactions.csv`
2. Enseña al modelo a reconocer patrones de fraude
3. Guarda el modelo en `fraud_model.pkl`
4. Muestra métricas de precisión

**Salida esperada:**
```
==================================================
INICIANDO ENTRENAMIENTO DEL MODELO
==================================================

1. Cargando datos de transacciones...
   ✓ Datos cargados: 20 transacciones

2. Preparando datos para el modelo...
   ✓ Características de entrada (X): (20, 6)
   ✓ Variable objetivo (y): (20,)

...

==================================================
¡ENTRENAMIENTO COMPLETADO EXITOSAMENTE!
==================================================
```

### PASO 3: Iniciar el servidor

```bash
python app.py
```

**Salida esperada:**
```
🚀 INICIANDO SERVIDOR...
==================================================
Abierto en: http://localhost:5000
Presiona CTRL+C para detener el servidor
==================================================
```

### PASO 4: Abrir la interfaz

Abre en tu navegador: **http://localhost:5000**

O abre el archivo `index_fraud.html` directamente (pero necesitas que el servidor esté corriendo)

---

## 🌐 Despliegue en Producción

### Opción 1: Frontend en Netlify + Backend en Render/Railway

#### PASO 1: Desplegar el Backend (API)

1. **Crear cuenta en Render** (gratuito): https://render.com
2. **Conectar tu repo de GitHub**
3. **Configurar como Web Service**:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Environment Variables**: 
     - `FLASK_ENV=production`
     - `PORT=10000`

4. **Obtener la URL de tu API** (ej: `https://tu-proyecto.onrender.com`)

#### PASO 2: Desplegar el Frontend en Netlify

1. **Ir a Netlify**: https://netlify.com
2. **Conectar tu repo de GitHub**
3. **Configurar build**:
   - **Branch**: `master`
   - **Build command**: `echo 'No build needed'`
   - **Publish directory**: `public`
4. **Variables de entorno**:
   - `API_URL`: La URL de tu backend (ej: `https://tu-proyecto.onrender.com`)

#### PASO 3: Actualizar URLs

Antes de desplegar, edita estos archivos:

**En `netlify.toml`**:
```toml
[build.environment]
  API_URL = "https://tu-backend-api.onrender.com"
```

**En `public/_redirects`**:
```
/api/*  https://tu-backend-api.onrender.com/:splat  200
```

### Opción 2: Despliegue Completo en Railway

1. **Railway**: https://railway.app (más fácil para Python)
2. **Conectar repo de GitHub**
3. **Configurar automáticamente** (detecta Python/Flask)
4. **¡Listo!** Una sola URL para todo

---

## 📊 Tecnologías Usadas

- **Backend**: Python + Flask
- **Machine Learning**: scikit-learn (Random Forest)
- **Frontend**: HTML + CSS + JavaScript
- **Datos**: Pandas + NumPy
- **Despliegue**: Netlify (frontend) + Render/Railway (backend)

---

## 📖 Explicación del Código

### 1️⃣ train_model.py - Entrenamiento

```python
# PASO 1: Cargar datos
datos = pd.read_csv('transactions.csv')

# PASO 2: Separar características (X) y objetivo (y)
X = datos.drop('is_fraud', axis=1)  # Todo excepto 'is_fraud'
y = datos['is_fraud']                # Solo 'is_fraud' (0=legítimo, 1=fraude)

# PASO 3: Dividir en entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# PASO 4: Normalizar (escala 0-1)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# PASO 5: Crear y entrenar el modelo
modelo = RandomForestClassifier(n_estimators=100)
modelo.fit(X_train_scaled, y_train)  # ¡EL MODELO APRENDE!

# PASO 6: Guardar para usar después
joblib.dump(modelo, 'fraud_model.pkl')
```

**¿Qué es Random Forest?**

Un "bosque" de 100 árboles de decisión. Cada árbol hace preguntas como:
- ¿Es el monto > $1000?
- ¿Es la hora < 6?
- ¿Está a más de 100 km?

Luego la mayoría "vota" si es fraude o no.

### 2️⃣ app.py - API Backend

```python
@app.route('/predict', methods=['POST'])
def predecir_fraude():
    # Recibe datos del navegador
    data = request.json
    
    # Crear DataFrame con los datos
    entrada = pd.DataFrame([data])
    
    # Normalizar (misma escala que en entrenamiento)
    entrada_normalizada = scaler.transform(entrada)
    
    # Pedir predicción al modelo
    prediccion = modelo.predict(entrada_normalizada)
    
    # Obtener probabilidades (0-100%)
    probabilidades = modelo.predict_proba(entrada_normalizada)
    
    # Devolver resultado al navegador
    return jsonify({
        'prediccion': 'FRAUDE' if prediccion == 1 else 'LEGÍTIMO',
        'confianza': probabilidades[1] * 100
    })
```

**¿Cómo funciona?**

1. El navegador envía datos (POST)
2. El servidor recibe los datos
3. Aplica las mismas transformaciones que en entrenamiento
4. Pide al modelo que prediga
5. Devuelve el resultado al navegador (JSON)

### 3️⃣ app_fraud.js - Lógica Frontend

```javascript
// Cuando el usuario hace click en "Analizar"
async function analizarTransaccion() {
    // 1. Obtener datos del formulario
    const monto = document.getElementById('amount').value;
    const hora = document.getElementById('hour').value;
    
    // 2. Validar que no falten datos
    if (!monto || !hora) {
        alert('Completa todos los campos');
        return;
    }
    
    // 3. Enviar al servidor
    const respuesta = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({amount: monto, hour: hora, ...})
    });
    
    // 4. Recibir resultado
    const resultado = await respuesta.json();
    
    // 5. Mostrar en la página
    mostrarResultados(resultado);
}
```

---

## 📊 Datos de Entrada

El modelo analiza **6 características**:

| Característica | Ejemplo | Rango | Significado |
|---|---|---|---|
| **amount** | 150 | 80-9000 | Monto de la transacción |
| **hour** | 14 | 0-23 | Hora del día |
| **merchant_category** | groceries | Texto | Tipo de comercio |
| **distance_from_home** | 5 | 0-10000 | Distancia en km |
| **days_since_last_transaction** | 5 | 0+ | Días desde última compra |
| **num_transactions_today** | 1 | 0+ | Compras hoy |

---

## 🧠 Cómo el Modelo Aprende

### EJEMPLO 1: FRAUDE

```
Transacción:
- Monto: $8000 (muy alto)
- Hora: 2 AM (inusual)
- Ubicación: 5000 km (otro país)
- Categoría: online (compra rápida)

Decisión: ⚠️ FRAUDE (95% confianza)
```

### EJEMPLO 2: LEGÍTIMO

```
Transacción:
- Monto: $150 (normal)
- Hora: 14:00 (tarde)
- Ubicación: 2 km (supermercado cercano)
- Categoría: groceries (compra común)

Decisión: ✅ LEGÍTIMO (98% confianza)
```

---

## 📈 Métricas de Rendimiento

Después de entrenar, verás algo como:

```
✓ Accuracy: 85%           # ¿Acertó en general?
✓ Precision: 80%          # De los fraudes detectados, ¿cuántos son reales?
✓ Recall: 75%             # De los fraudes reales, ¿cuántos detectó?
✓ F1-Score: 77%           # Promedio entre Precision y Recall
```

**¿Qué significan?**

- **Accuracy**: Porcentaje de predicciones correctas
- **Precision**: Evita "falsos positivos" (es realmente fraude?)
- **Recall**: Evita "falsos negativos" (detecta todos los fraudes?)

---

## 🎓 Conceptos Clave para Estudiar

### 1. Machine Learning Workflow

```
Datos → Preprocesamiento → Modelo → Predicción
```

### 2. Random Forest

- Múltiples "árboles de decisión"
- Cada árbol vota
- La mayoría "gana"

### 3. Normalización (Scaling)

¿Por qué? Los datos tienen rangos diferentes:
- Monto: 0-9000
- Hora: 0-23

Normalizar los pone en la misma escala (0-1)

### 4. Train/Test Split

- 80% para **entrenar** (aprender)
- 20% para **probar** (evaluar qué tan bien aprendió)

### 5. Overfitting vs Underfitting

- **Overfitting**: Memoriza datos, no generaliza
- **Underfitting**: No aprende suficiente
- **Equilibrio**: ¡El objetivo!

---

## 🐛 Solución de Problemas

### Problema: "ModuleNotFoundError: No module named 'flask'"

**Solución:**
```bash
pip install -r requirements.txt
```

### Problema: "Connection refused" en el navegador

**Solución:**
- Asegúrate que ejecutaste `python app.py`
- El servidor debe estar corriendo en `http://localhost:5000`

### Problema: El modelo no predice bien

**Solución:**
- Necesitas más datos (actualmente solo hay 20 transacciones)
- Descarga un dataset real de Kaggle
- Entrena con más datos

---

## 📚 Para Aprender Más

### Dataset Reales:
- [Kaggle - Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)

### Librerías Usadas:
- [Scikit-learn Docs](https://scikit-learn.org/)
- [Pandas Docs](https://pandas.pydata.org/)
- [Flask Docs](https://flask.palletsprojects.com/)

### Conceptos:
- Machine Learning en General
- Clasificación vs Regresión
- Evaluación de Modelos

---

## 💡 Ideas para Expandir el Proyecto

1. **Más datos**: Descargar dataset real de fraude
2. **Más modelos**: Comparar Random Forest con XGBoost, SVM, etc.
3. **Visualizaciones**: Gráficos de importancia de características
4. **Base de datos**: Guardar historial de predicciones
5. **API mejorada**: Agregar autenticación, límites de uso
6. **Interfaz mejorada**: Dashboard con estadísticas

---

## 👨‍💻 Autor

Proyecto educativo para **Tecnicatura en Inteligencia Artificial**

---

## 📝 Notas para Estudiar el Código

### Antes de leer el código, entiende:

1. ✅ ¿Qué es Machine Learning?
2. ✅ ¿Cómo funciona Random Forest?
3. ✅ ¿Qué es normalización?
4. ✅ ¿Cómo funciona Flask?
5. ✅ ¿Cómo se comunica JavaScript con Python?

### Al leer el código:

1. 📖 Lee `train_model.py` primero (es el corazón del proyecto)
2. 📖 Lee `app.py` (cómo se expone el modelo)
3. 📖 Lee `app_fraud.js` (cómo se usa desde el navegador)

### Cada función está comentada explicando:

- **¿QUÉ hace?**
- **¿CÓMO lo hace?**
- **¿PARA QUÉ lo hace?**

---

¡**Espero que disfrutes estudiando este código!** 🚀

Si tienes preguntas, revisa los comentarios en cada archivo. Están muy detallados para que entiendas cada línea.
