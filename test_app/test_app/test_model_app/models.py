from django.db import models


class MyModel(models.Model):
    objects = None


class MyOtherModel(models.Model):
    mymodel = models.ForeignKey(MyModel, on_delete=models.CASCADE)
