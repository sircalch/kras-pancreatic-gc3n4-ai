"""
prepare_kras_final_submission_package.py
Packages all generated files for Article 3 (KRAS-G12D & g-C3N4) into an official
submission-ready folder and ZIP package.
"""

import os
import shutil
import zipfile
from docx import Document
from docx.shared import Inches, Pt, RGBColor

def create_kras_cover_letter(sub_dir):
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
    
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_after = Pt(14)
    p_h.add_run(
        "Andrés Monreal Hernández, Ph.D.\n"
        "Universidad Estatal de Sonora\n"
        "Hermosillo, Sonora, Mexico\n"
        "Email: andres.monreal@ues.mx | ORCID: 0009-0009-1207-8597\n"
        "Date: August 30, 2026\n"
    ).font.bold = True
    
    p_ed = doc.add_paragraph()
    p_ed.paragraph_format.space_after = Pt(12)
    p_ed.add_run(
        "To: The Editor-in-Chief\n"
        "Beilstein Journal of Nanotechnology\n"
        "Beilstein-Institut, Frankfurt am Main, Germany\n"
    )
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(12)
    p_sub.add_run("Subject: Submission of Original Research Article for Peer Review").font.bold = True
    
    doc.add_paragraph("Dear Editor-in-Chief,")
    doc.add_paragraph(
        "On behalf of my co-authors (Sara Lizbeth Franco Amaya, Carlos Ivanhoe Martínez Osorio, and myself), "
        "I am pleased to submit our original research manuscript titled:"
    )
    
    p_t = doc.add_paragraph()
    p_t.paragraph_format.left_indent = Inches(0.4)
    p_t.paragraph_format.space_after = Pt(10)
    r_t = p_t.add_run("“Quantum-Informed and Machine Learning QSAR Investigation of Graphitic Carbon Nitride (g-C3N4) Nanocarriers Delivering Allosteric Inhibitors Targeting Oncogenic KRAS-G12D in Pancreatic Ductal Adenocarcinoma”")
    r_t.font.bold = True
    r_t.font.color.rgb = RGBColor(0, 105, 92)
    
    doc.add_paragraph(
        "for consideration for publication as a Full Research Article in the Beilstein Journal of Nanotechnology."
    )
    
    doc.add_paragraph(
        "The study integrates GFN2-xTB quantum-chemical adsorption modeling of pristine and B/P-doped 2D graphitic carbon "
        "nitride (g-C3N4), physical AutoDock Vina docking against the human KRAS-G12D crystal structure (PDB ID: 7RPZ, "
        "1.45 Å; native MRTX1133 pose reproduced at 1.419 Å heavy-atom RMSD), and a leak-free nested cross-validated "
        "RidgeCV surrogate model, for a curated set of 33 KRAS-G12D allosteric inhibitors and PDAC therapeutics. "
        "All quantum, docking and machine-learning results in the manuscript are computed from the deposited pipeline; "
        "no descriptor or energy value is estimated from an empirical formula."
    )
    
    doc.add_paragraph(
        "All authors have approved the manuscript and confirm no competing interests."
    )
    
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(14)
    p_sign.add_run(
        "Sincerely,\n\n"
        "Andrés Monreal Hernández, Ph.D. (Corresponding Author)\n"
        "Universidad Estatal de Sonora, Mexico\n"
        "Email: andres.monreal@ues.mx"
    )
    
    out_docx = os.path.join(sub_dir, "01_Cover_Letter_Beilstein_KRAS.docx")
    doc.save(out_docx)
    print(f"Generated KRAS Cover Letter: {out_docx}")


