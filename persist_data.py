import os
import pickle
from logger import setup_logger
logger = setup_logger(__name__)


class PickleStorage:
    """
    A class for storing and retrieving data using the pickle format.

    Attributes:
        filename (str): The filename to store the data in.
        data_folder (str): The folder where the data file is located.
        metadata (dict): The metadata of the stored data.

    Methods:
        read: Reads data from the file.
        create: Creates a new file with the given data.
        update: Updates the data in the file.
        delete: Deletes the file.
        g
    """

    def __init__(self, filename:str = None):
        """
        Initializes the PickleStorage class.

        Args:
            filename (str, optional): The filename to store the data in. Defaults to './data/fitbit_data.pickle'.

        Raises:
            OSError: If the directory for the filename cannot be created.
        """
        self.data_folder = './data/'

        if filename is None:
            self.filename = './data/fitbit_data.pickle'
            self.create()
        else:
            self.filename = filename
            self.data_folder = os.path.dirname(self.filename)

        self.metadata = self.get_storage_metadata()

    def read(self, create_if_not_found:bool = True, default_dic_values:dict = {}):
        """
        Reads data from the file.

        Args:
            create_if_not_found (bool, optional): Whether to create the file if it does not exist. Defaults to True.
            default_dic_values (dict, optional): Default values to use if the file does not exist. Defaults to {}.

        Returns:
            dict: The data stored in the file.

        Raises:
            FileNotFoundError: If the file does not exist and create_if_not_found is False.
        """
        try:
            with open(self.filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            if create_if_not_found:
                logger.info(f'{self.filename} not found, creating & setting to')
                self.create(default_dic_values)
                return default_dic_values
            else:
                raise FileNotFoundError(self.filename)

    def create(self, data:dict={}):
        """
        Creates a new file with the given data.

        Args:
            data (dict, optional): The data to store in the file. Defaults to {}.

        Returns:
            None

        Raises:
            OSError: If the file cannot be created.
            pickle.PicklingError: If the data cannot be pickled.
        """
        try:
            if not os.path.exists(os.path.dirname(self.filename)):
                os.makedirs(os.path.dirname(self.filename))

            with open(self.filename, "wb") as f:
                return pickle.dump(data, f)
        except OSError as e:
            logger.error(f"Error creating file: {e}")
        except pickle.PicklingError as e:
            logger.error(f"Error pickling data: {e}")

    def update(self, data:dict):
        """
        Updates the data in the file.

        Args:
            data (dict): The data to update.

        Returns:
            None

        Raises:
            pickle.PicklingError: If the data cannot be pickled.
            EOFError: If the file is empty.
        """
        with open(self.filename, "rb+") as f:
            pickled_data = pickle.load(f)
            pickled_data.update(data)
            f.seek(0)
            pickle.dump(pickled_data, f)

    def delete(self):
        """
        Deletes the file.

        Returns:
            None

        Raises:
            OSError: If the file cannot be deleted.
        """
        logger.warning("Deleting file: "+str(self.filename))
        os.remove(self.filename)

    def get_storage_metadata(self):
        """
        Retrieves metadata about the stored data.

        Returns:
            dict: The metadata of the stored data.

        Raises:
            FileNotFoundError: If the file does not exist.
            AssertionError: If the stored data is not a dictionary.
        """
        try:
            if os.path.exists(self.filename):
                with open(self.filename, "rb") as f:
                    result = pickle.loads(f.read())
            else:
                result = {} # load defaults
            assert isinstance(result, dict)
            return result
        except (FileNotFoundError) as e:
            logger.error(f"Unable to read file: {e}")
            return None
        except (AssertionError) as e:
            logger.error(f"Invalid param type passed: {e}")
            return None
