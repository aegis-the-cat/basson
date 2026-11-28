"""
This file contains all API for BASS library
"""

import sys, os, pathlib
from enum import IntFlag, IntEnum
import ctypes
import typing

#region CTypes types

INT =   ctypes.c_int        
BYTE =  ctypes.c_ubyte
WORD =  ctypes.c_ushort
DWORD = ctypes.c_ulong
QWORD = ctypes.c_uint64
FLOAT = ctypes.c_float
DOUBLE = ctypes.c_double
CHAR =  ctypes.c_char
PTR = ctypes.c_void_p # Pointer to something
CHARP = ctypes.c_char_p

BOOL = ctypes.c_int # BASS using integers as bollean
TRUE = 1 
'''`True` value in BASS'''
FALSE = 0 
'''`False` value in BASS'''
MINUSONE = 0xFFFFFFFF
'''`-1` value DWORD'''
QMINUSONE = 0xFFFFFFFFFFFFFFFF
'''`-1` value QWORD'''

# Pointers types (handles) BASS
#   There are different handle names for visual separating the destination. 
#   A universal handle is also provided. 
#   Basically it's all the same thing.
HANDLE =    DWORD
HMUSIC =    DWORD
HSAMPLE =   DWORD
HCHANNEL =  DWORD
HSTREAM =   DWORD
HRECORD =   DWORD
HSYNC =     DWORD
HDSP =      DWORD
HFX =       DWORD
HPLUGIN =   DWORD

# Streams callbacks
DOWNLOADPROC =  ctypes.CFUNCTYPE(None, PTR, DWORD, PTR)
DownloadProcType = typing.Callable[[PTR, DWORD, PTR], None]
FILECLOSEPROC = ctypes.CFUNCTYPE(None, PTR)
FileCloseProc = typing.Callable[[PTR], None]
FILELENPROC =   ctypes.CFUNCTYPE(QWORD, PTR)
FileLenProc = typing.Callable[[PTR], QWORD]
FILEREADPROC =  ctypes.CFUNCTYPE(DWORD, PTR, DWORD, PTR)
FileReadProcType = typing.Callable[[PTR, DWORD, PTR], DWORD]
FILESEEKPROC =  ctypes.CFUNCTYPE(BOOL, QWORD, PTR)
FileSeekProcType = typing.Callable[[QWORD, PTR], BOOL]
STREAMPROC =    ctypes.CFUNCTYPE(DWORD, HSTREAM, PTR, PTR)
StreamProcType = typing.Callable[[HSTREAM, PTR, PTR], DWORD]

# Record callback
RECORDPROC =    ctypes.CFUNCTYPE(BOOL, INT, PTR, DWORD, PTR)#second changed to int
RecordProcType = typing.Callable[[HRECORD, PTR, DWORD, PTR], BOOL]

# Channel callbacks
DSPPROC =       ctypes.CFUNCTYPE(None, HDSP, DWORD, PTR, DWORD, PTR)
DSPProcType = typing.Callable[[HDSP, DWORD, PTR, DWORD, PTR], None]
SYNCPROC =      ctypes.CFUNCTYPE(None, HSYNC, DWORD, DWORD, PTR)
SyncProcType = typing.Callable[[HSYNC, DWORD, DWORD, PTR], None]

IOSNOTIFYPROC = ctypes.CFUNCTYPE(None, DWORD)
IOSNotifyProcType = typing.Callable[[DWORD], None]
#endregion

#region CType Structures

# BASS / Config doesn't have any documented structures
# BASS / Plugins
class BASS_PLUGINFORM(ctypes.Structure):
    _fields_ = [
        ("ctype", DWORD),   # channel type
        ("name",  CHARP),   # format description (const char * or const wchar_t *)
        ("exts",  CHARP)    # file extension filter (const char * or const wchar_t *)
    ]
class BASS_PLUGININFO(ctypes.Structure):
    _fields_ = [
        ("version", DWORD),         # version (same form as BASS_GetVersion)
        ("formatc", DWORD),         # number of formats
        ("formats", ctypes.POINTER(BASS_PLUGINFORM)) # const BASS_PLUGINFORM *
    ]

# BASS / Initialization, info, etc...
class BASS_DEVICEINFO(ctypes.Structure):
    _fields_ = [
        ("name", CHARP),   # const char *name; (wchar_t* в некоторых конфигурациях Windows)
        ("driver", CHARP), # const char *driver; (wchar_t* в некоторых конфигурациях Windows)
        ("flags", DWORD)
    ]
class BASS_INFO(ctypes.Structure):
    _fields_ = [
        ("flags", DWORD),       # device capabilities (DSCAPS_xxx flags)
        ("hwsize", DWORD),      # unused
        ("hwfree", DWORD),      # unused
        ("freesam", DWORD),     # unused
        ("free3d", DWORD),      # unused
        ("minrate", DWORD),     # unused
        ("maxrate", DWORD),     # unused
        ("eax", BOOL),          # unused
        ("minbuf", DWORD),      # recommended minimum buffer length in ms
        ("dsver", DWORD),       # DirectSound version
        ("latency", DWORD),     # average delay (in ms) before start of playback
        ("initflags", DWORD),   # BASS_Init "flags" parameter
        ("speakers", DWORD),    # number of speakers available
        ("freq", DWORD)         # current output rate
    ]

# BASS / 3D
class BASS_3DVECTOR(ctypes.Structure):
    _fields_ = [
        ("x", FLOAT), # +=right, -=left
        ("y", FLOAT), # +=up, -=down
        ("z", FLOAT)  # +=front, -=behind
    ]

# BASS / Samples
class BASS_SAMPLE(ctypes.Structure):
    _fields_ = [
        ("freq",    DWORD), # default playback rate
        ("volume",  FLOAT), # default volume (0-1)
        ("pan",     FLOAT), # default pan (-1=left, 0=middle, 1=right)
        ("flags",   DWORD), # BASS_SAMPLE_xxx flags
        ("length",  DWORD), # length (in bytes)
        ("max",     DWORD), # maximum simultaneous playbacks
        ("origres", DWORD), # original resolution
        ("chans",   DWORD), # number of channels
        ("mingap",  DWORD), # minimum gap (ms) between creating channels
        ("mode3d",  DWORD), # BASS_3DMODE_xxx mode
        ("mindist", FLOAT), # minimum distance
        ("maxdist", FLOAT), # maximum distance
        ("iangle",  DWORD), # angle of inside projection cone
        ("oangle",  DWORD), # angle of outside projection cone
        ("outvol",  FLOAT), # delta-volume outside the projection cone
        ("vam",     DWORD), # unused
        ("priority", DWORD) # unused
    ]

# BASS / Streams
class BASS_FILEPROCS(ctypes.Structure):
    _fields_ = [
        ("close",  ctypes.POINTER(FILECLOSEPROC)),
        ("length", ctypes.POINTER(FILELENPROC)),
        ("read",   ctypes.POINTER(FILEREADPROC)),
        ("seek",   ctypes.POINTER(FILESEEKPROC))
    ]

# BASS / MOD music doesn't have any documented structures
# BASS / Recording
class BASS_RECORDINFO(ctypes.Structure):
    _fields_ = [
        ("flags",   DWORD), # device capabilities (DSCCAPS_xxx flags)
        ("formats", DWORD), # supported standard formats (WAVE_FORMAT_xxx flags)
        ("inputs",  DWORD), # number of inputs
        ("singlein", BOOL), # TRUE = only 1 input can be set at a time
        ("freq",    DWORD)  # current input rate
    ]

# BASS / Channels
class BASS_CHANNELINFO(ctypes.Structure):
    _fields_ = [
        ("freq",    DWORD),
        ("chans",   DWORD),
        ("flags",   DWORD),
        ("ctype",   DWORD),       # type of channel
        ("origres", DWORD),     # original resolution
        ("plugin",  HPLUGIN),
        ("sample",  HSAMPLE),
        ("filename", CHARP) # const char *
    ]
class TAG_APE_BINARY(ctypes.Structure):
    _fields_ = [
        ("key",     CHARP),   # const char *
        ("data",    PTR),  # const void *
        ("length",  DWORD)
    ]
class TAG_BEXT(ctypes.Structure):
    _fields_ = [
        ("Description",     CHAR * 256),
        ("Originator",      CHAR * 32),
        ("OriginatorReference", CHAR * 32),
        ("OriginationDate", CHAR * 10), # yyyy-mm-dd
        ("OriginationTime", CHAR * 8),   # hh-mm-ss
        ("TimeReference",   QWORD),                 # little-endian
        ("Version",         WORD),                        # little-endian
        ("UMID",            BYTE * 64),
        ("Reserved",        BYTE * 190)
        #TODO char CodingHistory[]
    ]
class TAG_CA_CODEC(ctypes.Structure):
    _fields_ = [
        ("ftype", DWORD), # file format
        ("atype", DWORD), # audio format
        ("name",  CHARP)  # const char *
    ]
class TAG_CART_TIMER(ctypes.Structure):
    _fields_ = [
        ("dwUsage", DWORD), # FOURCC timer usage ID
        ("dwValue", DWORD)  # timer value in samples from head
    ]
class TAG_CART(ctypes.Structure):
    _fields_ = [
        ("Version",     CHAR * 4),
        ("Title",       CHAR * 64),
        ("Artist",      CHAR * 64),
        ("CutID",       CHAR * 64),
        ("ClientID",    CHAR * 64),
        ("Category",    CHAR * 64),
        ("Classification", CHAR * 64),
        ("OutCue",      CHAR * 64),
        ("StartDate",   CHAR * 10),  # yyyy-mm-dd
        ("StartTime",   CHAR * 8),   # hh:mm:ss
        ("EndDate",     CHAR * 10),    # yyyy-mm-dd
        ("EndTime",     CHAR * 8),     # hh:mm:ss
        ("ProducerAppID", CHAR * 64),
        ("ProducerAppVersion", CHAR * 64),
        ("UserDef",     CHAR * 64),
        ("dwLevelReference", DWORD), # sample value for 0 dB reference
        ("PostTimer",   TAG_CART_TIMER * 8),
        ("Reserved",    CHAR * 276), 
        ("URL",         CHAR * 1024)
        #TODO char TagText[];
    ]
class TAG_CUE_POINT(ctypes.Structure):
    _fields_ = [
        ("dwName", DWORD),
        ("dwPosition", DWORD),
        ("fccChunk", DWORD),
        ("dwChunkStart", DWORD),
        ("dwBlockStart", DWORD),
        ("dwSampleOffset", DWORD)
    ]
class TAG_CUE(ctypes.Structure):
    _fields_ = [
        ("dwCuePoints", DWORD)
        #TODO TAG_CUE_POINT CuePoints[];
    ]
class TAG_ID3(ctypes.Structure):
    _fields_ = [
        ("id",      CHAR * 3),
        ("title",   CHAR * 30),
        ("artist",  CHAR * 30),
        ("album",   CHAR * 30),
        ("year",    CHAR * 4),
        ("comment", CHAR * 30),
        ("genre",   BYTE)
    ]
class TAG_SMPL_LOOP(ctypes.Structure):
    _fields_ = [
        ("dwIdentifier", DWORD),
        ("dwType", DWORD),
        ("dwStart", DWORD),
        ("dwEnd", DWORD),
        ("dwFraction", DWORD),
        ("dwPlayCount", DWORD)
    ]
class TAG_SMPL(ctypes.Structure):
    _fields_ = [
        ("dwManufacturer", DWORD),
        ("dwProduct", DWORD),
        ("dwSamplePeriod", DWORD),
        ("dwMIDIUnityNote", DWORD),
        ("dwMIDIPitchFraction", DWORD),
        ("dwSMPTEFormat", DWORD),
        ("dwSMPTEOffset", DWORD),
        ("cSampleLoops", DWORD),
        ("cbSamplerData", DWORD)
        #TODO TAG_SMPL_LOOP SampleLoops[]
    ]

# BASS / Effects (DirectX 8)
class BASS_DX8_CHORUS(ctypes.Structure):
    _fields_ = [
        ("fWetDryMix",  FLOAT),
        ("fDepth",      FLOAT),
        ("fFeedback",   FLOAT),
        ("fFrequency",  FLOAT),
        ("lWaveform",   DWORD), # 0=triangle, 1=sine
        ("fDelay",      FLOAT),
        ("lPhase",      DWORD)  # BASS_DX8_PHASE_xxx
    ]
class BASS_DX8_COMPRESSOR(ctypes.Structure):
    _fields_ = [
        ("fGain",       FLOAT),
        ("fAttack",     FLOAT),
        ("fRelease",    FLOAT),
        ("fThreshold",  FLOAT),
        ("fRatio",      FLOAT),
        ("fPredelay",   FLOAT)
    ]
class BASS_DX8_DISTORTION(ctypes.Structure):
    _fields_ = [
        ("fGain",       FLOAT),
        ("fEdge",       FLOAT),
        ("fPostEQCenterFrequency", FLOAT),
        ("fPostEQBandwidth", FLOAT),
        ("fPreLowpassCutoff", FLOAT)
    ]
class BASS_DX8_ECHO(ctypes.Structure):
    _fields_ = [
        ("fWetDryMix",  FLOAT),
        ("fFeedback",   FLOAT),
        ("fLeftDelay",  FLOAT),
        ("fRightDelay", FLOAT),
        ("lPanDelay",   BOOL)
    ]
class BASS_DX8_FLANGER(ctypes.Structure):
    _fields_ = [
        ("fWetDryMix",  FLOAT),
        ("fDepth",      FLOAT),
        ("fFeedback",   FLOAT),
        ("fFrequency",  FLOAT),
        ("lWaveform",   DWORD), # 0=triangle, 1=sine
        ("fDelay",      FLOAT),
        ("lPhase",      DWORD)  # BASS_DX8_PHASE_xxx
    ]
class BASS_DX8_GARGLE(ctypes.Structure):
    _fields_ = [
        ("dwRateHz",    DWORD), # Rate of modulation in hz
        ("dwWaveShape", DWORD)  # 0=triangle, 1=square
    ]
