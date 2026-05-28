import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv(r'C:\Users\camil\OneDrive\Escritorio\automatizado\motos_chilemotos\motos_chilemotos.csv', sep=';')

# limpieza
df = df.dropna(subset=["precio"]).copy()

df["precio_num"] = df["precio"].str.replace("$", "", regex=False).str.replace(".", "", regex=False).astype(float)

mask_millones = (df["precio_num"] >= 1) & (df["precio_num"] <= 39)
df.loc[mask_millones, "precio_num"] *= 1_000_000

mask_miles = (df["precio_num"] >= 40) & (df["precio_num"] <= 99_999)
df.loc[mask_miles, "precio_num"] *= 1_000

# limpiar cilindrada (va antes de filtros que la usan)
df = df.dropna(subset=["cilindrada"]).copy()
df["cilindrada_cc"] = pd.to_numeric(df["cilindrada"], errors="coerce")
df = df.dropna(subset=["cilindrada_cc"]).copy()
df.loc[df["cilindrada_cc"] < 30, "cilindrada_cc"] *= 1000
df = df[df["cilindrada_cc"] > 0].copy()

# eliminar basura y precios irreales
df = df[df["precio_num"] < 50_000_000]
# filtros de precio por cilindrada
mask_ok = (
    ((df["cilindrada_cc"] < 200) & (df["precio_num"].between(500_000, 6_000_000))) |
    ((df["cilindrada_cc"] >= 200) & (df["cilindrada_cc"] < 500) & (df["precio_num"].between(1_000_000, 15_000_000))) |
    ((df["cilindrada_cc"] >= 500) & (df["precio_num"] < 50_000_000))
)
df = df[mask_ok].copy()
# casos puntuales con datos corruptos
df = df[df["url"] != "https://www.chilemotos.com/moto/55502/"]
df = df[df["url"] != "https://www.chilemotos.com/moto/65454/"]
df = df[df["url"] != "https://www.chilemotos.com/moto/51950/"]

# relacion precio vs cilindrada
fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(df["cilindrada_cc"], df["precio_num"] / 1_000_000, alpha=0.4, s=20)
ax.set_xlabel("Cilindrada (cc)")
ax.set_ylabel("Precio (millones CLP)")
ax.set_title("Precio vs Cilindrada")
ax.set_xticks(range(0, 2600, 200))
ax.set_xlim(0, 2500)
ax.set_ylim(0, 30)
plt.tight_layout()
plt.show()

# limpiar kilometraje
df = df.dropna(subset=["kilometraje"]).copy()
df["km"] = pd.to_numeric(df["kilometraje"], errors="coerce")

# km vs precio, separado por cilindrada
df["rango_cc"] = pd.cut(df["cilindrada_cc"], bins=[0, 200, 500, 1000, 9999], labels=["0-200cc", "201-500cc", "501-1000cc", "1000cc+"])

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
for ax, (rango, grupo) in zip(axes.flat, df.groupby("rango_cc", observed=True)):
    ax.scatter(grupo["km"], grupo["precio_num"] / 1_000_000, alpha=0.4, s=15)
    ax.set_title(rango)
    ax.set_xlabel("Kilometraje")
    ax.set_ylabel("Precio (millones)")
    ax.set_xlim(0, 100000)

plt.tight_layout()
plt.show()

# depreciacion porcentual por km segun cilindrada
df["rango_km"] = pd.cut(df["km"], bins=[0, 10000, 30000, 50000, 999999], labels=["0-10k", "10k-30k", "30k-50k", "50k+"])

tabla = df.groupby(["rango_cc", "rango_km"], observed=True)["precio_num"].mean().reset_index()
base = tabla[tabla["rango_km"] == "0-10k"][["rango_cc", "precio_num"]].rename(columns={"precio_num": "base"})
tabla = tabla.merge(base, on="rango_cc")
tabla["depreciacion"] = ((tabla["base"] - tabla["precio_num"]) / tabla["base"] * 100).round(1)

fig, ax = plt.subplots(figsize=(10, 5))
for rango in tabla["rango_cc"].unique():
    sub = tabla[tabla["rango_cc"] == rango]
    ax.plot(sub["rango_km"], sub["depreciacion"], marker="o", label=rango)
ax.set_xlabel("Rango de kilometraje")
ax.set_ylabel("Depreciacion promedio (%)")
ax.set_title("Depreciacion por kilometraje segun cilindrada")
ax.legend()
plt.tight_layout()
plt.show()

# año vs precio (scatter por cilindrada)
df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
df = df.dropna(subset=["ano"]).copy()
df = df[(df["ano"] >= 2000) & (df["ano"] <= 2026)].copy()

fig, ax = plt.subplots(figsize=(10, 5))
colores = {"0-200cc": "#1f77b4", "201-500cc": "#ff7f0e", "501-1000cc": "#2ca02c", "1000cc+": "#d62728"}
for rango in df["rango_cc"].unique():
    sub = df[df["rango_cc"] == rango]
    ax.scatter(sub["ano"], sub["precio_num"] / 1_000_000, alpha=0.3, s=10, label=rango, color=colores.get(rango))
ax.set_xlabel("Año")
ax.set_ylabel("Precio (millones CLP)")
ax.set_title("Precio por año de fabricacion")
ax.legend()
plt.tight_layout()
plt.show()

print(f"\nResumen final: {len(df)} motos listas para analisis")
print(f"Rango de años: {int(df['ano'].min())} - {int(df['ano'].max())}")
print(f"Precio promedio: ${df['precio_num'].mean()/1_000_000:.2f}M CLP")

# guardar datos limpios
salida = r'C:\Users\camil\OneDrive\Escritorio\automatizado\motos_chilemotos\motos_limpias.csv'
try:
    df.to_csv(salida, sep=';', index=False)
    print(f"Datos limpios guardados en {salida}")
except PermissionError:
    salida = r'C:\Users\camil\OneDrive\Escritorio\automatizado\motos_chilemotos\motos_limpias_v2.csv'
    df.to_csv(salida, sep=';', index=False)
    print(f"Archivo original ocupado. Guardado como motos_limpias_v2.csv")

