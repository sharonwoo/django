from django.db import models


class MyModel(models.Model):
    objects = None


class MyOtherModel(models.Model):
    mymodel = models.ForeignKey(MyModel, on_delete=models.CASCADE)

class MyEmptyModel(models.Model):
    objects = None

class MyOtherEmptyModel(models.Model):
    myemptymodel = models.ForeignKey(MyEmptyModel, on_delete=models.CASCADE)
