from django.db import migrations, models


class Migration(migrations.Migration):
    """Ajoute uniquement la table de cache des notices des sources externes.

    Écrite à la main : makemigrations voulait aussi altérer
    appuser.current_collection, une divergence sans rapport avec ce cache.
    """

    dependencies = [
        ('main', '0003_appuser_is_demo_and_create_temoin'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlbumInfosCache',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False,
                                           verbose_name='ID')),
                ('source', models.CharField(max_length=100)),
                ('isbn', models.BigIntegerField()),
                ('payload', models.JSONField()),
                ('fetched_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name='albuminfoscache',
            constraint=models.UniqueConstraint(fields=('source', 'isbn'),
                                               name='unique_album_cache_source_isbn'),
        ),
    ]
