
import pytest
from django.core.validators import ValidationError

from wiki.models import City
from .base_geo_object import BaseTestGeoObjectModels


class TestGeoObjectModels(BaseTestGeoObjectModels):

    @pytest.mark.django_db
    def test_success_data_creation_success(self):
        self._create_default_data()

    # exceeded tests

    @pytest.mark.django_db
    def test_city_population_exceeded_success(self):
        self._create_default_data()
        
        test_city = City.objects.create(
            country=self.country_morocco,
            name='Test',
            population=1,
            area=220e6
        )
        
        test_city.population = self.country_morocco.population - self.city_casablanca.population - 1
        test_city.save()

    @pytest.mark.django_db
    def test_city_population_exceeded_fail(self):
        self._create_default_data()
        
        test_city = City.objects.create(
            country=self.country_morocco,
            name='Test',
            population=1,
            area=220e6
        )
        
        test_city.population = self.country_morocco.population - self.city_casablanca.population + 1
        with pytest.raises(ValidationError) as e_info:
            test_city.save()

    @pytest.mark.django_db
    def test_city_area_exceeded_fail(self):
        self._create_default_data()
        self.city_casablanca.area = 999e12
        with pytest.raises(ValidationError) as e_info:
            self.city_casablanca.save()
        
    @pytest.mark.django_db
    def test_city_population_exceeded_fail2(self):
        self._create_default_data()
        self.city_casablanca.population = 999e12
        with pytest.raises(ValidationError) as e_info:
            self.city_casablanca.save()

    @pytest.mark.django_db
    def test_country_area_exceeded_fail(self):
        self._create_default_data()
        self.country_morocco.area = 999e12
        with pytest.raises(ValidationError) as e_info:
            self.country_morocco.save()
        
    @pytest.mark.django_db
    def test_country_population_exceeded_fail(self):
        self._create_default_data()
        self.country_morocco.population = 999e12
        with pytest.raises(ValidationError) as e_info:
            self.country_morocco.save()

    # underestimated tests

    @pytest.mark.django_db
    def test_continent_area_underestimated_fail(self):
        self._create_default_data()
        self.continent_africa.area = 1
        with pytest.raises(ValidationError) as e_info:
            self.continent_africa.save()
        
    @pytest.mark.django_db
    def test_continent_population_underestimated_fail(self):
        self._create_default_data()
        self.continent_africa.population = 1
        with pytest.raises(ValidationError) as e_info:
            self.continent_africa.save()

    @pytest.mark.django_db
    def test_country_area_underestimated_fail(self):
        self._create_default_data()
        self.country_morocco.area = 1
        with pytest.raises(ValidationError) as e_info:
            self.country_morocco.save()
        
    @pytest.mark.django_db
    def test_country_population_underestimated_fail(self):
        self._create_default_data()
        self.country_morocco.population = self.city_casablanca.population - 1
        with pytest.raises(ValidationError) as e_info:
            self.country_morocco.save()

    @pytest.mark.django_db
    def test_country_population_underestimated_success(self):
        self._create_default_data()
        self.country_morocco.population = self.city_casablanca.population + 1
        self.country_morocco.save()


