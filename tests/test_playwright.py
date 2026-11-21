import time
from playwright.sync_api import sync_playwright

def test_registro_producto_playwright():
    """
    Prueba Funcional Automatizada con Playwright para DevanShop:
    1. Inicia Chromium mediante conexión directa CDP (sin drivers intermediarios).
    2. Navega a http://localhost:5000/.
    3. Cuenta los registros existentes y calcula el siguiente código autoincremental (TEC-004, TEC-005, etc.).
    4. Llena el formulario utilizando selectores modernos y auto-waiting nativo.
    5. Envía el formulario y valida que el elemento y la tabla se actualicen de inmediato.
    """
    print("=" * 60)
    print(" INICIANDO PRUEBA FUNCIONAL AUTOMATIZADA - PLAYWRIGHT (TEC) ")
    print("=" * 60)

    with sync_playwright() as p:
        print("[1/5] Lanzando navegador Chromium...")
        # args=["--start-maximized"] y no_viewport=True permiten que la ventana sea 100% responsiva al redimensionarla
        browser = p.chromium.launch(headless=False, slow_mo=600, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        url = "http://localhost:5000/"
        print(f"[2/5] Navegando a: {url}")
        page.goto(url)

        # Validación del título
        assert "DevanShop" in page.title()
        print(f"      [✓] Título verificado: '{page.title()}'")

        # Esperar a que la tabla cargue los productos iniciales
        page.wait_for_selector("#tbody-productos tr")
        total_existentes = page.locator("#tbody-productos tr").count()
        siguiente_numero = total_existentes + 1
        codigo_correlativo = f"TEC-{siguiente_numero:03d}"
        nombre_producto = f"Silla Gamer Ergonómica Devan Titan {siguiente_numero}"

        print(f"      [i] Productos existentes en tabla: {total_existentes}")
        print(f"      [i] Código autoincremental generado para la prueba: {codigo_correlativo}")

        producto_prueba = {
            "codigo": codigo_correlativo,
            "nombre": nombre_producto,
            "categoria": "Accesorios",
            "precio": "899.00",
            "stock": "6"
        }

        print(f"[3/5] Completando formulario con {codigo_correlativo} (Auto-waiting nativo)...")
        page.fill("#codigo", producto_prueba["codigo"])
        page.fill("#nombre", producto_prueba["nombre"])
        page.select_option("#categoria", producto_prueba["categoria"])
        page.fill("#precio", producto_prueba["precio"])
        page.fill("#stock", producto_prueba["stock"])

        print("[4/5] Haciendo clic en 'Guardar Producto'...")
        page.click("#btn-guardar")

        # Validación 1: Mensaje de confirmación
        print("[5/5] Realizando aserciones automáticas...")
        mensaje = page.locator("#mensaje-exito")
        mensaje.wait_for(state="visible", timeout=5000)
        assert "¡Producto registrado exitosamente en DevanShop!" in mensaje.inner_text()
        print("      [✓] Aserción 1 superada: Mensaje de confirmación visible en pantalla.")

        # Validación 2: El producto aparece en la tabla
        fila_producto = page.locator(f"text={producto_prueba['nombre']}")
        fila_producto.wait_for(state="visible", timeout=5000)
        assert fila_producto.is_visible()
        print(f"      [✓] Aserción 2 superada: '{producto_prueba['nombre']}' con código {codigo_correlativo} en la tabla.")

        print("\n" + "=" * 60)
        print(f" RESULTADO PLAYWRIGHT: PRUEBA CON {codigo_correlativo} COMPLETADA (PASSED) ")
        print("=" * 60)

        time.sleep(2)
        browser.close()

if __name__ == "__main__":
    test_registro_producto_playwright()
