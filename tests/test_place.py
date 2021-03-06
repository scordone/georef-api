from service import app
from . import SearchEntitiesTest

PLACES = [
    ('-27.27416', '-66.75292', {
        'provincia': '10',
        'departamento': '10035',
        'municipio': '100077'
    }),
    ('-35.493', '-60.968', {
        'provincia': '06',
        'departamento': '06588',
        'municipio': '060588'
    }),
    ('-53.873', '-67.825', {
        'provincia': '94',
        'departamento': '94007',
        'municipio': '940007'
    }),
    ('-25.718', '-53.994', {
        'provincia': '54',
        'departamento': '54049',
        'municipio': '540182'
    })
]

class SearchPlaceTest(SearchEntitiesTest):
    """Pruebas de búsqueda por ubicación."""

    def setUp(self):
        self.endpoint = '/api/v1.0/ubicacion'
        self.entity = 'ubicacion'
        super().setUp()

    def test_default_results_fields(self):
        """Las entidades devueltas deben tener los campos default."""
        place = PLACES[0]
        data = self.get_response({'lat':place[0], 'lon': place[1]})[0]
        fields = sorted([
            'provincia',
            'departamento',
            'municipio',
            'lat',
            'lon'
        ])
        self.assertListEqual(fields, sorted(data.keys()))

    def test_valid_coordinates_len_1(self):
        """Si las coordenadas son correctas, sólo debería haber un
        resultado."""
        place = PLACES[0]
        data = self.get_response({'lat':place[0], 'lon': place[1]})
        self.assertEqual(len(data), 1)

    def test_valid_coordinates(self):
        """Se deberían encontrar resultados para coordenadas válidas."""
        validations = []

        for lat, lon, data in PLACES:
            res = self.get_response({'lat': lat, 'lon': lon})[0]
            validations.append(all([
                res['municipio']['id'] == data['municipio'],
                res['departamento']['id'] == data['departamento'],
                res['provincia']['id'] == data['provincia']
            ]))

        self.assertTrue(validations and all(validations))

    def test_invalid_coordinates(self):
        """No se deberían encontrar resultados cuando se utilizan coordenadas
        erroneas."""
        place = PLACES[0]
        data = self.get_response({'lat': 0, 'lon': 0})
        self.assertEqual(len(data), 0)

    def test_empty_params(self):
        """Los parámetros que esperan valores no pueden tener valores
        vacíos."""
        params = ['lat', 'lon']
        self.assert_empty_params_return_400(params)

    def test_unknown_param_returns_400(self):
        """El endpoint no debe aceptar parámetros desconocidos."""
        self.assert_unknown_param_returns_400()
    
    def test_flat_results(self):
        """El parametro aplanar deberia aplanar los resultados devueltos."""
        place = PLACES[0]
        resp = self.get_response({
            'lat':place[0], 
            'lon': place[1],
            'aplanar': 1
        })

        self.assertTrue(all([
            not isinstance(v, dict) for v in resp[0].values()
        ]) and resp)


if __name__ == '__main__':
    unittest.main()