class BASS_DX8_I3DL2REVERB(ctypes.Structure):
    _fields_ = [
        ("lRoom",       INT),       # [-10000, 0]      default: -1000 mB
        ("lRoomHF",     INT),       # [-10000, 0]      default: 0 mB
        ("flRoomRolloffFactor", FLOAT), # [0.0, 10.0]      default: 0.0
        ("flDecayTime", FLOAT),     # [0.1, 20.0]      default: 1.49s
        ("flDecayHFRatio", FLOAT),  # [0.1, 2.0]       default: 0.83
        ("lReflections", INT),      # [-10000, 1000]   default: -2602 mB
        ("flReflectionsDelay", FLOAT),# [0.0, 0.3]       default: 0.007 s
        ("lReverb",     INT),       # [-10000, 2000]   default: 200 mB
        ("flReverbDelay", FLOAT),   # [0.0, 0.1]       default: 0.011 s
        ("flDiffusion", FLOAT),     # [0.0, 100.0]     default: 100.0 %
        ("flDensity",   FLOAT),     # [0.0, 100.0]     default: 100.0 %
        ("flHFReference", FLOAT)    # [20.0, 20000.0]  default: 5000.0 Hz
    ]
class BASS_DX8_PARAMEQ(ctypes.Structure):
    _fields_ = [
        ("fCenter",     FLOAT),
        ("fBandwidth",  FLOAT),
        ("fGain",       FLOAT)
    ]
class BASS_DX8_REVERB(ctypes.Structure):
    _fields_ = [
        ("fInGain",     FLOAT),        # [-96.0,0.0]            default: 0.0 dB
        ("fReverbMix",  FLOAT),     # [-96.0,0.0]            default: 0.0 db
        ("fReverbTime", FLOAT),    # [0.001,3000.0]         default: 1000.0 ms
        ("fHighFreqRTRatio", FLOAT) # [0.001,0.999]          default: 0.001
    ]
class BASS_FX_VOLUME_PARAM(ctypes.Structure):
    _fields_ = [
        ("fTarget",     FLOAT),
        ("fCurrent",    FLOAT),
        ("fTime",       FLOAT), # In seconds
        ("lCurve",      DWORD) # 0 for linear, 1 for logarithmic (BASS_SLIDE_LOG) - check constants
    ]

class WAVEFORMATEX(ctypes.Structure):
    _pack_ = 1 # From #pragma pack(push,1)
    _fields_ = [
        ("wFormatTag", WORD),
        ("nChannels", WORD),
        ("nSamplesPerSec", DWORD),
        ("nAvgBytesPerSec", DWORD),
        ("nBlockAlign", WORD),
        ("wBitsPerSample", WORD),
        ("cbSize", WORD)
    ]
LPWAVEFORMATEX = ctypes.POINTER(WAVEFORMATEX)
#endregion

#region Constants, Flags, Enums

BASS_CONFIG_THREAD          = 0x40000000 # flag: thread-specific setting #TODO is this var using anywhere??

class CommonFlag(IntFlag):
    ASYNCFILE:int              = 0x40000000
    """Read file asyncronosly"""
    UNICODE:int                = 0x80000000
    """String argument is UTF-8 encoded\n\nProbably using only on Windows"""
    NODEVICE = 0x20000
    """`Basson.Channel.device` option, set device to \"no device\""""

class ConfigOption(IntEnum):
    """Options, using in `BASS.GetConfig*()`.\n
    In Basson it already provided as atributes. f.e.:
    ```
    BASS_GetConfig(BASS_CONFIG_HANDLES) == basson.handles
    ```"""
    BUFFER          = 0
    UPDATEPERIOD    = 1
    GVOL_SAMPLE     = 4
    GVOL_STREAM     = 5
    GVOL_MUSIC      = 6
    CURVE_VOL       = 7
    CURVE_PAN       = 8
    FLOATDSP        = 9
    ALGORITHM3D     = 10
    NET_TIMEOUT     = 11
    NET_BUFFER      = 12
    PAUSE_NOPLAY    = 13
    NET_PREBUF      = 15
    NET_PASSIVE     = 18
    REC_BUFFER      = 19
    NET_PLAYLIST    = 21
    MUSIC_VIRTUAL   = 22
    VERIFY          = 23
    UPDATETHREADS   = 24
    DEV_BUFFER      = 27
    REC_LOOPBACK    = 28
    VISTA_TRUEPOS   = 30
    IOS_SESSION     = 34
    IOS_MIXAUDIO    = 34 # Alias for BASS_CONFIG_IOS_SESSION
    DEV_DEFAULT     = 36
    NET_READTIMEOUT = 37
    VISTA_SPEAKERS  = 38
    IOS_SPEAKER     = 39
    MF_DISABLE      = 40
    HANDLES         = 41
    UNICODE         = 42
    SRC             = 43
    SRC_SAMPLE      = 44
    ASYNCFILE_BUFFER = 45
    OGG_PRESCAN     = 47
    MF_VIDEO        = 48
    AIRPLAY         = 49
    DEV_NONSTOP     = 50
    IOS_NOCATEGORY  = 51
    VERIFY_NET      = 52
    DEV_PERIOD      = 53
    FLOAT           = 54
    NET_SEEK        = 56
    AM_DISABLE      = 58
    NET_PLAYLIST_DEPTH = 59
    NET_PREBUF_WAIT = 60
    ANDROID_SESSIONID = 62
    WASAPI_PERSIST  = 65
    REC_WASAPI      = 66
    ANDROID_AAUDIO  = 67
    SAMPLE_ONEHANDLE = 69
    NET_META        = 71
    NET_RESTRATE    = 72
    REC_DEFAULT     = 73
    NORAMP          = 74
    # BASS_SetConfigPtr options
    NET_AGENT       = 16
    NET_PROXY       = 17
    IOS_NOTIFY      = 46
    ANDROID_JAVAVM  = 63
    LIBSSL          = 64
    FILENAME        = 75

class IOSSessionFlag(IntFlag): #TODO porbably drop afterwards
    ''' Flags, using in `basson.ios_session`'''
    MIX        = 1
    '''Allow other apps to be heard at the same time.'''
    DUCK       = 2
    '''Allow other apps to be heard at the same time but reduce their volume level.'''
    AMBIENT    = 4
    '''Use the "ambient" category. '''
    SPEAKER    = 8
    '''Route the output to the speaker instead of the receiver when recording.'''
    DISABLE    = 16
    '''Disable BASS's audio session configuration management so that the app can handle that itself.'''
    DEACTIVATE = 32
    '''Deactivate the audio session when nothing is playing or recording. It is otherwise only deactivated when there are no initialized devices and during interruptions. '''
    AIRPLAY    = 64
    '''Allow playback on Airplay devices when recording (Airplay is always allowed when only playing). '''
    BTHFP      = 128
    '''Allow Bluetooth HFP (hands-free) devices when recording (Bluetooth is always allowed when only playing).'''
    BTA2DP     = 0x100
    '''Allow Bluetooth A2DP devices when recording (Bluetooth is always allowed when only playing).'''

class DeviceFlag(IntFlag):
    ''' Flags ising while `basson.init()` initialization or retrive these flags after'''
    #BITS8           = 1 # unused
    MONO            = 2
    '''Mono output'''
    #DIMENSIONAL     = 4 # unused
    BITS16          = 8
    '''Limit output to 16-bit'''
    REINIT          = 128
    '''Reinitialize the device while retaining the device's existing BASS channels and 3D settings'''
    #LATENCY         = 0x100 # unused
    #CPSPEAKERS      = 0x400 # unused
    SPEAKERS        = 0x800
    '''Force enable 8-channel output'''
    NOSPEAKER       = 0x1000
    '''Ignore speaker arrangement'''
    DMIX            = 0x2000
    '''Use ALSA "dmix" plugin'''
    FREQ            = 0x4000
    '''Set device's samplerate to `samplerate`'''
    STEREO          = 0x8000
    '''Stereo output'''
    HOG             = 0x10000
    """HOG / Exclusive mode"""
    AUDIOTRACK      = 0x20000
    """Use AudioTrack output"""
    DSOUND          = 0x40000
    """Use DirectSound output"""
    SOFTWARE        = 0x80000
    """Disable hardware/fastpath output"""

class D3AlgorithmsOption(IntEnum):
    """Software 3D mixing algorithms options in `basson.d3algorithm`"""
    DEFAULT          = 0
    '''If at least 4 speakers are available then the sound is panned among them'''
    OFF              = 1
    '''Left and right panning on only 2 speakers is used'''
    FULL             = 2
    LIGHT            = 3

# DirectSound interfaces (for use with BASS_GetDSoundObject)
BASS_OBJECT_DS              = 1 # IDirectSound
BASS_OBJECT_DS3DL           = 2 # IDirectSound3DListener

# BASS_DEVICEINFO flags
BASS_DEVICE_ENABLED         = 1
BASS_DEVICE_DEFAULT         = 2
BASS_DEVICE_INIT            = 4
BASS_DEVICE_LOOPBACK        = 8
BASS_DEVICE_DEFAULTCOM      = 128

BASS_DEVICE_TYPE_MASK       = 0xff000000
BASS_DEVICE_TYPE_NETWORK    = 0x01000000
BASS_DEVICE_TYPE_SPEAKERS   = 0x02000000
BASS_DEVICE_TYPE_LINE       = 0x03000000
BASS_DEVICE_TYPE_HEADPHONES = 0x04000000
BASS_DEVICE_TYPE_MICROPHONE = 0x05000000
BASS_DEVICE_TYPE_HEADSET    = 0x06000000
BASS_DEVICE_TYPE_HANDSET    = 0x07000000
BASS_DEVICE_TYPE_DIGITAL    = 0x08000000
BASS_DEVICE_TYPE_SPDIF      = 0x09000000
BASS_DEVICE_TYPE_HDMI       = 0x0a000000
BASS_DEVICE_TYPE_DISPLAYPORT = 0x40000000

# BASS_GetDeviceInfo flags
BASS_DEVICES_AIRPLAY        = 0x1000000

# defines for formats field of BASS_RECORDINFO (from MMSYSTEM.H)
WAVE_FORMAT_1M08            = 0x00000001 # 11.025 kHz, Mono,   8-bit
WAVE_FORMAT_1S08            = 0x00000002 # 11.025 kHz, Stereo, 8-bit
WAVE_FORMAT_1M16            = 0x00000004 # 11.025 kHz, Mono,   16-bit
WAVE_FORMAT_1S16            = 0x00000008 # 11.025 kHz, Stereo, 16-bit
WAVE_FORMAT_2M08            = 0x00000010 # 22.05  kHz, Mono,   8-bit
WAVE_FORMAT_2S08            = 0x00000020 # 22.05  kHz, Stereo, 8-bit
WAVE_FORMAT_2M16            = 0x00000040 # 22.05  kHz, Mono,   16-bit
WAVE_FORMAT_2S16            = 0x00000080 # 22.05  kHz, Stereo, 16-bit
WAVE_FORMAT_4M08            = 0x00000100 # 44.1   kHz, Mono,   8-bit
WAVE_FORMAT_4S08            = 0x00000200 # 44.1   kHz, Stereo, 8-bit
WAVE_FORMAT_4M16            = 0x00000400 # 44.1   kHz, Mono,   16-bit
WAVE_FORMAT_4S16            = 0x00000800 # 44.1   kHz, Stereo, 16-bit

# BASS_SAMPLE flags
class SampleFlag(IntFlag):
    BITS8           = 1 # 8 bit
    FLOAT           = 256 # 32 bit floating-point
    MONO            = 2 # mono
    LOOP            = 4 # looped
    D3              = 8 # 3D functionality
    SOFTWARE        = 16 # unused
    MUTEMAX         = 32 # mute at max distance (3D only)
    VAM             = 64 # unused
    FX              = 128 # unused
    OVER_VOL        = 0x10000 # override lowest volume
    OVER_POS        = 0x20000 # override longest playing
    OVER_DIST       = 0x30000 # override furthest from listener (3D only)

class StreamFlag(IntFlag):
    PRESCAN         = 0x20000 # scan file for accurate seeking and length
    AUTOFREE        = 0x40000 # automatically free the stream when it stops/ends
    RESTRATE        = 0x80000 # restrict the download rate of internet file stream
    BLOCK           = 0x100000 # download internet file stream in small blocks
    DECODE          = 0x200000 # don't play the stream, only decode
    STATUS          = 0x800000 # give server status info (HTTP/ICY tags) in DOWNLOADPROC

BASS_MP3_IGNOREDELAY        = 0x200 # ignore LAME/Xing/VBRI/iTunes delay & padding info
BASS_MP3_SETPOS             = StreamFlag.PRESCAN

class MusicFlag(IntFlag):
    FLOAT            = SampleFlag.FLOAT
    MONO             = SampleFlag.MONO
    LOOP             = SampleFlag.LOOP
    D3               = SampleFlag.D3
    FX               = SampleFlag.FX
    AUTOFREE         = StreamFlag.AUTOFREE
    DECODE           = StreamFlag.DECODE
    PRESCAN          = StreamFlag.PRESCAN # calculate playback length
    CALCLEN          = PRESCAN
    RAMP             = 0x200 # normal ramping
    RAMPS            = 0x400 # sensitive ramping
    SURROUND         = 0x800 # surround sound
    SURROUND2        = 0x1000 # surround sound (mode 2)
    FT2PAN           = 0x2000 # apply FastTracker 2 panning to XM files
    FT2MOD           = 0x2000 # play .MOD as FastTracker 2 does
    PT1MOD           = 0x4000 # play .MOD as ProTracker 1 does
    NONINTER         = 0x10000 # non-interpolated sample mixing
    SINCINTER        = 0x800000 # sinc interpolated sample mixing
    POSRESET         = 0x8000 # stop all notes when moving position
    POSRESETEX       = 0x400000 # stop all notes and reset bmp/etc when moving position
    STOPBACK         = 0x80000 # stop the music on a backwards jump effect
    NOSAMPLE         = 0x100000 # don't load the samples

