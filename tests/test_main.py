from app.main import app, url_store, lock
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_health_check(client):
    res = client.get('/')
    assert res.status_code == 200
    assert res.get_json()['status'] == 'healthy'

def test_create_short_url(client):
    res = client.post('/api/shorten', json={'url': 'https://example.com'})
    assert res.status_code == 201
    data = res.get_json()
    assert 'short_code' in data
    assert 'short_url' in data

def test_redirect_url(client):
    res = client.post('/api/shorten', json={'url': 'https://example.com'})
    short_code = res.get_json()['short_code']
    res_redirect = client.get(f'/{short_code}', follow_redirects=False)
    assert res_redirect.status_code == 302
    assert res_redirect.location == 'https://example.com'

def test_stats(client):
    res = client.post('/api/shorten', json={'url': 'https://example.com'})
    short_code = res.get_json()['short_code']
    client.get(f'/{short_code}')  # simulate one click
    res_stats = client.get(f'/api/stats/{short_code}')
    stats = res_stats.get_json()
    assert stats['clicks'] == 1
    assert stats['url'] == 'https://example.com'
    assert 'created_at' in stats

def test_invalid_short_code(client):
    res = client.get('/api/stats/fake123')
    assert res.status_code == 404
