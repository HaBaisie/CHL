# Seed comprehensive lab panels & sub-tests commonly requested in Nigerian hospitals/labs

from django.db import migrations

# Each panel: code, name, description, [(name, short_name, unit, reference_range), ...]
PANELS = [
    ("FBC", "Full Blood Count (FBC)", "Complete blood count with differential", [
        ("Haemoglobin", "Hb", "g/dL", "13.0-17.0 (M); 12.0-15.5 (F)"),
        ("Packed Cell Volume", "PCV", "%", "40-52 (M); 36-46 (F)"),
        ("Red Blood Cell Count", "RBC", "x10^12/L", "4.5-5.9 (M); 4.0-5.2 (F)"),
        ("White Blood Cell Count", "WBC", "x10^9/L", "4.0-11.0"),
        ("Platelet Count", "PLT", "x10^9/L", "150-450"),
        ("Mean Corpuscular Volume", "MCV", "fL", "80-100"),
        ("Mean Corpuscular Haemoglobin", "MCH", "pg", "27-33"),
        ("Mean Corpuscular Hb Concentration", "MCHC", "g/dL", "32-36"),
        ("Neutrophils", "Neut", "%", "40-75"),
        ("Lymphocytes", "Lymph", "%", "20-45"),
        ("Monocytes", "Mono", "%", "2-10"),
        ("Eosinophils", "Eos", "%", "1-6"),
        ("Basophils", "Baso", "%", "0-1"),
        ("Erythrocyte Sedimentation Rate", "ESR", "mm/hr", "0-15 (M); 0-20 (F)"),
    ]),
    ("GENO", "Haemoglobin Genotype", "Haemoglobin electrophoresis", [
        ("Haemoglobin Genotype", "Genotype", "", "AA / AS / SS / AC / SC / CC"),
    ]),
    ("BGRH", "Blood Group & Rhesus Factor", "ABO and Rhesus typing", [
        ("ABO Blood Group", "Group", "", "A / B / AB / O"),
        ("Rhesus Factor", "Rh", "", "Positive / Negative"),
    ]),
    ("MP", "Malaria Parasite (MP)", "Thick/thin film for malaria parasites", [
        ("Malaria Parasite (Thick/Thin Film)", "MP", "", "Negative"),
        ("Parasite Density", "Density", "parasites/µL", "Negative"),
    ]),
    ("WIDAL", "Widal Test", "Typhoid serology", [
        ("Salmonella typhi O (TO)", "TO", "titre", "< 1:80"),
        ("Salmonella typhi H (TH)", "TH", "titre", "< 1:160"),
        ("Salmonella paratyphi AH", "AH", "titre", "< 1:80"),
        ("Salmonella paratyphi BH", "BH", "titre", "< 1:80"),
    ]),
    ("HIV", "Retroviral Screening (HIV 1&2)", "HIV antibody screening", [
        ("HIV 1 & 2 Antibody", "HIV Ab", "", "Non-reactive"),
    ]),
    ("HBSAG", "Hepatitis B Surface Antigen (HBsAg)", "Hepatitis B screening", [
        ("HBsAg", "HBsAg", "", "Negative"),
    ]),
    ("HCV", "Hepatitis C Virus Antibody", "Hepatitis C screening", [
        ("Anti-HCV Antibody", "Anti-HCV", "", "Negative"),
    ]),
    ("VDRL", "VDRL / RPR (Syphilis Screening)", "Syphilis serology", [
        ("VDRL/RPR", "VDRL", "", "Non-reactive"),
    ]),
    ("UPT", "Pregnancy Test (Urine HCG)", "Qualitative urine hCG", [
        ("Beta-hCG (Urine)", "hCG", "", "Negative"),
    ]),
    ("SHCG", "Beta-hCG (Serum, Quantitative)", "Quantitative serum hCG", [
        ("Beta-hCG (Serum)", "hCG", "mIU/mL", "< 5 (non-pregnant)"),
    ]),
    ("URIN", "Urinalysis (Complete)", "Full urinalysis with microscopy", [
        ("Colour", "", "", "Pale yellow"),
        ("Appearance", "", "", "Clear"),
        ("pH", "", "", "4.5-8.0"),
        ("Specific Gravity", "SG", "", "1.005-1.030"),
        ("Protein", "", "", "Negative"),
        ("Glucose", "", "", "Negative"),
        ("Ketones", "", "", "Negative"),
        ("Blood", "", "", "Negative"),
        ("Bilirubin", "", "", "Negative"),
        ("Urobilinogen", "", "", "Normal"),
        ("Nitrite", "", "", "Negative"),
        ("Leukocyte Esterase", "", "", "Negative"),
        ("Pus Cells (Microscopy)", "", "/hpf", "0-5"),
        ("Red Blood Cells (Microscopy)", "", "/hpf", "0-2"),
        ("Epithelial Cells", "", "/hpf", "Few"),
        ("Casts", "", "", "None seen"),
        ("Crystals", "", "", "None seen"),
    ]),
    ("STOOL", "Stool Microscopy", "Stool microscopy, ova/cysts", [
        ("Colour", "", "", "Brown"),
        ("Consistency", "", "", "Formed"),
        ("Ova/Cysts", "", "", "Not seen"),
        ("Occult Blood", "", "", "Negative"),
        ("Reducing Substance", "", "", "Negative"),
        ("Pus Cells", "", "/hpf", "0-2"),
    ]),
    ("LFT", "Liver Function Test (LFT)", "Hepatic panel", [
        ("Total Bilirubin", "TB", "µmol/L", "3-17"),
        ("Direct (Conjugated) Bilirubin", "DB", "µmol/L", "0-5"),
        ("ALT (SGPT)", "ALT", "U/L", "5-40"),
        ("AST (SGOT)", "AST", "U/L", "5-40"),
        ("Alkaline Phosphatase", "ALP", "U/L", "40-129"),
        ("Gamma-GT", "GGT", "U/L", "8-61"),
        ("Total Protein", "TP", "g/L", "60-80"),
        ("Albumin", "Alb", "g/L", "35-50"),
        ("Globulin", "Glob", "g/L", "20-35"),
    ]),
    ("RFT", "Renal Function Test (E/U/Cr)", "Electrolytes, urea and creatinine", [
        ("Sodium", "Na+", "mmol/L", "135-145"),
        ("Potassium", "K+", "mmol/L", "3.5-5.1"),
        ("Chloride", "Cl-", "mmol/L", "98-107"),
        ("Bicarbonate", "HCO3-", "mmol/L", "22-29"),
        ("Urea", "", "mmol/L", "2.5-7.1"),
        ("Creatinine", "", "µmol/L", "62-115 (M); 53-97 (F)"),
    ]),
    ("FBS", "Fasting Blood Sugar (FBS)", "Fasting plasma glucose", [
        ("Fasting Blood Glucose", "FBG", "mg/dL", "70-100"),
    ]),
    ("RBS", "Random Blood Sugar (RBS)", "Random plasma glucose", [
        ("Random Blood Glucose", "RBG", "mg/dL", "< 200"),
    ]),
    ("OGTT", "Oral Glucose Tolerance Test (OGTT)", "75g glucose tolerance test", [
        ("Fasting Glucose", "", "mg/dL", "70-100"),
        ("2-Hour Post Glucose Load", "2hr", "mg/dL", "< 140"),
    ]),
    ("HBA1C", "Glycated Haemoglobin (HbA1c)", "Average glucose control (3 months)", [
        ("HbA1c", "", "%", "4.0-5.6"),
    ]),
    ("LIPID", "Lipid Profile", "Cholesterol and triglycerides", [
        ("Total Cholesterol", "TC", "mg/dL", "< 200"),
        ("Triglycerides", "TG", "mg/dL", "< 150"),
        ("HDL Cholesterol", "HDL", "mg/dL", "> 40 (M); > 50 (F)"),
        ("LDL Cholesterol", "LDL", "mg/dL", "< 100"),
        ("VLDL Cholesterol", "VLDL", "mg/dL", "5-40"),
    ]),
    ("TFT", "Thyroid Function Test (TFT)", "Thyroid hormone panel", [
        ("TSH", "", "µIU/mL", "0.4-4.0"),
        ("Total T3", "T3", "ng/mL", "0.8-2.0"),
        ("Total T4", "T4", "µg/dL", "5.0-12.0"),
        ("Free T4", "FT4", "ng/dL", "0.8-1.8"),
    ]),
    ("COAG", "Coagulation Profile", "Clotting studies", [
        ("Prothrombin Time", "PT", "seconds", "11-15"),
        ("International Normalised Ratio", "INR", "ratio", "0.8-1.2"),
        ("Activated Partial Thromboplastin Time", "APTT", "seconds", "25-35"),
        ("Bleeding Time", "BT", "minutes", "2-7"),
        ("Clotting Time", "CT", "minutes", "4-10"),
    ]),
    ("CARDIAC", "Cardiac Markers", "Troponin and CK-MB", [
        ("Troponin I", "TnI", "ng/mL", "< 0.04"),
        ("CK-MB", "", "U/L", "0-25"),
    ]),
    ("PSA", "Prostate Specific Antigen (PSA)", "Prostate screening", [
        ("Total PSA", "PSA", "ng/mL", "< 4.0"),
    ]),
    ("SFA", "Semen Analysis (SFA)", "Seminal fluid analysis", [
        ("Volume", "", "mL", "1.5-5.0"),
        ("Liquefaction Time", "", "minutes", "20-30"),
        ("pH", "", "", "7.2-8.0"),
        ("Sperm Count", "", "million/mL", ">= 15"),
        ("Sperm Motility (Progressive)", "", "%", ">= 32"),
        ("Sperm Morphology (Normal Forms)", "", "%", ">= 4"),
        ("Pus Cells", "", "/hpf", "0-2"),
    ]),
    ("AFB", "Sputum for AFB", "Acid-fast bacilli smear (TB screening)", [
        ("AFB Smear (Ziehl-Neelsen)", "AFB", "", "Not seen"),
    ]),
    ("G6PD", "G6PD Screening", "Glucose-6-phosphate dehydrogenase screening", [
        ("G6PD Screening", "G6PD", "", "Normal (not deficient)"),
    ]),
    ("SICKLE", "Sickling Test", "Sickle cell screening", [
        ("Sickling Test", "", "", "Negative"),
    ]),
    ("PBF", "Peripheral Blood Film (PBF)", "Blood film morphology", [
        ("Red Cell Morphology", "", "", "Normocytic normochromic"),
        ("White Cell Morphology", "", "", "Normal"),
        ("Platelet Morphology/Estimate", "", "", "Adequate"),
        ("Comment / Parasites Seen", "", "", "None seen"),
    ]),
    ("CRP", "C-Reactive Protein (CRP)", "Acute phase inflammatory marker", [
        ("CRP", "", "mg/L", "< 6"),
    ]),
    ("RA", "Rheumatoid Factor / ASO Titre", "Autoimmune/rheumatic screening", [
        ("Rheumatoid Factor", "RF", "IU/mL", "< 14"),
        ("ASO Titre", "ASO", "IU/mL", "< 200"),
    ]),
    ("URICA", "Serum Uric Acid", "Uric acid level", [
        ("Serum Uric Acid", "", "µmol/L", "202-416 (M); 143-339 (F)"),
    ]),
    ("IRON", "Iron Studies", "Iron, TIBC and ferritin", [
        ("Serum Iron", "", "µmol/L", "10-30"),
        ("Total Iron Binding Capacity", "TIBC", "µmol/L", "45-70"),
        ("Ferritin", "", "ng/mL", "20-250 (M); 10-120 (F)"),
    ]),
    ("BONE", "Bone Profile (Ca/PO4/Mg)", "Calcium, phosphate, magnesium", [
        ("Calcium (Total)", "Ca", "mmol/L", "2.1-2.6"),
        ("Phosphate", "PO4", "mmol/L", "0.8-1.5"),
        ("Magnesium", "Mg", "mmol/L", "0.66-1.07"),
    ]),
    ("PANC", "Pancreatic Enzymes", "Amylase and lipase", [
        ("Serum Amylase", "", "U/L", "30-110"),
        ("Serum Lipase", "", "U/L", "0-160"),
    ]),
    ("HVS", "High Vaginal Swab (HVS) M/C/S", "Microscopy, culture and sensitivity", [
        ("Appearance", "", "", "-"),
        ("Microscopy (Pus/Epithelial Cells)", "", "", "-"),
        ("Culture", "", "", "No growth"),
        ("Organism Isolated", "", "", "-"),
        ("Antibiotic Sensitivity", "", "", "-"),
    ]),
    ("UMCS", "Urine Culture & Sensitivity (M/C/S)", "Urine microbiology", [
        ("Colony Count", "", "CFU/mL", "< 10,000"),
        ("Organism Isolated", "", "", "No growth"),
        ("Antibiotic Sensitivity", "", "", "-"),
    ]),
    ("WOUND", "Wound Swab M/C/S", "Wound microbiology", [
        ("Gram Stain", "", "", "-"),
        ("Culture", "", "", "No growth"),
        ("Organism Isolated", "", "", "-"),
        ("Antibiotic Sensitivity", "", "", "-"),
    ]),
    ("BCS", "Blood Culture & Sensitivity", "Blood microbiology", [
        ("Culture (5-7 days incubation)", "", "", "No growth"),
        ("Organism Isolated", "", "", "-"),
        ("Antibiotic Sensitivity", "", "", "-"),
    ]),
    ("CSF", "CSF Analysis", "Cerebrospinal fluid analysis", [
        ("Appearance", "", "", "Clear, colourless"),
        ("Cell Count (WBC)", "", "cells/µL", "0-5"),
        ("Protein", "", "g/L", "0.15-0.45"),
        ("Glucose", "", "mmol/L", "2.5-4.4"),
        ("Gram Stain/Culture", "", "", "No organism seen"),
    ]),
    ("VITAMIN", "Vitamin & Micronutrient Panel", "Vitamin D, B12, folate", [
        ("Vitamin D (25-OH)", "VitD", "ng/mL", "30-100"),
        ("Vitamin B12", "B12", "pg/mL", "200-900"),
        ("Folate", "", "ng/mL", "2.7-17.0"),
    ]),
    ("HPYLORI", "H. Pylori Test", "Helicobacter pylori antigen/antibody", [
        ("H. Pylori Antigen/Antibody", "", "", "Negative"),
    ]),
    ("TORCH", "TORCH Screen", "Toxoplasma, Rubella, CMV, Herpes screening", [
        ("Toxoplasma IgG/IgM", "", "", "Negative"),
        ("Rubella IgG/IgM", "", "", "Negative"),
        ("CMV IgG/IgM", "", "", "Negative"),
        ("HSV IgG/IgM", "", "", "Negative"),
    ]),
]


def seed_panels(apps, schema_editor):
    LabTestPanel = apps.get_model('hospital', 'LabTestPanel')
    LabSubTest = apps.get_model('hospital', 'LabSubTest')

    for code, name, description, subtests in PANELS:
        panel, _ = LabTestPanel.objects.update_or_create(
            code=code,
            defaults={'name': name, 'description': description, 'is_active': True},
        )
        for order, (sub_name, short_name, unit, ref_range) in enumerate(subtests):
            LabSubTest.objects.update_or_create(
                panel=panel,
                name=sub_name,
                defaults={
                    'short_name': short_name,
                    'unit': unit,
                    'reference_range': ref_range,
                    'sort_order': order,
                },
            )


def unseed_panels(apps, schema_editor):
    LabTestPanel = apps.get_model('hospital', 'LabTestPanel')
    codes = [code for code, *_ in PANELS]
    LabTestPanel.objects.filter(code__in=codes).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0042_alter_bill_final_amount_alter_bill_total_amount'),
    ]

    operations = [
        migrations.RunPython(seed_panels, unseed_panels),
    ]
