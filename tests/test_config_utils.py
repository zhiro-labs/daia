from utils.config_utils import env_onoff_to_bool


def test_env_onoff_to_bool():
    assert env_onoff_to_bool("on") is True
    assert env_onoff_to_bool("ON") is True
    assert env_onoff_to_bool("off") is False
    assert env_onoff_to_bool("OFF") is False
    assert env_onoff_to_bool(None, default=True) is True
    assert env_onoff_to_bool(None, default=False) is False
    assert env_onoff_to_bool("other", default=False) is False
