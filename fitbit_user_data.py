import datetime
from logger import setup_logger
logger = setup_logger(__name__)
from typing import Literal
from fitbit_api_manager import FitbitPythonService as FBpy
from persist_data import PickleStorage

class FitbitUserData():
    '''
    '''
    def __init__(self):
        PS = PickleStorage()
        FB = FBpy(PS)


    #TODO API CALLS TO
        # ['Activity data', 'activities.json',f'{self.data_path}fitbit_data_user_activities.json' ],
        # ['Activity list', None, f'{self.data_path}fitbit_data_user_activities_list.json'],
        # ['Heart Rate Time Series by Date Range', f'activities/heart/date/{self.threeMonthsAgo}/today.json', f'{self.data_path}fitbit_data_user_heart_rate.json'],

    #TODO Infrastructure for data storage and retrieval
        # persist last retrieved date for each endpoint
        # persist last retrieved data for each endpoint

    def get_user_profile(self):

        resp = tuple() #(status, response obj)
        resp = self.FB.make_api_call(
                                endpoint='/profile.json',
                                arg1=1,
                                arg2=2,
                                NOT_IMPLEMENTED='GET_USER_PROFILE'
                )
        #ensuring we get back what we expet or assert/fail

        return resp

    def get_user_activities_general(self):
        pass

    def get_user_activities_detailed(self,
                                     afterDate:datetime.datetime = None,
                                     sort: Literal['asc', 'desc'] = 'desc',
                                     offset: Literal[0, 100] = 0,
                                     limit: Literal[0, 100] = 100
                                     ):
        pass