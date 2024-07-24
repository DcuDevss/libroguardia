# Generated by Django 5.0.6 on 2024-07-14 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comisarias', '0004_rename_codigopolicial_codigopolicialush_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comisariacuarta',
            name='codigo',
        ),
        migrations.RemoveField(
            model_name='comisariaprimera',
            name='codigo',
        ),
        migrations.RemoveField(
            model_name='comisariaquinta',
            name='codigo',
        ),
        migrations.RemoveField(
            model_name='comisariasegunda',
            name='codigo',
        ),
        migrations.RemoveField(
            model_name='comisariatercera',
            name='codigo',
        ),
        migrations.AddField(
            model_name='comisariacuarta',
            name='codigo',
            field=models.ManyToManyField(to='comisarias.codigopolicialush'),
        ),
        migrations.AddField(
            model_name='comisariaprimera',
            name='codigo',
            field=models.ManyToManyField(to='comisarias.codigopolicialush'),
        ),
        migrations.AddField(
            model_name='comisariaquinta',
            name='codigo',
            field=models.ManyToManyField(to='comisarias.codigopolicialush'),
        ),
        migrations.AddField(
            model_name='comisariasegunda',
            name='codigo',
            field=models.ManyToManyField(to='comisarias.codigopolicialush'),
        ),
        migrations.AddField(
            model_name='comisariatercera',
            name='codigo',
            field=models.ManyToManyField(to='comisarias.codigopolicialush'),
        ),
    ]
