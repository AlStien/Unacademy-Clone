from django.db import migrations, models
import django.db.models.deletion
from django.contrib.postgres.operations import TrigramExtension


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        TrigramExtension(),
    ]