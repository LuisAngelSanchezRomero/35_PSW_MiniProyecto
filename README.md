# DevanShop - Mini Proyecto de Automatización QA y Seguridad Web (Criterios OWASP)

Bienvenido al repositorio de **DevanShop**, un proyecto académico desarrollado para simular un maestro de productos web, automatizar pruebas funcionales con **Selenium WebDriver** y **Playwright**, y ejecutar análisis dinámicos de seguridad bajo los **Criterios de Vulnerabilidad OWASP Top 10** utilizando **OWASP ZAP**.

---

## Estructura del Proyecto

```text
DevanShop/
│
├── app/
│   └── app.py                     # Aplicación web (Backend Flask + Frontend UI)
│
├── tests/
│   ├── test_selenium.py           # Script de prueba funcional automatizada (Selenium)
│   └── test_playwright.py         # Script de prueba funcional automatizada (Playwright)
│
├── docs/
│   └── informe_seguridad_zap.md   # Informe DAST bajo criterios OWASP Top 10
│
├── requirements.txt               # Dependencias de Python (Flask, Selenium, Playwright)
└── README.md                      # Documentación principal del repositorio
```

---

## Requisitos Previos

* **Python 3.10 o superior**
* **Google Chrome** instalado en el sistema
* **OWASP ZAP** (Zed Attack Proxy) o Burp Suite Community

---

## Instalación y Configuración

1. **Abrir la terminal en la carpeta `DevanShop`:**
   ```bash
   cd DevanShop
   ```

2. **Instalar dependencias de Python:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Instalar los navegadores de Playwright (solo la primera vez):**
   ```bash
   playwright install chromium
   ```

---

## Paso a Paso de Ejecución (En Orden)

### PASO 1: Iniciar la Aplicación Web (DevanShop)
En una terminal:
```bash
python app/app.py
```
* Servidor activo en: **`http://localhost:5000/`**
* Muestra el panel interactivo de DevanShop con el formulario del maestro de productos y la tabla de catálogo.

---

### PASO 2: Ejecutar la Prueba Funcional con Selenium
Con `app.py` corriendo, en **otra terminal** ejecuta:
```bash
python tests/test_selenium.py
```
* Selenium abrirá Chrome automáticamente, completará los campos (código, nombre, precio, stock), presionará guardar, validará el mensaje de confirmación y comprobará que el nuevo producto aparezca en la tabla (`PASSED`).

---

### PASO 3: Ejecutar la Prueba Funcional con Playwright
Con `app.py` corriendo, ejecuta:
```bash
python tests/test_playwright.py
```
* Playwright abrirá Chromium a alta velocidad mediante CDP (Chrome DevTools Protocol) con *auto-waiting* nativo, ejecutará el registro y validará los resultados.

---

### PASO 4: Prueba de Seguridad con OWASP ZAP bajo Criterios OWASP
1. Inicia **OWASP ZAP**.
2. Con `http://localhost:5000/` activo, ve a **Automated Scan**.
3. Ingresa la URL: `http://localhost:5000/` y pulsa **Attack**.
4. Revisa los hallazgos en la pestaña **Alerts** clasificados según el OWASP Top 10:
   * **A05:2021 – Security Misconfiguration**: Falta de cabeceras `X-Frame-Options`, `Content-Security-Policy` y `X-Content-Type-Options`.
   * **A02:2021 – Cryptographic Failures**: Transmisión sin cifrado HSTS.
5. Consulta el informe detallado con interpretaciones y medidas preventivas en:  
   [`docs/informe_seguridad_zap.md`](docs/informe_seguridad_zap.md).

---

### PASO 5: Grabación del Video y Conclusiones
* Realizar la sustentación con cámara activa explicando el objetivo, la construcción y los resultados de las pruebas realizadas, así como las conclusiones sobre la importancia de las pruebas de software y la seguridad web.
