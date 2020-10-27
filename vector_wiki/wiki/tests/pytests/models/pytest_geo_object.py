
import pytest
from django.core.validators import ValidationError
from wiki.models import City, Continent, Country


class TestGeoObjectModels:

    def _create_default_data(self):
        self.continent_africa = Continent.objects.create(
            name='Africa',
            population=1.216e9,
            area=30.37e12
        )
        self.country_morocco = Country.objects.create(
            continent=self.continent_africa,
            name='Morocco',
            population=36.03e6,
            area=446.55e9
        )
        self.city_casablanca = City.objects.create(
            country=self.country_morocco,
            name='Casablanca',
            population=3.36e6,
            area=220e6
        )

    @pytest.mark.django_db
    def test_success_data_creation(self):
        self._create_default_data()

    # exceeded tests

    @pytest.mark.django_db
    def test_city_area_exceeded(self):
        self._create_default_data()
        self.city_casablanca.area = 999e12
        with pytest.raises(ValidationError) as e_info:
            self.city_casablanca.save()
        
    @pytest.mark.django_db
    def test_city_population_exceeded(self):
        self._create_default_data()
        self.city_casablanca.population = 999e12
        with pytest.raises(ValidationError) as e_info:
            self.city_casablanca.save()

    @pytest.mark.django_db
    def test_country_area_exceeded(self):
        self._create_default_data()
        self.country_morocco.area = 999e12
        with pytest.raises(ValidationError) as e_info:
            self.country_morocco.save()
        
    @pytest.mark.django_db
    def test_country_population_exceeded(self):
        self._create_default_data()
        self.country_morocco.population = 999e12
        with pytest.raises(ValidationError) as e_info:
            self.country_morocco.save()

    # underestimated tests

    @pytest.mark.django_db
    def test_continent_area_underestimated(self):
        self._create_default_data()
        self.continent_africa.area = 1
        with pytest.raises(ValidationError) as e_info:
            self.continent_africa.save()
        
    @pytest.mark.django_db
    def test_continent_population_underestimated(self):
        self._create_default_data()
        self.continent_africa.population = 1
        with pytest.raises(ValidationError) as e_info:
            self.continent_africa.save()

    @pytest.mark.django_db
    def test_country_area_underestimated(self):
        self._create_default_data()
        self.country_morocco.area = 1
        with pytest.raises(ValidationError) as e_info:
            self.country_morocco.save()
        
    @pytest.mark.django_db
    def test_country_population_underestimated(self):
        self._create_default_data()
        self.country_morocco.population = 1
        with pytest.raises(ValidationError) as e_info:
            self.country_morocco.save()


