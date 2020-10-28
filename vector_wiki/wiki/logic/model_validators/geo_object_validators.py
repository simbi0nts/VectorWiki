
from django.core.validators import ValidationError
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext as _


class BaseComparisonValidator:

    def clean_exceeded_field(self, field_to_validate: str, parent_field: str):
        """ Check for: new value (child) <= available value (parent value - all other childs values) """

        current_obj_value = getattr(self, field_to_validate)
        parent = getattr(self, parent_field)
        parent_value = getattr(parent, field_to_validate)
        
        filter_args = {
            parent_field: parent
        }
        other_childs_values = self.__class__.objects.filter(**filter_args)
        other_childs_values_sum = other_childs_values.aggregate(Sum(field_to_validate))
        other_childs_values_sum = other_childs_values_sum.get(f'{field_to_validate}__sum') or 0

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
        """ Check for: new value (parent) >= of all child values (if they exist) """

        current_obj_value = getattr(self, field_to_validate)

        filter_args = {
            parent_field_in_child_model: self
        }
        all_child_values = child_model.objects.filter(**filter_args)
        all_child_values_sum = all_child_values.aggregate(Sum(field_to_validate))
        all_child_values_sum = all_child_values_sum.get(f'{field_to_validate}__sum')

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