# Speaker assignment flags
class SpeakerFlag(IntFlag):
    FRONT          = 0x1000000 # front speakers
    REAR           = 0x2000000 # rear speakers
    CENLFE         = 0x3000000 # center & LFE speakers (5.1)
    SIDE           = 0x4000000 # side speakers (7.1)
    LEFT           = 0x10000000 # modifier: left
    RIGHT          = 0x20000000 # modifier: right

    FRONTLEFT      = FRONT  | LEFT
    FRONTRIGHT     = FRONT  | RIGHT
    REARLEFT       = REAR   | LEFT
    REARRIGHT      = REAR   | RIGHT
    CENTER         = CENLFE | LEFT
    LFE            = CENLFE | RIGHT
    SIDELEFT       = SIDE   | LEFT
    SIDERIGHT      = SIDE   | RIGHT
    REAR2          = SIDE
    REAR2LEFT      = SIDELEFT
    REAR2RIGHT     = SIDERIGHT

BASS_RECORD_ECHOCANCEL      = 0x2000
BASS_RECORD_AGC             = 0x4000


# DX7 voice allocation & management flags
BASS_VAM_HARDWARE           = 1
BASS_VAM_SOFTWARE           = 2
BASS_VAM_TERM_TIME          = 4
BASS_VAM_TERM_DIST          = 8
BASS_VAM_TERM_PRIO          = 16

# BASS_CHANNELINFO flags
BASS_ORIGRES_FLOAT          = 0x10000

# BASS_CHANNELINFO types
BASS_CTYPE_SAMPLE           = 1
BASS_CTYPE_RECORD           = 2
BASS_CTYPE_STREAM           = 0x10000
BASS_CTYPE_STREAM_VORBIS    = 0x10002
BASS_CTYPE_STREAM_OGG       = 0x10002
BASS_CTYPE_STREAM_MP1       = 0x10003
BASS_CTYPE_STREAM_MP2       = 0x10004
BASS_CTYPE_STREAM_MP3       = 0x10005
BASS_CTYPE_STREAM_AIFF      = 0x10006
BASS_CTYPE_STREAM_CA        = 0x10007
BASS_CTYPE_STREAM_MF        = 0x10008
BASS_CTYPE_STREAM_AM        = 0x10009
BASS_CTYPE_STREAM_SAMPLE    = 0x1000a
BASS_CTYPE_STREAM_DUMMY     = 0x18000
BASS_CTYPE_STREAM_DEVICE    = 0x18001
BASS_CTYPE_STREAM_WAV       = 0x40000 # WAVE flag (LOWORD=codec)
BASS_CTYPE_STREAM_WAV_PCM   = 0x50001
BASS_CTYPE_STREAM_WAV_FLOAT = 0x50003
BASS_CTYPE_MUSIC_MOD        = 0x20000
BASS_CTYPE_MUSIC_MTM        = 0x20001
BASS_CTYPE_MUSIC_S3M        = 0x20002
BASS_CTYPE_MUSIC_XM         = 0x20003
BASS_CTYPE_MUSIC_IT         = 0x20004
BASS_CTYPE_MUSIC_MO3        = 0x00100 # MO3 flag

# BASS_PluginLoad flags
BASS_PLUGIN_PROC            = 1

# 3D channel modes
BASS_3DMODE_NORMAL          = 0 # normal 3D processing
BASS_3DMODE_RELATIVE        = 1 # position is relative to the listener
BASS_3DMODE_OFF             = 2 # no 3D processing

# BASS_SampleGetChannel flags
BASS_SAMCHAN_NEW            = 1 # get a new playback channel
BASS_SAMCHAN_STREAM         = 2 # create a stream

BASS_STREAMPROC_END         = 0x80000000 # end of user stream flag

# Special STREAMPROCs
STREAMPROC_DUMMY            = 0 # "dummy" stream
STREAMPROC_PUSH             = -1 # push stream
STREAMPROC_DEVICE           = -2 # device mix stream
STREAMPROC_DEVICE_3D        = -3 # device 3D mix stream

# BASS_StreamCreateFileUser file systems
STREAMFILE_NOBUFFER         = 0
STREAMFILE_BUFFER           = 1
STREAMFILE_BUFFERPUSH       = 2

# BASS_StreamPutFileData options
BASS_FILEDATA_END           = 0 # end & close the file

# BASS_StreamGetFilePosition modes
BASS_FILEPOS_CURRENT        = 0
BASS_FILEPOS_DECODE         = BASS_FILEPOS_CURRENT
BASS_FILEPOS_DOWNLOAD       = 1
BASS_FILEPOS_END            = 2
BASS_FILEPOS_START          = 3
BASS_FILEPOS_CONNECTED      = 4
BASS_FILEPOS_BUFFER         = 5
BASS_FILEPOS_SOCKET         = 6
BASS_FILEPOS_ASYNCBUF       = 7
BASS_FILEPOS_SIZE           = 8
BASS_FILEPOS_BUFFERING      = 9
BASS_FILEPOS_AVAILABLE      = 10

# BASS_ChannelSetSync types
BASS_SYNC_POS               = 0
BASS_SYNC_END               = 2
BASS_SYNC_META              = 4
BASS_SYNC_SLIDE             = 5
BASS_SYNC_STALL             = 6
BASS_SYNC_DOWNLOAD          = 7
BASS_SYNC_FREE              = 8
BASS_SYNC_SETPOS            = 11
BASS_SYNC_MUSICPOS          = 10
BASS_SYNC_MUSICINST         = 1
BASS_SYNC_MUSICFX           = 3
BASS_SYNC_OGG_CHANGE        = 12
BASS_SYNC_DEV_FAIL          = 14
BASS_SYNC_DEV_FORMAT        = 15
BASS_SYNC_THREAD            = 0x20000000 # flag: call sync in other thread
BASS_SYNC_MIXTIME           = 0x40000000 # flag: sync at mixtime, else at playtime
BASS_SYNC_ONETIME           = 0x80000000 # flag: sync only once, else continuously

# BASS_ChannelIsActive return values
class ChannelStatus(IntEnum):
    STOPPED         = 0
    PLAYING         = 1
    STALLED         = 2
    PAUSED          = 3
    PAUSED_DEVICE   = 4

# Channel attributes
class ChannelOption(IntEnum):
    FREQ            = 1
    VOL             = 2
    PAN             = 3
    EAXMIX          = 4
    NOBUFFER        = 5
    VBR             = 6 # unused
    CPU             = 7
    SRC             = 8
    NET_RESUME      = 9
    SCANINFO        = 10
    NORAMP          = 11
    BITRATE         = 12
    BUFFER          = 13
    GRANULE         = 14
    USER            = 15       # from BASS 2.4.16
    TAIL            = 16       # from BASS 2.4.16
    PUSH_LIMIT      = 17 # from BASS 2.4.16
    DOWNLOADPROC    = 18 # from BASS 2.4.17
    VOLDSP          = 19     # from BASS 2.4.17
    VOLDSP_PRIORITY = 20 # from BASS 2.4.17
    MUSIC_AMPLIFY   = 0x100
    MUSIC_PANSEP    = 0x101
    MUSIC_PSCALER   = 0x102
    MUSIC_BPM       = 0x103
    MUSIC_SPEED     = 0x104
    MUSIC_VOL_GLOBAL = 0x105
    MUSIC_ACTIVE    = 0x106
    MUSIC_VOL_CHAN  = 0x200 # + channel #
    MUSIC_VOL_INST  = 0x300 # + instrument #

# BASS_ChannelSlideAttribute flags
BASS_SLIDE_LOG              = 0x1000000

# BASS_ChannelGetData flags
class DataLengthOption(IntEnum):
    FFT256            = 0x80000000 # 256 sample FFT
    FFT512            = 0x80000001 # 512 FFT
    FFT1024           = 0x80000002 # 1024 FFT
    FFT2048           = 0x80000003 # 2048 FFT
    FFT4096           = 0x80000004 # 4096 FFT
    FFT8192           = 0x80000005 # 8192 FFT
    FFT16384          = 0x80000006 # 16384 FFT
    FFT32768          = 0x80000007 # 32768 FFT
class DataFlag(IntFlag):
    AVAILABLE         = 0 # query how much data is buffered
    NOREMOVE          = 0x10000000 # flag: don't remove data from recording buffer
    FIXED             = 0x20000000 # unused
    FLOAT             = 0x40000000 # flag: return floating-point sample data
    FFT_INDIVIDUAL    = 0x10 # FFT flag: FFT for each channel, else all combined
    FFT_NOWINDOW      = 0x20 # FFT flag: no Hanning window
    FFT_REMOVEDC      = 0x40 # FFT flag: pre-remove DC bias
    FFT_COMPLEX       = 0x80 # FFT flag: return complex data
    FFT_NYQUIST       = 0x100 # FFT flag: return extra Nyquist value

# BASS_ChannelGetLevelEx flags
BASS_LEVEL_MONO = 1 # get mono level
BASS_LEVEL_STEREO = 2 # get stereo level
BASS_LEVEL_RMS = 4 # get RMS levels
BASS_LEVEL_VOLPAN = 8   # apply VOL/PAN attributes to the levels
BASS_LEVEL_NOREMOVE = 16 # don't remove data from recording buffer

# BASS_ChannelGetTags types : what's returned
BASS_TAG_ID3 = 0 # ID3v1 tags : TAG_ID3 structure
BASS_TAG_ID3V2 = 1 # ID3v2 tags : variable length block
BASS_TAG_OGG = 2 # OGG comments : series of null-terminated UTF-8 strings
BASS_TAG_HTTP = 3 # HTTP headers : series of null-terminated ASCII strings
BASS_TAG_ICY = 4 # ICY headers : series of null-terminated ANSI strings
BASS_TAG_META = 5 # ICY metadata : ANSI string
BASS_TAG_APE = 6 # APE tags : series of null-terminated UTF-8 strings
BASS_TAG_MP4 = 7 # MP4/iTunes metadata : series of null-terminated UTF-8 strings
BASS_TAG_WMA = 8 # WMA tags : series of null-terminated UTF-8 strings
BASS_TAG_VENDOR = 9 # OGG encoder : UTF-8 string
BASS_TAG_LYRICS3 = 10 # Lyric3v2 tag : ASCII string
BASS_TAG_CA_CODEC = 11 # CoreAudio codec info : TAG_CA_CODEC structure
BASS_TAG_MF = 13 # Media Foundation tags : series of null-terminated UTF-8 strings
BASS_TAG_WAVEFORMAT = 14 # WAVE format : WAVEFORMATEEX structure
BASS_TAG_AM_NAME = 16 # Android Media codec name : ASCII string
BASS_TAG_ID3V2_2 = 17 # ID3v2 tags (2nd block) : variable length block
BASS_TAG_AM_MIME = 18 # Android Media MIME type : ASCII string
BASS_TAG_LOCATION = 19 # redirected URL : ASCII string
BASS_TAG_RIFF_INFO = 0x100 # RIFF "INFO" tags : series of null-terminated ANSI strings
BASS_TAG_RIFF_BEXT = 0x101 # RIFF/BWF "bext" tags : TAG_BEXT structure
BASS_TAG_RIFF_CART = 0x102 # RIFF/BWF "cart" tags : TAG_CART structure
BASS_TAG_RIFF_DISP = 0x103 # RIFF "DISP" text tag : ANSI string
BASS_TAG_RIFF_CUE = 0x104 # RIFF "cue " chunk : TAG_CUE structure
BASS_TAG_RIFF_SMPL = 0x105 # RIFF "smpl" chunk : TAG_SMPL structure
BASS_TAG_APE_BINARY = 0x1000 # + index #, binary APE tag : TAG_APE_BINARY structure
BASS_TAG_MUSIC_NAME = 0x10000 # MOD music name : ANSI string
BASS_TAG_MUSIC_MESSAGE = 0x10001 # MOD message : ANSI string
BASS_TAG_MUSIC_ORDERS = 0x10002 # MOD order list : BYTE array of pattern numbers
BASS_TAG_MUSIC_AUTH = 0x10003 # MOD author : UTF-8 string
BASS_TAG_MUSIC_INST = 0x10100 # + instrument #, MOD instrument name : ANSI string
BASS_TAG_MUSIC_CHAN = 0x10200 # + channel #, MOD channel name : ANSI string
BASS_TAG_MUSIC_SAMPLE = 0x10300 # + sample #, MOD sample name : ANSI string

# BASS_ChannelGetLength/GetPosition/SetPosition modes
class PosModeOption(IntEnum):
    BYTE = 0 # byte position
    MUSIC_ORDER = 1 # order.row position, MAKELONG(order,row)
    OGG = 3 # OGG bitstream number
    END = 0x10 # trimmed end position
    LOOP = 0x11 # loop start positiom
    FLUSH = 0x1000000 # flag: flush decoder/FX buffers
    RESET = 0x2000000 # flag: reset user file buffers
    RELATIVE = 0x4000000 # flag: seek relative to the current position
    INEXACT = 0x8000000 # flag: allow seeking to inexact position
    DECODE = 0x10000000 # flag: get the decoding (not playing) position
    DECODETO = 0x20000000 # flag: decode to the position instead of seeking
    SCAN = 0x40000000 # flag: scan to the position

# BASS_RecordSetInput flags
BASS_INPUT_OFF = 0x10000
BASS_INPUT_ON = 0x20000

BASS_INPUT_TYPE_MASK = 0xff000000
BASS_INPUT_TYPE_UNDEF = 0x00000000
BASS_INPUT_TYPE_DIGITAL = 0x01000000
BASS_INPUT_TYPE_LINE = 0x02000000
BASS_INPUT_TYPE_MIC = 0x03000000
BASS_INPUT_TYPE_SYNTH = 0x04000000
BASS_INPUT_TYPE_CD = 0x05000000
BASS_INPUT_TYPE_PHONE = 0x06000000
BASS_INPUT_TYPE_SPEAKER = 0x07000000
BASS_INPUT_TYPE_WAVE = 0x08000000
BASS_INPUT_TYPE_AUX = 0x09000000
BASS_INPUT_TYPE_ANALOG = 0x0a000000

# BASS_ChannelSetFX effect types
BASS_FX_DX8_CHORUS = 0
BASS_FX_DX8_COMPRESSOR = 1
BASS_FX_DX8_DISTORTION = 2
BASS_FX_DX8_ECHO = 3
BASS_FX_DX8_FLANGER = 4
BASS_FX_DX8_GARGLE = 5
BASS_FX_DX8_I3DL2REVERB = 6
BASS_FX_DX8_PARAMEQ = 7
BASS_FX_DX8_REVERB = 8
BASS_FX_VOLUME = 9

