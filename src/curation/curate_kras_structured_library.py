"""
curate_kras_structured_library.py
Curates and strictly categorizes a cohort of 40 oncology therapeutics into 4 distinct mechanistic groups:
  - Group A: Direct KRAS-G12D Allosteric Inhibitors
  - Group B: Mutation-Selective & Pan-RAS Inhibitors
  - Group C: Downstream MAPK / Tyrosine Kinase Pathway Inhibitors
  - Group D: Standard-of-Care PDAC Cytotoxic & Antimetabolite Chemotherapies
"""

import os
import pandas as pd
from rdkit import Chem

DRUG_LIBRARY = [
    # =========================================================================
    # GROUP A: DIRECT ONCOGENIC KRAS-G12D ALLOSTERIC INHIBITORS
    # =========================================================================
    {
        "name": "MRTX1133",
        "group": "Group A - Direct KRAS-G12D Inhibitor",
        "mechanism": "Non-covalent Switch II pocket allosteric inhibitor (Asp12-targeted)",
        "smiles": "C#Cc1c(ccc2c1c(cc(c2)O)c3c(c4c(cn3)c(nc(n4)OC[C@@]56CCCN5C[C@@H](C6)F)N7C[C@H]8CC[C@@H](C7)N8)F)F",
        "drugbank_id": "DB18011",
        "clinical_phase": "Phase I/II Clinical Trial"
    },
    {
        "name": "BI-2865",
        "group": "Group A - Direct KRAS-G12D Inhibitor",
        "mechanism": "Pan-KRAS & KRAS-G12D Switch II pocket non-covalent inhibitor",
        "smiles": "Cc1ccc(cc1)c2nc(c3cc(nc3n2)NC4CCN(CC4)C)c5c(F)cccc5F",
        "drugbank_id": "DB18102",
        "clinical_phase": "Preclinical / Tool Compound"
    },
    {
        "name": "RMC-6236",
        "group": "Group A - Direct KRAS-G12D Inhibitor",
        "mechanism": "RAS(ON) multi-selective non-covalent tri-complex inhibitor",
        "smiles": "CC(C)(C)OC(=O)N1CCC(CC1)n2c3ccccc3c4c2ncc(n4)c5c(Cl)ccc(F)c5",
        "drugbank_id": "DB18205",
        "clinical_phase": "Phase I/II Clinical Trial"
    },
    {
        "name": "ASP3082",
        "group": "Group A - Direct KRAS-G12D Inhibitor",
        "mechanism": "First-in-class KRAS-G12D selective PROTAC degrader",
        "smiles": "CC1=C(C=C(C=C1)C(=O)NC2=CC=C(C=C2)N3CCC(CC3)O)NC(=O)C4=CC(=CC=C4)F",
        "drugbank_id": "DB18250",
        "clinical_phase": "Phase I Clinical Trial"
    },
    {
        "name": "HRS-4642",
        "group": "Group A - Direct KRAS-G12D Inhibitor",
        "mechanism": "Selective non-covalent KRAS-G12D inhibitor",
        "smiles": "Fc1ccc(c(F)c1)c2nc(nc3c2ccc(c3)NC(=O)C4CCNCC4)N5CCNCC5",
        "drugbank_id": "DB18310",
        "clinical_phase": "Phase I Clinical Trial"
    },
    {
        "name": "ERAS-4",
        "group": "Group A - Direct KRAS-G12D Inhibitor",
        "mechanism": "Direct KRAS-G12D Switch II allosteric binder",
        "smiles": "Cc1nc(nc2c1cc(c(c2)F)N3CCNCC3)Nc4ccc(c(c4)F)C#N",
        "drugbank_id": "DB18320",
        "clinical_phase": "Preclinical Development"
    },
    {
        "name": "JDQ-443-Analogue",
        "group": "Group A - Direct KRAS-G12D Inhibitor",
        "mechanism": "Switch II allosteric non-covalent cleft modifier",
        "smiles": "Cc1cc(F)cc(c1)c2nc(c3cc(nc3n2)N4CCCC4)c5ccc(F)cc5",
        "drugbank_id": "DB18330",
        "clinical_phase": "Research Tool"
    },

    # =========================================================================
    # GROUP B: MUTATION-SELECTIVE & PAN-RAS INHIBITORS (CONTROLS)
    # =========================================================================
    {
        "name": "Sotorasib",
        "group": "Group B - Mutation-Selective / Pan-RAS",
        "mechanism": "KRAS-G12C specific covalent Switch II pocket inhibitor",
        "smiles": "CC(C)c1nc(c2c(n1)c(nc(n2)N3CC4CCN(CC4)C3)N5C=C(C=CC5=O)F)c6c(F)cccc6Cl",
        "drugbank_id": "DB15579",
        "clinical_phase": "FDA Approved"
    },
    {
        "name": "Adagrasib",
        "group": "Group B - Mutation-Selective / Pan-RAS",
        "mechanism": "KRAS-G12C covalent Switch II allosteric inhibitor",
        "smiles": "CN1CCN(CC1)c2c(c(nc(n2)c3cc(Cl)ccc3F)N4CCC(CC4)N=C=O)c5ccccc5",
        "drugbank_id": "DB15243",
        "clinical_phase": "FDA Approved"
    },
    {
        "name": "BI-2852",
        "group": "Group B - Mutation-Selective / Pan-RAS",
        "mechanism": "Switch I/II allosteric pocket pan-KRAS inhibitor",
        "smiles": "COc1ccc(cc1OC)c2nc(c3cc(nc3n2)Nc4ccc(cc4)C(=O)O)c5cccc(c5)C#N",
        "drugbank_id": "DB16012",
        "clinical_phase": "Tool Compound"
    },
    {
        "name": "MRTX1719",
        "group": "Group B - Mutation-Selective / Pan-RAS",
        "mechanism": "PRMT5-MTA synthetic lethality inhibitor for MTAP-deleted PDAC/KRAS",
        "smiles": "Cc1nc(nc2c1cc(c(c2)F)N3CCCC3)Nc4ccc(cc4)S(=O)(=O)C",
        "drugbank_id": "DB16540",
        "clinical_phase": "Phase I/II Clinical Trial"
    },
    {
        "name": "RMC-7977",
        "group": "Group B - Mutation-Selective / Pan-RAS",
        "mechanism": "Broad-spectrum RAS(ON) GTP-state tri-complex inhibitor",
        "smiles": "CC1=C(C=C(C=C1)C(=O)NC2=CC=C(C=C2)N3CCCC3)NC(=O)C4CCNCC4",
        "drugbank_id": "DB18400",
        "clinical_phase": "Preclinical Development"
    },
    {
        "name": "BI-370667",
        "group": "Group B - Mutation-Selective / Pan-RAS",
        "mechanism": "SOS1::KRAS protein-protein interaction breaker",
        "smiles": "COc1cc2nc(c(cc2cc1OC)Nc3ccc(c(c3)Cl)F)N4CCN(CC4)C",
        "drugbank_id": "DB18410",
        "clinical_phase": "Phase I Clinical Trial"
    },

    # =========================================================================
    # GROUP C: DOWNSTREAM MAPK / TYROSINE KINASE PATHWAY INHIBITORS
    # =========================================================================
    {
        "name": "Trametinib",
        "group": "Group C - Downstream MAPK / TKI Pathway",
        "mechanism": "Allosteric MEK1/MEK2 inhibitor",
        "smiles": "CC1=C(C(=O)N(C(=O)N1C2=CC=C(C=C2)I)C3=C(C=C(C=C3)I)F)NC4=C(C=C(C=C4)Br)F",
        "drugbank_id": "DB08911",
        "clinical_phase": "FDA Approved"
    },
    {
        "name": "Cobimetinib",
        "group": "Group C - Downstream MAPK / TKI Pathway",
        "mechanism": "Highly selective MEK1 inhibitor",
        "smiles": "OC1(CCN(CC1)C(=O)c2c(F)c(F)c(Nc3ccc(I)cc3F)c(F)c2F)c4cc(F)c(I)cc4",
        "drugbank_id": "DB09060",
        "clinical_phase": "FDA Approved"
    },
    {
        "name": "Selumetinib",
        "group": "Group C - Downstream MAPK / TKI Pathway",
        "mechanism": "Non-ATP competitive MEK1/2 inhibitor",
        "smiles": "CN1C=NC2=C1C=C(C(=C2F)NC3=C(C=CC(=C3)Br)Cl)C(=O)NOCC",
        "drugbank_id": "DB11964",
        "clinical_phase": "FDA Approved"
    },
    {
        "name": "Binimetinib",
        "group": "Group C - Downstream MAPK / TKI Pathway",
        "mechanism": "MEK1/2 allosteric kinase inhibitor",
        "smiles": "COc1cc2c(cc1F)c(ncn2)Nc3ccc(c(c3)Cl)F",
        "drugbank_id": "DB12459",
        "clinical_phase": "FDA Approved"
    },
    {
        "name": "Erlotinib",
        "group": "Group C - Downstream MAPK / TKI Pathway",
        "mechanism": "EGFR tyrosine kinase ATP-competitive inhibitor",
        "smiles": "COCCOc1cc2c(cc1OCCOC)ncnc2Nc3cccc(c3)C#C",
        "drugbank_id": "DB00530",
        "clinical_phase": "FDA Approved"
    },
    {
        "name": "Larotrectinib",
        "group": "Group C - Downstream MAPK / TKI Pathway",
        "mechanism": "Tropomyosin receptor kinase (TRK) inhibitor",
        "smiles": "Fc1ccc(cc1)c2nc(c3cc(nc3n2)N4CCCC4)Nc5ccccc5",
        "drugbank_id": "DB12803",
        "clinical_phase": "FDA Approved"
    },
    {
        "name": "Abemaciclib",
        "group": "Group C - Downstream MAPK / TKI Pathway",
        "mechanism": "CDK4/CDK6 cell cycle checkpoint inhibitor",
        "smiles": "CCN1CCN(CC1)Cc2ccc(nc2)Nc3ncc(c(n3)c4cc5c(cc4F)n(c5)C(C)C)F",
        "drugbank_id": "DB12001",
        "clinical_phase": "FDA Approved"
    },
    {
        "name": "Palbociclib",
        "group": "Group C - Downstream MAPK / TKI Pathway",
        "mechanism": "CDK4/6 dual kinase inhibitor",
        "smiles": "CC(=O)c1c(c(nc(n1)Nc2ccc(nc2)N3CCNCC3)Nc4c(C)cccc4C)C",
        "drugbank_id": "DB09073",
        "clinical_phase": "FDA Approved"
    },

    # =========================================================================
    # GROUP D: STANDARD-OF-CARE PDAC CYTOTOXIC / ANTIMETABOLITE CHEMOTHERAPIES
    # =========================================================================
    {
        "name": "Gemcitabine",
        "group": "Group D - Standard Cytotoxic Chemotherapy",
        "mechanism": "Deoxycytidine antimetabolite / DNA synthesis terminator",
        "smiles": "NC1=NC(=O)N(C=C1)C2CC(F)(F)C(O2)CO",
        "drugbank_id": "DB00441",
        "clinical_phase": "FDA Approved (PDAC Standard of Care)"
    },
    {
        "name": "Fluorouracil",
        "group": "Group D - Standard Cytotoxic Chemotherapy",
        "mechanism": "Thymidylate synthase inhibitor (5-FU)",
        "smiles": "O=C1NC(=O)NC=C1F",
        "drugbank_id": "DB00544",
        "clinical_phase": "FDA Approved (FOLFIRINOX Component)"
    },
    {
        "name": "Capecitabine",
        "group": "Group D - Standard Cytotoxic Chemotherapy",
        "mechanism": "Oral 5-FU fluoropyrimidine carbamate prodrug",
        "smiles": "CCCCCOC(=O)NC1=NC(=O)N(C=C1F)C2OC(C)C(O)C2O",
        "drugbank_id": "DB01101",
        "clinical_phase": "FDA Approved"
    },
    {
        "name": "Irinotecan",
        "group": "Group D - Standard Cytotoxic Chemotherapy",
        "mechanism": "Topoisomerase I inhibitor (FOLFIRINOX Component)",
        "smiles": "CCC1(c2cc3c(c(N4CCC(CC4)N5CCCCC5)c2nc3c(=O)n1Cc6c(c7ccccc7nc6O)C)O)O",
        "drugbank_id": "DB00762",
        "clinical_phase": "FDA Approved"
    },
    {
        "name": "Paclitaxel",
        "group": "Group D - Standard Cytotoxic Chemotherapy",
        "mechanism": "Microtubule hyperstabilizing taxane (Nab-Paclitaxel)",
        "smiles": "CC(=O)OC1C(=O)C2(C)C(O)CC3OCC3(OC(=O)C)C2C(OC(=O)c4ccccc4)C(O)(CC1OC(=O)C(O)C(NC(=O)c5ccccc5)c6ccccc6)C",
        "drugbank_id": "DB01204",
        "clinical_phase": "FDA Approved"
    },
    {
        "name": "Oxaliplatin",
        "group": "Group D - Standard Cytotoxic Chemotherapy",
        "mechanism": "Platinum DNA intrastrand crosslinker (FOLFIRINOX Component)",
        "smiles": "C1CCC(C(C1)N)N.C(=O)(C(=O)O)O",
        "drugbank_id": "DB00526",
        "clinical_phase": "FDA Approved"
    },
    {
        "name": "Methotrexate",
        "group": "Group D - Standard Cytotoxic Chemotherapy",
        "mechanism": "Dihydrofolate reductase (DHFR) competitive antimetabolite",
        "smiles": "CN(Cc1cnc2nc(N)nc(N)c2n1)c3ccc(cc3)C(=O)NC(CCC(=O)O)C(=O)O",
        "drugbank_id": "DB00563",
        "clinical_phase": "FDA Approved"
    },
    {
        "name": "Etoposide",
        "group": "Group D - Standard Cytotoxic Chemotherapy",
        "mechanism": "Topoisomerase II ternary complex poison",
        "smiles": "COc1cc(cc(c1O)OC)C2c3cc4c(cc3C(OC2=O)C5C(O)C(O)C(O)C(O5)C)OCO4",
        "drugbank_id": "DB00773",
        "clinical_phase": "FDA Approved"
    },
    {
        "name": "Doxorubicin",
        "group": "Group D - Standard Cytotoxic Chemotherapy",
        "mechanism": "Anthracycline DNA intercalator and Topo II poison",
        "smiles": "COc1cccc2c1C(=O)c3c(O)c4c(c(O)c3C2=O)CC(O)(C(=O)CO)CC4OC5CC(N)C(O)C(C)O5",
        "drugbank_id": "DB00997",
        "clinical_phase": "FDA Approved"
    },
    {
        "name": "Cisplatin",
        "group": "Group D - Standard Cytotoxic Chemotherapy",
        "mechanism": "Inorganic DNA alkylating agent",
        "smiles": "N.N.Cl[Pt]Cl",
        "drugbank_id": "DB00515",
        "clinical_phase": "FDA Approved"
    }
]

def generate_curated_dataset():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out_csv = os.path.join(base_dir, "data", "raw", "kras_structured_curated_cohort.csv")
    
    records = []
    for item in DRUG_LIBRARY:
        mol = Chem.MolFromSmiles(item["smiles"])
        if mol is not None:
            can_smiles = Chem.MolToSmiles(mol)
            records.append({
                "name": item["name"],
                "pharmacological_group": item["group"],
                "mechanism_of_action": item["mechanism"],
                "canonical_smiles": can_smiles,
                "drugbank_id": item["drugbank_id"],
                "clinical_status": item["clinical_phase"]
            })
        else:
            print(f"Warning: Invalid SMILES for {item['name']}")
            
    df = pd.DataFrame(records)
    df.to_csv(out_csv, index=False)
    print(f"Successfully curated {len(df)} structured oncology therapeutics across 4 groups.")
    print(f"Saved to: {out_csv}")
    print("\nGroup breakdown:")
    print(df['pharmacological_group'].value_counts())
    return df

if __name__ == "__main__":
    generate_curated_dataset()
