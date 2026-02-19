![CI](https://github.com/raMoliner/qa-ui-selenium-saucedemo/actions/workflows/ci.yml/badge.svg)

# QA UI Automation – SauceDemo
**Selenium + Pytest + Allure + GitHub Actions**

Proyecto de automatización UI basado en **Page Object Model (POM)** utilizando Pytest y Selenium WebDriver sobre:
https://www.saucedemo.com

El proyecto incluye ejecución en CI, generación de reporte Allure y publicación automática en GitHub Pages.

---

##  Objetivo

Demostrar buenas prácticas en automatización UI:

- Arquitectura limpia con POM
- Separación clara entre tests y lógica de página
- Manejo de waits explícitos
- Evidencias automáticas en fallos
- Reportes profesionales (Allure)
- CI/CD con GitHub Actions

---

##  Arquitectura

qa-ui-selenium-saucedemo/
│
├── pages/ # Page Objects (locators + acciones)
├── tests/ # Casos de prueba Pytest
├── utils/ # Driver factory y utilidades
├── artifacts/
│ ├── allure-results/ # Resultados crudos
│ ├── allure-report/ # HTML generado
│ └── screenshots/ # Evidencias en fallos
└── .github/workflows/ # CI (GitHub Actions)


---

##  Stack

- Python 3.11
- Pytest
- Selenium WebDriver
- Allure Report
- GitHub Actions (CI/CD)
- GitHub Pages (publicación automática)

---

##  Cobertura actual

### Smoke Tests
- Login válido
- Login inválido (validación de mensaje de error)

### Smoke E2E Checkout
Flujo completo:

login → agregar producto → carrito → checkout → confirmación


Incluye validación de navegación y estados críticos.

---

##  Cómo ejecutar localmente

Crear entorno virtual:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Ejecutar en modo headless (default)

pytest -q

Ejecutar con navegador visible

HEADLESS=0 pytest -q

Ejecutar solo smoke

pytest -q -m smoke

 Allure Report

Generar resultados:

pytest -q --alluredir=artifacts/allure-results

Visualizar reporte local:

allure serve artifacts/allure-results

Reporte publicado automáticamente (CI)

Disponible en:

https://ramoliner.github.io/qa-ui-selenium-saucedemo/

El reporte se genera y publica automáticamente en cada push a main.
 Metadatos profesionales (Allure)

Los tests incluyen:

    Epic

    Feature

    Story

    Severity

    Owner

    Tags

Esto permite visualizar trazabilidad funcional y criticidad dentro del reporte.
 Evidencias

En caso de fallo:

    Screenshot automático

    Resultado registrado en Allure

    Artifact disponible en CI

 Consideraciones de estabilidad

    Modo headless por defecto para evitar prompts nativos del navegador (Password Manager / Leak Detection).

    Uso de WebDriverWait y ExpectedConditions.

    Separación estricta entre test logic y page actions.
