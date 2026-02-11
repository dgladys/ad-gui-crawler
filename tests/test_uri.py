from helpers.uri import UriParams

def test_uri_params_object():
    url = "https://allegrolokalnie.pl/oferty/q/krokodyl?sort=startingTime-desc&page=2&zrodlo=lokalnie&zrodlo=allegro"
    params = UriParams(url)
    assert params.is_valid() == True
    assert params.get_param("sort") == "startingTime-desc"
    assert params.get_param("page") == "2"
    assert params.get_int("page") == 2
    assert params.count() == 3
    assert params.has_param("zrodlo")
    assert not params.has_param("zrutlo")
    assert len(params.get_param("zrodlo")) == 2
    assert isinstance(params.to_json(), str)

def test_uri_params_invalid_url():
    url = "dfgfdgfdgfdgdf"
    params = UriParams(url)
    assert params.is_valid() == False
    assert params.count() == 0

