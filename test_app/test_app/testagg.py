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

    from test_model_app.models import MyModel, MyOtherModel, MyEmptyModel, MyOtherEmptyModel

    from django.contrib.postgres.aggregates import ArrayAgg
    from django.db.models import Q, Value

    """
    create one-off my model and other model data fields per
    https://code.djangoproject.com/ticket/35235#comment:8

    if there is no data, get None back for result
    can look at setUpTestData in test_aggregates.py
    """

    if not MyModel.objects.exists():
        MyModel.objects.create()

    if not MyOtherModel.objects.exists():
        my_model_instance = MyModel.objects.first()
        MyOtherModel.objects.create(mymodel=my_model_instance)

    print("models without data always return None: ")
    print(MyEmptyModel.objects.annotate(
        annotated_ids=ArrayAgg(
            "myotheremptymodel__id",
            filter=Q(
                myotheremptymodel__id__in=[],
            ),
            default=Value([]),
        )
    ).first(), '[] Value([])')

    print("models with data: ")

    for filter_value in ([], [-1]):
        for test_default in ([], Value([])):
            result = MyModel.objects.annotate(
                annotated_ids=ArrayAgg(
                    "myothermodel__id",
                    filter=Q(
                        myothermodel__id__in=filter_value,
                    ),
                    default=test_default,
                )
            ).first().annotated_ids
            print(result, filter_value, test_default)

    """ prints:
        [] [] []
        {} [] Value([])
        [] [-1] []
        [] [-1] Value([])
    """


if __name__ == "__main__":
    main()
