import pytest
from pytest_bdd import scenario, given, when, then, parsers

@scenario('my_api_scenario.feature', 'Getting data from the API every 4 hours')
def test_getting_data_from_the_api():
    pass

@given('I am accessing the API at <url>')
def access_api(url):
    return requests.get(url)

@when('I request data from the API')
def request_data_from_api():
    response = requests.get(url)
    assert response.status_code == 200
    return response.json()

@then('I receive the most recent data from the API')
def get_most_recent_data(response):
    assert response['data']['timestamp'] > (datetime.now() - timedelta(hours=4)).isoformat()
