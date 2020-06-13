# Generated by Django 3.0.4 on 2020-04-13 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
        ('cmdb', '0002_auto_20200413_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='project',
            field=models.ForeignKey(default=1, help_text='项目', on_delete=django.db.models.deletion.DO_NOTHING, related_name='server_project', to='project.Project'),
        ),
        migrations.AlterField(
            model_name='server',
            name='role',
            field=models.ForeignKey(default=1, help_text='角色', on_delete=django.db.models.deletion.DO_NOTHING, related_name='server_role', to='project.ProjectRole'),
        ),
    ]
