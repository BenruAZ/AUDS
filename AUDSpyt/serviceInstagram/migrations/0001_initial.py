# Generated by Django 2.1.2 on 2019-04-25 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userInfo', '0001_initial'),
        ('actividades', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='comentarios',
            fields=[
                ('instaId', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('instaUserAnonim', models.CharField(max_length=250)),
                ('likes', models.IntegerField()),
                ('texto', models.CharField(max_length=250)),
                ('fecha', models.DateTimeField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='instagramActivity',
            fields=[
                ('instaId', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('likes', models.IntegerField(default=-1)),
                ('uploaded', models.BooleanField(default=False)),
                ('url', models.CharField(default='anonimous', max_length=250)),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='actividades.Activity')),
            ],
        ),
        migrations.CreateModel(
            name='instagramDirect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instaId', models.CharField(max_length=250)),
                ('mensage', models.CharField(max_length=250)),
                ('reverse', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='instagramSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sesionjson', models.CharField(max_length=250)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='instagramUser',
            fields=[
                ('instaId', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('userInfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userInfo.UserInfo')),
            ],
        ),
        migrations.AddField(
            model_name='instagramdirect',
            name='instaUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviceInstagram.instagramUser'),
        ),
        migrations.AddField(
            model_name='comentarios',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviceInstagram.instagramActivity'),
        ),
        migrations.AddField(
            model_name='comentarios',
            name='instaUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviceInstagram.instagramUser'),
        ),
    ]
