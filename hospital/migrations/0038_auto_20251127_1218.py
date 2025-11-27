# hospital/migrations/0038_auto_20251127_1218.py
from django.db import migrations
from cloudinary.models import CloudinaryField

class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0037_alter_account_profile_pic_alter_doctor_profile_pic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_pic',
            field=CloudinaryField('profile_pic', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='profile_pic',
            field=CloudinaryField('profile_pic', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lab',
            name='profile_pic',
            field=CloudinaryField('profile_pic', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nurse',
            name='profile_pic',
            field=CloudinaryField('profile_pic', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='profile_pic',
            field=CloudinaryField('profile_pic', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pharmacy',
            name='profile_pic',
            field=CloudinaryField('profile_pic', blank=True, null=True),
        ),
    ]