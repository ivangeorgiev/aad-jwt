from django.urls import reverse

def test_can_open_home(client):
    response = client.get(reverse("hello-django"))
    assert response.status_code == 200
    assert response.content == b"Hello, Django!"
