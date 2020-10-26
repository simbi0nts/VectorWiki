
from django.db import models
from django.utils.translation import gettext as _


__all__ = (
    "Continent",
    "Country",
    "City",
)


class BaseGeoObject(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    population = models.PositiveIntegerField(verbose_name=_("population"))
    area = models.FloatField(verbose_name=_("area (sq. meter)"))
    
    class Meta:
        abstract = True


class Continent(BaseGeoObject):

    class Meta:
        verbose_name = _('continent')
        verbose_name_plural = _('continents')


class Country(BaseGeoObject):
    continent = models.ForeignKey(Continent, verbose_name=_('continent'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('continent')
        verbose_name_plural = _('continents')


class City(BaseGeoObject):
    country = models.ForeignKey(Country, verbose_name=_('country'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')
