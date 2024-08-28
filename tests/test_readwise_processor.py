from unittest.mock import patch
from backend.app.services.readwise_processor import fetch_from_export_api

def test_fetch_from_export_api():
    mock_response = {
        'results': [
            {
                'title': 'Test Book',
                'author': 'Test Author',
                'highlights': [
                    {
                        'text': 'Test highlight',
                        'id': '123',
                    }
                ]
            }
        ]
    }
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200
        
        result = fetch_from_export_api()
        
        assert len(result) == 1
        assert result[0]['title'] == 'Test Book'
        assert len(result[0]['highlights']) == 1
        assert result[0]['highlights'][0]['text'] == 'Test highlight'