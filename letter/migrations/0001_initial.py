# Generated by Django 3.2.6 on 2021-08-27 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('letterId', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(db_column='content', max_length=10000)),
                ('sendDate', models.DateTimeField(auto_now_add=True, db_column='sendDate')),
                ('receiveDate', models.DateTimeField(db_column='receiveDate')),
                ('emotion', models.IntegerField(null=True)),
                ('senderId', models.ForeignKey(db_column='senderId', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'letter',
            },
        ),
        migrations.CreateModel(
            name='Sendletter',
            fields=[
                ('sendCol', models.AutoField(primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(db_column='is_deleted', default=False)),
                ('letterId', models.ForeignKey(db_column='letterId', null=True, on_delete=django.db.models.deletion.SET_NULL, to='letter.letter')),
                ('senderId', models.ForeignKey(db_column='senderId', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'sendletter',
            },
        ),
        migrations.CreateModel(
            name='Receiveletter',
            fields=[
                ('receiveCol', models.AutoField(primary_key=True, serialize=False)),
                ('readCheck', models.BooleanField(db_column='readCheck', default=False)),
                ('is_deleted', models.BooleanField(db_column='is_deleted', default=False)),
                ('letterId', models.ForeignKey(db_column='letterId', null=True, on_delete=django.db.models.deletion.SET_NULL, to='letter.letter')),
                ('receiverId', models.ForeignKey(db_column='receiverid', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'receiveletter',
            },
        ),
    ]
