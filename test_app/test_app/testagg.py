# testagg.py
"""
python manage.py makemigrations
python manage.py migrate
"""

import os

import django


def main():
    # Set the environment variable to your Django settings module
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_app.settings")

    django.setup()

    from test_model_app.models import MyModel

    from django.contrib.postgres.aggregates import ArrayAgg
    from django.db.models import Q, Value

    for filter_value in ([], [-1]):
        for test_default in ([], Value([])):
            annotated_queryset = MyModel.objects.annotate(
                annotated_ids=ArrayAgg(
                    "myothermodel__id",
                    filter=Q(
                        myothermodel__id__in=filter_value,
                    ),
                    default=test_default,
                )
            )
            result = annotated_queryset.first()
            print(result, filter_value, test_default)


if __name__ == "__main__":
    main()
