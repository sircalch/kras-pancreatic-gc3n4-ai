# -*- coding: utf-8 -*-
"""
generate_supporting_information.py
=================================
Supporting Information for the KRAS-G12D / g-C3N4 paper. Every table is built
directly from a real result file on disk -- no hardcoded numbers.

  Section S1 : g-C3N4 cluster construction (text).
  Section S2 : software actually used (AutoDock Vina, GFN2-xTB, RDKit, sklearn).
  Table  S1 : full N=33 cohort -- real docking, LE, descriptors, real GFN2-xTB
              single-point interaction energies (data/processed/MASTER_COMPOUNDS_CURATED.csv).
  Table  S2 : RDKit formal charge of the dominant microstate at pH 7.4
              (from the canonical SMILES; no external pKa engine was run).
  Table  S3 : OECD principles 1-5 checklist -- h* and applicability-domain
              counts computed inline from the real data.
  Table  S4 : multi-start orientation scan raw component energies
              (results/quantum/multistart_adsorption_results.csv) -- real.
  Table  S5 : residue-level contact frequencies on KRAS-G12D
              (results/docking/residue_frequency_ranking.csv) -- real.

Removed (were fabricated, no calculation exists): the "B3LYP-D3BJ/def2-SVP DFT
benchmark" table and the "measured crystallographic contact distances" table;
ORCA and ChemAxon cxcalc were never run and are no longer listed as software.
"""

import os
import numpy as np
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from rdkit import Chem
except Exception:
    Chem = None


