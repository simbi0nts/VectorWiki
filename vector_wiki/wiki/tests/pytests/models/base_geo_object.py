
from wiki.models import City, Continent, Country, CountryStat, CityStat


class BaseTestGeoObjectModels:

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


class BaseTestGeoObjectStatModels(BaseTestGeoObjectModels):

    def _create_default_data(self):
        super()._create_default_data()

        self.country_morocco_stat = CountryStat.objects.create(
            country=self.country_morocco,
            
            number_of_hospitals=100,
            number_of_national_parks=100,
            number_of_rivers=100,
            number_of_schools=100
        )
        self.city_casablanca_stat = CityStat.objects.create(
            city=self.city_casablanca,
            
            number_of_roads=10,
            number_of_trees=10,
            number_of_shops=10,
            number_of_schools=10
        )