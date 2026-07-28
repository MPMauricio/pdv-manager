import glob
import json
from datetime import datetime
import pandas as pd

print("📁 BUSCANDO ARCHIVO EXCEL EN LA CARPETA...")
print("=" * 50)

# Buscar cualquier archivo .xlsx o .xls en la carpeta del proyecto
archivos_excel = glob.glob("*.xlsx") + glob.glob("*.xls")

if not archivos_excel:
    print("❌ Error: No se encontró ningún archivo Excel en esta carpeta.")
    print("👉 Por favor, copia o mueve tu archivo Excel dentro de la carpeta del proyecto.")
    input("\nPresiona ENTER para salir...")
    exit()

# Seleccionar el primer Excel encontrado
filename = archivos_excel[0]
print(f"✅ Archivo encontrado: {filename}")

# Leer Excel
df = pd.read_excel(filename)
print(f"📊 Registros encontrados: {len(df)}")
print("📋 Columnas detectadas:")
for col in df.columns:
    print(f"   - {col}")

# Limpiar datos - convertir todo a string
for col in df.columns:
    df[col] = df[col].fillna('').astype(str)

# Convertir a lista de diccionarios
data = df.to_dict('records')

# Crear estructura JSON
output = {
    "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "total_records": len(data),
    "data": data
}

# Convertir a JSON string
json_data = json.dumps(output, ensure_ascii=False)

