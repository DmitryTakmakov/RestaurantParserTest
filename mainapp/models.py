from django.db import models


class Restaurant(models.Model):
    restaurant_chain = models.CharField(max_length=64, verbose_name='Название сети')
    restaurant_id = models.CharField(max_length=128, verbose_name='Название ресторана')
    restaurant_location_longitude = models.DecimalField(max_digits=17, decimal_places=14,
                                                        verbose_name='Координаты ресторана, долгота')
    restaurant_location_latitude = models.DecimalField(max_digits=17, decimal_places=14,
                                                       verbose_name='Координаты ресторана, широта')

    class Meta:
        verbose_name = 'Ресторан'
        verbose_name_plural = 'Рестораны'

    def __str__(self):
        return f'{self.restaurant_chain} / {self.restaurant_id}'
