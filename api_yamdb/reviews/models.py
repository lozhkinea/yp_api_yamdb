from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(null=True)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL, related_name="titles"
    )

    def __str__(self):
        return (f"name={self.name[:15]}, "
               f"year={self.year}")
