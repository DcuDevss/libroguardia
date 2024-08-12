# Generated by Django 5.0.6 on 2024-08-11 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comisarias', '0009_detalledependenciamunicipal_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detalledependenciamunicipal',
            old_name='contacto',
            new_name='nombre_a_cargo',
        ),
        migrations.RenameField(
            model_name='detalledependenciamunicipal',
            old_name='telefono',
            new_name='numero_movil',
        ),
        migrations.RenameField(
            model_name='detalledependenciaprovincial',
            old_name='contacto',
            new_name='nombre_a_cargo',
        ),
        migrations.RenameField(
            model_name='detalledependenciaprovincial',
            old_name='telefono',
            new_name='numero_movil',
        ),
        migrations.RenameField(
            model_name='detalleinstitucionhospitalaria',
            old_name='contacto',
            new_name='nombre_a_cargo',
        ),
        migrations.RenameField(
            model_name='detalleinstitucionhospitalaria',
            old_name='telefono',
            new_name='numero_movil',
        ),
    ]
