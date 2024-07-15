# Generated by Django 4.2.14 on 2024-07-12 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('divas', '0002_community_forum_alter_submission_design_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('followers', models.IntegerField()),
                ('ranking', models.IntegerField()),
                ('about', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='community_forum',
            name='commented_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='divas.users'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='divas.users'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='divas.users'),
        ),
        migrations.AlterField(
            model_name='wishlistpost',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='divas.users'),
        ),
    ]