# BASS_DX8_PHASE_xxx
BASS_DX8_PHASE_NEG_180 = 0
BASS_DX8_PHASE_NEG_90 = 1
BASS_DX8_PHASE_ZERO = 2
BASS_DX8_PHASE_90 = 3
BASS_DX8_PHASE_180 = 4

# iOS notification types (BASS_CONFIG_IOS_NOTIFY)
BASS_IOSNOTIFY_INTERRUPT = 1 # interruption started
BASS_IOSNOTIFY_INTERRUPT_END = 2 # interruption ended
#endregion

#region Custom headers

# BASS_CONFIG_NET_PLAYLIST
class NetPlaylistOption(IntEnum):
    NEVER = 0
    ONLYSTREAMCREATEURL = 1
    STREAMCREATEFILE = 2

# BASS_CONFIG_NORAMP
class NorampOption(IntEnum):
    ENABLE = 0
    DISABLE = 1
    RAMPINGINOFF = 2
    RAMPINGOUTOFF = 3

# BASS_CONFIG_SCR
class SamplerateConversionOption(IntEnum):
    LINEAR = 0
    POINT8SINC = 1
    POINT16SINC = 2
    POINT32SINC = 3
    POINT64SINC = 4

class StatusOption(IntEnum):
    """Status options of audio device"""
    NOTSTARTED = 0
    ACTIVE = 1
    INACTIVE = 2
    INTERRUPTED = 3 # iOS specific

# BASS.GetInfo.flags
class InfoFlag(IntFlag):
    EMULDRIVER = 0x00000020
    CERTIFIED = 0x00000040
    HARDWARE = 0x80000000

class DXVersionOption(IntEnum):
    DX9 = 9
    DX8 = 8
    DX7 = 7
    DX5 = 5
    NONE = 0

# BASS_RECORDINFO flags (from DSOUND.H)
DSCCAPS_EMULDRIVER          = 0x00000020 # device does not have hardware DirectSound recording support
DSCCAPS_CERTIFIED           = 0x00000040 # device driver has been certified by Microsoft

# Channel.WHOAMI
class ChannelType(IntEnum):
    SAMPLE =    0
    STREAM =    1
    MUSIC =     2
    RECORD =    3

class MusicFreqOption(IntEnum):
    INIT = 0
    '''Specified in `Basson.init()`'''
    DEVICE = 1
    '''Device current output rate'''

class MusicSurroundOption(IntEnum):
    ''' Enable/disabe options for `Music` surround effect'''
    OFF = 0
    MODE1 = 1
    MODE2 = 2

class RecordFlag(IntFlag):
    '''Start recording flags for `Record`'''
    BIT8 = SampleFlag.BITS8
    FLOAT = SampleFlag.FLOAT
    PAUSE = 0x8000 # start recording paused

#endregion

#region Structures

class DeviceInfo(typing.TypedDict):
    ''' Dictionary for using with `Device` and `RecordDevice` properties'''
    name: str
    ''' Description of the device '''
    flags: DeviceFlag
    ''' The device's current status, a combination of flags''' #TODO describe flags
    driver: str 
    ''' Driver identification '''

class Info(typing.TypedDict):
    ''' Dictionary for using with `Info` property'''
    flags: DeviceFlag
    ''' The device's DirectSound capabilities, a combination of flags''' #TODO describe flags
    minbuf: int
    ''' The minimum buffer length (rounded up to the nearest millisecond) to avoid stuttering playback '''
    dsver: DXVersionOption
    '''DirectSound version.\n 
    `9` = DX9/8/7/5 features are available,\n 
    `8` = DX8/7/5 features are available,\n 
    `7` = DX7/5 features are available,\n 
    `5` = DX5 features are available,\n 
    `0` = none of the DX9/8/7/5 features are available'''
    latency: int
    ''' The average delay (rounded up to the nearest millisecond) for channel playback to start and be heard '''
    initflags: DeviceFlag
    ''' The flags parameter of the `Init` call. This will include any flags that were applied automatically'''
    speakers: int
    ''' The number of available speakers, which can be accessed via the speaker assignment flags '''
    freq: int
    ''' The output rate '''

class ChannelInfo(typing.TypedDict):
    ''' Dictionary for using with `ChannelInfo` property'''
    freq:int
    ''' Default samplerate'''
    chans:int
    ''' Number of channels'''

class RecordInfo(typing.TypedDict):
    flags: int #FIXME
    formats: int
    inputs: int
    singlein: bool
    freq: int
#endregion

