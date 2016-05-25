from django.db import models


class Thing(models.Model):
    pass


class SmallThing(models.Model):
    pass


class BigThing(models.Model):
    pass


class TagsTestsModel(models.Model):

    field1 = models.CharField(max_length=23)
    field2 = models.CharField('second field', max_length=42)

    def was_published_recently(self):
        return True
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    class Meta:
        verbose_name = "Tags Test Model"
        verbose_name_plural = "Tags Test Models"


class RendererTestModel(models.Model):
    decimal = models.DecimalField(decimal_places=5, max_digits=10)


class UtilsTestModel(models.Model):

    field1 = models.CharField(max_length=23)
    field2 = models.CharField('second field', max_length=42)

    def simple_method(self):
        return 42

    def was_published_recently(self):
        return True
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    class Meta:
        verbose_name = "Utils Test Model"
        verbose_name_plural = "Utils Test Models"
