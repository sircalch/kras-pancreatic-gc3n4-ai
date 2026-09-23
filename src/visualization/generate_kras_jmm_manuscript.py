"""
generate_kras_jmm_manuscript.py
================================
Builds a Journal of Molecular Modeling (Springer) submission variant of the
KRAS-G12D / g-C3N4 manuscript. Does NOT touch the Beilstein or Molecular
Diversity ("Full_Q1") outputs -- it post-processes a freshly regenerated copy
of the Full_Q1 docx, replacing only the Abstract (JMM requires a structured
Context/Methods abstract, 150-250 words) and trimming the accidental
"Molecular Diversity" keyword left over from that edition.

JMM submission-guideline requirements applied here (link.springer.com/journal/894/submission-guidelines):
  - Structured abstract with two subheadings: "Context" (why the work was
    done + summary of results) and "Methods" (computational techniques/
    software used).
  - Abstract length 150-250 words.
  - 4-6 keywords.
  - Plain font (Times New Roman, already used throughout).
"""

import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from docx import Document
from docx.shared import Pt

import generate_kras_full_manuscript as full_gen

JMM_CONTEXT = (
    "Oncogenic KRAS-G12D is a challenging pancreatic ductal adenocarcinoma (PDAC) target: MRTX1133 engages "
    "the Switch II allosteric pocket with high potency but has unfavorable pharmacokinetic properties, "
    "motivating exploration of two-dimensional graphitic carbon nitride (g-C3N4) as a supramolecular delivery "
    "template. We evaluate the molecular interaction space of 33 curated KRAS-G12D therapeutics across "
    "pristine and B/P co-doped g-C3N4 templates, benchmark a docking protocol via crystallographic pose-"
    "recovery (1.419 Å heavy-atom RMSD against the 1.30 Å human KRAS-G12D structure, PDB 7RPZ), and train "
    "a leak-free nested cross-validated QSPR surrogate. The surrogate achieves genuinely predictive out-of-fold "
    "accuracy (nested Q²_CV = 0.584; 1,000-permutation Y-scrambling p = 0.001); its applicability-domain "
    "coverage was stress-tested on a combinatorially enumerated 350-candidate virtual library (73.7% inside "
    "domain), and five independently curated clinical-stage oncology leads (Futibatinib, Belumosudil) were "
    "confirmed by prospective quantum calculations."
)

JMM_METHODS = (
    "GFN2-xTB tight-binding quantum calculations were performed on a finite 48-atom C21N21H6 heptazine "
    "cluster model (pristine and B/P co-doped, C20B1N20P1H6) to obtain standardized vertical electronic "
    "interaction and intramolecular deformation energies at a fixed initial stacking separation (z = 3.35 Å). "
    "AutoDock Vina docking against the KRAS-G12D Switch II pocket (PDB 7RPZ) was validated by redocking the "
    "native MRTX1133 pose. A Ridge-regression QSPR surrogate, structured under OECD Principles 1-5, was fit "
    "inside a nested 5×5 cross-validation (StandardScaler and Ridge-alpha tuning confined to outer-training "
    "folds only) and validated by 1,000-permutation Y-scrambling. Applicability-domain leverage (h* = 0.455) "
    "was stress-tested on a combinatorially enumerated 350-candidate virtual library, and separately, "
    "independently curated clinical-stage leads were evaluated by prospective GFN2-xTB single-point quantum "
    "confirmation."
)

JMM_KEYWORDS = (
    "KRAS-G12D; MRTX1133; Graphitic Carbon Nitride; QSPR Surrogate Modeling; "
    "GFN2-xTB Quantum Chemistry; Virtual Screening."
)


def _find_paragraph_index(doc, text_startswith):
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip().startswith(text_startswith):
            return i
    return -1


def generate_kras_jmm_manuscript():
    # Regenerate the Full_Q1 docx fresh so the JMM edition is never stale.
    full_gen.generate_kras_full_manuscript()

    src_docx = os.path.join(base_dir, "manuscript", "submission_ready",
                             "02_Manuscript_KRAS_gC3N4_Full_Q1_Research_Paper.docx")
    doc = Document(src_docx)

    # --- Locate the "Abstract" heading and the single paragraph after it ---
    abstract_heading_idx = None
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip() == "Abstract" and p.style.name.startswith("Heading"):
            abstract_heading_idx = i
            break
    if abstract_heading_idx is None:
        raise RuntimeError("Could not find 'Abstract' heading in source manuscript.")

    abstract_para = doc.paragraphs[abstract_heading_idx + 1]
    keywords_para = doc.paragraphs[abstract_heading_idx + 2]

    if "Keywords" not in keywords_para.text:
        raise RuntimeError("Unexpected structure: paragraph after Abstract body is not the Keywords line.")

    # --- Replace the old single-block abstract with a structured Context/Methods abstract ---
    # Insert two new labeled paragraphs immediately before the old abstract paragraph,
    # then delete the old one outright (python-docx has no in-place "replace text" for
    # a paragraph with mixed runs, so insert-then-remove is the reliable approach).
    p_context = abstract_para.insert_paragraph_before()
    r_label = p_context.add_run("Context ")
    r_label.font.bold = True
    p_context.add_run(JMM_CONTEXT)

    p_methods = abstract_para.insert_paragraph_before()
    r_label2 = p_methods.add_run("Methods ")
    r_label2.font.bold = True
    p_methods.add_run(JMM_METHODS)

    # Remove the now-empty original abstract paragraph.
    abstract_para._element.getparent().remove(abstract_para._element)

    # --- Fix the keywords line (drop the leftover "Molecular Diversity" journal-name artifact) ---
    for run in list(keywords_para.runs):
        run.text = ""
    keywords_para.runs[0].text = "Keywords: "
    keywords_para.runs[0].font.bold = True
    keywords_para.add_run(JMM_KEYWORDS)

    # --- Rename "4. Conclusions" -> "4. Summary" (JMM's own naming; also matches
    # the GBM/Tau/TNBC JMM editions for consistency across the series) ---
    for p in doc.paragraphs:
        if p.style.name.startswith("Heading") and p.text.strip() == "4. Conclusions" and p.runs:
            p.runs[0].text = "4. Summary"
            break

    out_dir = os.path.join(base_dir, "manuscript", "submission_ready")
    out_path = os.path.join(out_dir, "02_Manuscript_KRAS_gC3N4_JMM_Submission.docx")
    doc.save(out_path)
    print(f"[SUCCESS] Generated JMM submission manuscript: {out_path}")
    return out_path


if __name__ == "__main__":
    generate_kras_jmm_manuscript()
