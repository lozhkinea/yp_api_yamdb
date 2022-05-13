from django.db import models


# id,name,slug
class Category(models.Model):
    # Поля базы данных
    # CharField - строка с ограничением длины
    name = models.CharField(max_length=256)
    # SlugField - помогает создавать дружелюбные URL-адреса
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# id,name,slug
class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# id,name,year,category
class Title(models.Model):
    name = models.CharField(max_length=256)
    # IntegerField - для хранения целых чисел
    # установит значение поля в NULL, т.е. нет данных
    year = models.IntegerField()
    # ??? непонятно
    # rating = models.ManyToManyField(Review)
    # TextField - для больших текстовых блоков
    description = models.TextField(blank=True, null=True)
    # ForeignKey, ссылка на модель Categories
    # в колонке category будут указаны pk записей из таблицы Categories
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
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
