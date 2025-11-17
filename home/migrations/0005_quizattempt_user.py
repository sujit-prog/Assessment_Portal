# Generated migration for adding user field to QuizAttempt
# Save this as: home/migrations/0005_quizattempt_user.py

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0004_alter_category_id_alter_question_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizattempt',
            name='user',
            field=models.ForeignKey(
                default=1,  # Temporary default - update existing records afterward
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL
            ),
            preserve_default=False,
        ),
    ]