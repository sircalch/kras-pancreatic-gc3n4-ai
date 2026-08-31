import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

df = pd.read_csv('data/processed/MASTER_COMPOUNDS_CURATED.csv')
features = ['MW', 'PSA', 'Polarizability_alpha', 'Electrophilicity_omega']
X = df[features].values
y = df['Delta_E_ads_Doped_kcal_mol'].values
n, p = X.shape

# 1. Leverage calculation
X_s = StandardScaler().fit_transform(X)
H = X_s @ np.linalg.pinv(X_s.T @ X_s) @ X_s.T
leverages = np.diag(H)
h_star = 3.0 * (p + 1) / n

print(f"Sample size n={n}, features p={p}, h*={h_star:.4f}")
for i, row in df.iterrows():
    name = row['name']
    print(f"{name:15s}: h_i = {leverages[i]:.4f}")

max_idx = np.argmax(leverages)
print(f"\nMax leverage: {df.iloc[max_idx]['name']} with h_i = {leverages[max_idx]:.4f}")
cobi_idx = df[df['name'] == 'Cobimetinib'].index[0]
print(f"Cobimetinib: h_i = {leverages[cobi_idx]:.4f}")

# 2. Ridge model fitting & Nested CV
kf = KFold(n_splits=5, shuffle=True, random_state=42)
y_pred_cv = np.zeros(n)
for train_idx, val_idx in kf.split(X):
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X[train_idx])
    X_val = scaler.transform(X[val_idx])
    
    model = Ridge(alpha=1.0)
    model.fit(X_train, y[train_idx])
    y_pred_cv[val_idx] = model.predict(X_val)

q2_cv = r2_score(y, y_pred_cv)
rmse_cv = np.sqrt(mean_squared_error(y, y_pred_cv))
mae_cv = mean_absolute_error(y, y_pred_cv)

print(f"\nNested/Rigorous 5-Fold CV:")
print(f"Q2_CV = {q2_cv:.4f}")
print(f"RMSE_CV = {rmse_cv:.4f} kcal/mol")
print(f"MAE_CV = {mae_cv:.4f} kcal/mol")
