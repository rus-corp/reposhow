from django.db import models
from django.utils.text import slugify

from transliterate import translit



class Activity(models.Model):
    # Сферы деятельности
    name = models.CharField(max_length=150, )
    slug = models.SlugField(max_length=55, unique=True)

    class Meta:
        verbose_name = 'Сфера деятельности'
        verbose_name_plural = 'Сферы деятельности'

    def __str__(self) -> str:
        return self.name


    def save(self, *args, **kwargs):
        try:
            name = translit(self.name, reversed=True)
            self.slug = slugify(name)
        except:
            self.slug = slugify(self.name)
        super(Activity, self).save(*args, **kwargs)


class Category(models.Model):
    # Категории
    name = models.CharField(max_length=200)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='categoryes')
    slug = models.SlugField(max_length=55, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


    def save(self, *args, **kwargs):
        try:
            name = translit(self.name, reversed=True)
            self.slug = slugify(name)
        except:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Specialization(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='specializations')
    slug = models.SlugField(max_length=155, unique=True)

    class Meta:
        verbose_name = 'Специализации'
        verbose_name_plural = 'Специализации'

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        try:
            name = translit(self.name, reversed=True)
            self.slug = slugify(name)
        except:
            self.slug = slugify(self.name)
        super(Specialization, self).save(*args, **kwargs)
