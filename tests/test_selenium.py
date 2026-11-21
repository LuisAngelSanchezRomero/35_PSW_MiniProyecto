import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def test_registro_producto_devanshop():
    """
    Prueba Funcional Automatizada con Selenium para DevanShop:
    1. Abre el navegador y accede al catálogo de DevanShop.
    2. Calcula dinámicamente el siguiente código autoincremental (TEC-004, TEC-005, etc.).
    3. Completa el formulario de registro con datos secuenciales.
    4. Envía el formulario y valida la aparición del mensaje de éxito.
    5. Valida que el nuevo producto aparezca en la tabla del catálogo.
    """
    print("=" * 60)
    print(" INICIANDO PRUEBA FUNCIONAL AUTOMATIZADA - SELENIUM (TEC) ")
    print("=" * 60)
    
    print("[1/5] Inicializando WebDriver de Chrome...")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    
    try:
        url = "http://localhost:5000/"
        print(f"[2/5] Accediendo a la aplicación web: {url}")
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        
        # Validar título de página
        assert "DevanShop" in driver.title
        print(f"      [✓] Título verificado: '{driver.title}'")

        # Esperar que carguen los productos iniciales en la tabla
        time.sleep(1)
        filas_actuales = driver.find_elements(By.CSS_SELECTOR, "#tbody-productos tr")
        total_existentes = len(filas_actuales)
        
        # Calcular siguiente código correlativo TEC-XXX
        siguiente_numero = total_existentes + 1
        codigo_correlativo = f"TEC-{siguiente_numero:03d}"
        nombre_producto = f"Monitor Gamer Devan UltraSync {siguiente_numero}"

        print(f"      [i] Productos existentes en tabla: {total_existentes}")
        print(f"      [i] Código autoincremental generado para la prueba: {codigo_correlativo}")

        producto_prueba = {
            "codigo": codigo_correlativo,
            "nombre": nombre_producto,
            "precio": "1299.90",
            "stock": "14"
        }

        print(f"[3/5] Llenando formulario con {codigo_correlativo} - '{nombre_producto}'...")
        input_codigo = wait.until(EC.presence_of_element_located((By.ID, "codigo")))
        input_codigo.clear()
        input_codigo.send_keys(producto_prueba["codigo"])

        input_nombre = driver.find_element(By.ID, "nombre")
        input_nombre.clear()
        input_nombre.send_keys(producto_prueba["nombre"])

        input_precio = driver.find_element(By.ID, "precio")
        input_precio.clear()
        input_precio.send_keys(producto_prueba["precio"])

        input_stock = driver.find_element(By.ID, "stock")
        input_stock.clear()
        input_stock.send_keys(producto_prueba["stock"])

        time.sleep(1) # Pausa visible para la demostración

        print("[4/5] Enviando formulario (clic en 'Guardar Producto')...")
        btn_guardar = driver.find_element(By.ID, "btn-guardar")
        btn_guardar.click()

        # Validación 1: Mensaje de confirmación
        print("[5/5] Realizando aserciones y validaciones de resultados...")
        mensaje_exito = wait.until(EC.visibility_of_element_located((By.ID, "mensaje-exito")))
        assert "¡Producto registrado exitosamente en DevanShop!" in mensaje_exito.text
        print("      [✓] Aserción 1 superada: Mensaje de confirmación visualizado correctamente.")

        # Validación 2: El producto aparece en la tabla
        time.sleep(1)
        filas_nombres = driver.find_elements(By.CLASS_NAME, "col-nombre")
        nombres_en_tabla = [col.text for col in filas_nombres]
        
        assert producto_prueba["nombre"] in nombres_en_tabla
        print(f"      [✓] Aserción 2 superada: '{producto_prueba['nombre']}' se encuentra presente en la tabla del catálogo.")

        print("\n" + "=" * 60)
        print(f" RESULTADO: PRUEBA CON {codigo_correlativo} COMPLETADA (PASSED) ")
        print("=" * 60)

    except Exception as e:
        print(f"\n[!] ERROR EN LA PRUEBA FUNCIONAL: {e}")
        raise e
    finally:
        time.sleep(2)
        print("[*] Cerrando sesión del navegador...")
        driver.quit()

if __name__ == "__main__":
    test_registro_producto_devanshop()
