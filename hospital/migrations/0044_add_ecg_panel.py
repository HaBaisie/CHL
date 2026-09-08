# Add Electrocardiogram (ECG) as a lab test panel

from django.db import migrations

PANEL_CODE = "ECG"
PANEL_NAME = "Electrocardiogram (ECG)"
PANEL_DESCRIPTION = "12-lead ECG recording and interpretation"

SUBTESTS = [
    ("Heart Rate", "HR", "bpm", "60-100"),
    ("Rhythm", "", "", "Sinus rhythm"),
    ("PR Interval", "PR", "ms", "120-200"),
    ("QRS Duration", "QRS", "ms", "80-120"),
    ("QT Interval", "QT", "ms", "350-440"),
    ("QTc Interval", "QTc", "ms", "< 440 (M); < 460 (F)"),
    ("Axis", "", "", "Normal (-30 to +90)"),
    ("ST Segment", "ST", "", "No ST elevation/depression"),
    ("T Wave", "", "", "Normal"),
    ("Interpretation / Impression", "", "", "Normal ECG"),
]


def seed_ecg(apps, schema_editor):
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


def unseed_ecg(apps, schema_editor):
    LabTestPanel = apps.get_model('hospital', 'LabTestPanel')
    LabTestPanel.objects.filter(code=PANEL_CODE).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0043_seed_lab_panels'),
    ]

    operations = [
        migrations.RunPython(seed_ecg, unseed_ecg),
    ]
