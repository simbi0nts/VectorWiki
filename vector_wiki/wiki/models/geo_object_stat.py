
from django.core.validators import ValidationError
from django.db import models
from django.db.models import Sum
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

    def clean_country(self):
        ''' NOTE: we could've use DB unique property, but python-side code looks like a more flexible way '''

        if CountryStat.objects.filter(country=self.country).exists():
            raise ValidationError(_("Stat for current country is already exists"))

    def clean_number_of_schools(self):
        ''' NOTE: probably it's better to create some basic validation class (like BaseComparisonValidator),
            but I want to focus on other problems at the moment
        '''
        
        error_msg = _("number of schools in country can't be less then total number of schools in all cities")
        
        cities_stat = CityStat.objects.filter(city__country=self.country)
        cities_total_number_of_schools = cities_stat.aggregate(Sum("number_of_schools"))
        cities_total_number_of_schools = cities_total_number_of_schools.get("number_of_schools")

        if cities_total_number_of_schools is None:
            return

        if self.number_of_schools < cities_total_number_of_schools:
            raise ValidationError(error_msg)

    def full_clean(self, *args, **kwargs):
        super().full_clean(*args, **kwargs)
        self.clean_country()
        self.clean_number_of_schools()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


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

    def clean_city(self):
        ''' NOTE: we could've use DB unique property, but python-side code looks like a more flexible way '''

        if CityStat.objects.filter(city=self.city).exists():
            raise ValidationError(_("Stat for current city is already exists"))

    def clean_number_of_schools(self):
        ''' NOTE: probably it's better to create some basic validation class (like BaseComparisonValidator),
            but I want to focus on other problems at the moment
        '''

        error_msg = _('''number of schools in city can't be more then
                        (number of schools in country - total number of schools in all other cities)''')
        
        cities_stat = CityStat.objects.filter(city__country=self.city.country)
        cities_total_number_of_schools = cities_stat.aggregate(Sum("number_of_schools"))
        cities_total_number_of_schools = cities_total_number_of_schools.get("number_of_schools") or 0

        country_stat = CountryStat.objects.filter(country=self.city.country)
        if not country_stat:
            return
        country_number_of_schools = country_stat.first().number_of_schools

        if self.number_of_schools > (country_number_of_schools - cities_total_number_of_schools):
            raise ValidationError(error_msg)

    def full_clean(self, *args, **kwargs):
        super().full_clean(*args, **kwargs)
        self.clean_city()
        self.clean_number_of_schools()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
