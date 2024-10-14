import pytest
import os
from persist_data import PickleStorage

@pytest.fixture
def temp_storage(tmp_path):
    return PickleStorage(filename=tmp_path / "test_file.pkl")

class TestPickleStorage:
    def test_read(self, temp_storage):
        assert temp_storage.read() == {}

    @pytest.mark.parametrize("data", [{"key1": "value1"}, {"key2": "value2"}])
    def test_create(self, temp_storage, data):
        temp_storage.create(data)
        assert temp_storage.read() == data

    @pytest.mark.parametrize("data", [{"key1": "value1"}, {"key2": "value2"}])
    def test_update(self, temp_storage, data):
        temp_storage.create({"key3": "value3"})
        assert temp_storage.read() == {"key3": "value3"}
        temp_storage.update(data)
        assert temp_storage.read() == {**temp_storage.read(), **data}

    def test_delete(self, temp_storage):
        temp_storage.create({"key1": "value1"})
        assert os.path.exists(temp_storage.filename)
        temp_storage.delete()
        assert not os.path.exists(temp_storage.filename)

    def test_read_raises_file_not_found(self, temp_storage):
        filename = temp_storage.filename
        if os.path.exists(filename):
            os.remove(filename)

        with pytest.raises(FileNotFoundError):
            temp_storage.read(create_if_not_found=False)

    def test_read_raises_file_not_found_message(self, temp_storage):
        filename = temp_storage.filename
        if os.path.exists(filename):
            os.remove(filename)

        with pytest.raises(FileNotFoundError) as exc_info:
            temp_storage.read(create_if_not_found=False)

        assert str(exc_info.value) == str(filename)
