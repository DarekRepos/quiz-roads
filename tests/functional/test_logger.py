def test_info_level_log(client, caplog):
    """
    Verify log for INFO level
    """
    user_logs = client.get("/")
    assert len(caplog.records) == 1
    assert "Visited" in caplog.text
