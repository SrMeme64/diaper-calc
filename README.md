# 👶🧓 Calculadora de Pañales (Diaper Calc Cloud SaaS)

![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Render](https://img.shields.io/badge/Cloud_Deploy-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

<img width="1265" height="1600" alt="Diagrama" src="https://github.com/user-attachments/assets/48d4c139-024d-40be-a099-dea5af3dcaf3" />

🌐 **Demo en vivo (Cloud Deployment):** [https://diaper-calc.onrender.com](https://diaper-calc.onrender.com)
🌐 **Documentacion Detallada** [https://drive.google.com/file/d/1iklXPKwPrUg0m6IqkDF8BSd9a8PA_zgs/view?usp=drive_link](https://drive.google.com/file/d/1iklXPKwPrUg0m6IqkDF8BSd9a8PA_zgs/view?usp=drive_link)

---

##  Descripción del Proyecto

**Diaper Calc** es una aplicación web *Full-Stack* contenerizada y orientada a microservicios (*Stateless*) que resuelve el cálculo, pronóstico y presupuesto de abastecimiento de pañales para familias y cuidadores. 

A diferencia de calculadoras estáticas, el sistema implementa un motor de reglas de negocio farmacéuticas y clínicas que distingue entre dos perfiles poblacionales: **Etapa Infantil (0 a 36 meses)** y **Adulto Mayor / Incontinencia**. El backend procesa variables biométricas (peso actual y edad) para pronosticar el consumo diario, proyectar el inventario mensual, calcular el gasto promedio en moneda nacional (MXN) y emitir alertas sanitarias o de salud pediátrica.

---

##  Integrantes del Equipo (Equipo 1)

* **Javier Rodriguez Rodriguez** — *Backend Architecture, Docker Containerization & Cloud CI/CD*
* **Abigail Hernandez Contreras** — *Frontend UI/UX, Responsive Design & Data Visualization*
* **Braiam Augusto Hernandez Cen** — *DevOps, Environment Setup & Business Logic Integration*

---

##  Características Principales

*  **Doble Perfil Poblacional:**
  * **Infantil:** Clasificación clínica en 6 etapas (Etapa 0/RN hasta Etapa 5-6/Entrenamiento) basada en rangos de peso reales de distribución farmacéutica.
  * **Adulto Mayor:** Segmentación por tallas de cintura (CH a XG) y niveles de movilidad/incontinencia (*Leve*, *Moderada*, *Severa*).
*  **Autodetección Biométrica en Vivo:** Predicción instantánea de la etapa infantil en el frontend conforme el usuario ingresa el peso en kilogramos.
*  **Cálculo Desacoplado Peso/Edad:** El peso del paciente determina estrictamente la **talla ideal**, mientras que la edad (en meses) calcula la **frecuencia de evacuaciones diarias** para un abastecimiento hiperpreciso.
*  **Heurística de Alertas Pediátricas:** Evaluación matemática de la relación Peso/Edad para emitir advertencias en tiempo real sobre posible insuficiencia ponderal (bajo peso) o consejos antifugas para pesos elevados.
*  **Visualización de Datos:** Gráficas predictivas en lienzo de **Chart.js** que comparan el gasto financiero de la etapa actual frente al pronóstico económico de las etapas futuras.
*  **Sanitización y Blindaje Anti-Ruido:** Filtros de validación estrictos que bloquean entradas ilógicas o negativas (< 0.5 kg o > 25 kg en bebés) inhabilitando el envío de peticiones erróneas al servidor.
*  **Internacionalización (i18n):** Traducción simultánea en vivo (Español / Inglés) de toda la interfaz, reportes e inventarios sin recargar la página.
*  **Modo Oscuro Nativo:** Interfaz adaptable tipo SaaS con persistencia de tema visual en el almacenamiento local del navegador (`localStorage`).

---

##  Stack Tecnológico y Arquitectura

| Componente | Tecnología | Uso en el Proyecto |
| :--- | :--- | :--- |
| **Backend / API** | Python + FastAPI | Servidor asíncrono, ruteo web y motor de reglas matemáticas |
| **Plantillas / Vista** | Jinja2 Templates | Renderizado dinámico del DOM y paso de variables bilingües |
| **Frontend UI** | HTML5 + CSS3 + Vanilla JS | Maquetado modular responsive y manipulación de estado en vivo |
| **Gráficas** | Chart.js (CDN) | Proyección de barras comparativas de presupuestos mensuales |
| **Contenerización** | Docker (`python:3.9-slim`) | Empaquetado ligero y portable del microservicio |
| **Despliegue Cloud** | Render Web Services | Hosting en la nube bajo infraestructura de contenedores |
| **Automación DevOps** | GitHub Actions | Pipeline CI/CD para despliegue continuo vía Webhooks |

---

## 📈 Historial de Versiones y Evolución del Proyecto

* **Versión 1 (15 de Junio):** Estructura base contenerizada en Docker con servidor local funcional y maquetado HTML preliminar.
* **Versión 2 (22 de Junio):** Integración de FastAPI, segmentación Bebé/Adulto Mayor, reglas farmacéuticas de costos, CSS modular externo y modo oscuro.
* **Versión 3 (29 de Junio):** Despliegue exitoso en la nube a través de Render. Implementación de motor bilingüe de traducción instantánea y separación lógica de cálculo Peso vs. Meses.
* **Versión 4 - Final (6 de Julio):** Incorporación de pipeline CI/CD con GitHub Actions, sistema predictivo visual con Chart.js y motor de alertas de salud pediátrica.

---

## 🐳 Ejecución Local en Contenedores (Docker)

Si deseas levantar el entorno de desarrollo de forma local en tu máquina, asegúrate de tener instalado **Docker Desktop** y sigue estos pasos en tu terminal:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TU-USUARIO/diaper-calc.git](https://github.com/TU-USUARIO/diaper-calc.git)
cd diaper-calc
