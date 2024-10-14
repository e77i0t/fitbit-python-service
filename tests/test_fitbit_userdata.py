from logger import setup_logger
logger = setup_logger(__name__)
import datetime
import pytest
from fitbit_user_data import FitbitUserData as FBUserData

@pytest.fixture()
def mock_fitbit_user_data():
    pass


@pytest.mark.skip("NOT IMPLEMENTED YET")
def test_get_user_activities_detailed(mock_fitbit_user_data):
    after_date = datetime.datetime(2022, 1, 1)
    sort = 'desc'
    offset = 0
    limit = 100
    # activities = FBUserData.get_user_activities_detailed(
    #     afterDate=after_date,
    #     sort=sort,
    #     offset=offset,
    #     limit=limit)
    # assert len(activities) == limit
    # for activity in activities:
    #     assert activity['date'] >= after_date
    FB = FBUserData()
    resp = FB.get_user_profile()

    assert len(resp) == 2
    assert 'NOT_IMPLEMENTED' not in resp[1].keys()

    pass
