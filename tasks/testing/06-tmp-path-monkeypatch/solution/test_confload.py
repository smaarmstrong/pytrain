from confload import get_setting, load_config, save_config


def test_round_trip_preserves_values_and_types(tmp_path):
    cfg = {"retries": 3, "debug": True, "name": "api"}
    path = tmp_path / "config.json"
    save_config(path, cfg)
    assert load_config(path) == cfg


def test_missing_file_gives_empty_config(tmp_path):
    assert load_config(tmp_path / "does-not-exist.json") == {}


def test_setting_read_from_env(monkeypatch):
    monkeypatch.setenv("APP_TIMEOUT", "banana")
    assert get_setting("timeout") == "banana"


def test_setting_falls_back_to_default(monkeypatch):
    monkeypatch.delenv("APP_TIMEOUT", raising=False)
    assert get_setting("timeout", 30) == 30
    assert get_setting("timeout") is None


def test_true_false_become_bools(monkeypatch):
    monkeypatch.setenv("APP_DEBUG", "True")
    assert get_setting("debug") is True
    monkeypatch.setenv("APP_DEBUG", "false")
    assert get_setting("debug") is False


def test_digits_become_int(monkeypatch):
    monkeypatch.setenv("APP_RETRIES", "12")
    assert get_setting("retries") == 12
    assert isinstance(get_setting("retries"), int)
