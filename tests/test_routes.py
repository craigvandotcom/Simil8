def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Health check passed' in response.data

def test_process_highlights(client):
    response = client.post('/process-highlights')
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data
    assert data['status'] == 'success'

def test_generate_tweets(client):
    data = {'content': 'Test content for tweet generation'}
    response = client.post('/generate-tweets', json=data)
    assert response.status_code == 200
    result = response.get_json()
    assert 'status' in result
    assert result['status'] == 'success'
    assert 'variations' in result
    assert len(result['variations']) > 0

# Add more tests here