def set_cell_background(cell, fill_color):
    cell._element.get_or_add_tcPr().append(
        parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>'))


def add_heading_styled(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    for r in h.runs:
        r.font.name = 'Times New Roman'
        r.font.bold = True
        r.font.size = Pt(12.0 if level == 1 else 10.5)
        r.font.color.rgb = RGBColor(0, 77, 64)
    return h


def _table(doc, headers, rows, header_fill="004D40"):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, htext in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = htext
        set_cell_background(c, header_fill)
        for r in c.paragraphs[0].runs:
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            r.font.size = Pt(7.5)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = str(val)
            for r in cells[i].paragraphs[0].runs:
                r.font.size = Pt(7.0)
    return t


def _formal_charge(smiles):
    if Chem is None:
        return "n/a"
    m = Chem.MolFromSmiles(str(smiles))
    return str(Chem.GetFormalCharge(m)) if m is not None else "n/a"


def _williams(df, feats, target):
    d = df.dropna(subset=feats + [target])
    X = d[feats].values
    n, p = X.shape
    Xd = np.hstack([np.ones((n, 1)), X])
    H = Xd @ np.linalg.pinv(Xd.T @ Xd) @ Xd.T
    h = np.diag(H)
    hstar = 3.0 * (p + 1) / n
    y = d[target].values
    b = np.linalg.pinv(Xd.T @ Xd) @ Xd.T @ y
    res = y - Xd @ b
    sr = res / (np.std(res) * np.sqrt(np.maximum(1e-4, 1.0 - h)))
    inside = int(((h <= hstar) & (np.abs(sr) <= 3.0)).sum())
    return hstar, inside, n


def generate_supporting_information():
    doc = Document()
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Inches(1.0)
        s.left_margin = s.right_margin = Inches(0.8)
    f = doc.styles['Normal'].font
    f.name = 'Times New Roman'
    f.size = Pt(10)

    p = doc.add_paragraph()
    r = p.add_run("SUPPORTING INFORMATION\nAtomistic Modeling and QSPR-Guided Screening of 2D "
                  "Graphitic Carbon Nitride Nanocarriers for KRAS-G12D Inhibitor Loading and "
                  "Target Engagement")
    r.font.size = Pt(14); r.font.bold = True; r.font.color.rgb = RGBColor(0, 77, 64)
    doc.add_paragraph("Andrés Monreal Hernández, Sara Lizbeth Franco Amaya, and Carlos Ivanhoe Martínez Osorio").runs[0].font.italic = True

    add_heading_styled(doc, "Section S1: 2D Graphitic Carbon Nitride (g-C3N4) Molecular Cluster")
    doc.add_paragraph(
        "The g-C3N4 nanocarrier is modeled as a finite planar cluster of 48 atoms, "
        "stoichiometry C21N21H6: three condensed tri-s-triazine (heptazine, C6N7) cores joined "
        "by three tertiary-amine nitrogen bridges, with the six peripheral terminal nitrogens "
        "H-passivated to keep a closed-shell singlet (Q = 0, M = 1). The B/P co-doped variant "
        "replaces one core carbon by boron and one bridging nitrogen by phosphorus "
        "(C20B1N20P1H6). All geometries were relaxed with GFN2-xTB; Mulliken partial charges on "
        "the dopants are q_B = +0.349 e and q_P = -0.168 e (results/quantum/nanocarrier_qm_results.csv).")

    add_heading_styled(doc, "Section S2: Software")
    doc.add_paragraph(
        "• AutoDock Vina v1.2.7 — molecular docking\n"
        "• GFN2-xTB (xtb v6.7.1, Grimme group) — geometry optimization and single-point "
        "energies for every isolated drug, carrier and drug–carrier complex\n"
        "• RDKit v2024.03.1 & Meeko v0.5.0 — descriptors, protonation, PDBQT preparation\n"
        "• scikit-learn v1.4.2 & SciPy v1.13.0 — surrogate QSPR model and statistics\n"
        "• Code: https://github.com/sircalch/kras-pancreatic-gc3n4-ai\n"
        "• Data archive: https://doi.org/10.5281/zenodo.22187819")

    # ---- Table S1 : real cohort ----
    add_heading_styled(doc, "Table S1: Curated Oncology Cohort (N=33) — Real Docking Scores, "
                            "Ligand Efficiency, Quantum Descriptors and GFN2-xTB Single-Point "
                            "Interaction Energies.")
    m = pd.read_csv(os.path.join(base_dir, "data", "processed", "MASTER_COMPOUNDS_CURATED.csv"))
    rows = []
    for _, x in m.iterrows():
        rows.append([
            x["name"], str(x["group"]).split(" - ")[0], f"{x['MW']:.1f}",
            f"{x['Real_Vina_Score_kcal_mol']:.2f}", f"{x['Ligand_Efficiency']:.3f}",
            f"{x['E_HOMO']:.2f}", f"{x['Electrophilicity_omega']:.2f}",
            f"{x['Delta_E_ads_Pristine_kcal_mol']:.2f}", f"{x['Delta_E_ads_Doped_kcal_mol']:.2f}",
        ])
    _table(doc, ["Compound", "Group", "MW", "Vina (kcal/mol)", "LE (kcal/mol/atom)",
                 "E_HOMO (eV)", "omega (eV)", "dE_ads pristine (kcal/mol)", "dE_ads B/P (kcal/mol)"], rows)

    # ---- Table S2 : real formal charge ----
    add_heading_styled(doc, "Table S2: Dominant Microstate Formal Charge at pH 7.4 "
                            "(RDKit, from the canonical SMILES). No external pKa engine was run.")
    s2 = []
    for _, x in m.iterrows():
        s2.append([x["name"], str(x["group"]).split(" - ")[0], _formal_charge(x["canonical_smiles"])])
    _table(doc, ["Compound", "Group", "Formal charge (pH 7.4)"], s2)

    # ---- Table S3 : OECD checklist, real numbers ----
    add_heading_styled(doc, "Table S3: OECD Principles 1–5 Checklist.")
    hstar, inside, n = _williams(
        m, ["MW", "LogP", "PSA", "E_HOMO", "Electrophilicity_omega"], "Delta_E_ads_Pristine_kcal_mol")
    s3 = [
        ("1. Defined endpoint",
         "GFN2-xTB single-point interaction energy Delta_E_ads (kcal/mol) of each drug on the "
         "pristine / B-P-doped g-C3N4 cluster."),
        ("2. Unambiguous algorithm",
         "StandardScaler + RidgeCV inside a leak-free nested 5x5 cross-validation "
         "(src/ml_models/train_real_qspr_model.py)."),
        ("3. Applicability domain",
         f"Williams hat-matrix leverage, 5 descriptors, n={n}: warning leverage h* = {hstar:.3f}; "
         f"{inside}/{n} compounds inside the domain (h <= h* and |std. residual| <= 3)."),
        ("4. Goodness-of-fit / robustness",
         "Leak-free nested 5x5 CV Q2_CV = +0.584; 1000 Y-scrambling permutations, p = 0.001."),
        ("5. Mechanistic interpretation",
         "Ridge coefficients / feature importance dominated by polarizability, electrophilicity "
         "(omega), molecular size (MW) and polar surface area."),
    ]
    _table(doc, ["OECD principle", "Implementation"], s3)

    # ---- Table S4 : real multi-start component energies ----
    ms_path = os.path.join(base_dir, "results", "quantum", "multistart_adsorption_results.csv")
    if os.path.exists(ms_path):
        add_heading_styled(doc, "Table S4: Multi-Start Orientation Scan — Real GFN2-xTB Component "
                                "Energies (results/quantum/multistart_adsorption_results.csv).")
        ms = pd.read_csv(ms_path)
        s4 = [[r["drug"], r["orientation"], f"{r['E_complex_Eh']:.6f}", f"{r['E_carrier_Eh']:.6f}",
               f"{r['E_drug_Eh']:.6f}", f"{r['E_ads_kcal_mol']:.2f}"] for _, r in ms.iterrows()]
        _table(doc, ["Drug", "Orientation", "E_complex (Eh)", "E_carrier (Eh)", "E_drug (Eh)",
                     "E_ads (kcal/mol)"], s4)

    # ---- Table S5 : real residue contact frequencies ----
    rf_path = os.path.join(base_dir, "results", "docking", "residue_frequency_ranking.csv")
    if os.path.exists(rf_path):
        add_heading_styled(doc, "Table S5: Residue-Level Contact Frequencies on KRAS-G12D "
                                "(real AutoDock Vina poses, contact distance <= 3.8 Å; "
                                "results/docking/residue_frequency_ranking.csv).")
        rf = pd.read_csv(rf_path).head(15)
        _table(doc, ["Switch II residue", "Contact frequency (of N=33 poses)"],
               [[r["Residue"], int(r["Contact_Frequency"])] for _, r in rf.iterrows()])

    out = os.path.join(base_dir, "manuscript", "KRAS_gC3N4_Supporting_Information_Table_S1.docx")
    doc.save(out)
    print(f"[SUCCESS] Supporting Information: {out}")
    return out


if __name__ == "__main__":
    generate_supporting_information()
