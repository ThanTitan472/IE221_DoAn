# Generated by Django 5.1.3 on 2024-12-17 12:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0003_delete_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('medicine_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicines.medicine')),
                ('sale_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicines.sale')),
            ],
        ),
    ]