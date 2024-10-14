import datetime, timedelta
import pytest, responses
from logger import setup_logger
from colorlog import ColoredFormatter
logger = setup_logger(__name__)
from fitbit_api_manager import FitbitPythonService as FB
from persist_data import PickleStorage as PS

ps = PS()
fb = FB(ps)

@pytest.fixture
def mock_response():
    with responses.RequestsMock() as rsps:
        yield rsps

def test_setup_logger():
    logger = setup_logger('test')
    # assert isinstance(logger, logger.Logger)
    assert logger.name == 'test'
    assert len(logger.handlers) == 1
    handler = logger.handlers[0]
    # assert isinstance(handler, logger.StreamHandler)
    formatter = handler.formatter
    assert isinstance(formatter, ColoredFormatter)
    # Test that the formatter is using the expected format
    assert formatter._fmt == '%(log_color)s%(levelname)s%(reset)s %(asctime)s: %(message)s (%(filename)s:%(lineno)d)'

def test_fitbit_python_service():
    ps = PS()
    fb = FB(ps)
    current_timestamp = int(datetime.datetime.now().strftime('%Y%m%d%H'))
    next_hour = int( (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime('%Y%m%d%H'))
    assert current_timestamp == fb.get_current_timestamp()
    assert next_hour == fb.get_next_hour_timestamp()
    assert current_timestamp < next_hour

def test_rate_limiting_logic():

    current_timestamp = int(datetime.datetime.now().strftime('%Y%m%d%H'))
    next_hour = int( (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime('%Y%m%d%H'))
    assert current_timestamp == fb.get_current_timestamp()
    assert next_hour == fb.get_next_hour_timestamp()
    assert current_timestamp < next_hour

    assert fb.check_if_rate_limited() is False

    fb.set_rate_limited(True, current_timestamp)
    assert fb.check_if_rate_limited() is False

    current_timestamp = next_hour
    assert fb.check_if_rate_limited() is False

    fb.set_rate_limited(True, current_timestamp)
    assert fb.check_if_rate_limited() is True


# Test data for the test_make_api_calls function;
test_api_calls_error_cases_testdata_metadata = "responses_type, input_url, json_input, patch_http_status, response_data_tuple"
test_api_calls_error_cases_testdata = [
    (   #Testing that a 401 results int he expected tuple being returned
        responses.GET,
        'http://site.com/profile.json',
        {
            'arg1':1,
            'arg2': 2,
            'NOT_IMPLEMENTED': 'NOT_IMPLEMENTED'},
        401,
        (   False,
            responses.Response(
                 method='GET',
                 url='http://site.com/profile.json',
                 status=401)
            )
    ),

    (   #Testing that a 401 results int he expected tuple being returned
        responses.GET,
        'http://site.com/profile.json',
        {
            'arg1':1,
            'arg2': 2,
            'NOT_IMPLEMENTED': 'NOT_IMPLEMENTED'},
        429,
        (   False,
            responses.Response(
                method='GET',
                url='http://site.com/profile.json',
                status=429)
            )
        ),
]
@pytest.mark.parametrize(test_api_calls_error_cases_testdata_metadata, test_api_calls_error_cases_testdata)
def test_make_api_calls_error_cases(mock_response ,responses_type, input_url, json_input, patch_http_status, response_data_tuple):
    mock_response.add(
        method=responses_type,
        url=input_url,
        json=json_input,
        status=patch_http_status)
    response_data = fb.make_api_call(
                                    endpoint=input_url,
                                    arg1=1,
                                    arg2=2,
                                    NOT_IMPLEMENTED='NOT_IMPLEMENTED'
                    )

    assert response_data[0] == response_data_tuple[0]
    assert response_data[1].status_code == response_data_tuple[1].status

