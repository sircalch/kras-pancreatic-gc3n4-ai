# Atomistic Modeling and QSPR-Guided Screening of 2D Graphitic Carbon Nitride Nanocarriers for KRAS-G12D Inhibitor Loading and Target Engagement

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14920845.svg)](https://doi.org/10.5281/zenodo.14920845)
[![License: MIT](https://img.shields.io/badge/License-MIT-teal.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![xTB GFN2](https://img.shields.io/badge/Quantum%20Engine-GFN2--xTB-004D40.svg)](https://github.com/grimme-lab/xtb)
[![AutoDock Vina 1.2.7](https://img.shields.io/badge/Docking-AutoDock%20Vina%201.2.7-orange.svg)](https://github.com/ccsb-scripps/AutoDock-Vina)

**Authors**: Andrés Monreal Hernández, Sara Lizbeth Franco Amaya, Carlos Ivanhoe Martínez Osorio  
**Affiliation**: Universidad Estatal de Sonora, Hermosillo, Sonora, México  
**Permanent Archival DOI**: `10.5281/zenodo.14920845`

---

## 📌 Abstract

KRAS-G12D is the dominant oncogenic driver in pancreatic ductal adenocarcinoma (PDAC), yet clinical efficacy of targeted small-molecule inhibitors (e.g., MRTX1133) is severely hindered by the dense, hypovascularized desmoplastic tumor stroma. Two-dimensional (2D) graphitic carbon nitride ($g\text{-C}_3\text{N}_4$) nanosheets present a promising delivery platform. In this study, we establish a multi-scale computational framework integrating:
1. **Crystallographic Redocking Validation**: AutoDock Vina v1.2.7 achieves $1.419\ \text{Å}$ heavy-atom RMSD on the ultra-high resolution ($1.30\ \text{Å}$) human KRAS-G12D crystal structure (PDB ID: 7RPZ, co-crystallized with MRTX1133).
2. **Mechanistic Cohort Profiling**: Binding score distributions across $N=33$ curated clinical therapeutics stratified across 4 pharmacological classes in the Switch II allosteric pocket.
3. **Tight-Binding Quantum Chemistry (GFN2-xTB)**: Rigorous quantum mechanical adsorption simulation on pristine ($C_{21}N_{21}H_6$) and heteroatom B/P co-doped 2D nanosheets ($E_{\text{int,std}} = -4.98$ to $-39.89\ \text{kcal/mol}$).
4. **OECD-Compliant Surrogate QSPR Modeling**: Leak-free nested 5-fold cross-validation ($Q^2_{\text{CV}} = +0.5696$, $\text{RMSE} = 5.201\ \text{kcal/mol}$, $1,000$ Y-scrambling iterations $p=0.001$, warning leverage threshold $h^* = 0.455$).
5. **Decoupled Virtual Screening**: Screening of 350 DrugBank oncology candidates with prospective quantum confirmation on top clinical leads (Futibatinib, Belumosudil, Pimicotinib, Avapritinib, Capivasertib).

---

## 🔬 Repository Structure

```
├── data/
│   ├── processed/
│   │   ├── MASTER_COMPOUNDS_CURATED.csv      # N=33 curated master oncology cohort
│   │   ├── DRUGBANK_350_SCREENING_LIBRARY.csv # 350 DrugBank candidate dataset
│   ├── raw/
│   │   ├── 7rpz_receptor_clean.pdbqt          # Prepared 7RPZ receptor coordinates
│   │   ├── MRTX1133_ligand_native.pdbqt       # Native co-crystallized 6IC coordinates
│   ├── quantum/structures/                    # XYZ coordinates for pristine & B/P nanosheets
│   └── figures_source_package/                # Raw PDBQTs, Vina logs, and alignment matrices
├── figures/                                   # High-resolution publication figures (300 DPI)
├── manuscript/
│   ├── KRAS_gC3N4_Full_Q1_Research_Paper_Monreal_Hernandez_et_al.docx # Main manuscript
│   └── KRAS_gC3N4_Supporting_Information_Table_S1.docx               # Comprehensive SI
├── results/
│   ├── docking/validation/                    # Redocking logs and RMSD validation reports
│   ├── quantum/                               # GFN2-xTB adsorption & 10-system benchmark data
│   └── qspr/                                  # Ridge surrogate models, metrics, Williams plot data
├── src/
│   ├── curation/                              # PubChem API fetching and reference curation
│   ├── docking/                               # AutoDock Vina preparation and grid execution
│   ├── quantum/                               # GFN2-xTB energy evaluation and cluster builders
│   ├── descriptors/                           # Frontier orbital & RDKit descriptor calculation
│   ├── ml_models/                             # Nested Ridge QSPR training & Y-scrambling
│   └── visualization/                         # Manuscript & figure compilation pipelines
├── run_entire_kras_study.py                   # Master end-to-end execution pipeline
└── README.md
```

---

## ⚙️ Installation & Requirements

```bash
git clone https://github.com/sircalch/kras-pancreatic-gc3n4-ai.git
cd kras-pancreatic-gc3n4-ai

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required dependencies
pip install rdkit scikit-learn pandas numpy scipy matplotlib seaborn python-docx meeko
```

Quantum chemistry calculations utilize the `xtb` standalone executable (v6.7.1):
```bash
# Verify xTB installation
xtb --version
```

---

## 🚀 Reproducibility: End-to-End Pipeline Execution

To execute the entire multi-scale computational workflow from raw structures to final models:
```bash
python run_entire_kras_study.py
```

To regenerate the formatted submission manuscripts and supporting information:
```bash
python src/visualization/generate_kras_full_manuscript.py
python src/visualization/generate_supporting_information.py
```

---

## 📊 Summary of Benchmark Results

| Computational Benchmark | Target Metric | Achieved Value | Status |
|---|---|---|---|
| **Crystallographic Redocking** | PDB 7RPZ (MRTX1133) Heavy-Atom RMSD | **1.419 Å** ($\le 2.0\ \text{Å}$) | **Passed** |
| **Docking Score Recovery** | MRTX1133 Redocked Vina Affinity | **-9.16 kcal/mol** | **Passed** |
| **QSPR Outer Nested CV** | $Q^2_{\text{CV}}$ ($n=33, p=4$) | **+0.5696** ($> 0.50$) | **Passed** |
| **QSPR Model Error** | Nested Cross-Validated RMSE / MAE | **5.20 / 4.19 kcal/mol** | **Passed** |
| **Y-Scrambling Permutations** | 1,000 Scrambled Iterations Empirical $p$ | **p = 0.001** (mean $Q^2 = -0.2357$) | **Passed** |
| **OECD Applicability Domain** | Training Cohort within Warning $h^* = 0.455$ | **32/33 (97.0%)** | **Passed** |
| **Prospective Lead Confirmation** | GFN2-xTB Recalculation on Top Leads | **MAE = 3.94 kcal/mol** | **Passed** |

---

## 📜 Citation

```bibtex
@article{MonrealHernandez2026_KRAS_gC3N4,
  title={Atomistic Modeling and QSPR-Guided Screening of 2D Graphitic Carbon Nitride Nanocarriers for KRAS-G12D Inhibitor Loading and Target Engagement},
  author={Monreal Hern{\'a}ndez, Andr{\'e}s and Franco Amaya, Sara Lizbeth and Mart{\'i}nez Osorio, Carlos Ivanhoe},
  journal={ChemRxiv / Preprints},
  year={2026},
  doi={10.5281/zenodo.14920845},
  url={https://github.com/sircalch/kras-pancreatic-gc3n4-ai}
}
```

## 📄 License
This project and all associated datasets are released under the [MIT License](LICENSE).