# Plantilla HTML con tu código exacto
html_template = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>PDV Manager - Por Ruta</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; }
        
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 15px; 
            position: sticky; 
            top: 0; 
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header h1 { font-size: 1.3rem; margin-bottom: 5px; }
        .header .subtitle { font-size: 0.8rem; opacity: 0.9; }
        
        .btn { 
            padding: 12px 20px; 
            border: none; 
            border-radius: 10px; 
            font-size: 0.95rem; 
            cursor: pointer; 
            font-weight: 600;
            transition: all 0.3s;
        }
        .btn:active { transform: scale(0.95); }
        .btn-route { 
            background: #667eea; 
            color: white; 
            width: 100%; 
            margin-bottom: 10px;
            padding: 15px;
            font-size: 1rem;
        }
        .btn-route.active { 
            background: #764ba2; 
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            transform: scale(1.02);
        }
        
        .step-indicator {
            background: white;
            padding: 15px;
            margin: 10px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .step {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #ddd;
        }
        .step.active { border-left-color: #667eea; background: #e7f3ff; }
        .step.completed { border-left-color: #28a745; background: #d4edda; }
        .step-number {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: #ddd;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 10px;
        }
        .step.active .step-number { background: #667eea; }
        .step.completed .step-number { background: #28a745; }
        .step-label { font-weight: 600; color: #333; }
        
        .route-section {
            background: white;
            padding: 15px;
            margin: 10px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .section-title {
            font-size: 1rem;
            font-weight: bold;
            margin-bottom: 15px;
            color: #333;
        }
        .routes-grid { display: grid; grid-template-columns: 1fr; gap: 10px; }
        
        .alert-section {
            background: white;
            padding: 15px;
            margin: 10px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            display: none;
        }
        .alert-section.show { display: block; }
        .alert-buttons { display: grid; grid-template-columns: 1fr; gap: 10px; }
        .alert-btn {
            padding: 15px;
            border: 3px solid #e0e0e0;
            border-radius: 10px;
            text-align: center;
            cursor: pointer;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s;
        }
        .alert-btn:active { transform: scale(0.98); }
        .alert-btn.urge { background: #fff3cd; border-color: #ffc107; color: #856404; }
        .alert-btn.urge.active { background: #ffc107; color: white; }
        .alert-btn.desabastecido { background: #f8d7da; border-color: #dc3545; color: #721c24; }
        .alert-btn.desabastecido.active { background: #dc3545; color: white; }
        .alert-btn.sin-riesgo { background: #d4edda; border-color: #28a745; color: #155724; }
        .alert-btn.sin-riesgo.active { background: #28a745; color: white; }
        
        .pin-section {
            background: white;
            padding: 15px;
            margin: 10px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            display: none;
        }
        .pin-section.show { display: block; }
        .pin-input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1.1rem;
            text-align: center;
            letter-spacing: 2px;
        }
        .pin-input:focus { outline: none; border-color: #667eea; }
        
        .results-section {
            background: white;
            margin: 10px;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            display: none;
        }
        .results-section.show { display: block; }
        .results-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .results-count { font-size: 0.9rem; }
        .results-count strong { font-size: 1.2rem; }
        
        .table-row {
            padding: 15px;
            border-bottom: 1px solid #e0e0e0;
            transition: background 0.2s;
        }
        .table-row:active { background: #f8f9fa; }
        .table-row:last-child { border-bottom: none; }
        
        .row-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .pdv-name { font-weight: bold; font-size: 1rem; color: #333; }
        .pdv-phone { font-size: 0.85rem; color: #666; margin-top: 3px; }
        .pdv-pin {
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            margin-left: 5px;
        }
        
        .classification-badge {
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: bold;
            text-transform: uppercase;
        }
        .classification-badge.desabastecido { background: #f8d7da; color: #721c24; }
        .classification-badge.alerta { background: #fff3cd; color: #856404; }
        .classification-badge.sin-riesgo { background: #d4edda; color: #155724; }
        
        .row-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 10px;
        }
        .detail-item {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 8px;
        }
        .detail-label { font-size: 0.7rem; color: #666; margin-bottom: 3px; }
        .detail-value { font-weight: 600; color: #333; font-size: 0.95rem; }
        .detail-value.positive { color: #28a745; }
        .detail-value.warning { color: #ffc107; }
        .detail-value.danger { color: #dc3545; }
        
        .ruta-badge {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        .no-results {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        .no-results-icon { font-size: 3rem; margin-bottom: 15px; }
        
        .last-update {
            text-align: center;
            padding: 10px;
            background: #f8f9fa;
            font-size: 0.8rem;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }
        
        .debug-info {
            background: #fff3cd;
            padding: 10px;
            margin: 10px;
            border-radius: 8px;
            font-size: 0.8rem;
            display: none;
        }
        .debug-info.show { display: block; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📱 PDV Manager</h1>
        <div class="subtitle">Control por Ruta</div>
    </div>

    <div class="step-indicator">
        <div class="step" id="step1">
            <div class="step-number">1</div>
            <div class="step-label">Selecciona tu Ruta</div>
        </div>
        <div class="step" id="step2">
            <div class="step-number">2</div>
            <div class="step-label">Elige Tipo de Alerta</div>
        </div>
        <div class="step" id="step3">
            <div class="step-number">3</div>
            <div class="step-label">Ver PDVs</div>
        </div>
    </div>

    <div class="route-section" id="routeSection">
        <div class="section-title">🛣️ PASO 1: Selecciona tu Ruta</div>
        <div class="routes-grid" id="routesGrid"></div>
    </div>

    <div class="alert-section" id="alertSection">
        <div class="section-title">⚠️ PASO 2: ¿Qué tipo de PDV necesitas ver?</div>
        <div class="alert-buttons">
            <div class="alert-btn urge" onclick="selectAlert('Alerta', this)">
                ⚠️ ALERTA<br>
                <small style="font-size: 0.8rem;">Urgente - Amarillo</small>
            </div>
            <div class="alert-btn desabastecido" onclick="selectAlert('Desabastecido', this)">
                🚫 DESABASTECIDO<br>
                <small style="font-size: 0.8rem;">Rojo - Crítico</small>
            </div>
            <div class="alert-btn sin-riesgo" onclick="selectAlert('Sin Riesgo', this)">
                ✅ SIN RIESGO<br>
                <small style="font-size: 0.8rem;">Verde - Estable</small>
            </div>
        </div>
    </div>

    <div class="pin-section" id="pinSection">
        <div class="section-title"> Opcional: Buscar PDV específico por PIN</div>
        <input type="text" class="pin-input" id="pinInput" placeholder="Ingresa los últimos 4 dígitos" maxlength="4" oninput="searchByPin(this.value)">
        <p style="margin-top: 10px; font-size: 0.85rem; color: #666; text-align: center;">
            Deja vacío para ver todos los PDVs de la selección
        </p>
    </div>

    <div class="debug-info" id="debugInfo"></div>

    <div class="results-section" id="resultsSection">
        <div class="results-header">
            <div>
                <div style="font-size: 0.85rem; opacity: 0.9;">PDVs Encontrados</div>
                <div class="results-count"><strong id="resultsCount">0</strong> registros</div>
            </div>
            <div id="currentRoute" style="font-size: 0.9rem;"></div>
        </div>
        <div id="resultsContent"></div>
    </div>

    <div class="last-update" id="lastUpdate">Última actualización: --</div>

    <script>
        const appData = __JSON_DATA__;
        let allData = appData.data || [];
        let selectedRoute = null;
        let selectedAlert = null;
        let filteredData = [];

        console.log("Datos cargados:", allData.length, "registros");
        console.log("Primer registro:", allData[0]);
        console.log("Columnas disponibles:", Object.keys(allData[0]));

        document.addEventListener('DOMContentLoaded', function() {
            if (appData.last_update) {
                document.getElementById('lastUpdate').textContent = 'Última actualización: ' + appData.last_update;
            }
            populateRoutes();
        });

        function populateRoutes() {
            const routes = [...new Set(allData.map(item => item.Ruta).filter(r => r && r !== ''))].sort();
            const grid = document.getElementById('routesGrid');
            
            console.log("Rutas encontradas:", routes);
            
            if (routes.length === 0) {
                grid.innerHTML = '<p style="color: #dc3545; text-align: center;">No se encontraron rutas en los datos</p>';
                return;
            }
            
            routes.forEach(route => {
                const btn = document.createElement('div');
                btn.className = 'btn btn-route';
                btn.textContent = route;
                btn.onclick = () => selectRoute(route, btn);
                grid.appendChild(btn);
            });
        }

        function selectRoute(route, btnElement) {
            selectedRoute = route;
            
            document.querySelectorAll('.btn-route').forEach(b => b.classList.remove('active'));
            btnElement.classList.add('active');
            
            document.getElementById('step1').classList.add('completed');
            document.getElementById('step2').classList.add('active');
            
            document.getElementById('alertSection').classList.add('show');
            document.getElementById('alertSection').scrollIntoView({ behavior: 'smooth' });
            
            console.log("Ruta seleccionada:", route);
        }

        function selectAlert(alertType, btnElement) {
            selectedAlert = alertType;
            
            document.querySelectorAll('.alert-btn').forEach(b => b.classList.remove('active'));
            btnElement.classList.add('active');
            
            document.getElementById('step2').classList.add('completed');
            document.getElementById('step3').classList.add('active');
            
            document.getElementById('pinSection').classList.add('show');
            document.getElementById('resultsSection').classList.add('show');
            
            applyFilters();
            document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
            
            console.log("Alerta seleccionada:", alertType);
        }

        function applyFilters() {
            if (!selectedRoute || !selectedAlert) return;
            
            filteredData = allData.filter(item => {
                const itemRoute = item.Ruta || '';
                const itemClasificacion = item['Última Clasificación'] || '';
                
                return itemRoute === selectedRoute && itemClasificacion === selectedAlert;
            });
            
            displayResults(filteredData);
        }

        function searchByPin(pin) {
            if (!selectedRoute || !selectedAlert) {
                alert('Primero selecciona ruta y tipo de alerta');
                return;
            }
            
            if (!pin || pin.length < 4) {
                applyFilters();
                return;
            }
            
            const pinResults = filteredData.filter(item => {
                const phone = String(item['Telefono PDV'] || '');
                return phone.endsWith(pin);
            });
            
            displayResults(pinResults);
        }

        function displayResults(data) {
            const content = document.getElementById('resultsContent');
            const countEl = document.getElementById('resultsCount');
            const routeEl = document.getElementById('currentRoute');
            
            countEl.textContent = data.length;
            routeEl.textContent = selectedRoute || '';
            
            if (data.length === 0) {
                content.innerHTML = `
                    <div class="no-results">
                        <div class="no-results-icon">📂</div>
                        <h3>Sin resultados</h3>
                        <p>No hay PDVs que coincidan con los filtros</p>
                    </div>
                `;
                return;
            }
            
            let html = '';
            data.forEach((item, index) => {
                try {
                    const classification = item['Última Clasificación'] || '';
                    const classificationClass = getClassificationClass(classification);
                    const balance = parseFloat(item['Saldo Actual']) || 0;
                    const balanceClass = getBalanceClass(balance, classification);
                    const promedio = parseFloat(item['Promedio Recarga Prox. 48h']) || 0;
                    const abastecimiento = parseFloat(item['Abastecimiento Sugerido Prox. 48 Hrs.']) || 0;
                    const phone = item['Telefono PDV'] || '';
                    const pin = phone.length >= 4 ? phone.slice(-4) : phone;
                    const nombre = item['Nombre PDV'] || 'N/A';
                    const ruta = item.Ruta || 'N/A';

                    html += `
                        <div class="table-row">
                            <div class="row-header">
                                <div>
                                    <div class="pdv-name">${nombre}</div>
                                    <div class="pdv-phone">
                                         ${phone}
                                        <span class="pdv-pin">${pin}</span>
                                    </div>
                                </div>
                                <span class="classification-badge ${classificationClass}">${classification}</span>
                            </div>
                            <div class="row-details">
                                <div class="detail-item">
                                    <div class="detail-label">💰 Saldo Actual</div>
                                    <div class="detail-value ${balanceClass}">$${balance.toFixed(2)}</div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">📊 Promedio 48h</div>
                                    <div class="detail-value">$${promedio.toFixed(2)}</div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">📦 Abastecimiento</div>
                                    <div class="detail-value">$${abastecimiento.toFixed(2)}</div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">🛣️ Ruta</div>
                                    <div class="ruta-badge">${ruta}</div>
                                </div>
                            </div>
                        </div>
                    `;
                } catch (error) {
                    console.error("Error renderizando item", index, error);
                }
            });
            
            content.innerHTML = html;
        }

        function getClassificationClass(classification) {
            switch(classification) {
                case 'Alerta': return 'alerta';
                case 'Desabastecido': return 'desabastecido';
                case 'Sin Riesgo': return 'sin-riesgo';
                default: return '';
            }
        }

        function getBalanceClass(balance, classification) {
            if (classification === 'Desabastecido') return 'danger';
            if (classification === 'Alerta') return 'warning';
            if (balance < 5) return 'warning';
            return 'positive';
        }
    </script>
</body>
</html>'''

# Inyectar el JSON dentro del HTML
html_content = html_template.replace("__JSON_DATA__", json_data)

# Guardar y sobrescribir el archivo index.html local
output_filename = "index.html"
with open(output_filename, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"\n✨ HTML generado y actualizado: {output_filename}")
print(f"📦 Tamaño total: {len(html_content)} bytes")
print("\n✅ ¡PROCESO COMPLETADO EXITOSAMENTE!")