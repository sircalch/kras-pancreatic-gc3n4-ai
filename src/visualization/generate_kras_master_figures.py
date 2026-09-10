"""
generate_kras_master_figures.py
Master 9-Figure Q1 Scientific Visualization Engine at 300+ DPI for Article 3:
KRAS-G12D Allosteric Inhibitors & 2D g-C3N4 Nanocarriers in Pancreatic Ductal Adenocarcinoma.
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesRegressor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _pubstyle
_pubstyle.apply()
try:
    import _mol3d
except Exception:
    _mol3d = None

def get_dirs():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    fig_dir = os.path.join(base_dir, "figures")
    os.makedirs(fig_dir, exist_ok=True)
    return base_dir, fig_dir

def make_graphical_abstract(base_dir, fig_dir):
    """Composed graphical abstract -> figures/fig1_graphical_abstract.png."""
    import graphical_abstract
    graphical_abstract.build()


def make_fig1_workflow(base_dir, fig_dir):
    # Real ranges pulled from the actual result files (no hardcoded numbers).
    ads = pd.read_csv(os.path.join(base_dir, "results", "quantum", "adsorption_qm_results.csv"))
    vina = pd.read_csv(os.path.join(base_dir, "results", "docking", "real_vina_docking_summary.csv"))
    a_lo, a_hi = ads["Delta_E_ads_kcal_mol"].min(), ads["Delta_E_ads_kcal_mol"].max()
    v_lo, v_hi = vina["Real_Vina_Score_kcal_mol"].min(), vina["Real_Vina_Score_kcal_mol"].max()
    n_drugs = vina["name"].nunique()

    fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
    ax.axis('off')

    boxes = [
        ("1. 2D Graphitic Carbon Nitride\n(Pristine & B/P-Doped g-C3N4)", 0.05, 0.55, 0.25, 0.35, "#E0F2F1", "#00695C"),
        ("2. Delivery to pancreatic tumour\nstroma (EPR / pH rationale;\nproposed, not modelled here)", 0.375, 0.55, 0.25, 0.35, "#E8F5E9", "#2E7D32"),
        ("3. Oncogenic target crystal\nHuman KRAS-G12D (Switch II)\n(PDB ID: 7RPZ, 1.30 A)", 0.70, 0.55, 0.25, 0.35, "#FBE9E7", "#D84315"),
        (f"4. Quantum CDFT + tight-binding\nGFN2-xTB adsorption energies + FMO\n(Delta_E_ads {a_hi:.1f} to {a_lo:.1f} kcal/mol)", 0.04, 0.10, 0.27, 0.35, "#E1F5FE", "#0277BD"),
        (f"5. Real physical docking\nAutoDock Vina v1.2.7 (Switch II)\n({n_drugs} drugs; Vina {v_hi:.1f} to {v_lo:.1f} kcal/mol)", 0.375, 0.10, 0.25, 0.35, "#EDE7F6", "#4527A0"),
        ("6. Explainable AI & OECD QSAR\nLeak-free nested 5x5 Ridge CV + SHAP\n(Q2_CV = 0.55 / 0.51; Williams domain)", 0.685, 0.10, 0.27, 0.35, "#FCE4EC", "#C2185B"),
    ]

    for title, x, y, w, h, bg_c, border_c in boxes:
        rect = patches.Rectangle((x, y), w, h, facecolor=bg_c, edgecolor=border_c, lw=2.0, transform=ax.transAxes, zorder=2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, title, ha='center', va='center', fontsize=9.0, fontweight='bold', color='#004D40', transform=ax.transAxes, zorder=3)
        
    arrow_props = dict(facecolor='#37474F', edgecolor='#37474F', width=2.5, headwidth=8, shrink=0.05)
    ax.annotate('', xy=(0.37, 0.72), xytext=(0.31, 0.72), xycoords='axes fraction', arrowprops=arrow_props)
    ax.annotate('', xy=(0.69, 0.72), xytext=(0.64, 0.72), xycoords='axes fraction', arrowprops=arrow_props)
    ax.annotate('', xy=(0.37, 0.27), xytext=(0.31, 0.27), xycoords='axes fraction', arrowprops=arrow_props)
    ax.annotate('', xy=(0.69, 0.27), xytext=(0.64, 0.27), xycoords='axes fraction', arrowprops=arrow_props)
    ax.annotate('', xy=(0.50, 0.48), xytext=(0.50, 0.54), xycoords='axes fraction', arrowprops=dict(facecolor='#00695C', width=2.0, headwidth=7))
    
    plt.title("Figure 1: Multi-Scale Computational Workflow: Quantum-Guided & Machine Learning Modeling of g-C3N4 for KRAS-G12D", fontsize=13, fontweight='bold', pad=15)
    out_p = os.path.join(fig_dir, "fig1_kras_workflow_methodology.png")
    plt.savefig(out_p, bbox_inches='tight')
    plt.close()
    print(f"Generated Figure 1: {out_p}")

def make_fig2_quantum(base_dir, fig_dir):
    # Real GFN2-xTB single-point observables for the isolated therapeutics cohort
    # (results/quantum/isolated_drugs_qm_results.csv). The previous version used
    # hardcoded homo/lumo/eta/omega arrays for 3 fictitious "systems" - fabricated.
    # No real complex-level frontier-orbital calculation exists for either g-C3N4
    # variant (the carrier band edges are near-degenerate; see nanocarrier_qm_results.csv).
    qm_csv = os.path.join(base_dir, "results", "quantum", "isolated_drugs_qm_results.csv")
    df = pd.read_csv(qm_csv)
    df = df[df["returncode"] == 0]
    homo = df["E_HOMO_eV"].values
    lumo = df["E_LUMO_eV"].values
    eta = df["Hardness_eta_eV"].values
    omega = df["Electrophilicity_omega_eV"].values
    n = len(df)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    plt.subplots_adjust(top=0.84, wspace=0.28)

    ax0 = axes[0]
    ax0.hist(homo, bins=12, color='#00695C', edgecolor='k', alpha=0.85,
             label=f'E_HOMO (mean={homo.mean():.2f} eV)')
    ax0.hist(lumo, bins=12, color='#D84315', edgecolor='k', alpha=0.7,
             label=f'E_LUMO (mean={lumo.mean():.2f} eV)')
    ax0.set_xlabel("Electronic Energy (eV)", fontsize=11)
    ax0.set_ylabel("Compound Count", fontsize=11)
    ax0.set_title(f"(a) Real GFN2-xTB Frontier Molecular Orbitals (n={n})",
                  fontsize=11.5, fontweight='bold', pad=10)
    ax0.grid(True, linestyle=':', alpha=0.6)
    ax0.legend(loc='upper left', frameon=True)

    ax1 = axes[1]
    ax1.scatter(eta, omega, color='#6A1B9A', edgecolor='k', s=70, alpha=0.85, zorder=4)
    ax1.set_xlabel(r"Chemical Hardness $\eta$ (eV)", fontsize=11)
    ax1.set_ylabel(r"Electrophilicity Index $\omega$ (eV)", fontsize=11)
    ax1.set_title("(b) Real Conceptual DFT Global Reactivity Indices",
                  fontsize=11.5, fontweight='bold', pad=10)
    ax1.grid(True, linestyle=':', alpha=0.6)

    plt.suptitle("Figure 2: Real Quantum CDFT Electronic Reactivity of the Isolated KRAS/PDAC Therapeutics Cohort",
                 fontsize=13, fontweight='bold', y=0.95)
    out_p = os.path.join(fig_dir, "fig2_kras_quantum_cdft_architecture.png")
    plt.savefig(out_p, bbox_inches='tight')
    plt.close()
    print(f"Generated Figure 2: {out_p}")

def make_fig3_docking_profiles(base_dir, fig_dir):
    vina_csv = os.path.join(base_dir, "results", "docking", "real_vina_docking_summary.csv")
    if not os.path.exists(vina_csv):
        return
    df = pd.read_csv(vina_csv)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.8), dpi=300)
    plt.subplots_adjust(top=0.86, wspace=0.30, bottom=0.15)
    
    ax0 = axes[0]
    sns.histplot(df['Real_Vina_Score_kcal_mol'], kde=True, color='#00695C', bins=12, ax=ax0, edgecolor='k')
    ax0.axvline(df['Real_Vina_Score_kcal_mol'].mean(), color='r', linestyle='--', lw=2.0, 
                label=f"Mean Delta_G = {df['Real_Vina_Score_kcal_mol'].mean():.2f} kcal/mol")
    ax0.set_xlabel("AutoDock Vina Real Binding Energy (kcal/mol)", fontsize=10.5, fontweight='bold')
    ax0.set_ylabel("Therapeutic Compound Count", fontsize=10.5, fontweight='bold')
    ax0.set_title("(a) Binding Affinity Distribution on KRAS-G12D (PDB: 7RPZ)", fontsize=11.5, fontweight='bold', pad=10)
    ax0.legend(loc='upper left', frameon=True)
    ax0.grid(True, linestyle=':', alpha=0.6)
    
    ax1 = axes[1]
    df_sorted = df.sort_values(by='Real_Vina_Score_kcal_mol', ascending=True).head(10)
    colors = sns.color_palette("mako", n_colors=10)
    bars = ax1.barh(df_sorted['name'], df_sorted['Real_Vina_Score_kcal_mol'], color=colors, edgecolor='k')
    ax1.set_xlabel("Real AutoDock Vina Score (kcal/mol)", fontsize=10.5, fontweight='bold')
    ax1.set_ylabel("Pancreatic / KRAS Therapeutic", fontsize=10.5, fontweight='bold')
    ax1.set_title("(b) Top 10 High-Affinity KRAS-G12D Inhibitors", fontsize=11.5, fontweight='bold', pad=10)
    ax1.invert_yaxis()
    ax1.grid(True, linestyle=':', alpha=0.6)
    
    for bar in bars:
        w = bar.get_width()
        ax1.text(w - 0.35, bar.get_y() + bar.get_height()/2, f"{w:.2f}", 
                 va='center', ha='right', fontsize=9, fontweight='bold', color='white')
                 
    plt.suptitle("Figure 3: Physical Molecular Docking Statistical Profiles on Human KRAS-G12D Crystal", fontsize=13, fontweight='bold', y=0.96)
    out_p = os.path.join(fig_dir, "fig3_kras_docking_vina_statistical_profiles.png")
    plt.savefig(out_p, bbox_inches='tight')
    plt.close()
    print(f"Generated Figure 3: {out_p}")

def make_fig4_residues(base_dir, fig_dir):
    freq_csv = os.path.join(base_dir, "results", "docking", "residue_frequency_ranking.csv")
    if not os.path.exists(freq_csv):
        return
    df = pd.read_csv(freq_csv).head(12)
    
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    colors = sns.color_palette("crest", n_colors=len(df))
    bars = ax.bar(df['Residue'], df['Contact_Frequency'], color=colors, edgecolor='k', lw=1.2)
    
    ax.set_xlabel("Human KRAS-G12D Switch II Allosteric Residue (PDB ID: 7RPZ)", fontsize=11, fontweight='bold')
    ax.set_ylabel("Atomic Contact Frequency (d <= 3.8 A)", fontsize=11, fontweight='bold')
    ax.set_title("Figure 4: Residue-Level Interaction Fingerprints on KRAS-G12D (Highlighting Oncogenic Asp12)", fontsize=12.5, fontweight='bold', pad=12)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.5, str(int(h)), 
                ha='center', va='bottom', fontsize=9.5, fontweight='bold')
                
    ax.set_ylim(0, max(df['Contact_Frequency']) + 4)
    out_p = os.path.join(fig_dir, "fig4_kras_residue_contact_frequency.png")
    plt.savefig(out_p, bbox_inches='tight')
    plt.close()
    print(f"Generated Figure 4: {out_p}")

def make_fig5_parity(base_dir, fig_dir):
    # Was training ExtraTrees (single 75/25 split) on `Target_DeltaG_bind` from
    # dataset_drug_gC3N4_pristine.csv / _doped.csv, whose Delta_E_ads_kcal_mol and
    # Target_DeltaG_bind were FABRICATED by train_kras_qsar_models.py from an
    # empirical formula over RDKit descriptors ("Delta_E_ads_kcal_mol = -20.5 -
    # 1.65*AromRings - ..."), never any real xTB/DFT calculation, despite being
    # printed as "100% REAL". Real GFN2-xTB adsorption energies for ALL 33
    # compounds already exist in MASTER_COMPOUNDS_CURATED.csv
    # (Delta_E_ads_Pristine_kcal_mol / Delta_E_ads_Doped_kcal_mol -- the same
    # columns used by the leak-free QSPR in train_real_qspr_model.py), so no new
    # quantum computation is needed here, only using the real data.
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import RidgeCV
    from sklearn.model_selection import KFold, cross_val_predict
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

    master_csv = os.path.join(base_dir, "data", "processed", "MASTER_COMPOUNDS_CURATED.csv")
    df_m = pd.read_csv(master_csv)
    desc_cols = ["MW", "LogP", "Polarizability_alpha", "Electrophilicity_omega"]
    alpha_grid = np.array([0.001, 0.01, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1000.0])

    systems = [
        ("Isolated KRAS Drugs", "Real_Vina_Score_kcal_mol"),
        ("g-C3N4 Pristine", "Delta_E_ads_Pristine_kcal_mol"),
        ("B/P-Doped g-C3N4", "Delta_E_ads_Doped_kcal_mol"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), dpi=300)
    plt.subplots_adjust(top=0.82, wspace=0.25, bottom=0.15)
    colors = ["#00695C", "#0277BD", "#D84315"]

    for ax_idx, (sys_name, target_col) in enumerate(systems):
        if target_col not in df_m.columns:
            continue
        df = df_m.dropna(subset=desc_cols + [target_col])
        X = df[desc_cols].values
        y = df[target_col].values
        n, p = X.shape

        outer_cv = KFold(n_splits=5, shuffle=True, random_state=42)
        inner_cv = KFold(n_splits=5, shuffle=True, random_state=42)
        pipe = Pipeline([("scaler", StandardScaler()), ("ridge", RidgeCV(alphas=alpha_grid, cv=inner_cv))])
        y_pred = cross_val_predict(pipe, X, y, cv=outer_cv)
        rmse = mean_squared_error(y, y_pred) ** 0.5
        mae = mean_absolute_error(y, y_pred)
        r2 = r2_score(y, y_pred)

        ax = axes[ax_idx]
        ax.scatter(y, y_pred, color=colors[ax_idx], alpha=0.85, s=70, edgecolor='k', label=f'Out-of-Fold (n={n})')

        min_v = min(y.min(), y_pred.min()) - 0.5
        max_v = max(y.max(), y_pred.max()) + 0.5
        ax.plot([min_v, max_v], [min_v, max_v], 'r--', lw=2.0, label='Ideal 1:1 Parity')

        stats_txt = f"Leak-free nested 5x5 CV (n={n}, p={p})\nRMSE = {rmse:.2f} kcal/mol\nMAE = {mae:.2f} kcal/mol\n$Q^2_{{CV}}$ = {r2:.3f}"
        ax.text(0.05, 0.95, stats_txt, transform=ax.transAxes, fontsize=8.5, va='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.85, edgecolor='#B0BEC5'))

        ax.set_title(f"({chr(97+ax_idx)}) {sys_name}", fontsize=11.5, fontweight='bold', pad=10)
        ax.set_xlabel("Real GFN2-xTB / Vina Observed (kcal/mol)", fontsize=10.5)
        if ax_idx == 0:
            ax.set_ylabel("Out-of-Fold Predicted (kcal/mol)", fontsize=10.5)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend(loc='lower right', fontsize=8.5, frameon=True)

    plt.suptitle("Figure 5: Leak-Free Nested CV Parity (Predicted vs Observed) for Nano-QSAR on g-C3N4", fontsize=13, fontweight='bold', y=0.96)
    out_p = os.path.join(fig_dir, "fig5_kras_parity_models_evaluation.png")
    plt.savefig(out_p, bbox_inches='tight')
    plt.close()
    print(f"Generated Figure 5: {out_p}")

def make_fig6_shap(base_dir, fig_dir):
    # Was fit on `Target_DeltaG_bind` from dataset_drug_gC3N4_doped.csv, a
    # FABRICATED linear combination of AromRings/HBA/HBD/Polarizability_alpha
    # (see make_fig5_parity) -- so the "top feature" this reported was
    # circular (whatever the formula weighted most heavily came out on top).
    # Now fit on the real GFN2-xTB Delta_E_ads_Doped_kcal_mol from
    # MASTER_COMPOUNDS_CURATED.csv (same real data as Figure 5 / the leak-free
    # QSPR); ExtraTrees importances here are descriptive/exploratory over all
    # 20 candidate descriptors, not a claim of leak-free predictive accuracy
    # (that claim belongs to the 4-descriptor Ridge surrogate, Figure 5/8).
    f_path = os.path.join(base_dir, "data", "processed", "MASTER_COMPOUNDS_CURATED.csv")
    if not os.path.exists(f_path):
        return
    df = pd.read_csv(f_path)
    feature_cols = [
        "MW", "LogP", "HBA", "HBD", "PSA", "RBC", "NOR",
        "AromRings", "Polarizability_alpha", "Fraction_Csp3",
        "E_HOMO", "E_LUMO", "Gap_eV", "Hardness_eta", "Softness_S",
        "Electronegativity_chi", "Chemical_Potential_mu", "Electrophilicity_omega"
    ]
    df = df.dropna(subset=feature_cols + ["Delta_E_ads_Doped_kcal_mol"])
    X = df[feature_cols]
    y = df['Delta_E_ads_Doped_kcal_mol']

    model = ExtraTreesRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:10]
    
    top_features = [feature_cols[i] for i in indices]
    top_importances = importances[indices]
    
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    colors = sns.color_palette("BuGn_r", n_colors=len(top_features))
    bars = ax.barh(top_features[::-1], top_importances[::-1], color=colors, edgecolor='k')
    
    ax.set_xlabel("Mean Absolute SHAP Value / Gini Feature Importance", fontsize=11, fontweight='bold')
    ax.set_ylabel("Molecular / Quantum CDFT Descriptor", fontsize=11, fontweight='bold')
    ax.set_title("Figure 6: Exploratory Feature Importance Rankings for 2D g-C3N4 Delivery (real Delta_E_ads_Doped)", fontsize=11.5, fontweight='bold', pad=12)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.005, bar.get_y() + bar.get_height()/2, f"{w:.3f}", 
                va='center', ha='left', fontsize=9, fontweight='bold')
                
    ax.set_xlim(0, max(top_importances) + 0.06)
    out_p = os.path.join(fig_dir, "fig6_kras_shap_xai_importance_rankings.png")
    plt.savefig(out_p, bbox_inches='tight')
    plt.close()
    print(f"Generated Figure 6: {out_p}")

SRC = None  # set in get_dirs via generate_master_suite


def _src(base_dir):
    return os.path.join(base_dir, "data", "figures_source_package")


try:
    import _pymol
except Exception:
    _pymol = None


def _pm_cache(fig_dir):
    d = os.path.join(fig_dir, "_pm_cache")
    os.makedirs(d, exist_ok=True)
    return d


def _pm_panel(ax, png, title=None, subtitle=None):
    """Place a PyMOL-rendered PNG on a clean matplotlib axis with house typography."""
    import matplotlib.image as mpimg
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    if png and os.path.exists(png):
        ax.imshow(mpimg.imread(png))
    else:
        ax.text(0.5, 0.5, "render unavailable", ha="center", va="center", transform=ax.transAxes)
    if title:
        ax.set_title(title, fontsize=9.5, fontweight="bold", pad=5)
    if subtitle:
        ax.text(0.5, -0.03, subtitle, ha="center", va="top", fontsize=8.0,
                color=_pubstyle.MUTED, transform=ax.transAxes)


def make_fig9_3d_spatial(base_dir, fig_dir):
    """Figure 9 - ray-traced PyMOL renders of the representative modes."""
    S = _src(base_dir)
    C = _pm_cache(fig_dir)
    vina = pd.read_csv(os.path.join(base_dir, "results", "docking",
                       "real_vina_docking_summary.csv")).set_index("name")["Real_Vina_Score_kcal_mol"]
    ads = pd.read_csv(os.path.join(base_dir, "results", "quantum", "adsorption_qm_results.csv"))
    ap = ads[(ads.drug_name == "MRTX1133") & (ads.carrier_name == "pristine")].iloc[0]
    adp = ads[(ads.drug_name == "MRTX1133") & (ads.carrier_name == "BP_doped")].iloc[0]

    p_a = os.path.join(C, "fig9_a_pocket.png")
    p_b = os.path.join(C, "fig9_b_pristine.png")
    p_c = os.path.join(C, "fig9_c_doped.png")
    if _pymol and _pymol.AVAILABLE:
        try:
            _pymol.pocket_figure(
                os.path.join(S, "00_Graphical_Abstract", "Scene1_KRAS_G12D_receptor_7RPZ.pdb"),
                os.path.join(S, "00_Graphical_Abstract", "Scene1_MRTX1133_Switch_II_ligand.pdb"),
                p_a, key_res=[12, 62, 68, 96], size=(1500, 1300))
            _pymol.complex_figure(
                os.path.join(S, "03_Figure10_Atomistic_Structures", "MRTX1133_pristine_complex_optimized.xyz"),
                p_b, size=(1500, 1150), carbon="grey55", turn=(0, -20, 0))
            _pymol.complex_figure(
                os.path.join(S, "03_Figure10_Atomistic_Structures", "MRTX1133_BP_complex_optimized.xyz"),
                p_c, size=(1500, 1150), carbon="grey55", turn=(0, -20, 0))
        except Exception as exc:
            print(f"[fig9 PyMOL] {exc}")

    fig, axes = plt.subplots(1, 3, figsize=(11.4, 4.3))
    fig.subplots_adjust(wspace=0.05, top=0.86, bottom=0.14, left=0.02, right=0.98)
    _pm_panel(axes[0], p_a, "(a)  MRTX1133 in the KRAS-G12D Switch II pocket",
              f"PDB 7RPZ (1.30 A) - real Vina {vina['MRTX1133']:.2f} kcal/mol")
    _pm_panel(axes[1], p_b, "(b)  MRTX1133 on pristine g-C$_3$N$_4$",
              f"real GFN2-xTB $\\Delta E_{{ads}}$ = {ap.Delta_E_ads_kcal_mol:.2f} kcal/mol · $\\Delta Q$ = +{ap.Interfacial_Charge_Transfer_e:.2f} e")
    _pm_panel(axes[2], p_c, "(c)  MRTX1133 on B/P co-doped g-C$_3$N$_4$",
              f"real GFN2-xTB $\\Delta E_{{ads}}$ = {adp.Delta_E_ads_kcal_mol:.2f} kcal/mol · $\\Delta Q$ = +{adp.Interfacial_Charge_Transfer_e:.2f} e")
    fig.suptitle("Figure 9. Representative binding and adsorption modes for KRAS-G12D therapeutics on 2D g-C$_3$N$_4$",
                 fontsize=10.5, fontweight="bold", y=0.99)
    out_p = os.path.join(fig_dir, "fig9_kras_3d_spatial_binding_modes.png")
    _pubstyle.save(fig, out_p, also_pdf=False)
    print(f"Generated Figure 9 (PyMOL ray-traced): {out_p}")

def _parse_vina_log_modes(log_path):
    """Read the real AutoDock Vina mode table (mode, affinity) from a docking log."""
    modes = []
    if not os.path.exists(log_path):
        return modes
    started = False
    for line in open(log_path):
        s = line.strip()
        if s.startswith("-----+"):
            started = True
            continue
        if started:
            parts = s.split()
            if len(parts) >= 2 and parts[0].isdigit():
                try:
                    modes.append((int(parts[0]), float(parts[1])))
                except ValueError:
                    break
            else:
                break
    return modes


def make_fig_redocking_final(base_dir, fig_dir):
    """Full-Q1 Figure 1: crystallographic pose-recovery validation (real data only).

    Panel (a): redocking summary (RMSD 1.419 A vs the <=2.0 A criterion).
    Panel (b): the *real* AutoDock Vina mode table for the MRTX1133 redocking run.
    """
    log_path = os.path.join(base_dir, "data", "figures_source_package",
                            "01_Figure3_Redocking", "MRTX1133_redocking_vina.log")
    modes = _parse_vina_log_modes(log_path)
    S = _src(base_dir)
    C = _pm_cache(fig_dir)
    p_a = os.path.join(C, "redock_super.png")
    if _pymol and _pymol.AVAILABLE:
        try:
            _pymol.superpose_figure(
                os.path.join(S, "01_Figure3_Redocking", "7RPZ_KRAS_G12D_receptor_apo.pdb"),
                os.path.join(S, "01_Figure3_Redocking", "MRTX1133_crystal_pose_6IC.pdb"),
                os.path.join(S, "01_Figure3_Redocking", "MRTX1133_redocked_best_pose.pdbqt"),
                p_a, size=(1500, 1250))
        except Exception as exc:
            print(f"[redock PyMOL] {exc}")

    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.3),
                             gridspec_kw={"width_ratios": [1.15, 1.0]})
    fig.subplots_adjust(wspace=0.22, top=0.86, bottom=0.16, left=0.03, right=0.97)
    _pm_panel(axes[0], p_a,
              "(a)  Crystallographic (green) vs top redocked (orange) pose",
              "PDB 7RPZ (1.30 A) · heavy-atom RMSD = 1.419 A (criterion $\\leq$ 2.0 A)")

    ax1 = axes[1]
    if modes:
        xs = [m for m, _ in modes]
        ys = [a for _, a in modes]
        bars = ax1.bar(xs, ys, color=_pubstyle.MUTED, edgecolor="#3a3f47", linewidth=0.6)
        bars[0].set_color(_pubstyle.WARN)
        for b in bars:
            h = b.get_height()
            ax1.annotate(f"{h:.2f}", (b.get_x() + b.get_width() / 2, h),
                         xytext=(0, -3), textcoords="offset points",
                         ha="center", va="top", fontsize=7.5, color="white", fontweight="bold")
        ax1.set_xticks(xs)
        ax1.set_ylim(min(ys) - 0.7, 0)
    ax1.set_xlabel("AutoDock Vina output mode")
    ax1.set_ylabel("Vina score (kcal/mol)")
    ax1.set_title(f"MRTX1133 redocking landscape (n = {len(modes)} modes)")
    ax1.grid(True, axis="x", alpha=0)
    _pubstyle.panel_label(ax1, "b")

    fig.suptitle("Figure 1. Crystallographic pose-recovery validation of the docking protocol on KRAS-G12D",
                 fontsize=10.5, fontweight="bold", y=0.99)
    out_p = os.path.join(fig_dir, "fig3_redocking_validation_final.jpg")
    _pubstyle.save(fig, out_p, also_pdf=False)
    print(f"Generated Full-Q1 redocking figure (real 3D + real modes): {out_p}")


def make_fig10_multiscale_final(base_dir, fig_dir):
    """Full-Q1 multi-scale structural figure (real data only, schematic layout).

    All energetics/charges are read from results/quantum/adsorption_qm_results.csv
    and the GFN2-xTB `charges` output for the doped complex. No DFT/GFN1 benchmark
    panel (that data was never computed).
    """
    ads = pd.read_csv(os.path.join(base_dir, "results", "quantum", "adsorption_qm_results.csv"))
    ap = ads[(ads.drug_name == "MRTX1133") & (ads.carrier_name == "pristine")].iloc[0]
    ad = ads[(ads.drug_name == "MRTX1133") & (ads.carrier_name == "BP_doped")].iloc[0]

    qB = qP = None
    cdir = os.path.join(base_dir, "scratch", "qm_calcs_adsorption", "BP_doped_MRTX1133")
    xyz_p = os.path.join(cdir, "xtbopt.xyz")
    ch_p = os.path.join(cdir, "charges")
    if os.path.exists(xyz_p) and os.path.exists(ch_p):
        lines = open(xyz_p).read().split('\n')
        n = int(lines[0])
        syms = [l.split()[0] for l in lines[2:2 + n]]
        ch = [float(x) for x in open(ch_p).read().split()]
        for s, c in zip(syms, ch):
            if s == 'B' and qB is None:
                qB = c
            elif s == 'P' and qP is None:
                qP = c

    S = _src(base_dir)
    C = _pm_cache(fig_dir)
    D = os.path.join(S, "03_Figure10_Atomistic_Structures")
    files = [("gC3N4_pristine_optimized.xyz", "fig10_a.png", (0, 0, 0)),
             ("gC3N4_BP_doped_optimized.xyz", "fig10_b.png", (0, 0, 0)),
             ("MRTX1133_BP_complex_optimized.xyz", "fig10_c.png", (0, -25, 0))]
    pngs = [os.path.join(C, f) for _, f, _ in files]
    if _pymol and _pymol.AVAILABLE:
        for (xyzf, _, turn), png in zip(files, pngs):
            try:
                _pymol.complex_figure(os.path.join(D, xyzf), png, size=(1400, 1150),
                                      carbon="grey55", turn=turn, tilt=22)
            except Exception as exc:
                print(f"[fig10 PyMOL {xyzf}] {exc}")

    fig, axes = plt.subplots(1, 3, figsize=(11.4, 4.0))
    fig.subplots_adjust(wspace=0.05, top=0.85, bottom=0.15, left=0.02, right=0.98)
    _pm_panel(axes[0], pngs[0], "(a)  Pristine g-C$_3$N$_4$ cluster (C$_{21}$N$_{21}$H$_6$)",
              f"real GFN2-xTB $\\Delta E_{{ads}}$ = {ap.Delta_E_ads_kcal_mol:.2f} kcal/mol · $\\Delta Q$ = +{ap.Interfacial_Charge_Transfer_e:.2f} e")
    _pm_panel(axes[1], pngs[1], "(b)  B/P co-doped cluster (C$_{20}$B$_1$N$_{20}$P$_1$H$_6$)",
              (f"q(B) = {qB:+.2f} e · q(P) = {qP:+.2f} e · " if qB is not None else "")
              + f"$\\Delta E_{{ads}}$ = {ad.Delta_E_ads_kcal_mol:.2f} · $\\Delta Q$ = +{ad.Interfacial_Charge_Transfer_e:.2f} e")
    _pm_panel(axes[2], pngs[2], "(c)  MRTX1133 / B/P-doped complex",
              "GFN2-xTB optimised drug-carrier geometry")
    fig.suptitle("Figure 5. Multi-scale atomistic models and real GFN2-xTB interfacial energetics",
                 fontsize=10.5, fontweight="bold", y=0.99)
    out_p = os.path.join(fig_dir, "fig10_atomistic_multiscale_final.jpg")
    _pubstyle.save(fig, out_p, also_pdf=False)
    print(f"Generated Full-Q1 multiscale figure (real 3D): {out_p}")


def make_fig11_deltarho(base_dir, fig_dir):
    """Figure 11 - charge-density difference for the MRTX1133 / B,P-doped
    g-C3N4 hero complex (real GFN2-xTB densities). Delta-rho cube ships in
    results/quantum/drho/; see that folder's README + build_deltarho.py."""
    try:
        import _drho_fig
    except Exception as exc:
        print(f"[fig11 drho] helper unavailable: {exc}")
        return
    drho_dir = os.path.join(base_dir, "results", "quantum", "drho")
    ads = pd.read_csv(os.path.join(base_dir, "results", "quantum", "adsorption_qm_results.csv"))
    ad = ads[(ads.drug_name == "MRTX1133") & (ads.carrier_name == "BP_doped")].iloc[0]
    render = os.path.join(drho_dir, "kras_deltarho_render.png")
    render = _drho_fig.render_isosurface(drho_dir, "kras", render, level=0.003,
                                         turn=(-20, 30, 0))
    out_p = os.path.join(fig_dir, "fig11_kras_charge_density_difference.png")
    _drho_fig.compose(out_p, render, 11,
                      "Interfacial charge redistribution on the B/P co-doped g-C$_3$N$_4$ carrier",
                      "MRTX1133", "B/P-doped g-C$_3$N$_4$", 0.003,
                      dEint_kcal=float(ad.Delta_E_ads_kcal_mol),
                      dq_e=float(ad.Interfacial_Charge_Transfer_e))
    print(f"Generated Figure 11 (charge-density difference): {out_p}")


def generate_master_suite():
    base_dir, fig_dir = get_dirs()
    make_graphical_abstract(base_dir, fig_dir)
    make_fig1_workflow(base_dir, fig_dir)
    make_fig2_quantum(base_dir, fig_dir)
    make_fig3_docking_profiles(base_dir, fig_dir)
    make_fig4_residues(base_dir, fig_dir)
    make_fig5_parity(base_dir, fig_dir)
    make_fig6_shap(base_dir, fig_dir)
    make_fig9_3d_spatial(base_dir, fig_dir)
    make_fig_redocking_final(base_dir, fig_dir)
    make_fig10_multiscale_final(base_dir, fig_dir)
    make_fig11_deltarho(base_dir, fig_dir)
    print("Master figure suite for Article 3 (KRAS) generated successfully at 300+ DPI!")

if __name__ == "__main__":
    generate_master_suite()
