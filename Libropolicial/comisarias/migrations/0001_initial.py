# Generated by Django 5.0.6 on 2025-01-13 10:08

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('compartido', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DependenciasMunicipales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DependenciasProvinciales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DependenciasSecundarias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dependencia', models.CharField(max_length=100)),
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
            name='InstitucionesHospitalarias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiciosEmergencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SolicitanteCodigo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=100)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ComisariaTercera',
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
                ('codigo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compartido.codigopolicialush')),
                ('codigos_secundarios', models.ManyToManyField(blank=True, to='compartido.codigossecundarios')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_records', to=settings.AUTH_USER_MODEL)),
                ('cuarto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='compartido.cuartoguardiaush')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated_records', to=settings.AUTH_USER_MODEL)),
                ('dependencias_municipales', models.ManyToManyField(blank=True, to='comisarias.dependenciasmunicipales')),
                ('dependencias_provinciales', models.ManyToManyField(blank=True, to='comisarias.dependenciasprovinciales')),
                ('dependendencias_secundarias', models.ManyToManyField(blank=True, to='comisarias.dependenciassecundarias')),
                ('instituciones_federales', models.ManyToManyField(blank=True, to='comisarias.institucionesfederales')),
                ('instituciones_hospitalarias', models.ManyToManyField(blank=True, to='comisarias.institucioneshospitalarias')),
                ('servicios_emergencia', models.ManyToManyField(blank=True, to='comisarias.serviciosemergencia')),
                ('solicitante_codigo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comisarias.solicitantecodigo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ComisariaSegunda',
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
                ('codigo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compartido.codigopolicialush')),
                ('codigos_secundarios', models.ManyToManyField(blank=True, to='compartido.codigossecundarios')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_records', to=settings.AUTH_USER_MODEL)),
                ('cuarto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='compartido.cuartoguardiaush')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated_records', to=settings.AUTH_USER_MODEL)),
                ('dependencias_municipales', models.ManyToManyField(blank=True, to='comisarias.dependenciasmunicipales')),
                ('dependencias_provinciales', models.ManyToManyField(blank=True, to='comisarias.dependenciasprovinciales')),
                ('dependendencias_secundarias', models.ManyToManyField(blank=True, to='comisarias.dependenciassecundarias')),
                ('instituciones_federales', models.ManyToManyField(blank=True, to='comisarias.institucionesfederales')),
                ('instituciones_hospitalarias', models.ManyToManyField(blank=True, to='comisarias.institucioneshospitalarias')),
                ('servicios_emergencia', models.ManyToManyField(blank=True, to='comisarias.serviciosemergencia')),
                ('solicitante_codigo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comisarias.solicitantecodigo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ComisariaQuinta',
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
                ('codigo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compartido.codigopolicialush')),
                ('codigos_secundarios', models.ManyToManyField(blank=True, to='compartido.codigossecundarios')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_records', to=settings.AUTH_USER_MODEL)),
                ('cuarto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='compartido.cuartoguardiaush')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated_records', to=settings.AUTH_USER_MODEL)),
                ('dependencias_municipales', models.ManyToManyField(blank=True, to='comisarias.dependenciasmunicipales')),
                ('dependencias_provinciales', models.ManyToManyField(blank=True, to='comisarias.dependenciasprovinciales')),
                ('dependendencias_secundarias', models.ManyToManyField(blank=True, to='comisarias.dependenciassecundarias')),
                ('instituciones_federales', models.ManyToManyField(blank=True, to='comisarias.institucionesfederales')),
                ('instituciones_hospitalarias', models.ManyToManyField(blank=True, to='comisarias.institucioneshospitalarias')),
                ('servicios_emergencia', models.ManyToManyField(blank=True, to='comisarias.serviciosemergencia')),
                ('solicitante_codigo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comisarias.solicitantecodigo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ComisariaPrimera',
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
                ('codigo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compartido.codigopolicialush')),
                ('codigos_secundarios', models.ManyToManyField(blank=True, to='compartido.codigossecundarios')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_records', to=settings.AUTH_USER_MODEL)),
                ('cuarto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='compartido.cuartoguardiaush')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated_records', to=settings.AUTH_USER_MODEL)),
                ('dependencias_municipales', models.ManyToManyField(blank=True, to='comisarias.dependenciasmunicipales')),
                ('dependencias_provinciales', models.ManyToManyField(blank=True, to='comisarias.dependenciasprovinciales')),
                ('dependendencias_secundarias', models.ManyToManyField(blank=True, to='comisarias.dependenciassecundarias')),
                ('instituciones_federales', models.ManyToManyField(blank=True, to='comisarias.institucionesfederales')),
                ('instituciones_hospitalarias', models.ManyToManyField(blank=True, to='comisarias.institucioneshospitalarias')),
                ('servicios_emergencia', models.ManyToManyField(blank=True, to='comisarias.serviciosemergencia')),
                ('solicitante_codigo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comisarias.solicitantecodigo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ComisariaCuarta',
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
                ('codigo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compartido.codigopolicialush')),
                ('codigos_secundarios', models.ManyToManyField(blank=True, to='compartido.codigossecundarios')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_records', to=settings.AUTH_USER_MODEL)),
                ('cuarto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='compartido.cuartoguardiaush')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated_records', to=settings.AUTH_USER_MODEL)),
                ('dependencias_municipales', models.ManyToManyField(blank=True, to='comisarias.dependenciasmunicipales')),
                ('dependencias_provinciales', models.ManyToManyField(blank=True, to='comisarias.dependenciasprovinciales')),
                ('dependendencias_secundarias', models.ManyToManyField(blank=True, to='comisarias.dependenciassecundarias')),
                ('instituciones_federales', models.ManyToManyField(blank=True, to='comisarias.institucionesfederales')),
                ('instituciones_hospitalarias', models.ManyToManyField(blank=True, to='comisarias.institucioneshospitalarias')),
                ('servicios_emergencia', models.ManyToManyField(blank=True, to='comisarias.serviciosemergencia')),
                ('solicitante_codigo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comisarias.solicitantecodigo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DetalleDependenciaMunicipal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_movil_municipal', models.CharField(blank=True, max_length=20, null=True)),
                ('nombre_a_cargo_municipal', models.CharField(blank=True, max_length=255, null=True)),
                ('comisaria_cuarta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_dependencia_municipal', to='comisarias.comisariacuarta')),
                ('comisaria_primera', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_dependencia_municipal', to='comisarias.comisariaprimera')),
                ('comisaria_quinta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_dependencia_municipal', to='comisarias.comisariaquinta')),
                ('comisaria_segunda', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_dependencia_municipal', to='comisarias.comisariasegunda')),
                ('comisaria_tercera', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_dependencia_municipal', to='comisarias.comisariatercera')),
                ('dependencia_municipal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comisarias.dependenciasmunicipales')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleDependenciaProvincial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_movil_provincial', models.CharField(blank=True, max_length=20, null=True)),
                ('nombre_a_cargo_provincial', models.CharField(blank=True, max_length=255, null=True)),
                ('comisaria_cuarta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_dependencia_provincial', to='comisarias.comisariacuarta')),
                ('comisaria_primera', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_dependencia_provincial', to='comisarias.comisariaprimera')),
                ('comisaria_quinta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_dependencia_provincial', to='comisarias.comisariaquinta')),
                ('comisaria_segunda', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_dependencia_provincial', to='comisarias.comisariasegunda')),
                ('comisaria_tercera', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_dependencia_provincial', to='comisarias.comisariatercera')),
                ('dependencia_provincial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comisarias.dependenciasprovinciales')),
            ],
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
        migrations.CreateModel(
            name='DetalleInstitucionFederal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_movil_federal', models.CharField(blank=True, max_length=20, null=True)),
                ('nombre_a_cargo_federal', models.CharField(blank=True, max_length=255, null=True)),
                ('comisaria_cuarta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_institucion_federal', to='comisarias.comisariacuarta')),
                ('comisaria_primera', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_institucion_federal', to='comisarias.comisariaprimera')),
                ('comisaria_quinta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_institucion_federal', to='comisarias.comisariaquinta')),
                ('comisaria_segunda', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_institucion_federal', to='comisarias.comisariasegunda')),
                ('comisaria_tercera', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_institucion_federal', to='comisarias.comisariatercera')),
                ('institucion_federal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comisarias.institucionesfederales')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleInstitucionHospitalaria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_movil_hospital', models.CharField(blank=True, max_length=20, null=True)),
                ('nombre_a_cargo_hospital', models.CharField(blank=True, max_length=255, null=True)),
                ('comisaria_cuarta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_institucion_hospitalaria', to='comisarias.comisariacuarta')),
                ('comisaria_primera', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_institucion_hospitalaria', to='comisarias.comisariaprimera')),
                ('comisaria_quinta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_institucion_hospitalaria', to='comisarias.comisariaquinta')),
                ('comisaria_segunda', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_institucion_hospitalaria', to='comisarias.comisariasegunda')),
                ('comisaria_tercera', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_institucion_hospitalaria', to='comisarias.comisariatercera')),
                ('institucion_hospitalaria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comisarias.institucioneshospitalarias')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleServicioEmergencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_movil_bomberos', models.CharField(blank=True, max_length=20, null=True)),
                ('nombre_a_cargo_bomberos', models.CharField(blank=True, max_length=255, null=True)),
                ('comisaria_cuarta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_servicio_emergencia', to='comisarias.comisariacuarta')),
                ('comisaria_primera', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_servicio_emergencia', to='comisarias.comisariaprimera')),
                ('comisaria_quinta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_servicio_emergencia', to='comisarias.comisariaquinta')),
                ('comisaria_segunda', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_servicio_emergencia', to='comisarias.comisariasegunda')),
                ('comisaria_tercera', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles_servicio_emergencia', to='comisarias.comisariatercera')),
                ('servicio_emergencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comisarias.serviciosemergencia')),
            ],
        ),
    ]
