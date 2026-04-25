// ========================================
// LÓGICA DEL DETECTOR DE FRAUDE (FRONTEND)
// ========================================

// URL del servidor backend
// Para desarrollo local: http://localhost:5000
// Para producción: configura la variable de entorno API_URL en Netlify
const API_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000' 
    : (process.env.API_URL || 'https://tu-backend-api.onrender.com');

// FUNCIÓN: Cuando la página carga, ejecutar esto
document.addEventListener('DOMContentLoaded', function() {
    console.log('✓ Página cargada correctamente');
    
    // Agregar listeners (oyentes) a los botones
    document.getElementById('analyzeBtn').addEventListener('click', analizarTransaccion);
    document.getElementById('exampleBtn').addEventListener('click', cargarEjemplo);
    
    console.log('✓ Botones configurados');
});

// ============================
// FUNCIÓN 1: CARGAR EJEMPLO
// ============================
function cargarEjemplo() {
    /**
     * Esto carga automáticamente valores de ejemplo para que el usuario
     * pueda ver cómo funciona sin tener que escribir nada
     */
    console.log('📌 Cargando ejemplo...');
    
    // Datos de ejemplo
    document.getElementById('amount').value = '8000';
    document.getElementById('hour').value = '2';
    document.getElementById('merchant_category').value = 'online';
    document.getElementById('distance').value = '5000';
    document.getElementById('days_since').value = '1';
    document.getElementById('transactions').value = '1';
    
    console.log('✓ Ejemplo cargado');
    
    // Automáticamente analizar la transacción
    setTimeout(() => analizarTransaccion(), 500);
}

// ============================
// FUNCIÓN 2: ANALIZAR TRANSACCIÓN
// ============================
async function analizarTransaccion() {
    /**
     * ESTA ES LA FUNCIÓN PRINCIPAL
     * 
     * 1. Obtiene datos del formulario
     * 2. Los valida
     * 3. Los envía al servidor
     * 4. Recibe la predicción del modelo
     * 5. Muestra los resultados
     */
    
    console.log('\n' + '='.repeat(50));
    console.log('🔍 INICIANDO ANÁLISIS DE TRANSACCIÓN');
    console.log('='.repeat(50));
    
    // PASO 1: OBTENER DATOS DEL FORMULARIO
    // =====================================
    const amount = document.getElementById('amount').value;
    const hour = document.getElementById('hour').value;
    const merchant_category = document.getElementById('merchant_category').value;
    const distance_from_home = document.getElementById('distance').value;
    const days_since_last_transaction = document.getElementById('days_since').value;
    const num_transactions_today = document.getElementById('transactions').value;
    
    console.log('📋 Datos del formulario:');
    console.log(`   Monto: $${amount}`);
    console.log(`   Hora: ${hour}:00`);
    console.log(`   Categoría: ${merchant_category}`);
    console.log(`   Distancia: ${distance_from_home}km`);
    console.log(`   Días sin comprar: ${days_since_last_transaction}`);
    console.log(`   Transacciones hoy: ${num_transactions_today}`);
    
    // PASO 2: VALIDAR QUE TODOS LOS CAMPOS ESTÉN LLENOS
    // ==================================================
    if (!amount || !hour || !merchant_category || !distance_from_home || 
        !days_since_last_transaction || num_transactions_today === '') {
        console.log('✗ Error: Faltan datos');
        mostrarError('Por favor completa todos los campos');
        return;
    }
    
    // PASO 3: VALIDAR QUE LOS NÚMEROS SEAN VÁLIDOS
    // =============================================
    if (hour < 0 || hour > 23) {
        console.log('✗ Error: Hora inválida');
        mostrarError('La hora debe estar entre 0 y 23');
        return;
    }
    
    // PASO 4: PREPARAR LOS DATOS PARA ENVIAR
    // ========================================
    // Crear un objeto JSON con todos los datos
    const datosTransaccion = {
        amount: parseFloat(amount),
        hour: parseInt(hour),
        merchant_category: merchant_category,
        distance_from_home: parseFloat(distance_from_home),
        days_since_last_transaction: parseInt(days_since_last_transaction),
        num_transactions_today: parseInt(num_transactions_today)
    };
    
    console.log('📦 Datos preparados para enviar:', datosTransaccion);
    
    // PASO 5: ENVIAR DATOS AL SERVIDOR
    // =================================
    try {
        console.log('📡 Enviando solicitud al servidor...');
        
        // Usar fetch para enviar petición HTTP POST
        const respuesta = await fetch(`${API_URL}/predict`, {
            method: 'POST',  // Enviamos datos
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datosTransaccion)  // Convertir objeto a JSON
        });
        
        // PASO 6: VERIFICAR SI LA RESPUESTA FUE EXITOSA
        // =============================================
        if (!respuesta.ok) {
            throw new Error(`Error del servidor: ${respuesta.statusText}`);
        }
        
        // PASO 7: PARSEAR LA RESPUESTA JSON
        // =================================
        const resultado = await respuesta.json();
        console.log('✓ Respuesta recibida del servidor:', resultado);
        
        // PASO 8: MOSTRAR LOS RESULTADOS
        // ==============================
        mostrarResultados(resultado);
        
    } catch (error) {
        // Si hay un error, mostrarlo
        console.error('✗ Error en la solicitud:', error);
        mostrarError(`Error: ${error.message}. ¿El servidor está ejecutándose?`);
    }
}

