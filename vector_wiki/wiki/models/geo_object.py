
from django.core.validators import ValidationError
from django.db import models
from django.db.models import Sum
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

    def clean_exceeded_field(self, field_to_validate: str, parent_field: str):
        """ Check for: new value <= available value (parent value - all other childs values)
        """

        current_obj_value = getattr(self, field_to_validate)
        parent = getattr(self, parent_field)
        parent_value = getattr(parent, field_to_validate)
        
        filter_arg = {
            parent_field: parent
        }
        other_childs_values = self.__class__._default_manager.filter(
            **filter_arg
        ).exclude(pk=self.pk).aggregate(Sum(field_to_validate))
        other_childs_values_sum = other_childs_values.get(f'{field_to_validate}__sum') or 0

        if current_obj_value > (parent_value - other_childs_values_sum):
            raise ValidationError(
                _('The %(field_to_validate)s of the %(parent_field)s is exceeded'),
                params={
                    'field_to_validate': field_to_validate,
                    'parent_field': parent_field,
                },
            )

    def clean_underestimated_field(self, 
                                   field_to_validate: str, 
                                   child_model: models.Model,
                                   parent_field_in_child_model: str):
        """ Check for: new value >= of all child values (if they exist)
        """

        current_obj_value = getattr(self, field_to_validate)

        filter_arg = {
            parent_field_in_child_model: self
        }
        all_child_values = child_model._default_manager.filter(
            **filter_arg
        ).aggregate(Sum(field_to_validate))
        all_child_values_sum = all_child_values.get(f'{field_to_validate}__sum')

        if all_child_values_sum is None:
            # No data in child model yet
            return
        
        if current_obj_value < all_child_values_sum:
            raise ValidationError(
                _('The %(field_to_validate)s of the %(parent_field)s is underestimated'),
                params={
                    'field_to_validate': field_to_validate,
                    'parent_field': parent_field_in_child_model,
                },
            )

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

    def full_clean(self, *args, **kwargs):
        super().full_clean(*args, **kwargs)
        self.clean_population()
        self.clean_area()


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

    def full_clean(self, *args, **kwargs):
        super().full_clean(*args, **kwargs)
        self.clean_population()
        self.clean_area()


class City(BaseGeoObject):
    country = models.ForeignKey(Country, verbose_name=_('country'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')

    def clean_population(self, *args, **kwargs):
        self.clean_exceeded_field('population', 'country')

    def clean_area(self, *args, **kwargs):
        self.clean_exceeded_field('area', 'country')

    def full_clean(self, *args, **kwargs):
        super().full_clean(*args, **kwargs)
        self.clean_population()
        self.clean_area()
