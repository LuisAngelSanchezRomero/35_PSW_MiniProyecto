from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Base de datos en memoria (Mock de DevanShop con prefijo TEC)
productos = [
    {"id": 1, "codigo": "TEC-001", "nombre": "Laptop Gamer Devan Pro 16", "categoria": "Tecnología", "precio": 4200.00, "stock": 12},
    {"id": 2, "codigo": "TEC-002", "nombre": "Teclado Mecánico RGB Devan Switch Blue", "categoria": "Accesorios", "precio": 210.50, "stock": 35},
    {"id": 3, "codigo": "TEC-003", "nombre": "Mouse Inalámbrico Ergonómico Devan Precision", "categoria": "Accesorios", "precio": 95.00, "stock": 50}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevanShop - Maestro de Productos</title>
    <style>
        :root {
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --bg: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
            --success: #10b981;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; }
        body { background-color: var(--bg); color: var(--text-main); padding: 30px 15px; }
        .container { max-width: 1000px; margin: auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { font-size: 2.2rem; color: #818cf8; letter-spacing: -0.5px; }
        .header p { color: var(--text-muted); font-size: 1rem; margin-top: 6px; }
        
        .card { background-color: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 25px; margin-bottom: 30px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3); }
        .card-title { font-size: 1.3rem; margin-bottom: 20px; color: var(--text-main); border-bottom: 1px solid var(--border); padding-bottom: 10px; }
        
        .form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 18px; margin-bottom: 20px; }
        .form-group { display: flex; flex-direction: column; }
        label { font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); margin-bottom: 6px; }
        input, select { background-color: #0f172a; border: 1px solid var(--border); border-radius: 8px; color: var(--text-main); padding: 12px; font-size: 0.95rem; outline: none; transition: all 0.2s; }
        input:focus, select:focus { border-color: var(--primary); box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2); }
        
        .btn-submit { width: 100%; padding: 14px; background-color: var(--primary); color: white; border: none; border-radius: 8px; font-size: 1rem; font-weight: 600; cursor: pointer; transition: background 0.2s; }
        .btn-submit:hover { background-color: var(--primary-hover); }
        
        #mensaje-exito { display: none; background-color: rgba(16, 185, 129, 0.15); border: 1px solid var(--success); color: #34d399; padding: 14px; border-radius: 8px; margin-bottom: 20px; font-weight: 600; text-align: center; }
        
        .table-responsive { overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; text-align: left; }
        th { background-color: #0f172a; color: var(--text-muted); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; padding: 14px 16px; border-bottom: 1px solid var(--border); }
        td { padding: 14px 16px; border-bottom: 1px solid var(--border); font-size: 0.95rem; }
        tr:hover td { background-color: rgba(255, 255, 255, 0.02); }
        .badge { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; background-color: rgba(99, 102, 241, 0.2); color: #a5b4fc; }
        .price { color: #34d399; font-weight: 600; }
        .code-cell { font-family: monospace; font-weight: 700; color: #c7d2fe; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>DevanShop</h1>
            <p>Panel de Administración y Maestro de Productos</p>
        </div>

        <div id="mensaje-exito">¡Producto registrado exitosamente en DevanShop!</div>

        <div class="card">
            <h2 class="card-title">Registrar Nuevo Producto</h2>
            <form id="form-producto">
                <div class="form-grid">
                    <div class="form-group">
                        <label for="codigo">Código del Producto</label>
                        <input type="text" id="codigo" required placeholder="Ej: TEC-004">
                    </div>
                    <div class="form-group">
                        <label for="nombre">Nombre del Producto</label>
                        <input type="text" id="nombre" required placeholder="Ej: Auriculares Inalámbricos 7.1">
                    </div>
                    <div class="form-group">
                        <label for="categoria">Categoría</label>
                        <select id="categoria">
                            <option value="Tecnología">Tecnología</option>
                            <option value="Accesorios">Accesorios</option>
                            <option value="Componentes">Componentes</option>
                            <option value="Audio">Audio</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="precio">Precio (S/.)</label>
                        <input type="number" id="precio" step="0.01" min="0.01" required placeholder="249.90">
                    </div>
                    <div class="form-group">
                        <label for="stock">Stock Disponible</label>
                        <input type="number" id="stock" min="1" required placeholder="20">
                    </div>
                </div>
                <button type="submit" id="btn-guardar" class="btn-submit">Guardar Producto en Catálogo</button>
            </form>
        </div>

        <div class="card">
            <h2 class="card-title">Catálogo Actual (Maestro de Productos)</h2>
            <div class="table-responsive">
                <table id="tabla-productos">
                    <thead>
                        <tr>
                            <th>Código</th>
                            <th>Nombre</th>
                            <th>Categoría</th>
                            <th>Precio</th>
                            <th>Stock</th>
                        </tr>
                    </thead>
                    <tbody id="tbody-productos">
                        <!-- Carga dinámica -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        async function cargarProductos() {
            try {
                const res = await fetch('/api/productos');
                const data = await res.json();
                const tbody = document.getElementById('tbody-productos');
                tbody.innerHTML = '';
                data.forEach(p => {
                    tbody.innerHTML += `
                        <tr>
                            <td class="code-cell">${p.codigo}</td>
                            <td class="col-nombre">${p.nombre}</td>
                            <td><span class="badge">${p.categoria}</span></td>
                            <td class="price">S/. ${parseFloat(p.precio).toFixed(2)}</td>
                            <td>${p.stock} unidades</td>
                        </tr>
                    `;
                });
            } catch (err) {
                console.error("Error al cargar productos:", err);
            }
        }

        document.getElementById('form-producto').addEventListener('submit', async (e) => {
            e.preventDefault();
            const nuevo = {
                codigo: document.getElementById('codigo').value.trim(),
                nombre: document.getElementById('nombre').value.trim(),
                categoria: document.getElementById('categoria').value,
                precio: parseFloat(document.getElementById('precio').value),
                stock: parseInt(document.getElementById('stock').value)
            };

            try {
                const res = await fetch('/api/productos', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(nuevo)
                });

                if (res.ok) {
                    const msg = document.getElementById('mensaje-exito');
                    msg.style.display = 'block';
                    setTimeout(() => msg.style.display = 'none', 3500);
                    document.getElementById('form-producto').reset();
                    cargarProductos();
                }
            } catch (err) {
                alert("Error al conectar con el servidor");
            }
        });

        cargarProductos();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/productos', methods=['GET'])
def get_productos():
    return jsonify(productos)

@app.route('/api/reset', methods=['GET', 'POST'])
def reset_productos():
    global productos
    productos = [
        {"id": 1, "codigo": "TEC-001", "nombre": "Laptop Gamer Devan Pro 16", "categoria": "Tecnología", "precio": 4200.00, "stock": 12},
        {"id": 2, "codigo": "TEC-002", "nombre": "Teclado Mecánico RGB Devan Switch Blue", "categoria": "Accesorios", "precio": 210.50, "stock": 35},
        {"id": 3, "codigo": "TEC-003", "nombre": "Mouse Inalámbrico Ergonómico Devan Precision", "categoria": "Accesorios", "precio": 95.00, "stock": 50}
    ]
    return jsonify({"mensaje": "Catálogo reiniciado exitosamente a los 3 productos base", "total": len(productos)})

@app.route('/api/productos', methods=['POST'])
def add_producto():
    data = request.get_json()
    if not data or not data.get("codigo") or not data.get("nombre"):
        return jsonify({"error": "Datos incompletos"}), 400
    data['id'] = len(productos) + 1
    productos.append(data)
    return jsonify({"mensaje": "Producto agregado a DevanShop", "producto": data}), 201

if __name__ == '__main__':
    print("[*] Servidor DevanShop iniciado en http://localhost:5000")
    app.run(port=5000, debug=True)
