# 🎓 GUÍA DE ESTUDIO - Cómo Estudiar Este Código

## 👨‍💻 Antes de Empezar

Este proyecto tiene **MUCHO código comentado**. Cada función explica:
- ✅ ¿QUÉ hace?
- ✅ ¿CÓMO lo hace?
- ✅ ¿PARA QUÉ lo hace?

Lee los comentarios como si fueran parte del aprendizaje.

---

## 📖 Orden Recomendado de Lectura

### FASE 1: Entender la Teoría (1 hora)

```
TEORIA.md
├── Lee: "Machine Learning Básico"
├── Lee: "Clasificación"
├── Lee: "Random Forest"
└── Lee: "Preparación de Datos"
```

**Objetivo**: Entender QUÉ es lo que vas a ver en el código.

**Preguntas clave para hacerte:**
- ¿Qué es Machine Learning?
- ¿Cómo un árbol de decisión "decide"?
- ¿Por qué normalizamos datos?
- ¿Qué significa "accuracy"?

---

### FASE 2: Ejecutar y Jugar (30 minutos)

1. `python train_model.py`
   - Observa cómo el modelo aprende
   - Lee los mensajes que aparecen

2. `python app.py`
   - Inicia el servidor
   - Abre http://localhost:5000
   - Prueba con el botón "Cargar ejemplo"
   - Ingresa datos diferentes y ve qué predice

**Objetivo**: Ver que el modelo FUNCIONA antes de entender cómo.

---

### FASE 3: Leer el Código (2-3 horas)

#### 3.1 - train_model.py

**Estructura:**
```python
# 1. Importar librerías
import pandas
import sklearn

# 2. PASO 1: CARGAR LOS DATOS
datos = pd.read_csv('transactions.csv')

# 3. PASO 2: PREPARAR LOS DATOS
X = datos.drop('is_fraud', axis=1)
y = datos['is_fraud']

# ... más pasos ...

# 7. PASO 7: GUARDAR EL MODELO
joblib.dump(modelo, 'fraud_model.pkl')
```

**Qué estudiar:**
1. Lee los comentarios explicativos
2. Entiende cada PASO
3. Identifica dónde se "entrena" el modelo
4. Busca dónde se guardan los archivos

**Preguntas para hacerte:**
- ¿Por qué dividimos 80/20?
- ¿Qué hace `StandardScaler`?
- ¿Qué hace `LabelEncoder`?
- ¿Cómo el modelo "aprende"?

**Modificaciones para experimentar:**
```python
# Cambia la cantidad de árboles
modelo = RandomForestClassifier(n_estimators=50)  # Menos árboles

# Cambia el test_size
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
# Ahora 70% entrena, 30% prueba
```

---

#### 3.2 - app.py

**Estructura:**
```python
# 1. Importar Flask
from flask import Flask, request, jsonify

# 2. Crear la aplicación
app = Flask(__name__)

# 3. Cargar modelos guardados
modelo = joblib.load('fraud_model.pkl')

# 4. Definir rutas (funciones que responden a URLs)
@app.route('/predict', methods=['POST'])
def predecir_fraude():
    # Recibir datos
    data = request.json
    
    # Prepararlos
    entrada = pd.DataFrame([data])
    
    # Hacer predicción
    prediccion = modelo.predict(entrada_normalizada)
    
    # Devolver resultado
    return jsonify({'resultado': prediccion})

# 5. Iniciar servidor
app.run()
```

**Qué estudiar:**
1. Cómo Flask recibe datos del navegador
2. Cómo prepara los datos para el modelo
3. Cómo el modelo predice
4. Cómo devuelve el resultado

**Preguntas para hacerte:**
- ¿Qué es `@app.route`?
- ¿Por qué necesitamos normalizar aquí también?
- ¿Qué es `request.json`?
- ¿Por qué importamos `joblib.load`?