// ============================
// FUNCIÓN 3: MOSTRAR RESULTADOS
// ============================
function mostrarResultados(resultado) {
    /**
     * Recibe el resultado del servidor y lo muestra en la página
     */
    console.log('\n' + '='.repeat(50));
    console.log('📊 MOSTRANDO RESULTADOS');
    console.log('='.repeat(50));
    
    // PASO 1: MOSTRAR LA SECCIÓN DE RESULTADOS
    // =======================================
    const resultSection = document.getElementById('resultSection');
    resultSection.style.display = 'block';
    
    // PASO 2: MOSTRAR LA PREDICCIÓN (FRAUDE O LEGÍTIMO)
    // ================================================
    const predictionBox = document.getElementById('predictionBox');
    
    if (resultado.es_fraude === 1) {
        // ES FRAUDE
        predictionBox.className = 'prediction-box fraud';
        predictionBox.innerHTML = '⚠️ ¡ALERTA! Transacción sospechosa de FRAUDE';
        console.log('🚨 PREDICCIÓN: FRAUDE');
    } else {
        // ES LEGÍTIMO
        predictionBox.className = 'prediction-box legitimate';
        predictionBox.innerHTML = '✅ Transacción LEGÍTIMA verificada';
        console.log('✓ PREDICCIÓN: LEGÍTIMO');
    }
    
    // PASO 3: MOSTRAR BARRA DE CONFIANZA
    // ==================================
    const confianzaFraude = resultado.confianza_fraude;
    const confianzaLegitimo = resultado.confianza_legitimo;
    
    document.getElementById('fraudBar').style.width = confianzaFraude + '%';
    document.getElementById('fraudPercent').textContent = confianzaFraude.toFixed(1) + '%';
    document.getElementById('legitPercent').textContent = confianzaLegitimo.toFixed(1) + '%';
    
    console.log(`📈 Confianza de fraude: ${confianzaFraude.toFixed(1)}%`);
    console.log(`📈 Confianza de legítimo: ${confianzaLegitimo.toFixed(1)}%`);
    
    // PASO 4: LLENAR TABLA DE DETALLES
    // ================================
    const detallesHTML = `
        <tr>
            <td>💵 Monto</td>
            <td>$${resultado.transaccion.monto}</td>
        </tr>
        <tr>
            <td>⏰ Hora</td>
            <td>${resultado.transaccion.hora}:00</td>
        </tr>
        <tr>
            <td>🏪 Categoría</td>
            <td>${resultado.transaccion.categoria}</td>
        </tr>
        <tr>
            <td>🗺️ Distancia desde casa</td>
            <td>${resultado.transaccion.distancia} km</td>
        </tr>
        <tr>
            <td>📅 Días sin comprar</td>
            <td>${resultado.transaccion.días_desde_última} días</td>
        </tr>
        <tr>
            <td>🔢 Transacciones hoy</td>
            <td>${resultado.transaccion.transacciones_hoy}</td>
        </tr>
    `;
    
    document.getElementById('detailsTable').innerHTML = 
        '<tr><th>Parámetro</th><th>Valor</th></tr>' + detallesHTML;
    
    // PASO 5: GENERAR EXPLICACIÓN
    // ============================
    const explicacion = generarExplicacion(resultado, resultado.transaccion);
    document.getElementById('explanation').textContent = explicacion;
    
    console.log('✓ Resultados mostrados correctamente');
}

