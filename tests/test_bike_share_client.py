import pytest
from unittest.mock import patch, Mock
from ingestion.bike_share_client import (
    fetch_station_status,
    fetch_station_information,
    combine_station_data,
    _get_api_call,
)


class TestCombineStationData:
    def test_normal_merge(self):
        status = [
            {"station_id": "1", "num_bikes_available": 5, "num_docks_available": 10},
            {"station_id": "2", "num_bikes_available": 3, "num_docks_available": 7},
        ]
        info = [
            {"station_id": "1", "name": "Station A", "lat": 43.0, "lon": -79.0},
            {"station_id": "2", "name": "Station B", "lat": 43.1, "lon": -79.1},
        ]

        result = combine_station_data(status, info)

        assert len(result) == 2
        assert result[0]["name"] == "Station A"
        assert result[0]["station_status"]["num_bikes_available"] == 5
        assert result[1]["name"] == "Station B"
        assert result[1]["station_status"]["num_docks_available"] == 7

    def test_missing_status(self):
        status = [{"station_id": "1", "num_bikes_available": 5}]
        info = [
            {"station_id": "1", "name": "Station A"},
            {"station_id": "2", "name": "Station B"},
        ]

        result = combine_station_data(status, info)

        assert result[0]["station_status"] is not None
        assert result[1]["station_status"] is None

    def test_empty_lists(self):
        result = combine_station_data([], [])
        assert result == []

    def test_status_only(self):
        status = [{"station_id": "1", "num_bikes_available": 5}]
        info = []

        result = combine_station_data(status, info)
        assert result == []

    def test_info_only(self):
        status = []
        info = [{"station_id": "1", "name": "Station A"}]

        result = combine_station_data(status, info)
        assert result[0]["station_status"] is None


class TestFetchStationStatus:
    @patch("ingestion.bike_share_client._get_api_call")
    def test_success(self, mock_get):
        mock_get.return_value = {
            "data": {
                "stations": [
                    {"station_id": "1", "num_bikes_available": 5}
                ]
            }
        }

        result = fetch_station_status()

        assert result == [{"station_id": "1", "num_bikes_available": 5}]
        mock_get.assert_called_once()


class TestFetchStationInformation:
    @patch("ingestion.bike_share_client._get_api_call")
    def test_success(self, mock_get):
        mock_get.return_value = {
            "data": {
                "stations": [
                    {"station_id": "1", "name": "Station A", "lat": 43.0}
                ]
            }
        }

        result = fetch_station_information()

        assert result == [{"station_id": "1", "name": "Station A", "lat": 43.0}]


class TestGetApiCall:
    @patch("ingestion.bike_share_client.requests.get")
    def test_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"stations": []}}
        mock_get.return_value = mock_response

        result = _get_api_call("http://test.com")

        assert result == {"data": {"stations": []}}

    @patch("ingestion.bike_share_client.requests.get")
    def test_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        with pytest.raises(Exception, match="ApiRequestError"):
            _get_api_call("http://test.com")

    @patch("ingestion.bike_share_client.requests.get")
    def test_timeout(self, mock_get):
        import requests as req
        mock_get.side_effect = req.Timeout()

        with pytest.raises(req.Timeout):
            _get_api_call("http://test.com")
