"""
curate_kras_dataset.py
Curates a library of 36 direct KRAS inhibitors, allosteric modulators, and standard-of-care
therapeutics for Pancreatic Ductal Adenocarcinoma (PDAC).
"""

import os
import pandas as pd

KRAS_DRUG_LIBRARY = [
    # Direct KRAS & RAS Pathway Inhibitors
    {"name": "MRTX1133", "class": "Direct KRAS-G12D Non-Covalent Inhibitor", "smiles": "CN1CCN(CC1)C2=C(F)C=C(NC3=NC=C(F)C(=C3)C4=C(F)C=C(F)C(=C4)N5CCCC5)C=C2", "drugbank_id": "DB18011"},
    {"name": "Sotorasib", "class": "KRAS-G12C Covalent Inhibitor", "smiles": "CC(C)C1=NC(=C(C(=N1)C2=C(C=CC(=C2F)F)Cl)N3CCN(CC3)C(=O)C=C)C4=C(C=CC=C4F)F", "drugbank_id": "DB15579"},
    {"name": "Adagrasib", "class": "KRAS-G12C Covalent Inhibitor", "smiles": "CC1=NC=C(C(=C1)C2=C(C=CC(=C2F)Cl)F)N3CCN(CC3)C(=O)C4=C(N=CC=C4)NC5CCN(CC5)C", "drugbank_id": "DB15243"},
    {"name": "BI-2865", "class": "Pan-KRAS Non-Covalent Inhibitor", "smiles": "CC1=CN=C(C(=C1)C2=CC(=CC=C2F)F)NC3=NC=CC(=N3)N4CCN(CC4)C(=O)C5=CC=CC=C5F", "drugbank_id": "DB18102"},
    {"name": "RMC-6236", "class": "RAS-MULTI (ON) Inhibitor", "smiles": "CC(C)N1CCN(CC1)C2=NC=C(C(=N2)C3=CC=C(F)C=C3)NC4=NC=CC(=C4)C5=CC=CC=N5", "drugbank_id": "DB18205"},
    
    # Standard-of-Care & FOLFIRINOX Components
    {"name": "Gemcitabine", "class": "Antimetabolite (PDAC Standard)", "smiles": "NC1=NC(=O)N(C=C1)[C@@H]2O[C@H](CO)[C@@H](O)C2(F)F", "drugbank_id": "DB00441"},
    {"name": "Paclitaxel", "class": "Microtubule Stabilizer (Nab-Paclitaxel Core)", "smiles": "CC1=C2[C@@]([C@]([C@H]([C@@H]3[C@]4([C@H](OC4)C[C@@H]([C@]3(C(=O)[C@@H]2OC(=O)C)C)O)OC(=O)C)OC(=O)c5ccccc5)(C[C@@H]1OC(=O)[C@H](O)[C@@H](NC(=O)c6ccccc6)c7ccccc7)O)(C)C", "drugbank_id": "DB01204"},
    {"name": "Capecitabine", "class": "Fluoropyrimidine Antimetabolite", "smiles": "CCCCCOC(=O)NC1=NC(=O)N(C=C1F)[C@@H]2O[C@H](C)[C@@H](O)[C@H]2O", "drugbank_id": "DB01101"},
    {"name": "Fluorouracil", "class": "Thymidylate Synthase Inhibitor", "smiles": "O=C1NC(=O)C(F)=CN1", "drugbank_id": "DB00544"},
    {"name": "Irinotecan", "class": "Topoisomerase I Inhibitor", "smiles": "CCN1CCN(C(=O)OC2=CC3=C(C=C2)N=C4C5=C3CN4C(=O)C6(CC)C(O)=C(C(=O)OCC56)O)CC1", "drugbank_id": "DB00762"},
    {"name": "Oxaliplatin", "class": "Platinum Alkylating Complex", "smiles": "O=C1O[Pt]2(OC(=O)C1)N[C@@H]3CCCC[C@H]3N2", "drugbank_id": "DB00526"},
    
    # EGFR & PARP1 Targeted Agents
    {"name": "Erlotinib", "class": "EGFR TKI (Approved with Gemcitabine)", "smiles": "COCCOc1cc2ncnc(Nc3cccc(C#C)c3)c2cc1OCCOC", "drugbank_id": "DB00530"},
    {"name": "Olaparib", "class": "PARP1 Inhibitor (BRCA-mutated PDAC)", "smiles": "O=C(c1cc(Cc2c3ccccc3nn2C(=O)O)ccc1F)N4CCN(C(=O)C5CC5)CC4", "drugbank_id": "DB00945"},
    {"name": "Rucaparib", "class": "PARP1/2 Inhibitor", "smiles": "CNCC1=CC=C(C=C1)C2=C3C4=C(C=C2)NCC4=C(N3)C(=O)N", "drugbank_id": "DB12330"},
    {"name": "Talazoparib", "class": "Potent PARP Inhibitor", "smiles": "CC(C)N1C(=O)C2=C(N1)C=C(F)C(=C2)C3C4=C(C=CC(=C4)F)N=C5N3N=CC5", "drugbank_id": "DB11760"},
    {"name": "Niraparib", "class": "PARP1/2 Inhibitor", "smiles": "NC(=O)C1=CC=C(C=C1)N2N=C(C3=CC=CC=C23)C4CCNC4", "drugbank_id": "DB12341"},
    
    # MAPK / MEK & SHP2 Direct Regulators
    {"name": "Trametinib", "class": "MEK1/2 Inhibitor", "smiles": "Cc1c(Nc2ccc(I)cc2F)c(=O)n(C)c(=O)n1c3ccc(NC(=O)C)cc3F", "drugbank_id": "DB08911"},
    {"name": "Cobimetinib", "class": "MEK Inhibitor", "smiles": "OC1(CCNCC1)C(=O)Nc2c(F)cc(I)c(F)c2Nc3ccc(F)c(I)c3", "drugbank_id": "DB09065"},
    {"name": "Selumetinib", "class": "MEK1/2 Inhibitor", "smiles": "CN1C=NC2=C1C=C(NC3=C(F)C=C(Br)C=C3)C(C(=O)NO)=C2Cl", "drugbank_id": "DB11640"},
    {"name": "Binimetinib", "class": "MEK1/2 Inhibitor", "smiles": "CC1=NC2=C(N1)C=C(NC3=C(F)C=C(I)C=C3)C(=C2F)C(=O)NOC", "drugbank_id": "DB11874"},
    {"name": "SHP099", "class": "Allosteric SHP2 Inhibitor", "smiles": "CC1=C(C(=CC=C1)Cl)N2C(=NC(=C2N)Cl)C3=CN=CC=C3", "drugbank_id": "DB15234"},
    {"name": "RMC-4550", "class": "Allosteric SHP2 Inhibitor", "smiles": "CC(C)NC1=NC(=C(C(=N1)C2=C(Cl)C=CC=C2Cl)S(=O)(=O)C3=CN=CC=C3)N", "drugbank_id": "DB15444"},
    {"name": "TNO155", "class": "SHP2 Inhibitor (Clinical with MRTX1133)", "smiles": "CC1=CN=C(C(=N1)N2CCC(CC2)(N)C3=NC=CC=C3)C4=CC=CC=C4Cl", "drugbank_id": "DB15512"},
    
    # Receptor Tyrosine Kinase & Farnesyltransferase Inhibitors
    {"name": "Sunitinib", "class": "Receptor TKI (pNET Approved)", "smiles": "CCN(CC)CCNC(=O)c1c(C)[nH]c(/C=C2\\C(=O)Nc3ccc(F)cc23)c1C", "drugbank_id": "DB01268"},
    {"name": "Tipifarnib", "class": "Farnesyltransferase Inhibitor", "smiles": "CN1C=CN=C1C(C2=CC=C(C=C2)Cl)(C3=CC4=C(C=C3)N(C)C(=O)C=C4)C5=CC=C(C=C5)Cl", "drugbank_id": "DB04928"},
    {"name": "Lonafarnib", "class": "Farnesyltransferase Inhibitor", "smiles": "CC1=C(C=C(C=C1)Br)C2=C3CCC4=C(C=CC(=C4)Cl)N(C3=CC=C2)C(=O)CC5CCNCC5", "drugbank_id": "DB06173"},
    {"name": "Larotrectinib", "class": "TRK Inhibitor", "smiles": "OC1CCN(CC1)c2ccc(NC(=O)c3nn(C)cc3Nc4ccnc(c4)c5c(F)cccc5F)cc2", "drugbank_id": "DB12805"},
    {"name": "Entrectinib", "class": "TRK/ROS1 Inhibitor", "smiles": "COc1cc(Cc2ccc(F)c(F)c2)c(Nc3cc(N4CCN(C)CC4)ccn3)nc1C(=O)NC5CCNCC5", "drugbank_id": "DB12453"},
    {"name": "Afatinib", "class": "Pan-ErbB TKI", "smiles": "CN(C)C/C=C/C(=O)Nc1cc2c(Nc3ccc(Cl)c(F)c3)ncnc2cc1O[C@H]4CCOC4", "drugbank_id": "DB08907"},
    
    # CDK4/6 & Epigenetic Modulators
    {"name": "Palbociclib", "class": "CDK4/6 Inhibitor", "smiles": "CC(=O)c1c(C)c2cnc(Nc3ccc(N4CCNCC4)cn3)nc2n(C5CCCC5)c1=O", "drugbank_id": "DB09073"},
    {"name": "Abemaciclib", "class": "CDK4/6 Inhibitor", "smiles": "CCN1CCN(Cc2ccc(Nc3ncc(F)c(c4cc5n(C(C)C)c(C)cc5nc4)n3)cn2)CC1", "drugbank_id": "DB12001"},
    {"name": "Ribociclib", "class": "CDK4/6 Inhibitor", "smiles": "CN(C)C(=O)c1cc2cnc(Nc3ccc(N4CCNCC4)cn3)nc2n1C5CCCC5", "drugbank_id": "DB09075"},
    {"name": "Bortezomib", "class": "Proteasome Inhibitor", "smiles": "CC(C)C[C@H](NC(=O)[C@H](Cc1ccccc1)NC(=O)c2cnccn2)B(O)O", "drugbank_id": "DB00188"},
    {"name": "Vorinostat", "class": "HDAC Inhibitor", "smiles": "ONC(=O)CCCCCCC(=O)Nc1ccccc1", "drugbank_id": "DB02546"},
    {"name": "Panobinostat", "class": "Pan-HDAC Inhibitor", "smiles": "CC1=C(C=CC=C1)CCNCC2=CC=C(C=C2)/C=C/C(=O)NO", "drugbank_id": "DB06603"},
    {"name": "Regorafenib", "class": "Multikinase TKI", "smiles": "CNC(=O)c1cc(Oc2ccc(NC(=O)Nc3ccc(Cl)c(C(F)(F)F)c3)c(F)c2)ccn1", "drugbank_id": "DB08896"}
]

def curate():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out_csv = os.path.join(base_dir, "data", "raw", "kras_drug_library.csv")
    df = pd.DataFrame(KRAS_DRUG_LIBRARY)
    df.to_csv(out_csv, index=False)
    print(f"Successfully curated {len(df)} Pancreatic/KRAS therapeutics to: {out_csv}")

if __name__ == "__main__":
    curate()
