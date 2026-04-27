# 🔍 Detector de Fraude Financiero

## 👋 Presentación

Soy Marcos Facchetti y este proyecto demuestra cómo construí una solución completa para detectar fraude en transacciones financieras.

La aplicación combina:
- un modelo de Machine Learning entrenado con datos de transacciones,
- una API backend en Flask,
- y una interfaz web que consume la API en tiempo real.

Mi objetivo fue desarrollar un caso práctico sólido que muestre tanto habilidades técnicas como enfoque en producto.

Demo: https://fraud-detection-api-jmx0.onrender.com/

---

## 🎯 Qué resolví

- Detectar transacciones sospechosas mediante clasificación binaria
- Entrenar un modelo con transformaciones de datos consistentes
- Crear un backend que expone una API REST para predicciones
- Construir una interfaz UX simple para probar casos en vivo
- Desplegar todo en Render para un entorno de producción real

---

## 🧠 Por qué es relevante

Este proyecto es útil para un recruiter porque demuestra:

- experiencia en **end-to-end delivery**
- uso de **Python + Flask + scikit-learn**
- capacidad de integrar **backend y frontend**
- enfoque en **deploy y disponibilidad en la nube**
- documentación clara y fácil de revisar

---

## 📁 Estructura del proyecto

```bash
Proyecto_3/
├── train_model.py          # Entrena y guarda el modelo de fraude
├── app.py                  # API REST en Flask
├── index_fraud.html        # Interfaz web de demostración
├── style_fraud.css         # Estilos del frontend
├── app_fraud.js            # Lógica de interacción del navegador
├── transactions.csv        # Dataset de ejemplo
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Documentación del proyecto
```

---

## 🚀 Cómo ejecutarlo localmente

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Entrenar el modelo

```bash
python train_model.py
```

### Iniciar la API

```bash
python app.py
```

### Acceder a la aplicación

Abre tu navegador en:

```text
http://localhost:5000
```

---

## 🌐 Despliegue en Render

Este proyecto está desplegado en Render y funciona como una demo completa de frontend + backend.

- **URL de la aplicación / API**: `https://fraud-detection-api-jmx0.onrender.com`

### Configuración principal

- **Runtime**: Python 3
- **Build command**: `pip install -r requirements.txt`
- **Start command**: `python app.py`
- **Environment variables**:
  - `FLASK_ENV=production`
  - `PORT=10000`

> Nota: el servidor Flask sirve tanto el frontend como el backend en Render.

---

## 🛠️ Stack tecnológico

- **Python**
- **Flask**
- **scikit-learn**
- **Pandas**
- **NumPy**
- **HTML / CSS / JavaScript**

---

## 📌 Detalle técnico

### train_model.py

Este script:
- carga el dataset,
- codifica variables categóricas,
- normaliza los datos,
- entrena un modelo Random Forest,
- y guarda el modelo con `joblib`.

### app.py

Implementa una API REST que:
- recibe datos de transacciones,
- transforma y normaliza los datos,
- hace la predicción con el modelo cargado,
- y devuelve resultados en JSON.

### app_fraud.js

Controla la interacción del frontend:
- toma los valores del formulario,
- llama a la API `/predict`,
- y muestra el resultado en pantalla.

---

## 📎 Qué aporta este proyecto

- muestra una entrega completa de producto
- integra modelo, API y frontend
- está listo para revisión por un recruiter
- refleja buenas prácticas de despliegue en la nube

---

## 📌 Resultado esperado

La aplicación permite probar transacciones reales y obtiene una predicción clara de:
- **FRAUDE**
- **LEGÍTIMO**

Incluye además un porcentaje de confianza.

---

## 👨‍💻 Nota final

Este repositorio es una demostración práctica de mis habilidades en Inteligencia Artificial aplicada, desarrollo web y despliegue de soluciones en la nube.
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
