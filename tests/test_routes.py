def test_login_required(client):
    response = client.get("/")
    assert response.status_code == 302

def test_missing_page(client):
    response = client.get("/does-not-exist")
    assert response.status_code == 404
