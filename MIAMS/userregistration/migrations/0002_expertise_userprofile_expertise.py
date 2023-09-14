# Generated by Django 4.2.4 on 2023-09-14 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userregistration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expertise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='expertise',
            field=models.ManyToManyField(blank=True, to='userregistration.expertise'),
        ),
    ]