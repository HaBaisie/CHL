# Add Obstetric/Pelvic Ultrasound Scan as a lab test panel (Scan/Radiology group)

from django.db import migrations

PANEL_CODE = "OBSCAN"
PANEL_NAME = "Obstetric / Pelvic Ultrasound Scan"
PANEL_DESCRIPTION = "Obstetric and pelvic ultrasound scan report (Scan/Radiology)"

SUBTESTS = [
    ("Number of Fetuses", "", "", "Singleton"),
    ("Fetal Lie / Presentation", "Lie", "", "Cephalic"),
    ("Fetal Cardiac Activity", "FCA", "", "Present, regular"),
    ("Fetal Heart Rate", "FHR", "bpm", "110-160"),
    ("Placental Location", "", "", "Fundal / Anterior / Posterior"),
    ("Placental Grade", "", "", "Grade I-III (per gestation)"),
    ("Liquor Volume (Amniotic Fluid Index)", "AFI", "cm", "8-24"),
    ("Biparietal Diameter", "BPD", "mm", "As per gestational age chart"),
    ("Head Circumference", "HC", "mm", "As per gestational age chart"),
    ("Abdominal Circumference", "AC", "mm", "As per gestational age chart"),
    ("Femur Length", "FL", "mm", "As per gestational age chart"),
    ("Estimated Fetal Weight", "EFW", "g", "As per gestational age chart"),
    ("Fetal Anatomy Survey", "Anatomy", "", "Normal fetal anatomy, no gross abnormality seen"),
    ("Estimated Gestational Age", "Maturity", "weeks", "Corresponds with dates"),
    ("Expected Date of Delivery", "EDD", "", "Based on scan"),
    ("Cervical Length", "", "mm", ">= 25"),
    ("Uterus", "", "", "Normal size and contour"),
    ("Ovaries", "", "", "Normal bilaterally"),
    ("Impression / Comment", "", "", "-"),
]


def seed_obscan(apps, schema_editor):
    LabTestPanel = apps.get_model('hospital', 'LabTestPanel')
    LabSubTest = apps.get_model('hospital', 'LabSubTest')

    panel, _ = LabTestPanel.objects.update_or_create(
        code=PANEL_CODE,
        defaults={'name': PANEL_NAME, 'description': PANEL_DESCRIPTION, 'is_active': True},
    )
    for order, (sub_name, short_name, unit, ref_range) in enumerate(SUBTESTS):
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


def unseed_obscan(apps, schema_editor):
    LabTestPanel = apps.get_model('hospital', 'LabTestPanel')
    LabTestPanel.objects.filter(code=PANEL_CODE).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0044_add_ecg_panel'),
    ]

    operations = [
        migrations.RunPython(seed_obscan, unseed_obscan),
    ]
