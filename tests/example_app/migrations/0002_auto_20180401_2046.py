# Generated by Django 2.0.3 on 2018-04-01 18:46

from django.db import migrations, models
import django.db.models.deletion
import meta.models


class Migration(migrations.Migration):

    dependencies = [
        ('example_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=255, verbose_name='comment')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
            },
            bases=(meta.models.ModelMeta, models.Model),
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
            options={
                'verbose_name': 'publisher',
                'verbose_name_plural': 'publishers',
            },
            bases=(meta.models.ModelMeta, models.Model),
        ),
        migrations.AddField(
            model_name='post',
            name='related_posts',
            field=models.ManyToManyField(blank=True, to='example_app.Post', verbose_name='related posts'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='example_app.Post', verbose_name='post'),
        ),
        migrations.AddField(
            model_name='post',
            name='publisher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='example_app.Publisher', verbose_name='publisher'),
        ),
    ]
