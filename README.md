![CI](https://github.com/raMoliner/qa-ui-selenium-saucedemo/actions/workflows/ci.yml/badge.svg)

# QA UI Automation - SauceDemo (Selenium + Pytest, Python)

Proyecto de automatización UI usando Page Object Model (POM) y Pytest sobre https://www.saucedemo.com

## Stack
- Python + Pytest
- Selenium WebDriver
- POM (pages/)
- Evidencias: screenshots automáticos en fallos (artifacts/)

## Qué cubre
- Smoke Login (válido / inválido)
- Smoke E2E Checkout: login → agregar producto → carrito → checkout → confirmación

## Cómo ejecutar
Crear venv e instalar dependencias:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Run (headless):
pytest -q

## Run con navegador visible:
HEADLESS=0 pytest -q

## Run solo smoke:
pytest -q -m smoke


Notas de estabilidad

Headless es el default para evitar prompts nativos del navegador (Password Manager/Leak Detection) que no pertenecen al DOM y pueden interferir con tests UI.

En fallos, se guarda screenshot automáticamente en artifacts/screenshots/.


## Allure Report

pytest -q --alluredir=artifacts/allure-results

Open report:

allure serve artifacts/allure-results