#region BASS instance
class BASS:
    """ BASS API provider"""
    def __init__(self, dll_path:str = None, safe=True):
        """ Creates a new instance of the BASS library\n
        * On Windows, use `BASS.dll`
        * On MacOS, use `libbass.dylib`
        * On Linux, use `libbass.so`
        
        :param dll_path: Path to the BASS library. If `none` - try to load the library from the system.
        :param safe: If True, wrapper will be raise errors, if BASS returns an error value.
        """

        # Detect OS
        match sys.platform: #TODO iOS and Android
            case 'win32':
                dll_name = 'bass.dll'
                loader = ctypes.WinDLL
            case 'darwin':
                dll_name = 'libbass.dylib'
                loader = ctypes.CDLL
            case 'linux':
                dll_name = 'libbass.so'
                loader = ctypes.CDLL
            case _:
                raise ValueError('Unsupported OS')
        
        # 1. Find dll by checking predefined path
        if dll_path is not None: #NOTE can be not a regular filename
            if pathlib.Path(dll_path).is_dir():
                dll_path = pathlib.Path(dll_path / dll_name)
            if pathlib.Path(dll_path).is_file():
                dll_path = pathlib.Path(dll_path)
            else:
                raise FileNotFoundError(f'{dll_path} not found')
            
        # 2. ENV variable
        if dll_path is None:
            env = os.environ.get('BASSLIB')
            if env is not None:
                dll_path=env

        # 3. Check python.exe folder
        if dll_path is None:
            if pathlib.Path(pathlib.Path(sys.executable).parent / "bass" / dll_name).is_file():
                dll_path = pathlib.Path(pathlib.Path(sys.executable).parent / "bass" / dll_name)

        #TODO 4. in system
        
        # Loading library by ctype
        if dll_path is None: raise FileNotFoundError('BASS library doesn\'t found in system')
        try:
            self.dll = loader(dll_path) # Load library
            self._define_functions()    # Define function
            self.ErrorGetCode()         # Test, if it really BASS 
        except OSError: raise OSError(f"{dll_path} is not BASS library") #WinError 193 #TODO check on other systems #TODO check, if this execption can be raised other way
        except AttributeError: raise OSError(f"{dll_path} is not BASS library") #function BASS_ErrorGetCode is not presented. So, this file isn't BASS

        self.safe = safe
        """ If True, wrapper will be raise errors, if BASS returns an error value"""

    def _define_functions(self):
        """ Defines the functions of the BASS library """

        # BASS / Config
        self.dll.BASS_GetConfig.argtypes = [DWORD]
        self.dll.BASS_GetConfig.restype = DWORD

        self.dll.BASS_GetConfigPtr.argtypes = [DWORD]
        self.dll.BASS_GetConfigPtr.restype = PTR

        self.dll.BASS_SetConfig.argtypes = [DWORD, DWORD]
        self.dll.BASS_SetConfig.restype = BOOL

        self.dll.BASS_SetConfigPtr.argtypes = [DWORD, PTR]
        self.dll.BASS_SetConfigPtr.restype = BOOL

        # BASS / Plugins
        self.dll.BASS_PluginEnable.argtypes = [HPLUGIN, BOOL]
        self.dll.BASS_PluginEnable.restype = BOOL

        self.dll.BASS_PluginFree.argtypes = [HPLUGIN]
        self.dll.BASS_PluginFree.restype = BOOL

        self.dll.BASS_PluginGetInfo.argtypes = [HPLUGIN]
        self.dll.BASS_PluginGetInfo.restype = ctypes.POINTER(BASS_PLUGININFO)

        self.dll.BASS_PluginLoad.argtypes = [CHARP, DWORD]
        self.dll.BASS_PluginLoad.restype = DWORD

        # BASS /  Initialization, info, etc...
        self.dll.BASS_ErrorGetCode.argtypes = []
        self.dll.BASS_ErrorGetCode.restype = INT

        self.dll.BASS_Free.argtypes = []
        self.dll.BASS_Free.restype = BOOL
        
        self.dll.BASS_GetCPU.argtypes = []
        self.dll.BASS_GetCPU.restype = FLOAT

        self.dll.BASS_GetDevice.argtypes = []
        self.dll.BASS_GetDevice.restype = DWORD

        self.dll.BASS_GetDeviceInfo.argtypes = [DWORD, ctypes.POINTER(BASS_DEVICEINFO)]
        self.dll.BASS_GetDeviceInfo.restype = BOOL

        self.dll.BASS_GetInfo.argtypes = [ctypes.POINTER(BASS_INFO)]
        self.dll.BASS_GetInfo.restype = BOOL

        self.dll.BASS_GetVersion.argtypes = []
        self.dll.BASS_GetVersion.restype = DWORD
        
        self.dll.BASS_GetVolume.argtypes = []
        self.dll.BASS_GetVolume.restype = FLOAT

        self.dll.BASS_Init.argtypes = [INT, DWORD, DWORD, PTR, PTR]
        self.dll.BASS_Init.restype = BOOL
        
        self.dll.BASS_IsStarted.argtypes = []
        self.dll.BASS_IsStarted.restype = DWORD

        self.dll.BASS_Pause.argtypes = []
        self.dll.BASS_Pause.restype = BOOL

        self.dll.BASS_SetDevice.argtypes = [DWORD]
        self.dll.BASS_SetDevice.restype = BOOL

        self.dll.BASS_SetVolume.argtypes = [FLOAT]
        self.dll.BASS_SetVolume.restype = BOOL

        self.dll.BASS_Start.argtypes = []
        self.dll.BASS_Start.restype = BOOL

        self.dll.BASS_Stop.argtypes = []
        self.dll.BASS_Stop.restype = BOOL

        self.dll.BASS_Update.argtypes = [DWORD]
        self.dll.BASS_Update.restype = BOOL

        # BASS / 3D
        self.dll.BASS_Apply3D.argtypes = []
        self.dll.BASS_Apply3D.restype = None

        self.dll.BASS_Get3DFactors.argtypes = [ctypes.POINTER(FLOAT), ctypes.POINTER(FLOAT), ctypes.POINTER(FLOAT)]
        self.dll.BASS_Get3DFactors.restype = BOOL

        self.dll.BASS_Get3DPosition.argtypes = [ctypes.POINTER(BASS_3DVECTOR), ctypes.POINTER(BASS_3DVECTOR), ctypes.POINTER(BASS_3DVECTOR), ctypes.POINTER(BASS_3DVECTOR)]
        self.dll.BASS_Get3DPosition.restype = BOOL

        self.dll.BASS_Set3DFactors.argtypes = [FLOAT, FLOAT, FLOAT]
        self.dll.BASS_Set3DFactors.restype = BOOL

        self.dll.BASS_Set3DPosition.argtypes = [ctypes.POINTER(BASS_3DVECTOR), ctypes.POINTER(BASS_3DVECTOR), ctypes.POINTER(BASS_3DVECTOR), ctypes.POINTER(BASS_3DVECTOR)]
        self.dll.BASS_Set3DPosition.restype = BOOL

        # BASS / Samples
        self.dll.BASS_SampleCreate.argtypes = [DWORD, DWORD, DWORD, DWORD, DWORD]
        self.dll.BASS_SampleCreate.restype = HSAMPLE

        self.dll.BASS_SampleFree.argtypes = [HSAMPLE]
        self.dll.BASS_SampleFree.restype = BOOL

        self.dll.BASS_SampleGetChannel.argtypes = [HSAMPLE, DWORD]
        self.dll.BASS_SampleGetChannel.restype = DWORD

        self.dll.BASS_SampleGetChannels.argtypes = [HSAMPLE, HCHANNEL]
        self.dll.BASS_SampleGetChannels.restype = DWORD

        self.dll.BASS_SampleGetData.argtypes = [HSAMPLE, PTR]
        self.dll.BASS_SampleGetData.restype = BOOL

        self.dll.BASS_SampleGetInfo.argtypes = [HSAMPLE, ctypes.POINTER(BASS_SAMPLE)]
        self.dll.BASS_SampleGetInfo.restype = BOOL

        self.dll.BASS_SampleLoad.argtypes = [BOOL, PTR, QWORD, DWORD, DWORD, DWORD]
        self.dll.BASS_SampleLoad.restype = HSAMPLE

        self.dll.BASS_SampleSetData.argtypes = [HSAMPLE, PTR]
        self.dll.BASS_SampleSetData.restype = BOOL

        self.dll.BASS_SampleSetInfo.argtypes = [HSAMPLE, ctypes.POINTER(BASS_SAMPLE)]
        self.dll.BASS_SampleSetInfo.restype = BOOL

        self.dll.BASS_SampleStop.argtypes = [HSAMPLE]
        self.dll.BASS_SampleStop.restype = BOOL

        # BASS / Streams
        self.dll.BASS_StreamCreate.argtypes = [DWORD, DWORD, DWORD, STREAMPROC, PTR]
        self.dll.BASS_StreamCreate.restype = HSTREAM

        self.dll.BASS_StreamCreateFile.argtypes = [BOOL, PTR, QWORD, QWORD, DWORD]
        self.dll.BASS_StreamCreateFile.restype = HSTREAM

        self.dll.BASS_StreamCreateFileUser.argtypes = [DWORD, DWORD, ctypes.POINTER(BASS_FILEPROCS), PTR]
        self.dll.BASS_StreamCreateFileUser.restype = HSTREAM

        self.dll.BASS_StreamCreateURL.argtypes = [CHARP, DWORD, DWORD, ctypes.POINTER(DOWNLOADPROC), PTR]
        self.dll.BASS_StreamCreateURL.restype = HSTREAM

        self.dll.BASS_StreamFree.argtypes = [HSTREAM]
        self.dll.BASS_StreamFree.restype = BOOL

        self.dll.BASS_StreamGetFilePosition.argtypes = [HSTREAM, DWORD]
        self.dll.BASS_StreamGetFilePosition.restype = QWORD

        self.dll.BASS_StreamPutData.argtypes = [HSTREAM, PTR, DWORD]
        self.dll.BASS_StreamPutData.restype = DWORD

        self.dll.BASS_StreamPutFileData.argtypes = [HSTREAM, PTR, DWORD]
        self.dll.BASS_StreamPutFileData.restype = DWORD

        # BASS / MOD/MO3 music
        self.dll.BASS_MusicFree.argtypes = [HMUSIC]
        self.dll.BASS_MusicFree.restype = BOOL

        self.dll.BASS_MusicLoad.argtypes = [BOOL, PTR, QWORD, DWORD, DWORD, DWORD]
        self.dll.BASS_MusicLoad.restype = HMUSIC

        # BASS / Recording
        self.dll.BASS_RecordFree.argtypes = []
        self.dll.BASS_RecordFree.restype = BOOL

        self.dll.BASS_RecordGetDevice.argtypes = []
        self.dll.BASS_RecordGetDevice.restype = DWORD

        self.dll.BASS_RecordGetDeviceInfo.argtypes = [DWORD, ctypes.POINTER(BASS_DEVICEINFO)]
        self.dll.BASS_RecordGetDeviceInfo.restype = BOOL

        self.dll.BASS_RecordGetInfo.argtypes = [ctypes.POINTER(BASS_RECORDINFO)]
        self.dll.BASS_RecordGetInfo.restype = BOOL

        self.dll.BASS_RecordGetInput.argtypes = [INT, ctypes.POINTER(FLOAT)]
        self.dll.BASS_RecordGetInput.restype = DWORD

        self.dll.BASS_RecordGetInputName.argtypes = [INT]
        self.dll.BASS_RecordGetInputName.restype = CHARP

        self.dll.BASS_RecordInit.argtypes = [INT]
        self.dll.BASS_RecordInit.restype = BOOL

        self.dll.BASS_RecordSetDevice.argtypes = [DWORD]
        self.dll.BASS_RecordSetDevice.restype = BOOL

        self.dll.BASS_RecordSetInput.argtypes = [INT, DWORD, FLOAT]
        self.dll.BASS_RecordSetInput.restype = BOOL

        self.dll.BASS_RecordStart.argtypes = [DWORD, DWORD, DWORD, ctypes.POINTER(RECORDPROC), PTR]
        self.dll.BASS_RecordStart.restype = HRECORD

        # BASS / Channels
        self.dll.BASS_ChannelBytes2Seconds.argtypes = [DWORD, QWORD]
        self.dll.BASS_ChannelBytes2Seconds.restype = DOUBLE

        self.dll.BASS_ChannelFlags.argtypes = [DWORD, DWORD, DWORD]
        self.dll.BASS_ChannelFlags.restype = DWORD

        self.dll.BASS_ChannelFree.argtypes = [DWORD]
        self.dll.BASS_ChannelFree.restype = BOOL

        self.dll.BASS_ChannelGet3DAttributes.argtypes = [DWORD, ctypes.POINTER(DWORD), ctypes.POINTER(DWORD), ctypes.POINTER(FLOAT), ctypes.POINTER(FLOAT), ctypes.POINTER(DWORD), ctypes.POINTER(DWORD), ctypes.POINTER(FLOAT)]
        self.dll.BASS_ChannelGet3DAttributes.restype = BOOL

        self.dll.BASS_ChannelGet3DPosition.argtypes = [DWORD, ctypes.POINTER(BASS_3DVECTOR), ctypes.POINTER(BASS_3DVECTOR), ctypes.POINTER(BASS_3DVECTOR)]
        self.dll.BASS_ChannelGet3DPosition.restype = BOOL

        self.dll.BASS_ChannelGetAttribute.argtypes = [DWORD, DWORD, ctypes.POINTER(FLOAT)]
        self.dll.BASS_ChannelGetAttribute.restype = DOUBLE

        self.dll.BASS_ChannelGetAttributeEx.argtypes = [DWORD, DWORD, PTR, DWORD]
        self.dll.BASS_ChannelGetAttributeEx.restype = DOUBLE

        self.dll.BASS_ChannelGetData.argtypes = [DWORD, PTR, DWORD]
        self.dll.BASS_ChannelGetData.restype = DWORD

        self.dll.BASS_ChannelGetDevice.argtypes = [DWORD]
        self.dll.BASS_ChannelGetDevice.restype = DWORD

        self.dll.BASS_ChannelGetInfo.argtypes = [DWORD, ctypes.POINTER(BASS_CHANNELINFO)]
        self.dll.BASS_ChannelGetInfo.restype = BOOL

        self.dll.BASS_ChannelGetLength.argtypes = [DWORD, DWORD]
        self.dll.BASS_ChannelGetLength.restype = QWORD

        self.dll.BASS_ChannelGetLevel.argtypes = [DWORD]
        self.dll.BASS_ChannelGetLevel.restype = DWORD

        self.dll.BASS_ChannelGetLevelEx.argtypes = [DWORD, ctypes.POINTER(FLOAT), FLOAT, DWORD]
        self.dll.BASS_ChannelGetLevelEx.restype = BOOL

        self.dll.BASS_ChannelGetPosition.argtypes = [DWORD, DWORD]
        self.dll.BASS_ChannelGetPosition.restype = QWORD

        self.dll.BASS_ChannelGetTags.argtypes = [DWORD, DWORD]
        self.dll.BASS_ChannelGetTags.restype = CHARP

        self.dll.BASS_ChannelIsActive.argtypes = [DWORD]
        self.dll.BASS_ChannelIsActive.restype = DWORD

        self.dll.BASS_ChannelIsSliding.argtypes = [DWORD, DWORD]
        self.dll.BASS_ChannelIsSliding.restype = BOOL

        self.dll.BASS_ChannelLock.argtypes = [DWORD, BOOL]
        self.dll.BASS_ChannelLock.restype = BOOL

        self.dll.BASS_ChannelPause.argtypes = [DWORD]
        self.dll.BASS_ChannelPause.restype = BOOL

        self.dll.BASS_ChannelPlay.argtypes = [DWORD, BOOL]
        self.dll.BASS_ChannelPlay.restype = BOOL

        self.dll.BASS_ChannelRemoveDSP.argtypes = [DWORD, HDSP]
        self.dll.BASS_ChannelRemoveDSP.restype = BOOL

        self.dll.BASS_ChannelRemoveFX.argtypes = [DWORD, HFX]
        self.dll.BASS_ChannelRemoveFX.restype = BOOL

        self.dll.BASS_ChannelRemoveLink.argtypes = [DWORD, DWORD]
        self.dll.BASS_ChannelRemoveLink.restype = BOOL

        self.dll.BASS_ChannelRemoveSync.argtypes = [DWORD, HSYNC]
        self.dll.BASS_ChannelRemoveSync.restype = BOOL

        self.dll.BASS_ChannelSeconds2Bytes.argtypes = [DWORD, DOUBLE]
        self.dll.BASS_ChannelSeconds2Bytes.restype = QWORD

        self.dll.BASS_ChannelSet3DAttributes.argtypes = [DWORD, INT, FLOAT, FLOAT, INT, INT, FLOAT]
        self.dll.BASS_ChannelSet3DAttributes.restype = BOOL

        self.dll.BASS_ChannelSet3DPosition.argtypes = [DWORD, ctypes.POINTER(BASS_3DVECTOR), ctypes.POINTER(BASS_3DVECTOR), ctypes.POINTER(BASS_3DVECTOR)]
        self.dll.BASS_ChannelSet3DPosition.restype = BOOL

        self.dll.BASS_ChannelSetAttribute.argtypes = [DWORD, DWORD, FLOAT]
        self.dll.BASS_ChannelSetAttribute.restype = BOOL

        self.dll.BASS_ChannelSetAttributeEx.argtypes = [DWORD, DWORD, PTR, DWORD]
        self.dll.BASS_ChannelSetAttributeEx.restype = BOOL

        self.dll.BASS_ChannelSetDevice.argtypes = [DWORD, DWORD]
        self.dll.BASS_ChannelSetDevice.restype = BOOL

        self.dll.BASS_ChannelSetDSP.argtypes = [DWORD, ctypes.POINTER(DSPPROC), PTR, INT]
        self.dll.BASS_ChannelSetDSP.restype = HDSP

        self.dll.BASS_ChannelSetFX.argtypes = [DWORD, DWORD, INT]
        self.dll.BASS_ChannelSetFX.restype = HFX

        self.dll.BASS_ChannelSetLink.argtypes = [DWORD, DWORD]
        self.dll.BASS_ChannelSetLink.restype = BOOL

        self.dll.BASS_ChannelSetPosition.argtypes = [DWORD, QWORD, DWORD]
        self.dll.BASS_ChannelSetPosition.restype = BOOL

        self.dll.BASS_ChannelSetSync.argtypes = [DWORD, DWORD, DWORD, ctypes.POINTER(SYNCPROC), PTR]
        self.dll.BASS_ChannelSetSync.restype = HSYNC

        self.dll.BASS_ChannelSlideAttribute.argtypes = [DWORD, DWORD, FLOAT, DWORD]
        self.dll.BASS_ChannelSlideAttribute.restype = BOOL

        self.dll.BASS_ChannelStart.argtypes = [DWORD]
        self.dll.BASS_ChannelStart.restype = BOOL

        self.dll.BASS_ChannelStop.argtypes = [DWORD]
        self.dll.BASS_ChannelStop.restype = BOOL

        self.dll.BASS_ChannelUpdate.argtypes = [DWORD, DWORD]
        self.dll.BASS_ChannelUpdate.restype = BOOL

        # BASS / Effects
        self.dll.BASS_FXGetParameters.argtypes = [HFX, PTR]
        self.dll.BASS_FXGetParameters.restype = BOOL

        self.dll.BASS_FXReset.argtypes = [DWORD]
        self.dll.BASS_FXReset.restype = BOOL

        self.dll.BASS_FXSetParameters.argtypes = [HFX, PTR]
        self.dll.BASS_FXSetParameters.restype = BOOL

        self.dll.BASS_FXSetPriority.argtypes = [HFX, INT]
        self.dll.BASS_FXSetPriority.restype = BOOL

    def __del__(self):
        try: self.Free()
        except BASSError.Init: pass # BASS_Init never called (err 8), so whatever
        except AttributeError: pass # If failed load a dll. #TODO check, if anything else can raise this exception
        
    #region BASS / Config
    def GetConfig(self, option: DWORD) -> DWORD:
        """ Retrieves the current value of a configuration option.\n
        https://www.un4seen.com/doc/#bass/BASS_GetConfig.html"""
        result = self.dll.BASS_GetConfig(option)
        if self.safe and result == MINUSONE: self._raise_error('BASS_GetConfig')
        return result
    
    def GetConfigPtr(self, option: DWORD) -> PTR:
        """ Retrieves the current value of a configuration option.\n
        https://www.un4seen.com/doc/#bass/BASS_GetConfigPtr.html"""
        result = self.dll.BASS_GetConfigPtr(option)
        if self.safe and result == None: self._raise_error('BASS_GetConfigPtr')
        return result
    
    def SetConfig(self, option: DWORD, value: DWORD) -> BOOL:
        """ Sets the value of a config option.\n
        https://www.un4seen.com/doc/#bass/BASS_SetConfig.html"""
        result = self.dll.BASS_SetConfig(option, value)
        if self.safe and result == 0: self._raise_error('BASS_SetConfig')
        return result

    def SetConfigPtr(self, option: DWORD, value: PTR) -> BOOL:
        """ Sets the value of a config option.\n
        https://www.un4seen.com/doc/#bass/BASS_SetConfigPtr.html"""
        result = self.dll.BASS_SetConfigPtr(option, value)
        if self.safe and result == 0: self._raise_error('BASS_SetConfigPtr')
        return result
    #endregion

    #region BASS / Plugins
    def PluginEnable(self, handle:HPLUGIN, enable:BOOL) -> BOOL:
        """ Enables or disables an add-on\n
        https://www.un4seen.com/doc/#bass/BASS_PluginEnable.html"""
        result = self.dll.BASS_PluginEnable(handle, enable)
        if self.safe and result == 0: self._raise_error('BASS_PluginEnable')
        return result

    def PluginFree(self, handle:HPLUGIN) -> BOOL:
        """ Unplugs an add-on.\n
        https://www.un4seen.com/doc/#bass/BASS_PluginFree.html"""
        result = self.dll.BASS_PluginFree(handle)
        if self.safe and result == 0: self._raise_error('BASS_PluginFree')
        return result

    def PluginGetInfo(self, handle:HPLUGIN) -> BASS_PLUGININFO:
        """ Retrieves information about an add-on.\n
        https://www.un4seen.com/doc/#bass/BASS_PluginGetInfo.html"""
        result = self.dll.BASS_PluginGetInfo(handle)
        if self.safe and result == None: self._raise_error('BASS_PluginGetInfo')
        return result
    
    def PluginLoad(self, file:CHARP, flags:DWORD) -> HPLUGIN:
        """ Plugs an "add-on" into the standard stream and sample creation functions.\n
        https://www.un4seen.com/doc/#bass/BASS_PluginLoad.html"""
        result = self.dll.BASS_PluginLoad(file, flags)
        if self.safe and result == 0: self._raise_error('BASS_PluginLoad')
        return result
    #endregion

    #region BASS / Initialization, info, etc...
    def ErrorGetCode(self) -> INT:
        """ Retrieves the error code for the most recent BASS function call in the current thread.\n
        https://www.un4seen.com/doc/#bass/BASS_ErrorGetCode.html."""
        return self.dll.BASS_ErrorGetCode()

    def Free(self) -> BOOL:
        """ Frees all resources used by the output device, including all its samples, streams and MOD musics\n
        https://www.un4seen.com/doc/#bass/BASS_Free.html"""
        result = self.dll.BASS_Free()
        if self.safe and result == 0: self._raise_error('BASS_Free')
        return result

    def GetCPU(self) -> FLOAT:
        """ Retrieves the current CPU usage of BASS.\n
        https://www.un4seen.com/doc/#bass/BASS_GetCPU.html"""
        result = self.dll.BASS_GetCPU()
        return result

    def GetDevice(self) -> DWORD:
        """ Retrieves the current output device.\n
        https://www.un4seen.com/doc/#bass/BASS_GetDevice.html"""
        result = self.dll.BASS_GetDevice()
        if self.safe and result == MINUSONE: self._raise_error('BASS_GetDevice')
        return result

    def GetDeviceInfo(self, device:DWORD, info: BASS_DEVICEINFO|None) -> BOOL:
        """ Retrieves information on an output device.\n
        https://www.un4seen.com/doc/#bass/BASS_GetDeviceInfo.html"""
        result = self.dll.BASS_GetDeviceInfo(device, ctypes.byref(info))
        if self.safe and result == 0: self._raise_error('BASS_GetDeviceInfo')
        return result

    def GetInfo(self, info:BASS_INFO|None) -> BOOL:
        """ Retrieves information on the device being used.\n
        https://www.un4seen.com/doc/#bass/BASS_GetInfo.html"""
        result = self.dll.BASS_GetInfo(ctypes.byref(info))
        if self.safe and result == 0: self._raise_error('BASS_GetInfo')
        return result

    def GetVersion(self) -> DWORD:
        """ Retrieves the version of BASS that is loaded.\n
        https://www.un4seen.com/doc/#bass/BASS_GetVersion.html"""
        result = self.dll.BASS_GetVersion()
        return result

    def GetVolume(self) -> FLOAT:
        """ Retrieves the current master volume level.\n
        https://www.un4seen.com/doc/#bass/BASS_GetVolume.html"""
        result = self.dll.BASS_GetVolume()
        if self.safe and result == MINUSONE: self._raise_error('BASS_GetVolume')
        return result

    def Init(self, device:INT, freq:DWORD, flags:DWORD, win:INT, clsid:PTR|None=None) -> BOOL:
        """ Initializes an output device.\n
        https://www.un4seen.com/doc/#bass/BASS_Init.html"""
        result = self.dll.BASS_Init(device, freq, flags, win, clsid)
        if self.safe and result == 0: self._raise_error('BASS_Init')
        return result

    def IsStarted(self) -> DWORD:
        """ Checks if the output has been started and is active.\n
        https://www.un4seen.com/doc/#bass/BASS_IsStarted.html"""
        result = self.dll.BASS_IsStarted()
        return result

    def Pause(self) -> BOOL:
        """ Stops the output, pausing all musics/samples/streams on it.\n
        https://www.un4seen.com/doc/#bass/BASS_Pause.html"""
        result = self.dll.BASS_Pause()
        if self.safe and result == FALSE: self._raise_error('BASS_Pause')
        return result

    def SetDevice(self, device:DWORD) -> BOOL:
        """ Sets the device to use for subsequent calls in the current thread.
        https://www.un4seen.com/doc/#bass/BASS_SetDevice.html"""
        result = self.dll.BASS_SetDevice(device)
        if self.safe and result == FALSE: self._raise_error('BASS_SetDevice')
        return result

    def SetVolume(self, volume:FLOAT) -> BOOL:
        """ Sets the output master volume.\n
        https://www.un4seen.com/doc/#bass/BASS_SetVolume.html"""
        result = self.dll.BASS_SetVolume(volume)
        if self.safe and result == 0: self._raise_error('BASS_SetVolume')
        return result

    def Start(self) -> BOOL:
        """ Starts/resumes the output.\n
        https://www.un4seen.com/doc/#bass/BASS_Start.html"""
        result = self.dll.BASS_Start()
        if self.safe and result == 0: self._raise_error('BASS_Start')
        return result

    def Stop(self) -> BOOL:
        """ Stops the output, pausing all musics/samples/streams on it.\n
        https://www.un4seen.com/doc/#bass/BASS_Stop.html"""
        result = self.dll.BASS_Stop()
        if self.safe and result == 0: self._raise_error('BASS_Stop')
        return result

    def Update(self, length:DWORD) -> BOOL:
        """ Updates the `HSTREAM` and `HMUSIC` channel playback buffers.
        https://www.un4seen.com/doc/#bass/BASS_Update.html"""
        result = self.dll.BASS_Update(length)
        if self.safe and result == 0: self._raise_error('BASS_Update')
        return
    #endregion

    #region BASS / 3D
    def Apply3D(self) -> None:
        """ Applies changes made to the 3D system.\n
        https://www.un4seen.com/doc/#bass/BASS_Apply3D.html
        """
        self.dll.BASS_Apply3D()

    def Get3DFactors(self, distf:FLOAT|None=None, rollf:FLOAT|None=None, doppf:FLOAT|None=None) -> BOOL:
        """ Retrieves the factors that affect the calculations of 3D sound.\n
        https://www.un4seen.com/doc/#bass/BASS_Get3DFactors.html"""
        result = self.dll.BASS_Get3DFactors(ctypes.byref(distf), ctypes.byref(rollf), ctypes.byref(doppf))
        if self.safe and result == 0: self._raise_error('BASS_Get3DFactors')
        return result
    
    def Get3DPosition(self, pos:BASS_3DVECTOR|None=None, vel:BASS_3DVECTOR|None=None, front:BASS_3DVECTOR|None=None, top:BASS_3DVECTOR|None=None) -> BOOL:
        """ Retrieves the position, velocity, and orientation of the listener.\n
        https://www.un4seen.com/doc/#bass/BASS_Get3DPosition.html"""
        result = self.dll.BASS_Get3DPosition(ctypes.byref(pos), ctypes.byref(vel), ctypes.byref(front), ctypes.byref(top))
        if self.safe and result == 0: self._raise_error('BASS_Get3DPosition')
        return result
    
    def Set3DFactors(self, distf:FLOAT, rollf:FLOAT, doppf:FLOAT) -> BOOL:
        """ Sets the factors that affect the calculations of 3D sound.\n
        https://www.un4seen.com/doc/#bass/BASS_Set3DFactors.html"""
        result = self.dll.BASS_Set3DFactors(distf, rollf, doppf)
        if self.safe and result == 0: self._raise_error('BASS_Set3DFactors')
        return result

    def Set3DPosition(self, pos:BASS_3DVECTOR|None=None, vel:BASS_3DVECTOR|None=None, front:BASS_3DVECTOR|None=None, top:BASS_3DVECTOR|None=None) -> BOOL:
        """Sets the position, velocity, and orientation of the listener (ie. the player).\n
        https://www.un4seen.com/doc/#bass/BASS_Set3DPosition.html"""
        result = self.dll.BASS_Set3DPosition(ctypes.byref(pos), ctypes.byref(vel), ctypes.byref(front), ctypes.byref(top))
        if self.safe and result == 0: self._raise_error('BASS_Set3DPosition')
        return result
    #endregion

    #region BASS / Samples
    def SampleCreate(self, length:DWORD, freq:DWORD, chans:DWORD, max:DWORD, flags:DWORD) -> HSAMPLE:
        """Creates a new sample.\n
        https://www.un4seen.com/doc/#bass/BASS_SampleCreate.html"""
        result = self.dll.BASS_SampleCreate(length, freq, chans, max, flags)
        if self.safe and result == 0: self._raise_error('BASS_SampleCreate')
        return result
    
    def SampleFree(self, handle:HSAMPLE) -> BOOL:
        """Frees a sample's resources.\n
        https://www.un4seen.com/doc/#bass/BASS_SampleFree.html"""
        result = self.dll.BASS_SampleFree(handle)
        if self.safe and result == 0: self._raise_error('BASS_SampleFree')
        return result
    
    def SampleGetChannel(self, handle:HSAMPLE, flags:DWORD) -> HCHANNEL:
        """Creates a new channel from a sample.\n
        https://www.un4seen.com/doc/#bass/BASS_SampleGetChannel.html"""
        result = self.dll.BASS_SampleGetChannel(handle, flags)
        if self.safe and result == None: self._raise_error('BASS_SampleGetChannel')
        return result
    
    def SampleGetChannels(self, handle:HSAMPLE, channels:HCHANNEL|None) -> DWORD:
        """Retrieves all a sample's existing channels.\n
        https://www.un4seen.com/doc/#bass/BASS_SampleGetChannels.html"""
        result = self.dll.BASS_SampleGetChannels(handle, ctypes.byref(channels))
        if self.safe and result == MINUSONE: self._raise_error('BASS_SampleGetChannels')
        return result
    
    def SampleGetData(self, handle:HSAMPLE, buffer:PTR|None) -> BOOL:
        """Retrieves a copy of a sample's data.\n
        https://www.un4seen.com/doc/#bass/BASS_SampleGetData.html"""
        result = self.dll.BASS_SampleGetData(handle, ctypes.byref(buffer))
        if self.safe and result == 0: self._raise_error('BASS_SampleGetData')
        return result
    
    def SampleGetInfo(self, handle:HSAMPLE, info:BASS_SAMPLE|None) -> BOOL:
        """ Retrieves a sample's default attributes and other information.\n
        https://www.un4seen.com/doc/#bass/BASS_SampleGetInfo.html"""
        result = self.dll.BASS_SampleGetInfo(handle, ctypes.byref(info))
        if self.safe and result == 0: self._raise_error('BASS_SampleGetInfo')
        return result
    
    def SampleLoad(self, mem:BOOL, file:PTR|None, offset:QWORD, length:DWORD, max:DWORD, flags:DWORD) -> HSAMPLE:
        """Loads a WAV, AIFF, MP3, MP2, MP1, OGG or plugin supported sample.\n
        https://www.un4seen.com/doc/#bass/BASS_SampleLoad.html"""
        result = self.dll.BASS_SampleLoad(mem, ctypes.byref(file), offset, length, max, flags)
        if self.safe and result == 0: self._raise_error('BASS_SampleLoad')
        return result
    
    def SampleSetData(self, handle:HSAMPLE, buffer:PTR|None) -> BOOL:
        """ Sets a sample's data.\n
        https://www.un4seen.com/doc/#bass/BASS_SampleSetData.html"""
        result = self.dll.BASS_SampleSetData(handle, ctypes.byref(buffer))
        if self.safe and result == 0: self._raise_error('BASS_SampleSetData')
        return result

    def SampleSetInfo(self, handle:HSAMPLE, info:BASS_SAMPLE|None) -> BOOL:
        """Sets a sample's default attributes.\n
        https://www.un4seen.com/doc/#bass/BASS_SampleSetInfo.html"""
        result = self.dll.BASS_SampleSetInfo(handle, ctypes.byref(info))
        if self.safe and result == 0: self._raise_error('BASS_SampleSetInfo')
        return result

    def SampleStop(self, handle:HSAMPLE) -> BOOL:
        """Stops and frees all of a sample's channels (HCHANNEL).\n
        https://www.un4seen.com/doc/#bass/BASS_SampleStop.html"""
        result = self.dll.BASS_SampleStop(handle)
        if self.safe and result == 0: self._raise_error('BASS_SampleStop')
        return result
    #endregion

    #region BASS / Streams
    def StreamCreate(self, freq:DWORD, chans:DWORD, flags:DWORD, proc:StreamProcType|None, user:PTR|None) -> HSTREAM:
        """Creates a user sample stream.\n
        https://www.un4seen.com/doc/#bass/BASS_StreamCreate.html"""
        c_proc = STREAMPROC(proc)
        result = self.dll.BASS_StreamCreate(freq, chans, flags, c_proc, user)
        if self.safe and result == 0: self._raise_error('BASS_StreamCreate')
        return result
    
    def StreamCreateFile(self, mem:BOOL, file:str, offset:QWORD, length:QWORD, flags:DWORD) -> HSTREAM:
        """Creates a sample stream from an MP3, MP2, MP1, OGG, WAV, AIFF or plugin supported file.\n
        https://www.un4seen.com/doc/#bass/BASS_StreamCreateFile.html"""
        result = self.dll.BASS_StreamCreateFile(mem, file, offset, length, flags)#FIXME locator to buffer
        if self.safe and result == 0: self._raise_error('BASS_StreamCreateFile')
        return result
    
    def StreamCreateFileUser(self, system:DWORD, flags:DWORD, proc:BASS_FILEPROCS|None, user:PTR|None) -> HSTREAM:
        """Creates a user sample stream from a file.\n
        https://www.un4seen.com/doc/#bass/BASS_StreamCreateFileUser.html"""
        result = self.dll.BASS_StreamCreateFileUser(system, flags, ctypes.byref(proc), user)
        if self.safe and result == 0: self._raise_error
        return result
    
    def StreamCreateURL(self, url:PTR, offset:QWORD, flags:DWORD, proc:DownloadProcType|None, user:PTR|None) -> HSTREAM:
        """Creates a sample stream from an MP3, MP2, MP1, OGG, WAV, AIFF or plugin supported file on the internet, optionally receiving the downloaded data in a callback function.\n
        https://www.un4seen.com/doc/#bass/BASS_StreamCreateURL.html"""
        #c_proc = DOWNLOADPROC(proc) if proc != None else None
        result = self.dll.BASS_StreamCreateURL(url, offset, flags, proc, user)
        if self.safe and result == 0: self._raise_error('BASS_StreamCreateURL')
        return result
    
    def StreamFree(self, handle:HSTREAM):
        """Frees a sample stream's resources, including any sync/DSP/FX it has.\n
        https://www.un4seen.com/doc/#bass/BASS_StreamFree.html"""
        result = self.dll.BASS_StreamFree(handle)
        if self.safe and result == 0: self._raise_error('BASS_StreamFree')

    def StreamGetFilePosition(self, handle:HSTREAM, mode:DWORD) -> QWORD:
        """Retrieves the file position/status of a stream.\n
        https://www.un4seen.com/doc/#bass/BASS_StreamGetFilePosition.html"""
        result = self.dll.BASS_StreamGetFilePosition(handle, mode)
        if self.safe and result == MINUSONE: self._raise_error('BASS_StreamGetFilePosition')
        return result

    def StreamPutData(self, handle:HSTREAM, data:PTR|None, length:DWORD) -> DWORD:
        """Adds sample data to a "push" stream.\n
        https://www.un4seen.com/doc/#bass/BASS_StreamPutData.html"""
        result = self.dll.BASS_StreamPutData(handle, ctypes.byref(data), length)
        if self.safe and result == 0: self._raise_error('BASS_StreamPutData')
        return result

    def StreamPutFileData(self, handle:HSTREAM, data:PTR|None, length:DWORD) -> DWORD:
        """Adds data to a "push buffered" user file stream's buffer.\n
        https://www.un4seen.com/doc/#bass/BASS_StreamPutFileData.html"""
        result = self.dll.BASS_StreamPutFileData(handle, ctypes.byref(data), length)
        if self.safe and result == 0: self._raise_error('BASS_StreamPutFileData')
        return result
    #endregion

    #region BASS / MOD/MO3 music
    def MusicFree(self, handle:HMUSIC) -> BOOL:
        """Frees a MOD music's resources, including any sync/DSP/FX it has.\n
        https://www.un4seen.com/doc/#bass/BASS_MusicFree.html"""
        result = self.dll.BASS_MusicFree(handle)
        if self.safe and result == 0: self._raise_error('BASS_MusicFree')
        return result

    def MusicLoad(self, mem:BOOL, file:PTR|None, offset:QWORD, length:DWORD, flags:DWORD, freq:DWORD) -> HMUSIC:
        """Loads a MOD music file.\n
        https://www.un4seen.com/doc/#bass/BASS_MusicLoad.html"""
        result = self.dll.BASS_MusicLoad(mem, file, offset, length, flags, freq)
        if self.safe and result == 0: self._raise_error('BASS_ChannelPlay')
        return result
    #endregion

    #region BASS / Recording
    def RecordFree(self) -> BOOL:
        """Frees all resources used by the recording device.\n
        https://www.un4seen.com/doc/#bass/BASS_RecordFree.html"""
        result = self.dll.BASS_RecordFree()
        if self.safe and result == 0: self._raise_error('BASS_RecordFree')
        return result
    
    def RecordGetDevice(self) -> DWORD:
        """ Retrieves the recording device setting of the current thread.\n
        https://www.un4seen.com/doc/#bass/BASS_RecordGetDevice.html"""
        result = self.dll.BASS_RecordGetDevice()
        if self.safe and result == MINUSONE: self._raise_error('BASS_RecordGeetDevice')
        return result
    
    def RecordGetDeviceInfo(self, device:DWORD, info:BASS_DEVICEINFO|None) -> BOOL:
        """Retrieves information on a recording device.\n
        https://www.un4seen.com/doc/#bass/BASS_RecordGetDeviceInfo.html"""
        result = self.dll.BASS_RecordGetDeviceInfo(device, ctypes.byref(info))
        if self.safe and result == 0: self._raise_error('BASS_RecordGetDeviceInfo')
        return result
    
    def RecordGetInfo(self, info:BASS_RECORDINFO|None) -> BOOL:
        """Retrieves information on the recording device being used.\n
        https://www.un4seen.com/doc/#bass/BASS_RecordGetInfo.html"""
        result = self.dll.BASS_RecordGetInfo(ctypes.byref(info))
        if self.safe and result == 0: self._raise_error('BASS_RecordGetInfo')
        return result

    def RecordGetInput(self, input:INT, volume:FLOAT|None) -> DWORD:
        """Retrieves the current settings of a recording input source.\n
        https://www.un4seen.com/doc/#bass/BASS_RecordGetInput.html"""
        result = self.dll.BASS_RecordGetInput(input, ctypes.byref(volume))
        if self.safe and result == 0: self._raise_error('BASS_RecordGetInput')
        return result
    
    def RecordGetInputName(self, input:INT) -> str:
        """Retrieves the text description of a recording input source.\n
        https://www.un4seen.com/doc/#bass/BASS_RecordGetInputName.html"""
        result = self.dll.BASS_RecordGetInputName(input)
        if self.safe and result == None: self._raise_error('BASS_RecordGetInputName')
        return result
    
    def RecordInit(self, device:INT) -> BOOL:
        """Initializes a recording device.\n
        https://www.un4seen.com/doc/#bass/BASS_RecordInit.html"""
        result = self.dll.BASS_RecordInit(device)
        if self.safe and result == 0: self._raise_error('BASS_RecordInit')
        return result

    def RecordSetDevice(self, device:DWORD) -> BOOL:
        """Sets the recording device to use for subsequent calls in the current thread.\n
        https://www.un4seen.com/doc/#bass/BASS_RecordSetDevice.html"""
        result = self.dll.BASS_RecordSetDevice(device)
        if self.safe and result == 0: self._raise_error('BASS_RecordSetDevice')
        return result

    def RecordSetInput(self, input:INT, flags:DWORD, volume:FLOAT) -> BOOL:
        """Adjusts the settings of a recording input source.\n
        https://www.un4seen.com/doc/#bass/BASS_RecordSetInput.html"""
        result = self.dll.BASS_RecordSetInput(input, flags, volume)
        if self.safe and result == 0: self._raise_error('BASS_RecordSetInput')
        return result
  
    def RecordStart(self, freq:DWORD, chans:DWORD, flags:DWORD, proc:RecordProcType|None, user:PTR|None) -> HRECORD:
        """Starts recording.\n
        https://www.un4seen.com/doc/#bass/BASS_RecordStart.html"""
        c_proc = RECORDPROC(proc) if proc else None
        result = self.dll.BASS_RecordStart(freq, chans, flags, c_proc, user)
        if self.safe and result == 0: self._raise_error('BASS_RecordStart')
        return result
    #endregion

    #region BASS / Channels
    def ChannelBytes2Seconds(self, handle:HANDLE, pos:QWORD) -> DOUBLE:
        """ Translates a byte position into time (seconds), based on a channel's format.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelBytes2Seconds.html"""
        result = self.dll.BASS_ChannelBytes2Seconds(handle, pos)
        if self.safe and result == MINUSONE: self._raise_error('BASS_ChannelBytes2Seconds')
        return result
        
    def ChannelFlags(self, handle:HANDLE, flags:DWORD, mask:DWORD) -> DWORD:
        """Modifies and retrieves a channel's flags.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelFlags.html"""
        result = self.dll.BASS_ChannelFlags(handle, flags, mask)
        if self.safe and result == 0: self._raise_error('BASS_ChannelFlags')
        return result

    def ChannelFree(self, handle:HANDLE) -> BOOL:
        """Frees a channel, including any sync/DSP/FX it has.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelFree.html"""
        result = self.dll.BASS_ChannelFree(handle)
        if self.safe and result == 0: self._raise_error('BASS_ChannelFree')
        return result

    def ChannelGet3DAttributes(self, handle:HANDLE, mode:DWORD|None, min:FLOAT|None, max:FLOAT|None, iangle:DWORD|None, oangle:DWORD|None, outvol:FLOAT|None) -> BOOL:
        """Retrieves the 3D attributes of a sample, stream, or MOD music channel with 3D functionality.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelGet3DAttributes.html"""
        result = self.dll.BASS_ChannelGet3DAttributes(handle, ctypes.byref(mode), ctypes.byref(min), ctypes.byref(max), ctypes.byref(iangle), ctypes.byref(oangle), ctypes.byref(outvol))
        if self.safe and result == 0: self._raise_error('BASS_ChannelGet3DAttributes')
        return result

    def ChannelGet3DPosition(self, handle:HANDLE, pos:BASS_3DVECTOR|None, orient:BASS_3DVECTOR|None, vol:BASS_3DVECTOR|None) -> BOOL:
        """Retrieves the 3D position of a sample, stream, or MOD music channel with 3D functionality.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelGet3DPosition.html"""
        result = self.dll.BASS_ChannelGet3DPosition(handle, ctypes.byref(pos), ctypes.byref(orient), ctypes.byref(vol))
        if self.safe and result == 0: self._raise_error('BASS_ChannelGet3DPosition')
        return result

    def ChannelGetAttribute(self, handle:HANDLE, attrib:DWORD, value:FLOAT) -> BOOL:
        """Retrieves the value of a channel's attribute.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelGetAttribute.html"""
        result = self.dll.BASS_ChannelGetAttribute(handle, attrib, ctypes.byref(value))
        if self.safe and result == 0: self._raise_error('BASS_ChannelGetAttribute')
        return result

    def ChannelGetAttributeEx(self, handle:HANDLE, attrib:DWORD, value:PTR|None, size:DWORD) -> DWORD:
        """Retrieves the value of a channel's attribute.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelGetAttributeEx.html"""
        result = self.dll.BASS_ChannelGetAttributeEx(handle, attrib, ctypes.byref(value), size)
        if self.safe and result == 0: self._raise_error('BASS_ChannelGetAttributeEx')
        return result
    
    def ChannelGetData(self, handle:HANDLE, buffer:PTR|None, lenght:DWORD) -> DWORD:
        """Retrieves the immediate sample data (or an FFT representation of it) of a sample channel, stream, MOD music, or recording channel.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelGetData.html"""
        result = self.dll.BASS_ChannelGetData(handle, ctypes.byref(buffer), lenght)
        if self.safe and result == MINUSONE: self._raise_error('BASS_ChannelGetData')
        return result
    
    def ChannelGetDevice(self, handle:HANDLE) -> DWORD:
        """Retrieves the device that a channel is using.
        https://www.un4seen.com/doc/#bass/BASS_ChannelGetDevice.html"""
        result = self.dll.BASS_ChannelGetDevice(handle)
        if self.safe and result == MINUSONE: self._raise_error('BASS_ChannelGetDevice')
        return result
    
    def ChannelGetInfo(self, handle:HANDLE, info:BASS_CHANNELINFO|None) -> BOOL:
        """Retrieves information on a channel.
        https://www.un4seen.com/doc/#bass/BASS_ChannelGetInfo.html"""
        result = self.dll.BASS_ChannelGetInfo(handle, ctypes.byref(info))
        if self.safe and result == 0: self._raise_error('BASS_ChannelGetInfo')
        return result
    
    def ChannelGetLength(self, handle:HANDLE, mode:DWORD) -> QWORD:
        """Retrieves the length of a channel.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelGetLength.html"""
        result = self.dll.BASS_ChannelGetLength(handle, mode)
        if self.safe and result == MINUSONE: self._raise_error('BASS_ChannelGetLength')
        return result
        
    def ChannelGetLevel(self, handle:HANDLE) -> DWORD:
        """ Retrieves the level (peak amplitude) of a sample, stream, MOD music, or recording channel.
        https://www.un4seen.com/doc/#bass/BASS_ChannelGetLevel.html"""
        result = self.dll.BASS_ChannelGetLevel(handle)
        if self.safe and result == MINUSONE: self._raise_error('BASS_ChannelGetLevel')
        return result

    def ChannelGetLevelEx(self, handle:HANDLE, levels:FLOAT|None, lenght:FLOAT, flags:DWORD) -> BOOL:
        """ Retrieves the level of a sample, stream, MOD music, or recording channel.
        https://www.un4seen.com/doc/#bass/BASS_ChannelGetLevelEx.html"""
        result = self.dll.BASS_ChannelGetLevelEx(handle, ctypes.byref(levels), lenght, flags)
        if self.safe and result == 0: self._raise_error('BASS_ChannelGetLevelEx')
        return result

    def ChannelGetPosition(self, handle:HANDLE, mode:DWORD) -> QWORD:
        """Retrieves the current position of a channel.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelGetPosition.html"""
        result = self.dll.BASS_ChannelGetPosition(handle, mode)
        if self.safe and result == MINUSONE: self._raise_error('BASS_ChannelGetPosition')
        return result

    def ChannelGetTags(self, handle:HANDLE, flags:DWORD) -> str:
        """Retrieves tags/headers from a channel.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelGetTags.html"""
        result = self.dll.BASS_ChannelGetTags(handle, flags)
        if self.safe and result == None: self._raise_error('BASS_ChannelGetTags')
        return result

    def ChannelIsActive(self, handle:HANDLE) -> DWORD:
        """ Checks if a sample, stream, or MOD music is active (playing) or stalled. Can also check if a recording is in progress.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelIsActive.html"""
        result = self.dll.BASS_ChannelIsActive(handle)
        return result

    def ChannelIsSliding(self, handle:HANDLE, attrib:DWORD) -> BOOL:
        """ Checks if an attribute (or any attribute) of a sample, stream, or MOD music is sliding.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelIsSliding.html"""
        result = self.dll.BASS_ChannelIsActive(handle, attrib)
        return result

    def ChannelLock(self, handle:HANDLE, lock:BOOL) -> BOOL:
        """ Locks a stream, MOD music or recording channel to the current thread.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelLock.html"""
        result = self.dll.BASS_ChannelLock(handle, lock)
        if self.safe and result == 0: self._raise_error('BASS_ChannelLock')
        return result

    def ChannelPause(self, handle:HANDLE) -> BOOL:
        """Pauses a sample, stream, MOD music, or recording.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelPause.html"""
        result = self.dll.BASS_ChannelPause(handle)
        if self.safe and result == 0: self._raise_error('BASS_ChannelPause')
        return result

    def ChannelPlay(self, handle:HANDLE, restart:BOOL) -> BOOL:
        """Starts/resumes playback of a sample, stream, MOD music, or a recording.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelPlay.html"""
        result = self.dll.BASS_ChannelPlay(handle, restart)
        if self.safe and result == 0: self._raise_error('BASS_ChannelPlay')
        return result

    def ChannelRemoveDSP(self, handle:HANDLE, dsp:HDSP) -> BOOL:
        """Removes a DSP function from a stream, MOD music, or recording channel.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelRemoveDSP.html"""
        result = self.dll.BASS_ChannelRemoveDSP(handle, dsp)
        if self.safe and result == 0: self._raise_error('BASS_ChannelRemoveDSP')
        return result
        
    def ChannelRemoveFX(self, handle:HANDLE, fx:HFX) -> BOOL:
        """Removes an effect on a stream, MOD music, or recording channel.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelRemoveFX.html"""
        result = self.dll.BASS_ChannelRemoveFX(handle, fx)
        if self.safe and result == 0: self._raise_error('BASS_ChannelRemoveFX')
        return result

    def ChannelRemoveLink(self, handle:HANDLE, chan:HCHANNEL) -> BOOL:
        """Removes a links between two MOD music or stream channels.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelRemoveLink.html"""
        result = self.dll.BASS_ChannelRemoveLink(handle, chan)
        if self.safe and result == 0: self._raise_error('BASS_ChannelRemoveLink')
        return result

    def ChannelRemoveSync(self, handle:HANDLE, sync:HSYNC) -> BOOL:
        """Removes a synchronizer from a MOD music, stream or recording channel.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelRemoveSync.html"""
        result = self.dll.BASS_ChannelRemoveSync(handle, sync)
        if self.safe and result == 0: self._raise_error('BASS_ChannelRemoveSync')
        return result

    def ChannelSeconds2Bytes(self, handle:HANDLE, seconds:float) -> QWORD:
        """Translates a time (seconds) position into bytes, based on a channel's format.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelSeconds2Bytes.html"""
        result = self.dll.BASS_ChannelSeconds2Bytes(handle, seconds)
        if self.safe and result == MINUSONE: self._raise_error('BASS_ChannelSeconds2Bytes')
        return result
    
    def ChannelSet3DAttributes(self, handle:HANDLE, mode:INT, min:FLOAT, max:FLOAT, iangle:INT, oangle:INT, outvol:FLOAT) -> BOOL:
        """Sets the 3D attributes of a sample, stream, or MOD music channel with 3D functionality.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelSet3DAttributes.html"""
        result = self.dll.BASS_ChannelSet3DAttributes(handle, mode, min, max, iangle, oangle, outvol)
        if self.safe and result == 0: self._raise_error('BASS_ChannelSet3DAttributes')
        return result

    def ChannelSet3DPosition(self, handle:HANDLE, pos:BASS_3DVECTOR|None, orient:BASS_3DVECTOR|None, vel:BASS_3DVECTOR|None) -> BOOL:
        """Sets the 3D position of a sample, stream, or MOD music channel with 3D functionality.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelSet3DPosition.html"""
        result = self.dll.BASS_ChannelSet3DPosition(handle, ctypes.byref(pos), ctypes.byref(orient), ctypes.byref(vel))
        if self.safe and result == 0: self._raise_error('BASS_ChannelSet3DPosition')
        return result

    def ChannelSetAttribute(self, handle:HANDLE, attr:INT, value:FLOAT) -> BOOL:
        """Sets the value of a channel's attribute.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelSetAttribute.html"""
        result = self.dll.BASS_ChannelSetAttribute(handle, attr, value)
        if self.safe and result == 0: self._raise_error('BASS_ChannelSetAttribute')
        return result

    def ChannelSetAttributeEx(self, handle:HANDLE, attr:INT, value:FLOAT|None, options:INT) -> BOOL:
        """Sets the value of a channel's attribute.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelSetAttributeEx.html"""
        result = self.dll.BASS_ChannelSetAttribute(handle, attr, ctypes.byref(value), options)
        if self.safe and result == 0: self._raise_error('BASS_ChannelSetAttribute')
        return result

    def ChannelSetDevice(self, handle:HANDLE, device:DWORD) -> BOOL:
        """Changes the device that a stream, MOD music or sample is using.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelSetDevice.html"""
        result = self.dll.BASS_ChannelSetDevice(handle, device)
        if self.safe and result == 0: self._raise_error('BASS_ChannelSetDevice')
        return result
    
    def ChannelSetDSP(self, handle:HANDLE, proc:DSPProcType|None, user:PTR|None, priority:INT) -> BOOL:
        """Sets up a user DSP function on a stream, MOD music, or recording channel.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelSetDSP.html"""
        result = self.dll.BASS_ChannelSetDSP(handle, ctypes.byref(proc), ctypes.byref(user), priority)
        if self.safe and result == 0: self._raise_error('BASS_ChannelSetDSP')
        return result
    
    def ChannelSetFX(self, handle:HANDLE, type:DWORD, priority:INT) -> HFX:
        """Sets an effect on a stream, MOD music, or recording channel.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelSetFX.html"""
        result = self.dll.BASS_ChannelSetFX(handle, type, priority)
        if self.safe and result == 0: self._raise_error('BASS_ChannelSetFX')
        return result

    def ChannelSetLink(self, handle:HANDLE, chan:HANDLE) -> BOOL:
        """Links two MOD music or stream channels together.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelSetLink.html"""
        result = self.dll.BASS_ChannelSetLink(handle, chan)
        if self.safe and result == 0: self._raise_error('BASS_ChannelSetLink')
        return result

    def ChannelSetPosition(self, handle:HANDLE, pos:QWORD, mode:DWORD) -> BOOL:
        """Sets the current position of a channel.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelSetPosition.html"""
        result = self.dll.BASS_ChannelSetPosition(handle, pos, mode)
        if self.safe and result == 0: self._raise_error('BASS_ChannelSetPosition')
        return result
    
    def ChannelSetSync(self, handle:HANDLE, type:DWORD, param:QWORD, proc:SyncProcType|None, user:PTR|None) -> HSYNC:
        """Sets up a synchronizer on a MOD music, stream or recording channel.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelSetSync.html"""
        result = self.dll.BASS_ChannelSetSync(handle, type, param, ctypes.byref(proc), ctypes.byref(user))
        if self.safe and result == 0: self._raise_error('BASS_ChannelSetSync')
        return result
    
    def ChannelSlideAttribute(self, handle:HANDLE, attr:DWORD, value:FLOAT, time:DWORD) -> BOOL:
        """Slides a channel's attribute from its current value to a new value.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelSlideAttribute.html"""
        result = self.dll.BASS_ChannelSlideAttribute(handle, attr, value, time)
        if self.safe and result == 0: self._raise_error('BASS_ChannelSlideAttribute')
        return result
    
    def ChannelStart(self, handle:HANDLE) -> BOOL:
        """Starts/resumes playback of a sample, stream, MOD music, or a recording.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelStart.html"""
        result = self.dll.BASS_ChannelStart(handle)
        if self.safe and result == 0: self._raise_error('BASS_ChannelStart')
        return result
    
    def ChannelStop(self, handle:HANDLE) -> BOOL:
        """Stops a sample, stream, MOD music, or recording.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelStop.html"""
        result = self.dll.BASS_ChannelStop(handle)
        if self.safe and result == 0: self._raise_error('BASS_ChannelStop')
        return result
    
    def ChannelUpdate(self, handle:HANDLE, length:DWORD) -> BOOL:
        """Updates the playback buffer of a stream or MOD music.\n
        https://www.un4seen.com/doc/#bass/BASS_ChannelUpdate.html"""
        result = self.dll.BASS_ChannelUpdate(handle, length)
        if self.safe and result == 0: self._raise_error('BASS_ChannelUpdate')
        return result
    #endregion

    #region BASS / Effects
    def FXGetParameters(self, handle:HFX, params:PTR|None) -> BOOL:
        """Retrieves the parameters of an effect.\n
        https://www.un4seen.com/doc/#bass/BASS_FXGetParameters.html"""
        result = self.dll.BASS_FXGetParameters(handle, ctypes.byref(params))
        if self.safe and result == 0: self._raise_error('BASS_FXGetParameters')
        return result

    def FXReset(self, handle:HANDLE) -> BOOL:
        """Resets the state of an effect or all effects on a channel.\n
        https://www.un4seen.com/doc/#bass/BASS_FXReset.html"""
        result = self.dll.BASS_FXReset(handle)
        if self.safe and result == 0: self._raise_error('BASS_FXReset')
        return result
    
    def FXSetParameters(self, handle:HFX, params:PTR|None) -> BOOL:
        """Sets the parameters of an effect.\n
        https://www.un4seen.com/doc/#bass/BASS_FXSetParameters.html"""
        result = self.dll.BASS_FXSetParameters(handle, ctypes.byref(params))
        if self.safe and result == 0: self._raise_error('BASS_FXSetParameters')
        return result

    def FXSetPriority(self, handle:HFX, priority:INT) -> BOOL:
        """Sets the priority of an effect or DSP function, which determines its position in the DSP chain.\n
        https://www.un4seen.com/doc/#bass/BASS_FXSetPriority.html"""
        result = self.dll.BASS_FXSetPriority(handle, priority)
        if self.safe and result == 0: self._raise_error('BASS_FXSetPriority')
        return result
