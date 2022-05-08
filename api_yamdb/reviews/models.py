from django.db import models


# id,name,slug
class Categories(models.Model):
    # Поля базы данных
    # CharField - строка с ограничением длины
    name = models.CharField(max_length=200)
    # SlugField - помогает создавать дружелюбные URL-адреса
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


# id,name,slug
class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


# id,name,year,category
class Titles(models.Model):
    name = models.CharField(max_length=200)
    # IntegerField - для хранения целых чисел
    # установит значение поля в NULL, т.е. нет данных
    year = models.IntegerField(null=True)
    # ??? непонятно
    # rating = models.ManyToManyField(Review)
    # TextField - для больших текстовых блоков
    description = models.TextField(blank=True)
    # ForeignKey, ссылка на модель Categories
    # в колонке category будут указаны pk записей из таблицы Categories
    genre = models.ForeignKey(
        Genres,
        blank=True,
        null=True,
        # если удаляется жанр, произведения остаются
        on_delete=models.SET_NULL,
        # связь между моделями
        related_name='titles'
    )
    category = models.ForeignKey(
        Categories,
        blank=True,
        null=True,
        # если удаляется категория, произведения остаются
        on_delete=models.SET_NULL,
        # связь между моделями
        related_name='titles'
    )

    def __str__(self):
        return (f'name={self.name[:15]}, '
                f'year={self.year}')
