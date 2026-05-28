# Motos usadas en Chile - Prediccion de precios

Scrapee datos de chilemotos.com (como 1000 avisos) para explorar el mercado de motos usadas en Chile y tratar de predecir precios segun año, km y cilindrada.

## Que hay aca

- `src/script_motos_scrap.py` — el scraper con Playwright, recorre todas las paginas del catalogo
- `src/EDA_motos.py` — limpia los datos (los precios vienen escritos como la gente, con puntos y a veces sin los miles) y genera 4 graficos
- `src/modelo_motos.py` — RandomForest para estimar precio
- `src/app_motos.py` — dashboard sencillo con Streamlit
- `data/` — los csv, el crudo y el limpio

## Como corre

```bash
pip install pandas matplotlib scikit-learn streamlit playwright
cd motos-chilemotos
python src/EDA_motos.py      # genera los graficos y el csv limpio
python src/modelo_motos.py   # entrena el modelo y muestra metricas
streamlit run src/app_motos.py  # dashboard interactivo
```

## El modelo

El RandomForest con 300 arboles predice el precio explicando un 82% de la variabilidad (R² en test). Las variables mas importantes son cilindrada (78%), año (14%) y km (8%). El error promedio es de ~$895k (~33%).

Le falta marca y modelo para mejorarlo, pero para ser solo 3 variables no esta mal.