#endregion

#region BASSError exception
    def _raise_error(self, name):
        """ Raises a BASSError if fucntion returns "failed" value """
        match self.ErrorGetCode():
            case 0 : raise BASSError.OK       (BASSError.OK.__doc__)
            case 1 : raise BASSError.Mem      (BASSError.Mem.__doc__)
            case 2 : raise BASSError.Fileopen (BASSError.Fileopen.__doc__)
            case 3 : raise BASSError.Driver   (BASSError.Driver.__doc__)
            case 4 : raise BASSError.BufLost  (BASSError.BufLost.__doc__)
            case 5 : raise BASSError.Handle   (BASSError.Handle.__doc__)
            case 6 : raise BASSError.Format   (BASSError.Format.__doc__)
            case 7 : raise BASSError.Position (BASSError.Position.__doc__)
            case 8 : raise BASSError.Init     (BASSError.Init.__doc__)
            case 9 : raise BASSError.Start    (BASSError.Start.__doc__)
            case 10: raise BASSError.Ssl      (BASSError.Ssl.__doc__)
            case 11: raise BASSError.Reinit   (BASSError.Reinit.__doc__)
            case 14: raise BASSError.Already  (BASSError.Already.__doc__)
            case 17: raise BASSError.Notaudio (BASSError.Notaudio.__doc__)
            case 18: raise BASSError.Nochan   (BASSError.Nochan.__doc__)
            case 19: raise BASSError.Illtype  (BASSError.Illtype.__doc__)
            case 20: raise BASSError.Illparam (BASSError.Illparam.__doc__)
            case 21: raise BASSError.No3D     (BASSError.No3D.__doc__)
            case 22: raise BASSError.NoEAX    (BASSError.NoEAX.__doc__)
            case 23: raise BASSError.Device   (BASSError.Device.__doc__)
            case 24: raise BASSError.Noplay   (BASSError.Noplay.__doc__)
            case 25: raise BASSError.Freq     (BASSError.Freq.__doc__)
            case 27: raise BASSError.Notfile  (BASSError.Notfile.__doc__)
            case 29: raise BASSError.NoHW     (BASSError.NoHW.__doc__)
            case 31: raise BASSError.Empty    (BASSError.Empty.__doc__)
            case 32: raise BASSError.NoNet    (BASSError.NoNet.__doc__)
            case 33: raise BASSError.Create   (BASSError.Create.__doc__)
            case 34: raise BASSError.NoFX     (BASSError.NoFX.__doc__)
            case 37: raise BASSError.NotAvail (BASSError.NotAvail.__doc__)
            case 38: raise BASSError.Decode   (BASSError.Decode.__doc__)
            case 39: raise BASSError.DX       (BASSError.DX.__doc__)
            case 40: raise BASSError.Timeout  (BASSError.Timeout.__doc__)
            case 41: raise BASSError.Fileform (BASSError.Fileform.__doc__)
            case 42: raise BASSError.Speaker  (BASSError.Speaker.__doc__)
            case 43: raise BASSError.Version  (BASSError.Version.__doc__)
            case 44: raise BASSError.Codec    (BASSError.Codec.__doc__)
            case 45: raise BASSError.Ended    (BASSError.Ended.__doc__)
            case 46: raise BASSError.Busy     (BASSError.Busy.__doc__)
            case 47: raise BASSError.Unstreamable (BASSError.Unstreamable.__doc__)
            case 48: raise BASSError.Protocol (BASSError.Protocol.__doc__)
            case 49: raise BASSError.Denied   (BASSError.Denied.__doc__)
            #case MINUSONE: BASSError.Unknown (BASSError.Unknown.__doc__)
            case _: raise BASSError.Unknown (BASSError.Unknown.__doc__)
            
