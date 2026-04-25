# 📚 GUÍA TEÓRICA - Conceptos Clave del Detector de Fraude

## 📖 Índice
1. [Machine Learning Básico](#1-machine-learning-básico)
2. [Clasificación](#2-clasificación)
3. [Random Forest](#3-random-forest)
4. [Preparación de Datos](#4-preparación-de-datos)
5. [Evaluación del Modelo](#5-evaluación-del-modelo)
6. [Detección de Anomalías](#6-detección-de-anomalías)

---

## 1. Machine Learning Básico

### ¿Qué es Machine Learning?

Es un tipo de **Inteligencia Artificial** donde las máquinas **aprenden de datos** en lugar de ser programadas explícitamente.

**Ejemplo tradicional (sin ML):**
```
Regla programada:
SI monto > 5000 Y hora < 6
ENTONCES es fraude
```

❌ Problema: No considera otros factores, es muy rígido

**Ejemplo con ML:**
```
El modelo observa 1000 transacciones fraudulentas
Identifica PATRONES automáticamente
Predice fraude en nuevas transacciones
```

✅ Mejor: Flexible, aprende nuevos patrones

### Tipos de Machine Learning

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Supervisado** | Aprende de datos etiquetados | Fraude (1) o No fraude (0) ← Este proyecto |
| **No Supervisado** | Encuentra patrones sin etiquetas | Agrupar clientes similares |
| **Refuerzo** | Aprende con recompensas/castigos | AlphaGo |

---

## 2. Clasificación

### ¿Qué es Clasificación?

Es predecir una **categoría** (clase) basado en características de entrada.

**En nuestro proyecto:**
- Entrada: Datos de una transacción (monto, hora, etc.)
- Salida: Clase → `FRAUDE` o `LEGÍTIMO`

### Clasificación Binaria vs Multiclase

**Binaria (nuestro caso):**
```
Resultado: 0 (no fraude) o 1 (fraude)
```

**Multiclase:**
```
Resultado: 0 (legítimo), 1 (sospechoso), 2 (fraude confirmado)
```

### Matriz de Confusión

Muestra qué tan bien el modelo clasifica:

```
                Predicción Fraud   Predicción Legítimo
Real Fraud              TP                   FN
Real Legítimo           FP                   TN
```

- **TP** (True Positive): Detectó fraude correctamente
- **FN** (False Negative): No detectó fraude que sí existía (🚨 Malo)
- **FP** (False Positive): Dijo fraude pero era legítimo (Molesto)
- **TN** (True Negative): Dijo legítimo y era correcto

---

## 3. Random Forest

### ¿Qué es un Árbol de Decisión?

Es como un árbol que "decide" ramificándose:

```
            ¿Monto > $1000?
             /            \
           Sí              No
           /                \
    ¿Hora < 6?        ¿Distancia > 100km?
     /      \            /         \
   Sí       No         Sí          No
   |        |          |           |
FRAUDE   LEGÍTIMO    FRAUDE     LEGÍTIMO
```

El árbol aprende dónde hacer cada "pregunta" para clasificar mejor.

### ¿Qué es Random Forest?

Es **múltiples árboles de decisión** trabajando juntos:

```
Árbol 1: Predice FRAUDE
Árbol 2: Predice LEGÍTIMO
Árbol 3: Predice FRAUDE
Árbol 4: Predice LEGÍTIMO
Árbol 5: Predice FRAUDE

Votación: 3 FRAUDE vs 2 LEGÍTIMO
→ Resultado final: FRAUDE ✓
```

### Ventajas de Random Forest

✅ **Robusto**: Muchos árboles = menos errores individuales
✅ **Rápido**: Entrena rápido
✅ **Explicable**: Puedo ver qué características son importantes
✅ **No requiere normalización**: Maneja bien datos crudos
❌ **Puede overfitear**: Con demasiados árboles

---

## 4. Preparación de Datos

### ¿Por qué preparar datos?

Los modelos funcionan mejor con datos limpios y bien formateados.

```
Datos Crudos → [Limpieza] → [Normalización] → Datos Listos
```

### Paso 1: Limpieza

- Remover datos duplicados
- Llenar valores faltantes
- Eliminar outliers (valores muy extraños)

```python
# Ejemplo: Rellenar valores faltantes con la media
datos['edad'].fillna(datos['edad'].mean(), inplace=True)
```

### Paso 2: Codificación de Categorías

Los modelos solo entienden **números**.

Conversión:
```
'groceries' → 0
'shopping'  → 1
'restaurant'→ 2
'casino'    → 3
```

```python
label_encoder = LabelEncoder()
datos['categoria'] = label_encoder.fit_transform(datos['categoria'])
```

### Paso 3: Normalización (Scaling)

Los datos tienen rangos muy diferentes:
- Monto: 80 - 9000
- Hora: 0 - 23

Si no normalizamos, el modelo piensa que "monto" es más importante.

**Solución: Escalar a 0-1**

```
Fórmula: (valor - min) / (max - min)

Ejemplo:
Monto 500:  (500-80) / (9000-80) = 0.054
Hora 14:    (14-0) / (23-0) = 0.609
```

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
datos_normalizados = scaler.fit_transform(datos)
```

### Paso 4: División Train/Test

```
Datos → [80% Entrenar] | [20% Probar]
```

**¿Por qué?**
- Entrenar: El modelo aprende
- Probar: Evaluamos si aprendió (con datos NO vistos antes)

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

---

## 5. Evaluación del Modelo

### Métricas Principales

#### 1️⃣ Accuracy (Precisión General)

¿Qué porcentaje de predicciones fueron correctas?

```
Accuracy = (TP + TN) / (TP + TN + FP + FN)

Ejemplo:
90 aciertos de 100 = 90%
```

⚠️ **Problema**: En fraude es malo porque hay pocas transacciones fraudulentas (el modelo podría decir "siempre legítimo" y aún tener 95% de accuracy)

#### 2️⃣ Precision

De las transacciones que predijimos como **fraude**, ¿cuántas realmente eran fraude?

```
Precision = TP / (TP + FP)

Ejemplo:
Predije 100 como fraude, 80 eran reales
Precision = 80/100 = 80%
```

✅ **Importancia**: Evita alertas falsas (molestar al cliente)

#### 3️⃣ Recall (Sensibilidad)

De todos los fraudes reales, ¿cuántos detecté?

```
Recall = TP / (TP + FN)

Ejemplo:
Había 100 fraudes reales, detecté 80
Recall = 80/100 = 80%
```

✅ **Importancia**: Evita perder fraudes (riesgo financiero)

#### 4️⃣ F1-Score

**Promedio entre Precision y Recall**

```
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

✅ Usa esto cuando quieres **balance** entre los dos

### Interpretación

```
Modelo 1: Accuracy 99%, Precision 50%, Recall 30%
→ Detecta casi nada, aunque tenga alta accuracy

Modelo 2: Accuracy 85%, Precision 90%, Recall 85%
→ Mejor balance, más útil en la práctica
```

---

## 6. Detección de Anomalías

### ¿Qué es una Anomalía?

Un evento **poco común** o **diferente del patrón normal**.

**Ejemplos en Fraude:**

```
Patrón normal del usuario:
- Compra diaria $50-200
- Entre 10 AM - 5 PM
- En Buenos Aires
- Categoría: groceries, restaurants

Anomalía:
- Compra $8000 a las 2 AM
- En Japón
- Categoría: casino
→ ¡ALERTA! Diferente a lo normal
```

### Técnicas de Detección

| Técnica | Cómo funciona | Uso |
|---------|---------------|-----|
| **Reglas** | Monto > X AND Hora < Y | Simple, rápido, limitado |
| **Estadística** | ¿Está fuera de 3σ (desv.estándar)? | Útil si datos son normales |
| **Clustering** | Agrupar usuarios similares | Encontrar grupos anómalos |
| **ML (nuestro caso)** | Modelo aprende qué es normal | ✅ Flexible y preciso |

---

## 🎯 Aplicación en Nuestro Proyecto

### Flujo Completo

```
1. Usuario intenta una transacción
   ↓
2. Sistema recibe: monto, hora, ubicación, etc.
   ↓
3. Prepara datos (normaliza, codifica categorías)
   ↓
4. Random Forest predice
   ↓
5. Devuelve: FRAUDE o LEGÍTIMO + confianza
   ↓
6. Si es fraude: BLOQUEAR/ALERTAR
   Si es legítimo: AUTORIZAR
```

### Decisiones del Modelo

El modelo aprendió patrones como:

```
SI monto > 5000 Y hora < 6 Y distancia > 1000km
→ FRAUDE (85% confianza)

SI monto < 500 Y hora entre 9-17 Y distancia < 50km
→ LEGÍTIMO (95% confianza)

SI monto = 2000 Y hora = 14 Y categoría = "online"
→ DEPENDE (55% fraude, 45% legítimo)
```

---

## 📊 Comparación con Otros Modelos

```
Modelo              Velocidad  Precisión  Facilidad  Explicabilidad
─────────────────────────────────────────────────────────────────
Random Forest       ⭐⭐⭐      ⭐⭐⭐    ⭐⭐⭐    ⭐⭐⭐
XGBoost             ⭐⭐       ⭐⭐⭐⭐  ⭐⭐     ⭐⭐
Regresión Logística ⭐⭐⭐⭐    ⭐⭐     ⭐⭐⭐⭐  ⭐⭐⭐⭐
Red Neuronal        ⭐         ⭐⭐⭐⭐  ⭐       ⭐
SVM                 ⭐⭐⭐      ⭐⭐⭐    ⭐⭐     ⭐
```

---

## 💡 Problemas Comunes

### Problema 1: Overfitting

**¿Qué es?** El modelo memoriza los datos en lugar de aprender patrones.

```
Accuracy entrenamiento: 99%
Accuracy prueba: 60%
↑ Diferencia grande = OVERFITTING
```

**Solución:**
- Menos árboles
- Más datos
- Usar regularización

### Problema 2: Underfitting

**¿Qué es?** El modelo no aprende suficiente.

```
Accuracy entrenamiento: 70%
Accuracy prueba: 70%
↑ Ambos bajos = UNDERFITTING
```

**Solución:**
- Más árboles
- Datos más relevantes
- Menos normalización

### Problema 3: Clase Desbalanceada

**¿Qué es?** Hay muchos más "legítimos" que "fraudes".

```
Legítimos: 10,000 transacciones
Fraudes: 100 transacciones
(Proporción 100:1)
```

**Solución:**
- Usar weighted classes
- Oversampling fraudes
- Usar F1-Score, no Accuracy

---

## 🚀 Siguientes Pasos para Aprender

1. **Entrenar el modelo** con `train_model.py`
2. **Estudiar cada línea de código**
3. **Experimentar**: Cambiar parámetros del modelo
4. **Probar nuevos datos**: Crear casos de prueba
5. **Expandir**: Agregar más características, más datos
6. **Optimizar**: Usar XGBoost, tuning de hiperparámetros

---

## 📚 Recursos para Aprender Más

### Videos YouTube
- Curso ML Completo
- Random Forest explicado
- Detección de fraude

### Libros
- "Hands-On Machine Learning" - Aurélien Géron
- "Introduction to Statistical Learning" - James, Witten, Hastie, Tibshirani

### Cursos Online
- Coursera: Machine Learning
- DataCamp: Skill Tracks
- Fast.ai: Practical Deep Learning

---

**¡Ahora sí! Ve a leer el código con estos conceptos frescos en mente.** 🎓
