# Generated by Django 5.0.6 on 2024-06-24 19:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comisarias', '0002_comisariacuarta_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodigoPolicial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='CuartoGuardia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuarto', models.CharField(max_length=1)),
            ],
        ),
        migrations.AlterField(
            model_name='comisariacuarta',
            name='codigo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='comisarias.codigopolicial'),
        ),
        migrations.AlterField(
            model_name='comisariaprimera',
            name='codigo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='comisarias.codigopolicial'),
        ),
        migrations.AlterField(
            model_name='comisariaquinta',
            name='codigo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='comisarias.codigopolicial'),
        ),
        migrations.AlterField(
            model_name='comisariasegunda',
            name='codigo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='comisarias.codigopolicial'),
        ),
        migrations.AlterField(
            model_name='comisariatercera',
            name='codigo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='comisarias.codigopolicial'),
        ),
        migrations.AddField(
            model_name='comisariacuarta',
            name='cuarto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='comisarias.cuartoguardia'),
        ),
        migrations.AddField(
            model_name='comisariaprimera',
            name='cuarto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='comisarias.cuartoguardia'),
        ),
        migrations.AddField(
            model_name='comisariaquinta',
            name='cuarto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='comisarias.cuartoguardia'),
        ),
        migrations.AddField(
            model_name='comisariasegunda',
            name='cuarto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='comisarias.cuartoguardia'),
        ),
        migrations.AddField(
            model_name='comisariatercera',
            name='cuarto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='comisarias.cuartoguardia'),
        ),
    ]
