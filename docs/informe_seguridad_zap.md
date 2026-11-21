# Informe de Pruebas de Seguridad Web (DAST) bajo Criterios OWASP Top 10

## 1. Información General de la Auditoría
* **Proyecto Evaluado:** DevanShop (Maestro de Productos Web)
* **URL Objetivo:** `http://localhost:5000/`
* **Estándar de Evaluación:** OWASP Top 10 (Open Worldwide Application Security Project)
* **Herramientas Utilizadas:** OWASP ZAP (Zed Attack Proxy) Community v2.15 / Burp Suite Community Edition
* **Modalidad de Prueba:** Dynamic Application Security Testing (DAST) - Caja Negra

---

## 2. Clasificación de Hallazgos según Criterios OWASP Top 10

De acuerdo con la guía oficial de vulnerabilidades OWASP Top 10, los hallazgos detectados durante el escaneo automatizado en DevanShop se categorizan de la siguiente manera:

| Criterio OWASP Top 10 | Vulnerabilidad / Alerta Detectada en ZAP | Riesgo | Estado |
| :--- | :--- | :---: | :---: |
| **A05:2021 – Security Misconfiguration** | Ausencia de Cabecera Anti-Clickjacking (`X-Frame-Options`) | **Medio** | Identificado |
| **A05:2021 – Security Misconfiguration** | Ausencia de Política de Contenido (`Content-Security-Policy`) | **Medio** | Identificado |
| **A05:2021 – Security Misconfiguration** | Omisión de Cabecera defensiva `X-Content-Type-Options: nosniff` | **Bajo** | Identificado |
| **A02:2021 – Cryptographic Failures** | Transmisión HTTP sin cifrado (Falta de HSTS en producción) | **Bajo** | Identificado |
| **A03:2021 – Injection (Prueba de XSS)** | Riesgo de inyección de scripts HTML/JS en formulario de inputs | **Potencial** | Validado con defensas |

---

## 3. Detalle Técnico de Hallazgos, Interpretación y Medidas Preventivas

### Hallazgo 1: Ausencia de Cabecera `X-Frame-Options` (Clickjacking)
* **Criterio OWASP:** **A05:2021 – Security Misconfiguration (CWE-1021)**
* **Interpretación del Hallazgo:**  
  La respuesta HTTP del servidor Flask no incluye la cabecera `X-Frame-Options`. Esto significa que un atacante puede cargar la interfaz de DevanShop dentro de un elemento `<iframe>` transparente en un sitio malicioso. Al hacer esto, el usuario cree interactuar con la página externa cuando en realidad está haciendo clic sobre los botones de DevanShop (ataque de Clickjacking).
* **Medida Preventiva / Remediación:**  
  Configurar el middleware de Flask o el servidor inverso (Nginx) para enviar la cabecera:
  ```http
  X-Frame-Options: DENY
  ```
  O en código Python (Flask):
  ```python
  @app.after_request
  def add_security_headers(response):
      response.headers['X-Frame-Options'] = 'DENY'
      return response
  ```

---

### Hallazgo 2: Ausencia de `Content-Security-Policy` (CSP)
* **Criterio OWASP:** **A05:2021 – Security Misconfiguration (CWE-693) / A03: Injection**
* **Interpretación del Hallazgo:**  
  Al no tener definida una directiva CSP, el navegador web confía en cualquier contenido y script que se ejecute en la página. Si un usuario malicioso lograra inyectar código JavaScript a través de un campo de texto (XSS reflejado o almacenado), el navegador lo ejecutaría sin restricciones, permitiendo el robo de cookies de sesión o la redirección a portales falsos.
* **Medida Preventiva / Remediación:**  
  Establecer una política CSP restrictiva que autorice únicamente la ejecución de scripts locales y fuentes de confianza:
  ```http
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';
  ```

---

### Hallazgo 3: Omisión de `X-Content-Type-Options: nosniff`
* **Criterio OWASP:** **A05:2021 – Security Misconfiguration (CWE-16)**
* **Interpretación del Hallazgo:**  
  Sin esta cabecera, navegadores web antiguos o vulnerables pueden ejecutar *MIME-sniffing*, intentando adivinar el tipo de archivo e interpretando respuestas de texto o imágenes como scripts JavaScript ejecutables.
* **Medida Preventiva / Remediación:**  
  Indicarle al navegador que respete estrictamente el `Content-Type` declarado:
  ```http
  X-Content-Type-Options: nosniff
  ```

---

### Hallazgo 4: Ausencia de HSTS (`Strict-Transport-Security`)
* **Criterio OWASP:** **A02:2021 – Cryptographic Failures (CWE-319)**
* **Interpretación del Hallazgo:**  
  En un despliegue de desarrollo local (HTTP), los datos viajan en texto claro. Al migrar a producción, la falta de HSTS permite ataques de degradación de protocolo (*SSL Striping*).
* **Medida Preventiva / Remediación:**  
  Al activar HTTPS con certificado SSL/TLS en producción, forzar la cabecera HSTS:
  ```http
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  ```

---

## 4. Evidencia Gráfica del Escaneo (Capturas de Pantalla)

1. **Escaneo Automatizado en OWASP ZAP:**  
   *URL objetivo:* `http://localhost:5000/`  
   *Resultado:* Árbol de URLs exploradas y spidering completado con 0 errores de conectividad.
2. **Pestaña de Alertas de OWASP ZAP:**  
   *Alertas de Riesgo Medio (bandera amarilla):* `Missing Anti-clickjacking Header`, `Content Security Policy (CSP) Header Not Set`.  
   *Alertas de Riesgo Bajo (bandera azul):* `X-Content-Type-Options Header Missing`.
