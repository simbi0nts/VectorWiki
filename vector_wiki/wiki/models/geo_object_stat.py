
from django.db import models
from django.utils.translation import gettext as _
from wiki.models import Country, City


__all__ = (
    "CountryStat",
    "CityStat",
)


class CountryStat(models.Model):
    country = models.ForeignKey(Country, verbose_name=_('country'), on_delete=models.CASCADE)

    number_of_hospitals = models.PositiveIntegerField(
        verbose_name=_("number of hospitals"),
        blank=True, null=True
    )
    number_of_national_parks = models.PositiveIntegerField(
        verbose_name=_("number of national parks"),
        blank=True, null=True
    )
    number_of_rivers = models.PositiveIntegerField(
        verbose_name=_("number of rivers"),
        blank=True, null=True
    )
    number_of_schools = models.PositiveIntegerField(
        verbose_name=_("number of schools"),
        blank=True, null=True
    )

    class Meta:
        verbose_name = _('country stats')
        verbose_name_plural = _('countries stats')


class CityStat(models.Model):
    city = models.ForeignKey(City, verbose_name=_('city'), on_delete=models.CASCADE)

    number_of_roads = models.PositiveIntegerField(
        verbose_name=_("number of roads"),
        blank=True, null=True
    )
    number_of_trees = models.PositiveIntegerField(
        verbose_name=_("number of trees"),
        blank=True, null=True
    )
    number_of_shops = models.PositiveIntegerField(
        verbose_name=_("number of shops"),
        blank=True, null=True
    )
    number_of_schools = models.PositiveIntegerField(
        verbose_name=_("number of schools"),
        blank=True, null=True
    )

    class Meta:
        verbose_name = _('city stats')
        verbose_name_plural = _('cities stats')
