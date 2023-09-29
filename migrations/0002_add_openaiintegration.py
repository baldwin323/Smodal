from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Smodal", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="OpenAIIntegration",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("api_key", models.CharField(max_length=255)),
                ("ui_state", models.BooleanField(default=False)),
            ],
        ),
    ]
