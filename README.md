# Analisis de Motos Usadas - Chilemotos

Scraping, limpieza, analisis exploratorio y modelo de prediccion de precios de motos usadas en Chile, utilizando datos de Chilemotos.com.

## Scripts

- `script_motos_scrap.py` — Scraper con Playwright que recorre las 100 paginas del catalogo y guarda los datos en CSV.
- `EDA_motos.py` — Limpieza de datos (precios mal escritos, unidades de cilindrada inconsistentes, outliers) y 4 graficos exploratorios.
- `modelo_motos.py` — RandomForestRegressor para predecir precio en funcion de ano, kilometraje y cilindrada. Evaluacion con R², MAE y MAPE.
- `app_motos.py` — Dashboard interactivo con Streamlit.

## Resultados del modelo

| Metrica       | Valor  |
|---------------|--------|
| R² (test)     | 0.815  |
| MAE           | $895k  |
| MAPE          | 33.4%  |

## Como ejecutar

```bash
pip install pandas matplotlib scikit-learn streamlit playwright
python EDA_motos.py
python modelo_motos.py
streamlit run app_motos.py
```

## Mejoras futuras

- Extraer marca y modelo del titulo para mejorar la prediccion
- Scrapear periodicamente para detectar cambios de precio
- Probar modelos mas avanzados (XGBoost, redes neuronales)
