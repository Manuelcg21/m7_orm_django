# Generated by Django 5.0.6 on 2024-07-26 01:10

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('cod', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('cod', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Inmueble',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField(max_length=1500)),
                ('m2_construidos', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('m2_totales', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('num_estacionamientos', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('num_habitaciones', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('num_baños', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('direccion', models.CharField(choices=[('casa', 'Casa'), ('departamento', 'Departamento'), ('bodega', 'Bodega')], max_length=155)),
                ('tipo_inmueble', models.CharField(choices=[('casa', 'Casa'), ('departamento', 'Departamento'), ('bodega', 'Bodega')], max_length=255)),
                ('precio', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1000)])),
                ('precio_ufs', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(1.0)])),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='inmuebles', to='main.comuna')),
                ('propietario', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='inmuebles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comuna',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='comunas', to='main.region'),
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('rechazada', 'Rechazada'), ('aprobada', 'Aprobada')], max_length=50)),
                ('arrendador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitudes', to=settings.AUTH_USER_MODEL)),
                ('inmueble', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitudes', to='main.inmueble')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
