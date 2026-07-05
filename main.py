import json
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, "res": None, "perfil_seleccionado": "bebe", "lang_actual": "es"
    })

@app.post("/calcular")
async def calcular_stock(
    request: Request,
    perfil: str = Form("bebe"),
    peso_bebe: float = Form(7.0),
    peso_adulto: float = Form(70.0),
    meses: int = Form(0),
    grado_incontinencia: str = Form("moderada"),
    lang: str = Form("es")
):
    res = {}

    if perfil == "bebe":
        peso = peso_bebe
        
        # 1. EVALUACIÓN DE TALLAS Y ETAPAS
        if peso <= 4.5:
            etapa = {"es": "Etapa 0 (Recién nacido)", "en": "Stage 0 (Newborn)"}
            talla = {"es": "RN / P", "en": "RN / P"}
            tip = {"es": "No compres en grandes cantidades. Crecen rapidísimo.", "en": "Don't buy in bulk. They grow fast."}
            costo_u, et_idx = 4.50, 0
        elif peso <= 8.0:
            etapa = {"es": "Etapa 1 (Lactante temprano)", "en": "Stage 1 (Early Infant)"}
            talla = {"es": "S / CH", "en": "S / CH"}
            tip = {"es": "Gana peso rápido. Compra de forma moderada.", "en": "Fast weight gain. Buy moderately."}
            costo_u, et_idx = 5.20, 1
        elif peso <= 11.0:
            etapa = {"es": "Etapa 2 (Bebé en desarrollo)", "en": "Stage 2 (Growing Baby)"}
            talla = {"es": "M / Med", "en": "M / Med"}
            tip = {"es": "Un pañal bien ajustado aquí otorga hasta 2 horas más de sueño.", "en": "Well-fitted diapers give up to 2 extra hours of sleep."}
            costo_u, et_idx = 6.10, 2
        elif peso <= 14.0:
            etapa = {"es": "Etapa 3 (Gateo)", "en": "Stage 3 (Crawling)"}
            talla = {"es": "G / Grande", "en": "G / Grande"}
            tip = {"es": "Un buen ajuste en el gateo reduce el riesgo de dermatitis en un 70%.", "en": "Good crawling fit reduces diaper rash risk by 70%."}
            costo_u, et_idx = 6.90, 3
        elif peso <= 16.0:
            etapa = {"es": "Etapa 4 (Primeros pasos)", "en": "Stage 4 (First Steps)"}
            talla = {"es": "XG / J", "en": "XG / J"}
            tip = {"es": "Pásate a formato calzoncito (Pull-up) para mayor movilidad.", "en": "Switch to pull-up pants for mobility."}
            costo_u, et_idx = 7.80, 4
        else:
            etapa = {"es": "Etapa 5-6 (Entrenamiento de baño)", "en": "Stage 5-6 (Potty Training)"}
            talla = {"es": "XXG / XJ", "en": "XXG / XJ"}
            tip = {"es": "Usa calzoncillos entrenadores. No regreses al pañal tradicional.", "en": "Use training pants. Don't go back to standard diapers."}
            costo_u, et_idx = 8.90, 5

        # 2. EVALUACIÓN DE CONSUMO DIARIO
        if meses == 0 and peso <= 4.5: diarios = 11
        elif meses <= 1: diarios = 11
        elif meses <= 3: diarios = 9
        elif meses <= 8: diarios = 7
        elif meses <= 12: diarios = 6
        elif meses <= 24: diarios = 5
        else: diarios = 4

        # 3. ALERTA CLÍNICA DE PESO (Heurística Pediátrica)
        alerta = None
        # Cálculo de peso mínimo esperado (aprox. percentil 3) según meses
        peso_min_esperado = 2.5 + (meses * 0.42) if meses <= 12 else 7.5 + ((meses - 12) * 0.18)
        if peso < (peso_min_esperado * 0.82):
            alerta = {
                "tipo": "peligro",
                "es": f"⚠️ ALERTA CLÍNICA: El peso ({peso} kg) es bajo para {meses} meses de edad. Sugerimos valoración pediátrica.",
                "en": f"⚠️ CLINICAL ALERT: Weight ({peso} kg) is low for {meses} months old. Pediatric assessment suggested."
            }
        elif peso > (peso_min_esperado * 2.2) and meses > 2:
            alerta = {
                "tipo": "aviso",
                "es": f"ℹ️ NOTA: Peso elevado ({peso} kg) para la edad. Verifique el ajuste en los muslos para evitar fugas.",
                "en": f"ℹ️ NOTE: High weight ({peso} kg) for age. Check thigh fit to prevent leakage."
            }

        # 4. DATOS PARA LA GRÁFICA PREDICTIVA (Gasto mensual por etapa)
        labels_es = ["Etapa 0 (RN)", "Etapa 1 (S)", "Etapa 2 (M)", "Etapa 3 (G)", "Etapa 4 (XG)", "Etapa 5/6 (XXG)"]
        labels_en = ["Stage 0 (NB)", "Stage 1 (S)", "Stage 2 (M)", "Stage 3 (L)", "Stage 4 (XL)", "Stage 5/6 (XXL)"]
        # Promedio mensual estimado en pesos (MXN) para cada etapa
        costos_grafica = [11*30*4.50, 9*30*5.20, 7*30*6.10, 6*30*6.90, 5*30*7.80, 4*30*8.90]

        mensuales = diarios * 30
        gasto = mensuales * costo_u
        res = {
            "is_adult": False,
            "tipo": {"es": "Infantil", "en": "Infant"}, 
            "etapa": etapa, "talla": talla,
            "diarios": diarios, "mensuales": mensuales, "gasto_mensual": f"${gasto:,.2f} MXN",
            "tip": tip,
            "alerta": alerta,
            "chart_data": json.dumps({
                "labels_es": labels_es, "labels_en": labels_en,
                "data": costos_grafica, "current_idx": et_idx
            })
        }
        peso_ret = peso_bebe

    else:
        # LÓGICA DE ADULTO
        peso = peso_adulto
        if peso <= 60: talla = {"es": "Chica (CH)", "en": "Small (CH)"}
        elif peso <= 85: talla = {"es": "Mediana (M)", "en": "Medium (M)"}
        elif peso <= 100: talla = {"es": "Grande (G)", "en": "Large (G)"}
        else: talla = {"es": "Extra Grande (XG)", "en": "Extra Large (XG)"}

        if grado_incontinencia == "leve": 
            diarios, costo_u = 3, 14.00
            etapa_str = {"es": "Incontinencia LEVE", "en": "Incontinence LIGHT"}
        elif grado_incontinencia == "moderada": 
            diarios, costo_u = 4, 17.50
            etapa_str = {"es": "Incontinencia MODERADA", "en": "Incontinence MODERATE"}
        else: 
            diarios, costo_u = 6, 21.00
            etapa_str = {"es": "Incontinencia SEVERA", "en": "Incontinence SEVERE"}

        mensuales = diarios * 30
        gasto = mensuales * costo_u
        res = {
            "is_adult": True,
            "tipo": {"es": "Adulto Mayor", "en": "Senior"},
            "etapa": etapa_str, "talla": talla, 
            "diarios": diarios, "mensuales": mensuales, "gasto_mensual": f"${gasto:,.2f} MXN",
            "tip": {"es": "Aplicar crema protectora con óxido de zinc.", "en": "Apply zinc oxide barrier cream."},
            "alerta": None, "chart_data": None
        }
        peso_ret = peso_adulto

    return templates.TemplateResponse("index.html", {
        "request": request, "res": res, "perfil_seleccionado": perfil,
        "peso_ingresado": peso_ret, "meses_ingresados": meses, "lang_actual": lang
    })
