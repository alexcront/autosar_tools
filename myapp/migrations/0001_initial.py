# Generated by Django 3.0.4 on 2021-02-22 10:55

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(max_length=1000)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('REQUESTED', 'Requested'), ('REJECTED', 'Rejected'), ('NEW', 'New'), ('IN_PROGRESS', 'In progress'), ('POSTPONED', 'Postponed'), ('DONE', 'Done'), ('POSTPONED', 'Graduate')], default='REQUESTED', max_length=11)),
                ('category', multiselectfield.db.fields.MultiSelectField(choices=[('HEX', 'hex'), ('ARXML', 'arxml'), ('DBC', 'dbc'), ('LOGS', 'logs'), ('EXCEL', 'excel')], max_length=24)),
                ('category_icon', multiselectfield.db.fields.MultiSelectField(choices=[('HEX', 'ni ni-archive-2'), ('ARXML', 'ni ni-collection'), ('DBC', 'ni ni-money-coins'), ('LOGS', 'ni ni-single-copy-04'), ('EXCEL', 'ni ni-books')], max_length=24)),
            ],
        ),
    ]
