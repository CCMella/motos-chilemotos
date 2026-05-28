# Analisis de Motos Usadas - Chilemotos

Scraping, limpieza, analisis exploratorio y modelo de prediccion de precios de motos usadas en Chile, utilizando datos de Chilemotos.com.

## Estructura

```
motos-chilemotos/
├── data/
│   ├── motos_chilemotos.csv   (datos crudos del scraper)
│   └── motos_limpias.csv      (datos limpios para el modelo)
├── src/
│   ├── script_motos_scrap.py  — Scraper con Playwright
│   ├── EDA_motos.py           — Limpieza y graficos exploratorios
│   ├── modelo_motos.py        — RandomForestRegressor
│   └── app_motos.py           — Dashboard con Streamlit
├── .gitignore
└── README.md
```

## Resultados del modelo

| Metrica       | Valor  |
|---------------|--------|
| R² (test)     | 0.815  |
| MAE           | $895k  |
| MAPE          | 33.4%  |

## Como ejecutar

```bash
pip install pandas matplotlib scikit-learn streamlit playwright
cd motos-chilemotos
python src/EDA_motos.py
python src/modelo_motos.py
streamlit run src/app_motos.py
```

## Mejoras futuras

- Extraer marca y modelo del titulo para mejorar la prediccion
- Scrapear periodicamente para detectar cambios de precio
- Probar modelos mas avanzados (XGBoost, redes neuronales)
