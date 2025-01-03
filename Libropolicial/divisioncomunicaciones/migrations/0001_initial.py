# Generated by Django 5.0.6 on 2024-10-28 11:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('compartido', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EncargadoGuardia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_apellido', models.CharField(blank=True, max_length=255, null=True)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalGuardia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_apellido', models.CharField(blank=True, max_length=255, null=True)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DivisionComunicaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio_guardia', models.DateTimeField(blank=True, null=True)),
                ('finalizacion_guardia', models.DateTimeField(blank=True, null=True)),
                ('oficial_servicio', models.CharField(blank=True, max_length=100, null=True)),
                ('distribucion_personal_moviles', models.TextField(blank=True, null=True)),
                ('novedades', models.TextField(blank=True, null=True)),
                ('codigo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compartido.codigopolicialush')),
                ('codigos_secundarios', models.ManyToManyField(blank=True, to='compartido.codigossecundarios')),
                ('cuarto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compartido.cuartoguardiaush')),
                ('encargado_guardia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='divisioncomunicaciones.encargadoguardia')),
                ('personal_guardia', models.ManyToManyField(blank=True, related_name='comunicaciones_guardia', to='divisioncomunicaciones.personalguardia')),
            ],
        ),
        migrations.CreateModel(
            name='EventoGuardia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_evento', models.CharField(blank=True, choices=[('PRESENTE', 'Presente'), ('INICIA', 'Inicia'), ('FINALIZA', 'Finaliza'), ('SE_RETIRA', 'Se Retira'), ('CONSTANCIA', 'Constancia')], max_length=20, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('hora_evento', models.DateTimeField(blank=True, null=True)),
                ('guardia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventos', to='divisioncomunicaciones.divisioncomunicaciones')),
            ],
        ),
        migrations.CreateModel(
            name='EventoGuardiaBis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_eventobis', models.CharField(blank=True, choices=[('ENCARGADO DE GUARDIA', 'Encargado de Guardia'), ('OPERADOR Y LIBRO DE GUARDIA', 'Operador y Librero'), ('CONSIGNA', 'Consigna'), ('PUESTO LLAVERO', 'Puesto llavero')], max_length=50, null=True)),
                ('nombre_jerarquia', models.CharField(blank=True, max_length=255, null=True)),
                ('guardia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventosbis', to='divisioncomunicaciones.divisioncomunicaciones')),
            ],
        ),
        migrations.CreateModel(
            name='EventoGuardiaBisUno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_eventobisuno', models.CharField(blank=True, choices=[('MOVIL', 'Movil'), ('PATRULLA', 'Patrulla')], max_length=50, null=True)),
                ('movil_patrulla', models.CharField(blank=True, max_length=100, null=True)),
                ('nombre_jerarquia_movil_patrulla', models.TextField(blank=True, null=True)),
                ('guardia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventosbisuno', to='divisioncomunicaciones.divisioncomunicaciones')),
            ],
        ),
    ]
