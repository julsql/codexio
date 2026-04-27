from django.contrib.auth.hashers import make_password
from django.db import migrations, models


DEMO_USERNAME = 'temoin'
DEMO_EMAIL = 'temoin@codexio.local'
DEMO_COLLECTION_TITLE = 'Collection témoin'
DEMO_COLLECTION_TOKEN = 'TEMOIN-COLLECTION-TOKEN-NOT-FOR-API-USE-0000000000000000000000000'


def _resync_pk_sequence(schema_editor, table):
    """Réaligne la séquence d'auto-id sur MAX(id) — protège contre les bases
    où des lignes ont été insérées avec id explicite sans bumper la séquence."""
    if schema_editor.connection.vendor != 'postgresql':
        return
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            "SELECT setval(pg_get_serial_sequence(%s, 'id'), "
            "COALESCE((SELECT MAX(id) FROM " + table + "), 1), true);",
            [table],
        )


def create_demo_user_and_collection(apps, schema_editor):
    AppUser = apps.get_model('main', 'AppUser')
    Collection = apps.get_model('main', 'Collection')
    Profile = apps.get_model('main', 'Profile')

    for table in ('main_profile', 'main_collection', 'main_appuser'):
        _resync_pk_sequence(schema_editor, table)

    profile_bd, _ = Profile.objects.get_or_create(name='BD')

    collection, _ = Collection.objects.get_or_create(
        title=DEMO_COLLECTION_TITLE,
        defaults={
            'token': DEMO_COLLECTION_TOKEN,
            'doc_id': '',
            'sheet_name': '',
            'profile': profile_bd,
        },
    )

    demo_user, _ = AppUser.objects.update_or_create(
        username=DEMO_USERNAME,
        defaults={
            'email': DEMO_EMAIL,
            'password': make_password(None),
            'is_demo': True,
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'current_collection': collection,
        },
    )

    collection.accounts.add(demo_user)


def delete_demo_user_and_collection(apps, schema_editor):
    AppUser = apps.get_model('main', 'AppUser')
    Collection = apps.get_model('main', 'Collection')

    AppUser.objects.filter(username=DEMO_USERNAME).delete()
    Collection.objects.filter(title=DEMO_COLLECTION_TITLE).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_create_users_and_profile_and_collection'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='is_demo',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(
            create_demo_user_and_collection,
            delete_demo_user_and_collection,
        ),
    ]
