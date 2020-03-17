# Generated by Django 3.0.3 on 2020-03-12 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    state_operations = [
        migrations.AlterField(
            model_name='enumerator',
            name='enumeratorID',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True, verbose_name='enumeratorID'),
        ),
        migrations.RemoveField(
            model_name='enumerator',
            name='qualifications',
        ),
    ]
    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]