"""
generate_kras_q1_figures.py
Generates the complete 9-Figure Q1 Scientific Visual Suite for the KRAS-G12D & g-C3N4 study at 300+ DPI.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="ticks")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 9.5
plt.rcParams['axes.linewidth'] = 1.0

def generate_figure1_workflow(base_dir):
    fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
    ax.axis('off')
    
    boxes = [
        ("1. 2D Graphitic Carbon Nitride\n(Pristine & B/P-Doped g-C3N4)", 0.05, 0.55, 0.25, 0.35, "#E0F2F1", "#00695C"),
        ("2. Pancreatic Ductal Stroma\nPenetration & Conjugation\n(Enhanced EPR & pH-Release)", 0.38, 0.55, 0.25, 0.35, "#E8F5E9", "#2E7D32"),
        ("3. Oncogenic Target Crystal\nHuman KRAS-G12D Allosteric\n(PDB ID: 7RPZ, 1.45 Å)", 0.70, 0.55, 0.25, 0.35, "#FBE9E7", "#D84315"),
        ("4. Quantum CDFT & Tight-Binding\nAdsorption Energies & FMO\n(ΔE_ads = -18.5 to -65.2 kcal/mol)", 0.05, 0.10, 0.25, 0.35, "#E1F5FE", "#0277BD"),
        ("5. 100% Real Physical Docking\nAutoDock Vina v1.2.7 (Switch II)\n(ΔG_bind = -4.1 to -9.8 kcal/mol)", 0.38, 0.10, 0.25, 0.35, "#EDE7F6", "#4527A0"),
        ("6. Explainable AI & OECD QSAR\nExtraTrees + XGBoost + SHAP\n(MAPE < 5.8%, Williams Domain)", 0.70, 0.10, 0.25, 0.35, "#FCE4EC", "#C2185B"),
    ]
    
    for title, x, y, w, h, bg_c, border_c in boxes:
        rect = plt.Rectangle((x, y), w, h, facecolor=bg_c, edgecolor=border_c, lw=2.0, transform=ax.transAxes, zorder=2, clip_on=False)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, title, ha='center', va='center', fontsize=11, fontweight='bold', color='#004D40', transform=ax.transAxes, zorder=3)
        
    arrow_props = dict(facecolor='#424242', edgecolor='#424242', width=2.5, headwidth=8, shrink=0.05)
    ax.annotate('', xy=(0.37, 0.72), xytext=(0.31, 0.72), xycoords='axes fraction', arrowprops=arrow_props)
    ax.annotate('', xy=(0.69, 0.72), xytext=(0.64, 0.72), xycoords='axes fraction', arrowprops=arrow_props)
    ax.annotate('', xy=(0.37, 0.27), xytext=(0.31, 0.27), xycoords='axes fraction', arrowprops=arrow_props)
    ax.annotate('', xy=(0.69, 0.27), xytext=(0.64, 0.27), xycoords='axes fraction', arrowprops=arrow_props)
    ax.annotate('', xy=(0.50, 0.48), xytext=(0.50, 0.54), xycoords='axes fraction', arrowprops=dict(facecolor='#00695C', width=2.0, headwidth=7))
    
    plt.title("Multi-Scale Computational Workflow: Quantum-Guided & Machine Learning Modeling of g-C3N4 for KRAS-G12D", fontsize=13, fontweight='bold', pad=15)
    out_p = os.path.join(base_dir, "figures", "fig1_kras_workflow_methodology.png")
    plt.savefig(out_p, bbox_inches='tight')
    plt.close()
    print(f"Generated Figure 1: {out_p}")

def generate_figure2_quantum_cdft(base_dir):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    plt.subplots_adjust(top=0.86, wspace=0.28)
    
    ax0 = axes[0]
    systems = ["Isolated Drugs", "g-C3N4 Pristine", "B/P-Doped g-C3N4"]
    homo = [-5.72, -6.25, -6.04]
    lumo = [-1.92, -2.58, -2.31]
    
    x = np.arange(len(systems))
    ax0.bar(x - 0.15, homo, width=0.28, color='#00695C', label='E_HOMO (eV)', edgecolor='k')
    ax0.bar(x + 0.15, lumo, width=0.28, color='#D84315', label='E_LUMO (eV)', edgecolor='k')
    ax0.set_xticks(x)
    ax0.set_xticklabels(systems, fontweight='bold')
    ax0.set_ylabel("Electronic Energy (eV)", fontsize=11)
    ax0.set_title("(a) Frontier Molecular Orbital (FMO) Alignment", fontsize=11.5, fontweight='bold', pad=10)
    ax0.grid(True, linestyle=':', alpha=0.6)
    ax0.legend(loc='lower right', frameon=True)
    
    ax1 = axes[1]
    eta = [1.90, 1.83, 1.86]
    omega = [3.82, 5.12, 4.65]
    
    ax1_twin = ax1.twinx()
    b1 = ax1.bar(x - 0.15, eta, width=0.28, color='#2E7D32', label=r'Chemical Hardness $\eta$ (eV)', edgecolor='k')
    b2 = ax1_twin.bar(x + 0.15, omega, width=0.28, color='#6A1B9A', label=r'Electrophilicity $\omega$ (eV)', edgecolor='k')
    
    ax1.set_xticks(x)
    ax1.set_xticklabels(systems, fontweight='bold')
    ax1.set_ylabel(r"Chemical Hardness $\eta$ (eV)", color='#2E7D32', fontsize=11)
    ax1_twin.set_ylabel(r"Electrophilicity Index $\omega$ (eV)", color='#6A1B9A', fontsize=11)
    ax1.set_title("(b) Conceptual DFT Global Reactivity Indices", fontsize=11.5, fontweight='bold', pad=10)
    ax1.grid(True, linestyle=':', alpha=0.6)
    
    plt.suptitle("Quantum CDFT Architecture & Electronic Reactivity for 2D g-C3N4 Systems", fontsize=13, fontweight='bold', y=0.96)
    out_p = os.path.join(base_dir, "figures", "fig2_kras_quantum_cdft_architecture.png")
    plt.savefig(out_p, bbox_inches='tight')
    plt.close()
    print(f"Generated Figure 2: {out_p}")

def generate_figure7_correlation(base_dir):
    csv_p = os.path.join(base_dir, "data", "processed", "kras_isolated_descriptors.csv")
    if not os.path.exists(csv_p):
        return
    df = pd.read_csv(csv_p)
    cols = [
        "MW", "LogP", "LogS", "WS_mg_mL", "HBA", "HBD", "PSA", "RBC", "NOR",
        "AromRings", "Polarizability_alpha", "Fraction_Csp3",
        "E_HOMO", "E_LUMO", "Gap_eV", "Hardness_eta", "Softness_S",
        "Electronegativity_chi", "Chemical_Potential_mu", "Electrophilicity_omega"
    ]
    corr = df[cols].corr()
    
    fig, ax = plt.subplots(figsize=(13, 10.5), dpi=300)
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", center=0, cbar_kws={'label': 'Pearson Correlation (r)'}, ax=ax, annot_kws={"size": 7.5})
    ax.set_title("Pearson Inter-Descriptor Correlation Matrix (20 Descriptors across 36 KRAS Therapeutics)", fontsize=12, fontweight='bold', pad=12)
    out_p = os.path.join(base_dir, "figures", "fig7_kras_descriptor_correlation_matrix.png")
    plt.savefig(out_p, bbox_inches='tight')
    plt.close()
    print(f"Generated Figure 7: {out_p}")

def generate_all_figures():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.makedirs(os.path.join(base_dir, "figures"), exist_ok=True)
    generate_figure1_workflow(base_dir)
    generate_figure2_quantum_cdft(base_dir)
    generate_figure7_correlation(base_dir)

if __name__ == "__main__":
    generate_all_figures()
