def test_home_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """

    response = client.get("/")
    assert response.status_code == 200


def test_home_page_post(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (POST)
    THEN check that the status code a '405' is returned
    """

    response = client.post("/")
    assert response.status_code == 405
