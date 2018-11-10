# Generated by Django 2.1.3 on 2018-11-09 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Выездная школа'), (2, 'Кружок'), (4, 'Единоразовое мероприятие'), (8, 'Другое'), (16, 'Онлайн-курсы')])),
                ('description', models.TextField()),
                ('start_datetime', models.DateTimeField(null=True)),
                ('finish_datetime', models.DateTimeField(null=True)),
                ('week_day', models.PositiveSmallIntegerField()),
                ('place_address', models.TextField()),
                ('place_location_latitude', models.FloatField(null=True)),
                ('place_location_longitude', models.FloatField(null=True)),
                ('repeatable', models.BooleanField()),
                ('contact_email', models.EmailField(max_length=254)),
                ('contact_data', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='EventCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Category')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Event')),
            ],
        ),
        migrations.CreateModel(
            name='EventSubcategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Event')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_person', models.BooleanField()),
                ('full_name', models.CharField(max_length=512)),
                ('contact_data', models.TextField()),
                ('contact_email', models.EmailField(max_length=254)),
                ('description', models.TextField()),
                ('is_verificated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Category')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('vk_id', models.BigIntegerField(db_index=True, primary_key=True, serialize=False)),
                ('banned', models.BooleanField(default=False)),
                ('spent_time', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='UserAchievement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Achievement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.User')),
            ],
        ),
        migrations.CreateModel(
            name='UserEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.User')),
            ],
        ),
        migrations.CreateModel(
            name='UserInterests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Category')),
                ('subcategory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Subcategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.User')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Organizer'),
        ),
        migrations.AddField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.User'),
        ),
    ]