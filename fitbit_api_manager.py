import datetime, timedelta
import requests
from logger import setup_logger
logger = setup_logger(__name__)
from persist_data import PickleStorage as PS

class FitbitPythonService:
    def __init__(self, pickle_storage:PS):
        self.current_hour_timestamp: int = self.get_current_timestamp()
        self.next_hour_timestamp: int = self.get_next_hour_timestamp()
        self.rate_limited: tuple[bool, int] = (False, self.next_hour_timestamp)
        self.access_token = 'REPLACE_ME'
        self.headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        logger.info("FitbitPythonService initialized! ")

    def get_current_timestamp(self):
        return int(datetime.datetime.now().strftime('%Y%m%d%H'))

    def get_next_hour_timestamp(self):
        return int(
            (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime('%Y%m%d%H')
            )

    def set_rate_limited(self, rate_limited:bool, current_hour_timestamp:datetime):
        self.rate_limited = rate_limited, current_hour_timestamp

    def check_if_rate_limited(self) -> bool:
        assert isinstance(self.rate_limited, tuple) and len(self.rate_limited) == 2
        assert isinstance(self.rate_limited[1], int) and self.rate_limited[0] in [True, False]

        if self.rate_limited[0]:
            if self.current_hour_timestamp == self.rate_limited[1]:
                logger.info(f"Rate limit hour passed, resetting! {self.current_hour_timestamp, self.rate_limited}")
                self.set_rate_limited(False, self.get_next_hour_timestamp())
                return False
            else:
                logger.info(f"Still within rate limited hour, resetting! {self.current_hour_timestamp, self.rate_limited}")
                return True
        else:
            logger.info(f"NOT Rate Limited {self.rate_limited}")
            return False

    def make_api_call(self, endpoint:str, **kargs) -> tuple:
        """Make an API call to the Fitbit API and return the response.

        Args:
            endpoint (str): The URL of the API endpoint to make a request to.
            **kargs (dict): Optional keyword arguments to pass to the API.

        Returns:
            tuple: A tuple containing two elements.
                The first element is a boolen for sucess/failue.
                The secondis the response object from the request.
        """

        #assert expectations for args
        logger.info(f"API Call Init: {endpoint}, {kargs}")

        # Generate endpoint URI
        # Make API Call
            # Scan for Error codes
            # Handle Rate Limiting
            # If successful handle pagination (prob need to manage this if making large # of calls)

        try:
            response = requests.get(endpoint, headers=self.headers)
            logger.debug(f'>>>>> RESPONSE type: {type(response)}')
            # self.fitBitCallsPerHour +=1
            if response.status_code == 401:
                logger.error('API Call Failed: Token _probably_ Expired, get a new one!! https://dev.fitbit.com/build/reference/web-api/troubleshooting-guide/oauth2-tutorial/?clientEncodedId=23PKPQ&redirectUri=http://localhost&applicationType=PERSONAL')
                return(False, response)
            elif response.status_code == 429:
                logger.warning('API Call Failed: Rate Limited by Server (currently 150 calls/hr)!')
                return(False, response)
            elif response.status_code != 200:
                logger.error(f"API Call Failed: Error ({endpoint}): {response.status_code}, {response.reason}, {response.text}")
                return(False, response)

            api_data_json = response.json()
            # master_dict.update(api_data_json)
            # if 'pagination' in api_data_json and \
            #         'next' in api_data_json['pagination'] and \
            #         len(api_data_json['pagination']['next'])>5:
            #     self.paginationCount += 1
            #     endpoint = api_data_json['pagination']['next']
            #     print(f'... added {len(api_data_json["activities"])} activities to master_dict')
            #     print(f"\t Added {len(api_data_json['activities'])} activities; Next page available:", api_data_json['pagination']['next'])
            # else:
            #     print(f"\t No next page available. Total Page Count: {self.paginationCount}")
        except Exception as e:
            exception_mesggage = f'Unexpected Error {response.status_code}: {str(e)}'
            logger.exception(exception_mesggage)
            raise Exception(exception_mesggage)

        logger.info("API Call Done.")
        return (True, response)