
from django.db import models
from django.utils.translation import gettext as _

from wiki.logic.model_validators.geo_object_validators import \
    BaseComparisonValidator

__all__ = (
    "Continent",
    "Country",
    "City",
)


class BaseGeoObject(models.Model, BaseComparisonValidator):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    population = models.PositiveIntegerField(verbose_name=_("population"))
    area = models.FloatField(verbose_name=_("area (sq. meter)"))
    
    class Meta:
        abstract = True

    def full_clean(self, *args, **kwargs):
        super().full_clean(*args, **kwargs)
        self.clean_population()
        self.clean_area()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Continent(BaseGeoObject):

    class Meta:
        verbose_name = _('continent')
        verbose_name_plural = _('continents')

    def clean_population(self, *args, **kwargs):
        self.clean_underestimated_field('population', Country, 'continent')

    def clean_area(self, *args, **kwargs):
        self.clean_underestimated_field('area', Country, 'continent')


class Country(BaseGeoObject):
    continent = models.ForeignKey(Continent, verbose_name=_('continent'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')

    def clean_population(self, *args, **kwargs):
        self.clean_exceeded_field('population', 'continent')
        self.clean_underestimated_field('population', City, 'country')

    def clean_area(self, *args, **kwargs):
        self.clean_exceeded_field('area', 'continent')
        self.clean_underestimated_field('area', City, 'country')


class City(BaseGeoObject):
    country = models.ForeignKey(Country, verbose_name=_('country'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')

    def clean_population(self, *args, **kwargs):
        self.clean_exceeded_field('population', 'country')

    def clean_area(self, *args, **kwargs):
        self.clean_exceeded_field('area', 'country')