// ============================
// FUNCIÓN 4: GENERAR EXPLICACIÓN
// ============================
function generarExplicacion(resultado, transaccion) {
    /**
     * Genera una explicación legible sobre por qué el modelo
     * detectó la transacción como fraude o legítimo
     */
    let explicacion = '';
    
    if (resultado.es_fraude === 1) {
        // Razones por las que se considera fraude
        explicacion = 'El modelo detectó esta transacción como SOSPECHOSA debido a: ';
        
        // Analizar diferentes patrones
        let razones = [];
        
        if (transaccion.hora < 6 || transaccion.hora > 23) {
            razones.push('compra realizada a una hora inusual');
        }
        
        if (transaccion.distancia > 100) {
            razones.push('ubicación muy lejana del domicilio');
        }
        
        if (transaccion.monto > 1000) {
            razones.push('monto de dinero muy elevado');
        }
        
        if (transaccion.transacciones_hoy > 3) {
            razones.push('múltiples compras en poco tiempo');
        }
        
        if (transaccion.días_desde_última === 0 && transaccion.transacciones_hoy > 1) {
            razones.push('patrón de compras acelerado');
        }
        
        explicacion += razones.join(', ') || 'combinación de factores sospechosos';
        explicacion += '. Se recomienda VERIFICAR IDENTIDAD del usuario.';
        
    } else {
        // Razones por las que se considera legítimo
        explicacion = 'El modelo verificó que esta transacción es LEGÍTIMA. ';
        explicacion += 'Los parámetros coinciden con el patrón de compras habitual del usuario: ';
        
        let aspectos = [];
        
        if (transaccion.hora >= 9 && transaccion.hora <= 20) {
            aspectos.push('hora de compra normal');
        }
        
        if (transaccion.distancia < 50) {
            aspectos.push('ubicación cercana al domicilio');
        }
        
        if (transaccion.monto < 1000) {
            aspectos.push('monto razonable');
        }
        
        if (transaccion.transacciones_hoy <= 2) {
            aspectos.push('ritmo de compras usual');
        }
        
        explicacion += aspectos.join(', ') || 'patrones normales de consumo';
        explicacion += '. Transacción AUTORIZADA.';
    }
    
    return explicacion;
}

// ============================
// FUNCIÓN 5: MOSTRAR ERROR
// ============================
function mostrarError(mensaje) {
    /**
     * Muestra un mensaje de error al usuario
     */
    console.error('❌ ' + mensaje);
    
    // Mostrar una alerta
    alert(mensaje);
    
    // Opcionalmente, ocultar la sección de resultados
    document.getElementById('resultSection').style.display = 'none';
}

// ============================
// FUNCIÓN HELPER: FORMATO MONEDA
// ============================
function formatearMoneda(cantidad) {
    /**
     * Convierte un número en formato de moneda
     * Ej: 1000 → $1,000.00
     */
    return new Intl.NumberFormat('es-AR', {
        style: 'currency',
        currency: 'ARS'
    }).format(cantidad);
}
