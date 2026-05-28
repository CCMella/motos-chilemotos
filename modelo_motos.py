import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split

df = pd.read_csv(r'C:\Users\camil\OneDrive\Escritorio\automatizado\motos_chilemotos\motos_limpias.csv', sep=';')

print(f"Datos cargados: {len(df)} motos")

X = df[["ano", "km", "cilindrada_cc"]].values
y = df["precio_num"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

modelo = RandomForestRegressor(n_estimators=300, max_depth=10, random_state=42, n_jobs=-1)
modelo.fit(X_train, y_train)

y_train_pred = modelo.predict(X_train)
y_test_pred = modelo.predict(X_test)

importancia = modelo.feature_importances_
print(f"\nImportancia:")
print(f"  año:        {importancia[0]:.1%}")
print(f"  km:         {importancia[1]:.1%}")
print(f"  cilindrada: {importancia[2]:.1%}")
print(f"\nR² entrenamiento (70%): {r2_score(y_train, y_train_pred):.3f}")
print(f"R² prueba      (30%): {r2_score(y_test, y_test_pred):.3f}")

mae = mean_absolute_error(y_test, y_test_pred)
mape = (abs(y_test - y_test_pred) / y_test).mean() * 100
print(f"Error absoluto medio (MAE): ${mae:,.0f}")
print(f"Error porcentual medio (MAPE): {mape:.1f}%")

print(f"\nPrediccion moto 2020 con 20.000 km y 150cc:")
pred = modelo.predict([[2020, 20000, 150]])
print(f"  Precio estimado: ${pred[0]:,.0f}")
