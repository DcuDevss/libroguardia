# Generated by Django 5.0.6 on 2024-12-30 09:41

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('compartido', '0003_codigopolicialtol_codigossecundariostol_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DependenciasMunicipalesTOL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DependenciasProvincialesTOL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DependenciasSecundariasTOL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dependenciaTOL', models.CharField(max_length=100)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='InstitucionesFederales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='InstitucionesHospitalariasTOL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiciosEmergenciaTOL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SolicitanteCodigoTOL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigoTOL', models.CharField(max_length=100)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ComisariaTolhuin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField(default=django.utils.timezone.now)),
                ('movil_patrulla', models.CharField(blank=True, max_length=255, null=True)),
                ('a_cargo', models.CharField(blank=True, max_length=255, null=True)),
                ('secundante', models.CharField(blank=True, max_length=255, null=True)),
                ('lugar_codigo', models.CharField(blank=True, max_length=255, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('instituciones_intervinientes', models.TextField(blank=True, null=True)),
                ('tareas_judiciales', models.TextField(blank=True, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('firmas', models.TextField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('codigoTOL', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compartido.codigopolicialtol')),
                ('codigos_secundariosTOL', models.ManyToManyField(blank=True, to='compartido.codigossecundariostol')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_records', to=settings.AUTH_USER_MODEL)),
                ('cuartoTOL', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='compartido.cuartoguardiatol')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated_records', to=settings.AUTH_USER_MODEL)),
                ('dependencias_municipalesTOL', models.ManyToManyField(blank=True, to='comisariastolhuin.dependenciasmunicipalestol')),
                ('dependencias_provincialesTOL', models.ManyToManyField(blank=True, to='comisariastolhuin.dependenciasprovincialestol')),
                ('dependencias_secundariasTOL', models.ManyToManyField(blank=True, to='comisariastolhuin.dependenciassecundariastol')),
                ('instituciones_federales', models.ManyToManyField(blank=True, to='comisariastolhuin.institucionesfederales')),
                ('instituciones_hospitalariasTOL', models.ManyToManyField(blank=True, to='comisariastolhuin.institucioneshospitalariastol')),
                ('servicios_emergenciaTOL', models.ManyToManyField(blank=True, to='comisariastolhuin.serviciosemergenciatol')),
                ('solicitante_codigoTOL', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comisariastolhuin.solicitantecodigotol')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DetalleDependenciaMunicipalTOL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_movil_municipalTOL', models.CharField(blank=True, max_length=20, null=True)),
                ('nombre_a_cargo_municipalTOL', models.CharField(blank=True, max_length=255, null=True)),
                ('comisaria_tolhuin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_dependencia_municipalTOL', to='comisariastolhuin.comisariatolhuin')),
                ('dependencia_municipalTOL', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comisariastolhuin.dependenciasmunicipalestol')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleDependenciaProvincialTOL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_movil_provincialTOL', models.CharField(blank=True, max_length=20, null=True)),
                ('nombre_a_cargo_provincialTOL', models.CharField(blank=True, max_length=255, null=True)),
                ('comisaria_tolhuin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_dependencia_provincialTOL', to='comisariastolhuin.comisariatolhuin')),
                ('dependencia_provincialTOL', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comisariastolhuin.dependenciasprovincialestol')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleDependenciaSecundariaTOL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_movil_secundariaTOL', models.CharField(blank=True, max_length=20, null=True)),
                ('nombre_a_cargo_secundariaTOL', models.CharField(blank=True, max_length=255, null=True)),
                ('comisaria_tolhuin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_dependencia_secundariaTOL', to='comisariastolhuin.comisariatolhuin')),
                ('dependencia_secundariaTOL', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comisariastolhuin.dependenciassecundariastol')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleInstitucionFederal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_movil_federal', models.CharField(blank=True, max_length=20, null=True)),
                ('nombre_a_cargo_federal', models.CharField(blank=True, max_length=255, null=True)),
                ('comisaria_tolhuin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_institucion_federal', to='comisariastolhuin.comisariatolhuin')),
                ('institucion_federal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comisariastolhuin.institucionesfederales')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleInstitucionHospitalariaTOL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_movil_hospitalTOL', models.CharField(blank=True, max_length=20, null=True)),
                ('nombre_a_cargo_hospitalTOL', models.CharField(blank=True, max_length=255, null=True)),
                ('comisaria_tolhuin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_institucion_hospitalariaTOL', to='comisariastolhuin.comisariatolhuin')),
                ('institucion_hospitalariaTOL', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comisariastolhuin.institucioneshospitalariastol')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleServicioEmergenciaTOL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_movil_bomberosTOL', models.CharField(blank=True, max_length=20, null=True)),
                ('nombre_a_cargo_bomberosTOL', models.CharField(blank=True, max_length=255, null=True)),
                ('comisaria_tolhuin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_servicio_emergenciaTOL', to='comisariastolhuin.comisariatolhuin')),
                ('servicio_emergenciaTOL', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comisariastolhuin.serviciosemergenciatol')),
            ],
        ),
    ]