class BASSError(Exception):
    '''
    Class contain all BASS exceptions
    '''

    class OK        (Exception):
        """All is OK"""
    class Mem       (Exception):
        """Memory error"""
    class Fileopen  (Exception):
        """Cannot open the file"""
    class Driver    (Exception):
        """Cannot find a free or valid driver"""

    class BufLost   (Exception):
        """Sample buffer was lost"""
    class Handle    (Exception):
        """Invalid handle"""
    class Format    (Exception):
        """Unsupported sample format"""
    class Position  (Exception):
        """Invalid position"""

    class Init      (Exception):
        """`init` call was being failed"""
    class Start     (Exception):
        """`start` call was being failed"""
    class Ssl       (Exception):
        """SSL/HTTPS support isn't avaliable"""
    class Reinit    (Exception):
        """Device reqied to be reinitialized"""

    class Already   (Exception):
        """Last action already done (`init`, `pause`, etc.)"""
    class Notaudio  (Exception):
        """File doesn't contain audio"""
    class Nochan    (Exception):
        """Cannot get a free channel"""
    class Illtype   (Exception):
        """Illegal type specified"""

    class Illparam  (Exception):
        """Illegal parameter specified"""
    class No3D      (Exception):
        """Driver don't have 3D support"""
    class NoEAX     (Exception):
        """Driver don't have EAX support"""
    class Device    (Exception):
        """Illegal device number"""

    class Noplay    (Exception):
        """Channel not playing"""
    class Freq      (Exception):
        """Illegal samplerate"""
    class Notfile   (Exception):
        """The stream is not a file stream"""
    class NoHW      (Exception):
        """No hardware voices avaliable"""

    class Empty     (Exception):
        """File don't have sample data"""
    class NoNet     (Exception):
        """Internet connection couldn't be opened"""
    class Create    (Exception):
        """File couldn't be created"""
    class NoFX      (Exception):
        """FX is not avaliable"""

    class NotAvail  (Exception):
        """Requested data or action is not avaliable"""
    class Decode    (Exception):
        """Channel is/isn't a decoding channel"""
    class DX        (Exception):
        """Reqested DirectX version don't installed"""
    class Timeout   (Exception):
        """Connection timeout"""

    class Fileform  (Exception):
        """Unsupported file format"""
    class Speaker   (Exception):
        """Unavaliable speaker"""
    class Version   (Exception):
        """Unsupported BASS version (used by plugins)"""
    class Codec     (Exception):
        """Codec is not avaliable or supported"""

    class Ended     (Exception):
        """File has been reached end"""
    class Busy      (Exception):
        """Device is busy"""
    class Unstreamable (Exception):
        """File is unstremable"""
    class Protocol  (Exception):
        """Unsopported protocol"""

    class Denied    (Exception):
        """Access denied"""
    class Unknown   (Exception):
        """Some other mystery problem"""

#endregion