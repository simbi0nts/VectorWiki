
import pytest
from django.core.validators import ValidationError

from wiki.models import City, Country, CityStat, CountryStat
from .base_geo_object import BaseTestGeoObjectStatModels


class TestGeoObjectModels(BaseTestGeoObjectStatModels):

    @pytest.mark.django_db
    def test_success_data_creation_success(self):
        self._create_default_data()

    @pytest.mark.django_db
    def test_add_existing_city_fail(self):
        self._create_default_data()
        
        city_test_stat = CityStat(
            city=self.city_casablanca,
            
            number_of_roads=10,
            number_of_trees=10,
            number_of_shops=10,
            number_of_schools=10
        )
        
        with pytest.raises(Exception) as e_info:
            city_test_stat.save()


    @pytest.mark.django_db
    def test_add_existing_country_fail(self):
        self._create_default_data()
        
        country_test_stat = CountryStat(
            country=self.country_morocco,
            
            number_of_hospitals=100,
            number_of_national_parks=100,
            number_of_rivers=100,
            number_of_schools=100
        )
        
        with pytest.raises(Exception) as e_info:
            country_test_stat.save()

    @pytest.mark.django_db
    def test_add_new_city_stat_success(self):
        self._create_default_data()

        test_city = City.objects.create(
            country=self.country_morocco,
            name='Test',
            population=1,
            area=220e6
        )

        city_test_stat = CityStat(
            city=test_city,
            
            number_of_roads=10,
            number_of_trees=10,
            number_of_shops=10,
            number_of_schools=10
        )
        city_test_stat.save()

    @pytest.mark.django_db
    def test_add_new_country_stat_success(self):
        self._create_default_data()

        country_test = Country.objects.create(
            continent=self.continent_africa,
            name='Test',
            population=36.03e6,
            area=446.55e9
        )

        country_test_stat = CountryStat(
            country=country_test,
            number_of_hospitals=100,
            number_of_national_parks=100,
            number_of_rivers=100,
            number_of_schools=100
        )
        country_test_stat.save()

