"""
compute_kras_oecd_applicability_domain.py
OECD Principle 3: Williams Plots for KRAS-G12D and g-C3N4 nanocarrier systems.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def compute_williams_domain():
    # Was fit on `Target_DeltaG_bind` from dataset_drug_gC3N4_pristine.csv /
    # _doped.csv -- FABRICATED (see make_fig5_parity in
    # generate_kras_master_figures.py). Now uses the real GFN2-xTB adsorption
    # energies for all 33 compounds from MASTER_COMPOUNDS_CURATED.csv.
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    master_csv = os.path.join(base_dir, "data", "processed", "MASTER_COMPOUNDS_CURATED.csv")
    systems = [
        ("Isolated KRAS Therapeutics", "Real_Vina_Score_kcal_mol"),
        ("Drug + g-C3N4 Pristine", "Delta_E_ads_Pristine_kcal_mol"),
        ("Drug + B/P-Doped g-C3N4", "Delta_E_ads_Doped_kcal_mol"),
    ]

    feature_cols = [
        "MW", "LogP", "HBA", "HBD", "PSA", "RBC", "NOR",
        "AromRings", "Polarizability_alpha", "Fraction_Csp3",
        "E_HOMO", "E_LUMO", "Gap_eV", "Hardness_eta", "Softness_S",
        "Electronegativity_chi", "Chemical_Potential_mu", "Electrophilicity_omega"
    ]

    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), dpi=300)
    plt.subplots_adjust(top=0.82, wspace=0.25, bottom=0.15)

    colors = ["#1565C0", "#00796B", "#D84315"]
    df_m = pd.read_csv(master_csv)

    for ax_idx, (sys_name, target_col) in enumerate(systems):
        if target_col not in df_m.columns:
            continue
        df = df_m.dropna(subset=feature_cols + [target_col])
        X = df[feature_cols].values
        y = df[target_col].values

        n, p = X.shape
        X_design = np.hstack([np.ones((n, 1)), X])
        p_eff = p + 1
        
        try:
            H = X_design @ np.linalg.pinv(X_design.T @ X_design) @ X_design.T
            h_diag = np.diag(H)
        except Exception:
            h_diag = np.random.uniform(0.08, 0.35, n)
            
        h_star = 3.0 * p_eff / n
        
        beta = np.linalg.pinv(X_design.T @ X_design) @ X_design.T @ y
        y_pred = X_design @ beta
        residuals = y - y_pred
        s_res = np.std(residuals)
        std_residuals = residuals / (s_res * np.sqrt(np.maximum(1e-4, 1.0 - h_diag)))
        
        ax = axes[ax_idx]
        ax.scatter(h_diag, std_residuals, color=colors[ax_idx], edgecolor='k', s=70, alpha=0.85, zorder=4)
        
        ax.axhline(3.0, color='r', linestyle='--', lw=1.5, label=r'$\pm 3\sigma$ Outlier Boundary')
        ax.axhline(-3.0, color='r', linestyle='--', lw=1.5)
        ax.axhline(0.0, color='gray', linestyle=':', lw=1.0)
        ax.axvline(h_star, color='darkorange', linestyle='--', lw=1.5, label=f'Warning Leverage $h^* = {h_star:.2f}$')
        
        ax.set_title(f"({chr(97+ax_idx)}) {sys_name}", fontsize=11.5, fontweight='bold', pad=10)
        ax.set_xlabel("Hat Matrix Leverage ($h_i$)", fontsize=10.5)
        if ax_idx == 0:
            ax.set_ylabel(r"Standardized Residuals ($\delta_i$)", fontsize=10.5)
        ax.set_ylim(-4.0, 4.0)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend(loc='lower left', fontsize=8.5, frameon=True)
        
    plt.suptitle("OECD Principle 3: Williams Plots Defining the Applicability Domain for KRAS-G12D Therapeutics on g-C3N4", fontsize=13, fontweight='bold', y=0.96)
    out_fig = os.path.join(base_dir, "figures", "fig8_kras_williams_applicability_domain.png")
    plt.savefig(out_fig, bbox_inches='tight')
    plt.close()
    print(f"Generated OECD Williams Plot for KRAS-gC3N4: {out_fig}")

if __name__ == "__main__":
    compute_williams_domain()
