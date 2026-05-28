import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

st.set_page_config(layout="wide")
st.title("Analisis de Motos Usadas - Chilemotos")

df = pd.read_csv(r'data/motos_limpias.csv', sep=';')

st.sidebar.header("Filtros")
rango_cc = st.sidebar.slider("Cilindrada (cc)", 0, 2000, (0, 2000))
rango_ano = st.sidebar.slider("Ano", 2000, 2026, (2010, 2025))
rango_precio = st.sidebar.slider("Precio (millones)", 0.0, 30.0, (0.0, 30.0))

mask = (
    (df["cilindrada_cc"] >= rango_cc[0]) & (df["cilindrada_cc"] <= rango_cc[1]) &
    (df["ano"] >= rango_ano[0]) & (df["ano"] <= rango_ano[1]) &
    (df["precio_num"] >= rango_precio[0] * 1_000_000) & (df["precio_num"] <= rango_precio[1] * 1_000_000)
)
df_filtrado = df[mask].copy()

st.subheader(f"Datos: {len(df_filtrado)} motos (de {len(df)} totales)")
st.dataframe(df_filtrado[["titulo", "ano", "precio_num", "cilindrada_cc", "km"]].head(20), use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("Precio promedio", f"${df_filtrado['precio_num'].mean()/1_000_000:.2f}M")
col2.metric("Ano promedio", f"{df_filtrado['ano'].mean():.0f}")
col3.metric("Cilindrada promedio", f"{df_filtrado['cilindrada_cc'].mean():.0f} cc")

st.subheader("Graficos")

fig1, ax1 = plt.subplots(figsize=(8, 4))
ax1.scatter(df_filtrado["cilindrada_cc"], df_filtrado["precio_num"] / 1_000_000, alpha=0.4, s=15)
ax1.set_xlabel("Cilindrada (cc)")
ax1.set_ylabel("Precio (millones CLP)")
ax1.set_title("Precio vs Cilindrada")
st.pyplot(fig1)

tabla = df_filtrado.groupby(["rango_cc", "rango_km"], observed=True)["precio_num"].mean().reset_index()
base = tabla[tabla["rango_km"] == "0-10k"][["rango_cc", "precio_num"]].rename(columns={"precio_num": "base"})
tabla = tabla.merge(base, on="rango_cc")
tabla["depreciacion"] = ((tabla["base"] - tabla["precio_num"]) / tabla["base"] * 100).round(1)

fig2, ax2 = plt.subplots(figsize=(8, 4))
for rango in tabla["rango_cc"].unique():
    sub = tabla[tabla["rango_cc"] == rango]
    ax2.plot(sub["rango_km"], sub["depreciacion"], marker="o", label=rango)
ax2.set_xlabel("Rango de kilometraje")
ax2.set_ylabel("Depreciacion promedio (%)")
ax2.set_title("Depreciacion por kilometraje segun cilindrada")
ax2.legend()
st.pyplot(fig2)

st.subheader("Prediccion de Precio")

col_a, col_b, col_c = st.columns(3)
ano_pred = col_a.number_input("Ano", min_value=2000, max_value=2026, value=2020)
km_pred = col_b.number_input("Kilometraje", min_value=0, max_value=200000, value=20000)
cc_pred = col_c.number_input("Cilindrada (cc)", min_value=50, max_value=2000, value=300)

if st.button("Estimar Precio"):
    X = df[["ano", "km", "cilindrada_cc"]].values
    y = df["precio_num"].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    modelo = RandomForestRegressor(n_estimators=300, max_depth=10, random_state=42, n_jobs=-1)
    modelo.fit(X_train, y_train)
    pred = modelo.predict([[ano_pred, km_pred, cc_pred]])
    st.success(f"**Precio estimado: ${pred[0]:,.0f}**")