**Modificaciones para experimentar:**
```python
# Agregar una nueva ruta para obtener información
@app.route('/info', methods=['GET'])
def get_info():
    return jsonify({'modelo': 'Detector de Fraude v1.0'})

# Luego accede a: http://localhost:5000/info
```

---

#### 3.3 - app_fraud.js

**Estructura:**
```javascript
// 1. Cuando la página carga
document.addEventListener('DOMContentLoaded', function() {
    // Agregar listeners
})

// 2. Cuando el usuario presiona "Analizar"
async function analizarTransaccion() {
    // Obtener datos del formulario
    const monto = document.getElementById('amount').value
    
    // Enviar al servidor
    const respuesta = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        body: JSON.stringify({...})
    })
    
    // Recibir resultado
    const resultado = await respuesta.json()
    
    // Mostrar en la página
    mostrarResultados(resultado)
}

// 3. Mostrar resultados
function mostrarResultados(resultado) {
    // Actualizar HTML con los resultados
}
```

**Qué estudiar:**
1. Cómo JavaScript obtiene datos del HTML
2. Cómo comunica con el servidor Python
3. Cómo recibe la respuesta
4. Cómo actualiza la página

**Preguntas para hacerte:**
- ¿Qué es `async/await`?
- ¿Qué es `fetch`?
- ¿Qué es `JSON`?
- ¿Cómo actualiza HTML dinámicamente?

**Modificaciones para experimentar:**
```javascript
// Agregar validación adicional
if (amount < 0) {
    alert('El monto no puede ser negativo');
    return;
}

// Agregar spinner de carga
document.getElementById('analyzeBtn').textContent = '⏳ Analizando...';

// Deshabilitar botón mientras carga
document.getElementById('analyzeBtn').disabled = true;
```

---

### FASE 4: Experimentos y Modificaciones (2-4 horas)

#### Experimento 1: Cambiar Datos de Entrada

En `transactions.csv`:
```csv
amount,hour,merchant_category,distance_from_home,days_since_last_transaction,num_transactions_today,is_fraud
```

Modifica las filas para crear tus propios ejemplos y reentrena.

```bash
# 1. Edita transactions.csv
# 2. python train_model.py
# 3. python app.py
# 4. Prueba en el navegador
```

#### Experimento 2: Agregar Más Características

En `train_model.py`, agrega:
```python
# Nueva columna: ¿Es fin de semana?
datos['is_weekend'] = 0  # Agregar esta columna

# Luego usarla en el modelo
X = datos.drop('is_fraud', axis=1)  # Incluirá is_weekend automáticamente
```

#### Experimento 3: Cambiar el Modelo

En `train_model.py`:
```python
# Cambiar de Random Forest a XGBoost
from sklearn.ensemble import GradientBoostingClassifier

modelo = GradientBoostingClassifier(n_estimators=100)
modelo.fit(X_train_scaled, y_train)
```

Luego reentrena y ve si es mejor.

#### Experimento 4: Visualizar Importancia de Características

Agregar al final de `train_model.py`:
```python
import matplotlib.pyplot as plt

# Ver qué características son más importantes
importances = modelo.feature_importances_
features = X.columns
plt.barh(features, importances)
plt.xlabel('Importancia')
plt.title('Importancia de cada característica')
plt.show()
```

---

## 🎯 Checklist de Aprendizaje

Completa cada item cuando lo hayas entendido:

### Conceptos Teóricos
- [ ] Entendí qué es Machine Learning
- [ ] Entendí qué es Random Forest
- [ ] Entendí train/test split
- [ ] Entendí normalización de datos
- [ ] Entendí precision/recall/accuracy

### Ejecución
- [ ] Logré instalar dependencias
- [ ] Logré entrenar el modelo
- [ ] Logré iniciar el servidor
- [ ] Logré acceder a la interfaz web
- [ ] Logré hacer una predicción

### Código Python
- [ ] Entendí train_model.py completamente
- [ ] Entendí cómo cargar datos
- [ ] Entendí cómo normalizar datos
- [ ] Entendí cómo entrenar el modelo
- [ ] Entendí app.py completamente
- [ ] Entendí cómo Flask recibe datos
- [ ] Entendí cómo hacer predicciones

