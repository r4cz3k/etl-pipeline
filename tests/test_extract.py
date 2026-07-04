from unittest.mock import MagicMock, patch
import requests
from src.extract import get_data, fetch_page


@patch('src.extract.rq.get')
def test_loop_stops_on_empty(mock_get):
    mock_get.return_value.json.return_value = {'products': [], 'total': 0}

    result = get_data('https://mock-url.com')
    assert result == []

@patch('src.extract.rq.get')
def test_pagination_merges_two_pages(mock_get):
    first_page = MagicMock()
    first_page.json.return_value = {'products': [{'id': 1}], 'total': 2}

    second_page = MagicMock()
    second_page.json.return_value = {'products': [{'id': 2}], 'total': 2}

    third_page = MagicMock()
    third_page.json.return_value = {'products': [], 'total': 2}

    mock_get.side_effect = [first_page, second_page, third_page]

    result = get_data('https://mock-url.com')
    assert len(result) == 2

@patch('src.extract.sleep') # Too long wait time without mocking sleep function
@patch('src.extract.rq.get')
def test_retry_succeeds_after_two_500s(mock_get, mock_sleep):
    error = requests.exceptions.HTTPError()
    error.response = MagicMock() # Fresh HTTPError has set response = None - no way to set status_code without MagicMock()
    error.response.status_code = 500

    success = MagicMock()

    mock_get.side_effect = [error, error, success]

    result = fetch_page('https://mock-url.com', params={'skip': 30})

    assert mock_get.call_count == 3
    assert result == success

