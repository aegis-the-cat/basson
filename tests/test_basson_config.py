
import pytest
import basson

EXPECTLIST = [
    ("asyncfile_buffer",    17, 8192),
    ("asyncfile_buffer",    0xFFFFFF, 16777216),
    ("buffer",              -17, 10),
    ("buffer",              5002, 5000),
    ("device_buffer",       -17, 0),
    ("device_period",       -17, -17),
    ("device_period",       17, 17),
    ("global_volume_music", -17, 0),
    ("global_volume_music", 17171, 10000),
    ("global_volume_sample", -17, 0),
    ("global_volume_sample", 17171, 10000),
    ("global_volume_stream", -17, 0),
    ("global_volume_stream", 17171, 10000),
    ("libpath",             "libaegis.dll", "libaegis.dll"),
    ("music_max_virtual_channels", -17 ,0),
    ("music_max_virtual_channels", 1717 ,512),
    ("net_agent",           "basson/0.4","basson/0.4"),
    ("net_buffer",          -17, 0),
    ("net_playlist_depth",  -17, 0),
    ("net_prebuffer",       -17, 0),
    ("net_proxy",            "example@aegis.com", "example@aegis.com"),
    ("net_readtimeout",     -17, 0),
    ("net_restrate",        -17, 1),
    ("net_timeout",         -17, 0),
    ("samplerate_conversion_quality", -17, 0),
    ("samplerate_conversion_quality_sample", -17, 0),
    ("updateperiod",        -17, 0),
    ("verify",              -17, 1000),
]

@pytest.fixture
def instance():
    return basson.Basson()

@pytest.mark.parametrize(
    "option, control, expected",
    EXPECTLIST,
    ids=[f"{name}={control}" for name, control, _ in EXPECTLIST],
)
def test_bass_config(instance, option, control, expected):
    try:
        setattr(instance, option, control)
        value = getattr(instance, option)
    except basson.BASSError.Illparam:
        pytest.skip(f"{option}={control} is not supported on this system")

    assert value == expected, (
        f"{option}={control}: expected {expected!r}, "
        f"got {value!r} ({type(value).__name__})"
    )
