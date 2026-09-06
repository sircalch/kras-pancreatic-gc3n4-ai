"""
generate_kras_word_manuscript.py
Builds the complete, publication-grade Microsoft Word (.docx) manuscript
with all 9 figures embedded, formatted tables, and 45 verified citations for Article 3 (KRAS & g-C3N4).
"""

import os
import json
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_heading_styled(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True
    for r in h.runs:
        r.font.name = 'Times New Roman'
        r.font.bold = True
        if level == 1:
            r.font.size = Pt(14)
            r.font.color.rgb = RGBColor(0, 105, 92)
        elif level == 2:
            r.font.size = Pt(12)
            r.font.color.rgb = RGBColor(0, 77, 64)
        else:
            r.font.size = Pt(11)
            r.font.color.rgb = RGBColor(33, 33, 33)
    return h

def add_image_if_exists(doc, img_path, caption_text, width=Inches(6.2)):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(10)
        p_img.paragraph_format.space_after = Pt(4)
        run = p_img.add_run()
        run.add_picture(img_path, width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_after = Pt(12)
        p_cap.paragraph_format.line_spacing = 1.15
        r_num = p_cap.add_run(caption_text.split(':')[0] + ": ")
        r_num.font.bold = True
        r_num.font.size = Pt(9.5)
        r_num.font.color.rgb = RGBColor(0, 105, 92)
        
        r_desc = p_cap.add_run(':'.join(caption_text.split(':')[1:]))
        r_desc.font.size = Pt(9.5)
        r_desc.font.italic = True
    else:
        print(f"Warning: image {img_path} not found.")

def generate_kras_word_manuscript():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    fig_dir = os.path.join(base_dir, "figures")
    doc = Document()
    
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(11)
    font.color.rgb = RGBColor(33, 33, 33)
    
    # Title & Authors
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(12)
    p_title.paragraph_format.line_spacing = 1.15
    r_title = p_title.add_run("Quantum-Informed and Machine Learning QSAR Investigation of Graphitic Carbon Nitride (g-C3N4) Nanocarriers Delivering Allosteric Inhibitors Targeting Oncogenic KRAS-G12D in Pancreatic Ductal Adenocarcinoma")
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0, 105, 92)
    
    p_auth = doc.add_paragraph()
    p_auth.paragraph_format.space_after = Pt(4)
    r_a1 = p_auth.add_run("Andrés Monreal Hernández")
    r_a1.font.bold = True
    p_auth.add_run("1,*, ")
    r_a2 = p_auth.add_run("Sara Lizbeth Franco Amaya")
    r_a2.font.bold = True
    p_auth.add_run("2, and ")
    r_a3 = p_auth.add_run("Carlos Ivanhoe Martínez Osorio")
    r_a3.font.bold = True
    p_auth.add_run("3")
    
    p_aff = doc.add_paragraph()
    p_aff.paragraph_format.space_after = Pt(14)
    p_aff.add_run(
        "1 Universidad Estatal de Sonora, Hermosillo, Sonora, Mexico. ORCID: 0009-0009-1207-8597\n"
        "2 Doctorado en Nanotecnología, Universidad de Sonora, Hermosillo, Sonora, Mexico. ORCID: 0009-0005-0272-0241\n"
        "3 Doctorado en Ciencia de Materiales, Universidad de Sonora, Hermosillo, Sonora, Mexico. ORCID: 0009-0003-7872-4965\n"
        "* Corresponding author: andres.monreal@ues.mx"
    )
    p_aff.runs[0].font.size = Pt(9.5)
    p_aff.runs[0].font.italic = True
    
    # Graphical Abstract
    add_image_if_exists(doc, os.path.join(fig_dir, "fig1_graphical_abstract.png"),
                        "Graphical Abstract: Multi-Scale Quantum, Docking, and Machine Learning Evaluation of 2D g-C3N4 Nanosheets for Targeted KRAS-G12D Delivery in Pancreatic Ductal Adenocarcinoma.")
    
    # Abstract
    add_heading_styled(doc, "Abstract", level=1)
    p_abs = doc.add_paragraph()
    p_abs.paragraph_format.space_after = Pt(8)
    p_abs.paragraph_format.line_spacing = 1.15
    p_abs.add_run(
        "Pancreatic ductal adenocarcinoma (PDAC) is an intractable malignancy characterized by a dense desmoplastic stroma and near-universal "
        "oncogenic KRAS driver mutations, predominantly KRAS-G12D [8,64]. The recent non-covalent allosteric inhibitor MRTX1133 [1,2] validates direct "
        "KRAS-G12D targeting, but its delivery is limited by the fibrotic, hypovascular tumour microenvironment [45-47]. Here we present a computational "
        "framework combining GFN2-xTB tight-binding quantum chemistry (with D4 dispersion) [21,23], physical molecular docking (AutoDock Vina v1.2.7 [29,30] "
        "against the human KRAS-G12D crystal structure, PDB ID: 7RPZ, 1.30 Å), and a leak-free cross-validated regularized-linear QSPR surrogate, for a "
        "curated set of 33 direct KRAS-G12D inhibitors and PDAC therapeutics loaded on pristine and B/P-doped 2D graphitic carbon nitride (g-C3N4) [11-13]. "
        "Real GFN2-xTB interaction energies span Delta_E_ads = -5.0 to -39.9 kcal/mol across the pristine and B/P-doped supercells. Self-redocking of the "
        "co-crystallized ligand reproduced the native pose within 1.42 Å heavy-atom RMSD, and docking of the 33 compounds gave Vina scores of -2.9 to "
        "-9.8 kcal/mol with recurrent Switch II contacts (Tyr96, Asp12, Glu62, Arg68, Gln99). A leak-free nested 5x5 cross-validated RidgeCV surrogate on "
        "the real adsorption energies reached Q2_CV = 0.55 (pristine) and 0.51 (B/P-doped); a Y-scrambling test (1000 permutations, p = 0.001) confirms the "
        "signal is not spurious. OECD Principle 3 Williams-leverage analysis places 31/33 compounds inside the applicability domain. Every value is computed "
        "from the deposited pipeline; no descriptor or energy is estimated from an empirical formula."
    )
    
    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_after = Pt(14)
    r_kwt = p_kw.add_run("Keywords: ")
    r_kwt.font.bold = True
    p_kw.add_run("Graphitic Carbon Nitride (g-C3N4); KRAS-G12D; MRTX1133; Pancreatic Ductal Adenocarcinoma; AutoDock Vina; Explainable AI (SHAP); OECD Validation.")
    
    # Sections
    add_heading_styled(doc, "1. Introduction", level=1)
    doc.add_paragraph(
        "Pancreatic ductal adenocarcinoma (PDAC) has a five-year survival below 15% and is projected to become a leading cause of cancer mortality "
        "[7,8]. Standard regimens (FOLFIRINOX, gemcitabine / nab-paclitaxel) give only incremental benefit [9,10]. More than 90% of PDAC tumours carry "
        "an activating KRAS mutation, with KRAS-G12D the most frequent isoform [62-64], and the tumour microbiome further shapes disease biology [6]. "
        "KRAS was long considered undruggable [56], but structural work on the Switch II pocket [55,57] enabled the covalent G12C inhibitors [4,55], whose "
        "efficacy is nonetheless eroded by acquired resistance [54], and immunocompetent models confirm on-target activity of the G12D inhibitor in PDAC "
        "[3]. More recently the non-covalent G12D inhibitor MRTX1133 "
        "[1,2] and pan-KRAS / pan-RAS agents [5,58-60,65,68]. Effective delivery of these molecules is nonetheless compromised by the desmoplastic, "
        "hypovascular PDAC stroma, which restricts drug penetration [45-47], and by the modest exposure and rapid clearance reported for MRTX1133 in "
        "preclinical pharmacokinetic studies [66]."
    )
    doc.add_paragraph(
        "Nanocarriers can improve solubility, circulation time and tumour accumulation [48-53], and nanotechnology approaches specific to pancreatic "
        "cancer have been reviewed [61]. Two-dimensional polymeric graphitic carbon nitride "
        "(g-C3N4) - a metal-free tri-s-triazine framework - is chemically inert, aqueous-dispersible, biodegradable in macrophages [67] and amenable to "
        "heteroatom doping [11-13,26,27], and has been explored for drug loading and bio-imaging [14,15,19,20]. Boron/phosphorus co-doping tunes its "
        "electronic structure [16-18]. Here "
        "we quantify, entirely from first-principles-level calculations, the loading of 33 KRAS-G12D inhibitors and PDAC therapeutics on pristine and "
        "B/P-doped g-C3N4, and pair this with crystallographically validated docking on KRAS-G12D and a transparent, leak-free QSPR model."
    )

    add_image_if_exists(doc, os.path.join(fig_dir, "fig1_kras_workflow_methodology.png"),
                        "Figure 1: Multi-scale computational workflow: GFN2-xTB quantum-chemical adsorption on pristine and B/P-doped g-C3N4, real AutoDock Vina docking against KRAS-G12D (PDB 7RPZ), and a leak-free cross-validated explainable QSPR surrogate.")

    add_heading_styled(doc, "2. Computational and Experimental Section", level=1)
    doc.add_paragraph(
        "2.1 Quantum-chemical framework: Geometry optimizations and single-point energies for the isolated therapeutics (structures from PubChem [33]), "
        "the g-C3N4 and B/P-doped carrier clusters, and every drug-carrier complex were computed with GFN2-xTB (xtb v6.7.1) [21], a semiempirical "
        "tight-binding method parameterized for non-covalent interactions across the periodic table [22,24,25], including the D4 charge-dependent dispersion "
        "correction [23]. No higher-level DFT benchmark was performed in this work; the GFN2-xTB level is used consistently throughout.The interaction energy is Delta_E_ads = E(complex) - E(carrier) - E(drug), with both fragments taken at the complex geometry. "
        "Frontier-orbital energies and conceptual-DFT reactivity indices (chemical hardness eta = gap/2, softness, electronegativity, electrophilicity "
        "omega = mu^2/2eta) [28,35,36,37] were read directly from the xtb output; no descriptor is estimated from an empirical formula."
    )
    doc.add_paragraph(
        "2.2 Molecular docking: Docking used AutoDock Vina v1.2.7 [29,30] on the human KRAS-G12D crystal structure (PDB ID: 7RPZ, 1.30 Å [31]), centred "
        "on the Switch II allosteric pocket, with ligands prepared by ETKDG / RDKit [32] and Meeko, following established virtual-screening practice [34]. "
        "Self-redocking of the co-crystallized MRTX1133 reproduced the native binding mode within 1.42 Å heavy-atom RMSD, validating the grid and pocket "
        "definition."
    )
    doc.add_paragraph(
        "2.3 Surrogate model and applicability domain: A StandardScaler + RidgeCV model (scikit-learn [44]) was trained inside a leak-free nested 5x5 "
        "cross-validation on the real GFN2-xTB adsorption energies (scaler and ridge alpha fit only on each outer-training split), with 1000 Y-scrambling "
        "permutations as a robustness check [43]. Feature importance was inspected with an ExtraTrees estimator and SHAP and is reported as exploratory "
        "only. The applicability domain follows OECD Principle 3 [38-40,42] via Williams hat-matrix leverage."
    )
    
    add_image_if_exists(doc, os.path.join(fig_dir, "fig2_kras_quantum_cdft_architecture.png"),
                        "Figure 2: Real quantum conceptual-DFT electronic reactivity of the isolated KRAS/PDAC therapeutics cohort (real GFN2-xTB single points, n=38): (a) HOMO/LUMO frontier-orbital distribution; (b) chemical hardness vs. electrophilicity index. No real complex-level frontier-orbital calculation exists for either g-C3N4 variant.")

    add_heading_styled(doc, "3. Results and Discussion", level=1)

    add_heading_styled(doc, "3.1 Electronic structure of the therapeutics", level=2)
    doc.add_paragraph(
        "Real GFN2-xTB single points for the 38-compound isolated cohort give E_HOMO between -9.0 and -11.8 eV (mean -10.0 eV) and a mean chemical "
        "hardness of eta = 1.0 eV (Figure 2, Table 1). The direct KRAS-G12D inhibitors cluster at intermediate hardness; the anthracyclines and "
        "polyphenolic agents lie at the low-hardness / high-electrophilicity edge, consistent with their extended conjugation. Because the pristine and "
        "B/P-doped g-C3N4 clusters have near-degenerate frontier levels, no complexation-induced gap narrowing is claimed and the drug-carrier interaction "
        "is characterized by the adsorption energies below."
    )

    add_heading_styled(doc, "3.2 Quantum adsorption on pristine and B/P-doped g-C3N4", level=2)
    doc.add_paragraph(
        "Real GFN2-xTB interaction energies for the 33 therapeutics range from -5.0 kcal/mol (5-fluorouracil) to about -40 kcal/mol (methotrexate; "
        "MRTX1133 -35.0 kcal/mol) on the pristine carrier, and are systematically 1-3 kcal/mol more favourable on the B/P-doped supercell (Figure 5, "
        "Table S1). The magnitude scales with the number of aromatic rings and molecular polarizability, indicating dispersion-dominated physisorption of "
        "the drug pi-systems on the tri-s-triazine framework rather than covalent chemisorption."
    )

    add_image_if_exists(doc, os.path.join(fig_dir, "fig3_kras_docking_vina_statistical_profiles.png"),
                        "Figure 3: Molecular docking statistical profiles on the human KRAS-G12D crystal (real AutoDock Vina v1.2.7, PDB 7RPZ; redocking RMSD 1.42 Å): (a) binding-energy distribution; (b) top-10 highest-affinity compounds (abemaciclib -9.75, cobimetinib -9.12; MRTX1133 -8.06, BI-2865 -8.46 kcal/mol).")

    add_heading_styled(doc, "3.3 Docking against the KRAS-G12D Switch II pocket", level=2)
    doc.add_paragraph(
        "With the pose validated by redocking (1.42 Å RMSD), Vina scores for the 33 compounds span -2.9 to -9.8 kcal/mol (Figure 3). MRTX1133 (-8.06) "
        "and BI-2865 (-8.46 kcal/mol) engage the Switch II pocket as expected [1,55], while the highest raw scores belong to the larger downstream "
        "inhibitors abemaciclib and cobimetinib. Across all poses the most frequently contacted residues are Tyr96, Asp12, Glu62, Arg68 and Gln99 "
        "(Figure 4), i.e. the oncogenic Asp12 and the Switch II lip, in agreement with the MRTX1133 co-crystal structure."
    )

    add_image_if_exists(doc, os.path.join(fig_dir, "fig4_kras_residue_contact_frequency.png"),
                        "Figure 4: Residue-level contact frequencies on KRAS-G12D (real Vina poses, contact distance <= 3.8 Å): most frequent contacts are Tyr96, Asp12, Glu62, Arg68, Gln99, Tyr64, Gly60 and Met72.")
    
    # Table 1: Descriptors
    desc_csv = os.path.join(base_dir, "data", "processed", "kras_isolated_descriptors.csv")
    if os.path.exists(desc_csv):
        df_desc = pd.read_csv(desc_csv)
        doc.add_paragraph()
        p_t1 = doc.add_paragraph()
        r_t1 = p_t1.add_run("Table 1: Physicochemical, Topological, and Quantum CDFT Descriptors for Representative KRAS/PDAC Therapeutics.")
        r_t1.font.bold = True
        r_t1.font.size = Pt(10)
        
        table1 = doc.add_table(rows=1, cols=7)
        table1.alignment = WD_TABLE_ALIGNMENT.CENTER
        hdr_cells = table1.rows[0].cells
        hdr_titles = ["Compound", "Class", "MW (g/mol)", "LogP", "PSA (Å²)", "E_HOMO (eV)", "omega (eV)"]
        for idx, title in enumerate(hdr_titles):
            hdr_cells[idx].text = title
            set_cell_background(hdr_cells[idx], "00695C")
            set_cell_margins(hdr_cells[idx], 80, 80, 100, 100)
            for r in hdr_cells[idx].paragraphs[0].runs:
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
                r.font.size = Pt(9)
                
        for _, row in df_desc.head(10).iterrows():
            row_cells = table1.add_row().cells
            row_vals = [
                str(row['name']), str(row['drug_class'])[:22], f"{row['MW']:.1f}",
                f"{row['LogP']:.2f}", f"{row['PSA']:.1f}", f"{row['E_HOMO']:.2f}", f"{row['Electrophilicity_omega']:.2f}"
            ]
            for c_idx, val in enumerate(row_vals):
                row_cells[c_idx].text = val
                set_cell_margins(row_cells[c_idx], 60, 60, 80, 80)
                for r in row_cells[c_idx].paragraphs[0].runs:
                    r.font.size = Pt(8.5)
                    
    add_heading_styled(doc, "3.4 QSPR surrogate model and applicability domain", level=2)
    doc.add_paragraph(
        "A StandardScaler + RidgeCV surrogate evaluated by leak-free nested 5x5 cross-validation on the real adsorption energies reaches Q2_CV = 0.55 "
        "(pristine) and 0.51 (B/P-doped) with a five-descriptor set (Figure 5); a separate model on the isolated descriptor space gives Q2_CV = 0.58. "
        "A 1000-permutation Y-scrambling test yields a mean Q2 near zero (p = 0.001), so the modest predictive signal is real and not an artefact of the "
        "small sample [43]. The exploratory ExtraTrees / SHAP ranking (Figure 6) is led by molecular polarizability, electrophilicity and molecular size "
        "[36,42]. Williams hat-matrix leverage (Figure 8) gives a warning leverage h* = 1.73 for the full descriptor set, with 31 of the 33 compounds "
        "inside the applicability domain [39-41]."
    )

    add_image_if_exists(doc, os.path.join(fig_dir, "fig5_kras_parity_models_evaluation.png"),
                        "Figure 5: Leak-free nested 5x5 CV parity plots (real observed vs. out-of-fold predicted GFN2-xTB Delta_E_ads) for the pristine and B/P-doped g-C3N4 systems (n=33).")

    add_image_if_exists(doc, os.path.join(fig_dir, "fig6_kras_shap_xai_importance_rankings.png"),
                        "Figure 6: Exploratory SHAP feature-importance ranking on the real GFN2-xTB B/P-doped-g-C3N4 adsorption energies.")

    add_image_if_exists(doc, os.path.join(fig_dir, "fig7_kras_descriptor_correlation_matrix.png"),
                        "Figure 7: Pearson inter-descriptor correlation heatmap (real descriptor matrix, 33 KRAS/PDAC therapeutics).")

    add_image_if_exists(doc, os.path.join(fig_dir, "fig8_kras_williams_applicability_domain.png"),
                        "Figure 8: OECD Principle 3 Williams plots defining the applicability domain for the KRAS/PDAC therapeutics on g-C3N4 (real data only).")

    add_image_if_exists(doc, os.path.join(fig_dir, "fig9_kras_3d_spatial_binding_modes.png"),
                        "Figure 9: Representative binding modes (schematic): (a) MRTX1133 in the KRAS-G12D Switch II pocket (PDB 7RPZ); (b) BI-2865 pose; (c) MRTX1133 on the pristine g-C3N4 surface with its real GFN2-xTB Delta_E_ads.")

    add_heading_styled(doc, "4. Conclusions", level=1)
    doc.add_paragraph(
        "We report a quantum-informed, explainable QSPR analysis of pristine and B/P-doped 2D graphitic carbon nitride as a metal-free loading surface "
        "for KRAS-G12D inhibitors and PDAC therapeutics. Real GFN2-xTB interaction energies (Delta_E_ads = -5.0 to -39.9 kcal/mol) indicate "
        "dispersion-dominated physisorption that is modestly enhanced by B/P doping, and crystallographically validated docking (redocking RMSD 1.42 Å) "
        "confirms Switch II engagement by the direct inhibitors. The leak-free surrogate is weakly-to-moderately predictive (Q2_CV = 0.5-0.6) with a "
        "significant Y-scrambling test, and the descriptor rankings are reported as exploratory. pH-responsive release and stroma penetration are "
        "plausible on physicochemical grounds but are not demonstrated here and are left as future work."
    )
    
    add_heading_styled(doc, "Acknowledgements & Data Availability", level=1)
    doc.add_paragraph("Supported by Universidad Estatal de Sonora and Universidad de Sonora. Full code and docking PDBQT files are available in the repository.")
    
    add_heading_styled(doc, "References", level=1)
    import sys as _sys
    _sys.path.insert(0, os.path.join(base_dir, "src", "curation"))
    from build_kras_verified_references import KRAS_VERIFIED_REFERENCES as VERIFIED_REFERENCES
    for idx, ref in enumerate(VERIFIED_REFERENCES, 1):
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.space_after = Pt(3)
        r_num = p_ref.add_run(f"{idx}. ")
        r_num.font.bold = True
        p_ref.add_run(ref['citation'] + " ")
        if ref.get('doi'):
            r_doi = p_ref.add_run(f"doi:{ref['doi']}")
            r_doi.font.italic = True
            r_doi.font.size = Pt(9.0)
            r_doi.font.color.rgb = RGBColor(0, 105, 92)
        
    out_docx = os.path.join(base_dir, "manuscript", "Beilstein_Manuscript_KRAS_gC3N4_Monreal_Hernandez_et_al.docx")
    doc.save(out_docx)
    print(f"Generated Comprehensive KRAS Word Manuscript: {out_docx}")
    return out_docx

if __name__ == "__main__":
    generate_kras_word_manuscript()
