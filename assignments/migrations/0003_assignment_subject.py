# Generated by Django 2.0.3 on 2018-04-06 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0002_auto_20180404_1240'),
        ('assignments', '0002_assignment_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='subject',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='subjects.Subject'),
            preserve_default=False,
        ),
    ]