### Código JavaScript
- [ ] Entendí app_fraud.js completamente
- [ ] Entendí cómo obtener datos del HTML
- [ ] Entendí cómo enviar al servidor
- [ ] Entendí cómo recibir respuesta
- [ ] Entendí cómo actualizar la página

### Experimentación
- [ ] Modifiqué parámetros del modelo
- [ ] Cambié datos de entrenamiento
- [ ] Agregué validaciones nuevas
- [ ] Intenté con otros modelos
- [ ] Visualicé importancia de features

---

## 📝 Notas Personales - Espacio para Apuntes

Mientras estudias, escribe aquí tus propias notas:

### Mi Resumen del Proyecto:
```
[Escribe aquí lo que aprendiste con tus propias palabras]
```

### Conceptos Clave:
```
1. Machine Learning: ...
2. Random Forest: ...
3. Normalización: ...
```

### Partes del Código que NO Entendí:
```
[Escribe aquí y luego vuelve a leerlas]
```

### Mis Experimentos:
```
- Experimento 1: ...
- Experimento 2: ...
```

---

## 💡 Preguntas Clave Para Auto-Evaluarte

Cuando termines de estudiar, responde estas:

1. **¿Qué es Machine Learning?**
   - Debería poder explicar en 1 minuto

2. **¿Cómo Random Forest toma una decisión?**
   - Debería poder describir el "bosque de árboles"

3. **¿Por qué dividimos datos 80/20?**
   - Debería entender train vs test

4. **¿Qué hace `StandardScaler`?**
   - Debería poder explicar normalización

5. **¿Cómo el navegador se comunica con Python?**
   - Debería entender el flujo: HTML → JS → Fetch → Flask → Respuesta

6. **¿Qué haría si quiero mejor precisión?**
   - Debería tener ideas: más datos, otro modelo, más características, etc.

---

## 📚 Recursos Adicionales

Si quieres profundizar:

### YouTube
- Busca: "Random Forest explained"
- Busca: "Flask Tutorial"
- Busca: "Fetch API JavaScript"

### Kaggle
- Busca: "Credit Card Fraud Detection"
- Descarga un dataset real
- Intenta entrenar con tus propios datos

### Documentación
- scikit-learn.org (Random Forest)
- flask.palletsprojects.com (Flask)
- developer.mozilla.org (JavaScript Fetch)

---

## 🎓 Pasos Siguientes

Una vez termines de estudiar este proyecto:

1. **Crea tu propio dataset**: Con datos que te interesen
2. **Prueba otro modelo**: XGBoost, SVM, Redes Neuronales
3. **Mejora la interfaz**: Agregar gráficos, tablas
4. **Agrega base de datos**: Guardar historial de predicciones
5. **Despliega online**: Usar Heroku o AWS
6. **Participa en Kaggle**: Compite con otros modelos

---

## ⚡ Tips Finales

✅ **Lee el código lentamente**
- Cada línea tiene un propósito
- Tómate tu tiempo

✅ **Ejecuta el código paso por paso**
- Agrega prints() para ver qué pasa
- Usa el debugger de VS Code

✅ **Modifica y experimenta**
- Cambia valores
- Ve qué sucede
- Aprende del error

✅ **Escribe tus propias notas**
- Con tus palabras
- En tu propio archivo
- Así lo memorizas mejor

✅ **Enseña a otros**
- Explica lo que aprendiste
- Si no puedes explicar, no entendiste
- La enseñanza es el mejor aprendizaje

---

## 🎉 ¡Listo para Comenzar!

Ahora sí, ve y:

1. Lee TEORIA.md
2. Ejecuta train_model.py
3. Abre http://localhost:5000
4. Lee el código con los comentarios
5. Experimenta y modifica
6. Aprende y diviértete

**¡Bienvenido al mundo del Machine Learning!** 🚀
