# Generated by Django 5.0.6 on 2024-09-07 15:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comisarias', '0005_institucionesfederales_detalleinstitucionfederal_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comisariacuarta',
            old_name='dependencias_secundarias',
            new_name='dependendencias_secundarias',
        ),
        migrations.RenameField(
            model_name='comisariaprimera',
            old_name='dependencias_secundarias',
            new_name='dependendencias_secundarias',
        ),
        migrations.RenameField(
            model_name='comisariaquinta',
            old_name='dependencias_secundarias',
            new_name='dependendencias_secundarias',
        ),
        migrations.RenameField(
            model_name='comisariasegunda',
            old_name='dependencias_secundarias',
            new_name='dependendencias_secundarias',
        ),
        migrations.RenameField(
            model_name='comisariatercera',
            old_name='dependencias_secundarias',
            new_name='dependendencias_secundarias',
        ),
        migrations.CreateModel(
            name='DetalleDependenciaSecundaria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_movil_secundaria', models.CharField(blank=True, max_length=20, null=True)),
                ('nombre_a_cargo_secundaria', models.CharField(blank=True, max_length=255, null=True)),
                ('comisaria_cuarta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_dependencia_secundaria', to='comisarias.comisariacuarta')),
                ('comisaria_primera', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_dependencia_secundaria', to='comisarias.comisariaprimera')),
                ('comisaria_quinta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_dependencia_secundaria', to='comisarias.comisariaquinta')),
                ('comisaria_segunda', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_dependencia_secundaria', to='comisarias.comisariasegunda')),
                ('comisaria_tercera', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_dependencia_secundaria', to='comisarias.comisariatercera')),
                ('dependencia_secundaria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comisarias.dependenciassecundarias')),
            ],
        ),
    ]
