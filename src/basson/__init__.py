__VERSION__ = "0.4.1"

from .api import (
    BASS,       # API provider
    BASSError,  # Exception class

    #1                  #2                  #3                  #4
    Info,               DeviceInfo,
    ConfigOption,       IOSSessionFlag,     DeviceFlag,         D3AlorithmsOption,
    CommonFlag,         StatusOption,       NetPlaylistOption,  DXVersionOption,
    NorampOption,       SamplerateConversionOption, ChannelType, DataLengthOption,
    DataFlag,           PosModeOption,      ChannelOption,      SampleFlag,
    StreamFlag,         InfoFlag,           MusicFreqOption,    MusicFlag,
    SpeakerFlag,        MusicSurroundOption, 
)

from .basson import (
    Basson      # Main wrapper class
)

from .channel import (
    Channel,
)

from .stream import (
    StreamFile,         StreamURL,
)

from .music import (
    Music
)

from .record import (
    Record
)

__all__ = [
    "BASS", "BASSError", 
    "Basson",

    #1                  #2                  #3                  #4
    "ConfigOption",     "IOSSessionFlag",   "DeviceFlag",       "D3AlorithmsOption", 
    "CommonFlag",       "StatusOption",     "NetPlaylistOption", "DXVersionOption",
    "NorampOption",     "SamplerateConversionOption", "ChannelType", "DataLengthOption",
    "DataFlag",         "PosModeOption",    "ChannelOption",    "SampleFlag",
    "StreamFlag",       "InfoFlag",         "MusicFreqOption",  "MusicFlag",
    "SpeakerFlag",      "MusicSurroundOption", 

    "Info",             "DeviceInfo",

    "Channel",

    "StreamFile",       "StreamURL",
    "Music",
    "Record",
    ]