def create_kras_cover_letter_md(sub_dir):
    """Molecular Diversity edition. Only real, pipeline-traceable claims."""
    doc = Document()
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Inches(1.0)
        s.left_margin = s.right_margin = Inches(1.0)
    f = doc.styles['Normal'].font
    f.name = 'Times New Roman'; f.size = Pt(11); f.color.rgb = RGBColor(33, 33, 33)

    doc.add_paragraph("Andrés Monreal Hernández, Ph.D.\nUniversidad Estatal de Sonora, Hermosillo, Sonora, Mexico\n"
                      "Email: andres.monreal@ues.mx | ORCID: 0009-0009-1207-8597").runs[0].font.bold = True
    doc.add_paragraph("To: The Editor-in-Chief, Molecular Diversity (Springer Nature)")
    doc.add_paragraph("Dear Editor,")
    doc.add_paragraph("We submit our original research manuscript for consideration in Molecular Diversity:")
    r = doc.add_paragraph().add_run("“Quantum-Validated QSPR and Molecular Screening of KRAS-G12D Inhibitors across "
                                    "Graphitic Carbon Nitride Interaction Space”")
    r.font.bold = True; r.font.color.rgb = RGBColor(0, 105, 92)
    doc.add_paragraph(
        "The work combines cheminformatics descriptors, physical docking and tight-binding quantum chemistry to "
        "rank a curated set of 33 KRAS-G12D inhibitors and PDAC therapeutics by their loading behaviour on 2D "
        "g-C3N4, in line with the journal's scope in molecular design and structure–property relationships.")
    doc.add_paragraph("Real, pipeline-traceable results:").runs[0].font.bold = True
    for h in [
        "Redocking on the human KRAS-G12D crystal structure (PDB ID: 7RPZ, 1.45 Å) reproduced the native "
        "MRTX1133 pose at 1.419 Å heavy-atom RMSD (AutoDock Vina v1.2.7).",
        "GFN2-xTB single-point interaction energies for all 33 drugs on pristine and B/P-doped g-C3N4 clusters "
        "span Delta_E_ads = -5.0 to -39.9 kcal/mol; frontier-orbital and conceptual-DFT indices are taken "
        "directly from the xtb output (no empirical formula).",
        "Leak-free nested 5x5 cross-validated RidgeCV surrogate on the real GFN2-xTB adsorption energies: "
        "Q2_CV = +0.584 for the primary QSPR model; the per-carrier figure models reach Q2_CV = 0.55 (pristine) "
        "and 0.51 (B/P-doped); 1000 Y-scrambling permutations, p = 0.001.",
        "OECD Principle 3 applicability domain by Williams leverage: 31/33 compounds inside the domain.",
        "Full open-source pipeline and data archive (Zenodo 10.5281/zenodo.22187819).",
    ]:
        p = doc.add_paragraph(h); p.paragraph_format.left_indent = Inches(0.3)
    doc.add_paragraph("The manuscript is original, not under consideration elsewhere, and all authors approve the "
                      "submission and declare no competing interests.")
    doc.add_paragraph("Sincerely,\nAndrés Monreal Hernández, Ph.D. (Corresponding Author)")
    out_docx = os.path.join(sub_dir, "01_Cover_Letter_Molecular_Diversity.docx")
    doc.save(out_docx)
    print(f"Generated KRAS Molecular Diversity Cover Letter: {out_docx}")


def build_kras_submission_bundle():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sub_dir = os.path.join(base_dir, "manuscript", "submission_ready")
    os.makedirs(sub_dir, exist_ok=True)
    
    create_kras_cover_letter(sub_dir)
    create_kras_cover_letter_md(sub_dir)

    manuscripts = {
        os.path.join(base_dir, "manuscript", "KRAS_gC3N4_Full_Q1_Research_Paper_Monreal_Hernandez_et_al.docx"): "02_Manuscript_KRAS_gC3N4_Full_Q1_Research_Paper.docx",
        os.path.join(base_dir, "manuscript", "Beilstein_Manuscript_KRAS_gC3N4_Monreal_Hernandez_et_al.docx"): "02_Manuscript_KRAS_gC3N4_Beilstein_Submission.docx"
    }
    
    for src_docx, dst_name in manuscripts.items():
        dst_docx = os.path.join(sub_dir, dst_name)
        if os.path.exists(src_docx):
            shutil.copyfile(src_docx, dst_docx)

    src_si = os.path.join(base_dir, "manuscript", "KRAS_gC3N4_Supporting_Information_Table_S1.docx")
    dst_si = os.path.join(sub_dir, "03_Supporting_Information_KRAS_gC3N4_Monreal_Hernandez_et_al.docx")
    if os.path.exists(src_si):
        shutil.copyfile(src_si, dst_si)

    zip_path = os.path.join(base_dir, "kras-pancreatic-gC3N4-ai-FINAL-SUBMISSION-READY.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_f:
        for root, dirs, files in os.walk(sub_dir):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, sub_dir)
                zip_f.write(file_path, os.path.join("submission_ready", rel_path))
                
    print(f"\n=======================================================")
    print(f">>> KRAS SUBMISSION PACKAGE GENERATED SUCCESSFULLY ({os.path.getsize(zip_path)} bytes) <<<")
    print(f" -> {zip_path}")
    print(f"=======================================================")

if __name__ == "__main__":
    build_kras_submission_bundle()
