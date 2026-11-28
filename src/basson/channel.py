from __future__ import annotations

from .basson import Basson
from .api import *

class Channel():
    def __init__(self, bass:Basson=None, handle:int=None):
        
        if 0: #HACK Just for doctrings
            self.bass = bass.bass
            ''' Current BASS library'''
            self.HANDLE = handle
            ''' Contain handle of current channel. Uses for any interaction with channel '''
            self.WHOAMI:ChannelType = None
            ''' Tells that a object is '''
        self._links = []
        ''' List of channels that are linked to this channel'''


    def __del__(self):
        self.bass.ChannelFree(self.HANDLE)

    def bytes2seconds(self, bytes:int) -> float:
        ''' Converts bytes to seconds'''
        return self.bass.ChannelBytes2Seconds(self.HANDLE, bytes)
    def seconds2bytes(self, seconds:float):
        ''' Converts seconds to bytes'''
        return self.bass.ChannelSeconds2Bytes(self.HANDLE, seconds)

#region Core functions
    @property
    def device(self) -> int:
        ''' Number of system device, in usage by this channel

        :param device: Device to use\n
            * `0` - no sound
            * `1...` - audio device   
            * `CommonFlag.NODEVICE` - no device
        :raise BASSError.Device: `device` is invalid
        :raise BASSError.Init: Requested device has not been initialized
        :raise BASSError.NotAvail: Only decoding channels are allowed to use the `CommonFlag.NODEVICE` option
        '''
        return self.bass.ChannelGetDevice(self.HANDLE)
    @device.setter
    def device(self, device:int):
        self.bass.ChannelSetDevice(self.HANDLE, device)

    def length_get(self, mode:PosModeOption=PosModeOption.BYTE) -> int|None:
        ''' Returns length of channel    
        Notes:
            If `.WHOAMI is 'Music'` and in `Music` initilization don't setted `basson.MusicFlag.PRESCAN` flag, will be return `None`
        :param mode: Mode of length
        :return: Length of channel
        '''
        var = self.bass.ChannelGetLength(self.HANDLE, mode)
        return var if var != QMINUSONE else None

    @property
    def length(self) -> int | None:
        '''Length of channel\n
        Same as `.length_get(basson.PosModeOption.BYTE)'''
        return self.length_get(PosModeOption.BYTE)

    def position_get(self, mode:PosModeOption|MusicFlag=PosModeOption.BYTE) -> int:
        ''' Returns position of channel
        :param mode: Mode of position
        '''
        return self.bass.ChannelGetPosition(self.HANDLE, mode)
    def position_set(self, value:int, mode:PosModeOption|MusicFlag):
        ''' Sets position of channel, and some flags
        :param value: Position of channel
        :param mode: Mode of position
        '''
        self.bass.ChannelSetPosition(self.HANDLE, value, mode)

    @property
    def position(self) -> int:
        ''' Position of channel in bytes\n
        Same as `.position_get/set(basson.PosModeOption.BYTE)`
        ''' 
        return self.bass.ChannelGetPosition(self.HANDLE, PosModeOption.BYTE)
    @position.setter
    def position(self, value:int):
        self.bass.ChannelSetPosition(self.HANDLE, value, PosModeOption.BYTE) 

    @property
    def status(self) -> ChannelStatus:
        ''' Checks if a sample, stream, or MOD music is active (playing) or stalled. Can also check if a recording is in progress. '''
        return self.bass.ChannelIsActive(self.HANDLE)

    def lock(self, lock:bool):
        ''' Locks a channel '''
        self.bass.ChannelLock(self.HANDLE, lock)

    def play(self, restart: bool = False):
        ''' Starts/resumes playback of channel. Same as `start`, but have option start from begining
        :param restart: Start playback from begin
        '''
        try:
            self.bass.ChannelPlay(self.HANDLE, restart)
        except BASSError.Start:
                self.start()        
            
    def pause(self):
        ''' Pauses playback/recording of channel'''
        self.bass.ChannelPause(self.HANDLE)

    def stop(self):
        ''' Stops playback/recording of channel'''
        self.bass.ChannelStop(self.HANDLE)   

    def start(self):
        ''' Starts/resumes playback/recording of channel'''
        self.bass.ChannelStart(self.HANDLE)

    def link_set(self, channel:Channel):
        ''' Links a channel to another channel'''
        self.bass.ChannelSetLink(self.HANDLE, channel.HANDLE)
        if channel not in self._links:
            self._links.append(channel.HANDLE)
            channel._links.append(self.HANDLE)
        else:
            pass

    def link_remove(self, channel:Channel):
        ''' Removes link a channel from another channel'''
        self.bass.ChannelRemoveLink(self.HANDLE, channel.HANDLE)
        if channel in self._links:
            self._links.remove(channel.HANDLE)
            channel._links.remove(self.HANDLE)
        else:
            pass

    # set/removeDSP
    # set/removeFX
    # set/removeLink
    # set/removeSync
    # get3dattributes
    # get3dposition
    # IsSliding
    # SlideAtrribute
    # level (LevelEx)

    #def get_data(self, buffer:bytearray, length:DataLengthOption|DataFlag|int):
    #    ''' Retrieves the immediate sample data (or an FFT representation of it) of a sample channel, stream, MOD music, or recording channel.'''
    #    c_buffer = buffer
    #    self.bass.ChannelGetData(self.HANDLE, c_buffer, length)
    #    return c_buffer
    
# endregion

# region ChannelGetAttibute(ex)
    def _getconf(self, option):
        value = FLOAT()
        self.bass.ChannelGetAttribute(self.HANDLE, option, value)
        return value.value
    def _setconf(self, option, value):
        self.bass.ChannelSetAttribute(self.HANDLE, option, value)

    #def _getconfex(self, option):
    #    value = FLOAT()
    #    self.bass.ChannelGetAttributeEx(self.HANDLE, option, value)
    #    return value.value
    #def _setconfex(self, option, value):
    #    self.bass.ChannelSetAttributeEx(self.HANDLE, option, value)

    @property
    def bitrate(self) -> float:
        ''' The average bitrate of a file stream. '''
        return self._getconf(ChannelOption.BITRATE)

    @property
    def buffer(self) -> float:
        ''' The playback buffering length in seconds.\n
        `0` = no buffering. This is automatically capped to the full length of the channel's playback buffer
        '''
        return self._getconf(ChannelOption.BUFFER)
    @buffer.setter
    def buffer(self, value:float):
        self._setconf(ChannelOption.BUFFER, value)

    @property
    def cpu_usage(self) -> float:
        ''' The CPU usage of a channel in %'''
        return self._getconf(ChannelOption.CPU)

    @property
    def frequency(self) -> float:
        ''' The sample rate of a channel\n
        `0` - original rate'''
        return self._getconf(ChannelOption.FREQ)
    @frequency.setter
    def frequency(self, value:float):
        self._setconf(ChannelOption.FREQ, value)

    @property
    def granule(self) -> float:
        ''' The processing granularity of a channel '''
        try:
            return self._getconf(ChannelOption.GRANULE)
        except BASSError.OK:
            return None
    @granule.setter
    def granule(self, value:float):
        self._setconf( ChannelOption.GRANULE, value)
        
    @property
    def music_active(self) -> int:
        ''' The number of active channels in a MOD music '''
        #HACK If music is stoped / not played yet it can raise error
        try:
            return int(self._getconf(ChannelOption.MUSIC_ACTIVE))
        except BASSError.OK:
            return 0
        
    @property
    def music_amplify(self) -> int:
        ''' The amplification level of a MOD music '''
        return int(self._getconf(ChannelOption.MUSIC_AMPLIFY))
    @music_amplify.setter
    def music_amplify(self, value:int):
        self._setconf(ChannelOption.MUSIC_AMPLIFY, value)

    @property
    def music_bpm(self) -> int:
        ''' The BPM of a MOD music '''
        return int(self._getconf(ChannelOption.MUSIC_BPM))
    @music_bpm.setter
    def music_bpm(self, value:int):
        self._setconf(ChannelOption.MUSIC_BPM, value)
    
    @property
    def music_pansep(self) -> int:
        ''' The pan separation of a MOD music '''
        return int(self._getconf(ChannelOption.MUSIC_PANSEP))
    @music_pansep.setter
    def music_pansep(self, value:int):
        self._setconf(ChannelOption.MUSIC_PANSEP, value)
    
    @property
    def music_position_scaler(self) -> int:
        ''' The position scaler of a MOD music '''
        return int(self._getconf(ChannelOption.MUSIC_PSCALER))
    @music_position_scaler.setter
    def music_position_scaler(self, value:int):
        self._setconf(ChannelOption.MUSIC_PSCALER, value)
    
    @property
    def music_speed(self) -> int:
        ''' The speed of a MOD music '''
        return int(self._getconf(ChannelOption.MUSIC_SPEED))
    @music_speed.setter
    def music_speed(self, value:int):
        self._setconf(ChannelOption.MUSIC_SPEED, value)
    
    @property
    def music_volume_channel(self, channel:int) -> float:
        ''' The volume of a certain channel in MOD music\n
        :param channel: Number of channel, where `0` - first channel
        :param volume: Volume level'''
        return self._getconf(ChannelOption.MUSIC_VOL_CHAN + channel)
    @music_volume_channel.setter
    def music_volume_channel(self, channel:int, volume:float):
        self._setconf(ChannelOption.MUSIC_VOL_CHAN + channel, volume)
    
    @property
    def music_volume(self) -> int:
        ''' The global volume of a MOD music '''
        return int(self._getconf(ChannelOption.MUSIC_VOL_GLOBAL))
    @music_volume.setter
    def music_volume(self, value:int):
        self._setconf(ChannelOption.MUSIC_VOL_GLOBAL, value)

    @property
    def music_volume_instrument(self, instrument:int) -> float:
        '''Volume level of instrument of a MOD music\n
        :param instument: Number of instrument, where `0` - first instrument
        :param value: Volume level'''
        return self._getconf(ChannelOption.MUSIC_VOL_INST + instrument)
    @music_volume_instrument.setter
    def music_volume_instrument(self, instrument:int, volume:float):
        self._selfconf(ChannelOption.MUSIC_VOL_INST+instrument, volume)

    @property
    def net_resume(self) -> float:
        ''' The download buffer level required to resume stalled playback, in % '''
        return self._getconf(ChannelOption.NET_RESUME)
    @net_resume.setter
    def net_resume(self, value:float):
        self._setconf(ChannelOption.NET_RESUME, value)
    
    @property
    def noramp(self) -> NorampOption:
        ''' Enable or disable playback ramping '''
        #HACK On some reason for `noramp` and `pan`, if we don't touched yet, BASS_ChannelGetAttribute will return False 
        #   but BASS_ErrorGetCode says OK. So need to exclude raising exception in this situation
        try:
            return int(self._getconf(ChannelOption.NORAMP))
        except BASSError.OK :
            return NorampOption.ENABLE # default value
    @noramp.setter
    def noramp(self, value:NorampOption):
        self._setconf(ChannelOption.NORAMP, value)
    
    @property
    def pan(self) -> float:
        ''' The panning position of a channel '''
        #HACK look at `noramp` comment
        try:
            return self._getconf( ChannelOption.PAN)
        except BASSError.OK:
            return 0.0 # default value
    @pan.setter
    def pan(self, value:float):
        self._setconf(ChannelOption.PAN, value)

    @property
    def push_limit(self) -> int:
        ''' The maximum amount of data that a push stream can have queued '''
        return int(self._getconf(ChannelOption.PUSH_LIMIT))
    @push_limit.setter
    def push_limit(self, value:int):
        self._setconf(ChannelOption.PUSH_LIMIT, value)
    
    @property
    def src(self) -> SamplerateConversionOption:
        ''' The sample rate conversion quality of a channel '''
        return int(self._getconf(ChannelOption.SRC))
    @src.setter
    def src(self, value:SamplerateConversionOption):
        self._setconf(ChannelOption.SRC, value)
    
    @property
    def tail(self) -> float:
        ''' An amount of time to add to the length of a channel '''
        return self._getconf(ChannelOption.TAIL)
    @tail.setter
    def tail(self, value:float):
        self._setconf(ChannelOption.TAIL, value)

    @property
    def volume(self) -> float:
        ''' Volume of channel '''
        return self._getconf( ChannelOption.VOL)
    @volume.setter
    def volume(self, value:float):
        self._setconf( ChannelOption.VOL, value)

    @property
    def dsp_volume(self) -> float:
        ''' The volume level applied in the DSP chain of a channel '''
        return self._getconf( ChannelOption.VOLDSP)
    @dsp_volume.setter
    def dsp_volume(self, value:float):
        self._setconf( ChannelOption.VOLDSP, value)

    @property
    def dsp_volume_priority(self) -> int:
        ''' The priority of the volume DSP '''
        return int(self._getconf(ChannelOption.VOLDSP_PRIORITY))
    @dsp_volume_priority.setter
    def dsp_volume_priority(self, value:int):
        self._setconf(ChannelOption.VOLDSP_PRIORITY, value)

    # atrribute DownloadCallback #TODO поскольку работаем в python и мы будем сами писать эти callback, то вызов атрибута скорее всего не понадобится
    # atribute scaninfo
    # atribute user

#endregion

#region ChannelFlags

    def _getflag(self, flag:int) -> bool:
        return bool(self.bass.ChannelFlags(self.HANDLE, 0, 0) & flag)
    def _setflags(self, flag:int, value:bool):
        self.bass.ChannelFlags(self.HANDLE, flag if value else 0, flag)

    @property
    def loop(self) -> bool:
        ''' Loop the channel\n
        Cannot be affected at `Music`, if it loops itself'''
        return self._getflag(SampleFlag.LOOP)
    @loop.setter
    def loop(self, value:bool):
        self._setflags(SampleFlag.LOOP, value)

    @property
    def mutemax(self) -> bool:
        ''' Mute the channel when it is at/beyond its max distance '''
        return self._getflag(SampleFlag.MUTEMAX)
    @mutemax.setter
    def mutemax(self, value:bool):
        self._setflags(SampleFlag.MUTEMAX, value)

    # It propabaly can make alot of problems afterwards
    #@property
    #def autofree(self) -> bool:
    #    ''' Free the channel when playback ends '''
    #    # Flag value is same for `Music` and `Stream`
    #    return self._getflag(StreamFlag.AUTOFREE)
    #@autofree.setter
    #def autofree(self, value:bool):
    #    self._setflags(StreamFlag.AUTOFREE, value)

    @property
    def restrict_rate(self) -> bool:
        ''' Restrict the download rate '''
        return self._getflag(StreamFlag.RESTRATE)
    @restrict_rate.setter
    def restrict_rate(self, value:bool):
        self._setflags(StreamFlag.RESTRATE, value)

    @property
    def noninter(self) -> bool:
        ''' Use non-interpolated sample mixing '''
        return self._getflag(MusicFlag.NONINTER)
    @noninter.setter
    def noninter(self, value:bool):
        self._setflags(MusicFlag.NONINTER, value)

    @property
    def sincinter(self) -> bool:
        ''' Use sinc interpolation '''
        return self._getflag(MusicFlag.SINCINTER)
    @sincinter.setter
    def sincinter(self, value:bool):
        self._setflags(MusicFlag.SINCINTER, value)

    @property
    def ramp(self) -> bool:
        ''' Use "normal" ramping '''
        return self._getflag(MusicFlag.RAMP)
    @ramp.setter
    def ramp(self, value:bool):
        self._setflags(MusicFlag.RAMP, value)

    @property
    def ramps(self) -> bool:
        ''' Use "sensetive" ramping '''
        return self._getflag(MusicFlag.RAMPS)
    @ramps.setter
    def ramps(self, value:bool):
        self._setflags(MusicFlag.RAMPS, value)

    @property
    def surround(self) -> MusicSurroundOption:
        ''' Use surround sound '''
        mode1 = self._getflag(MusicFlag.SURROUND)
        mode2 = self._getflag(MusicFlag.SURROUND2) 
        if mode1:
            return MusicSurroundOption.MODE1
        elif mode2:
            return MusicSurroundOption.MODE2
        else:
            return MusicSurroundOption.OFF
    @surround.setter
    def surround(self, value:MusicSurroundOption):
        match value:
            case MusicSurroundOption.OFF:
                self._setflags(MusicFlag.SURROUND, False)
                self._setflags(MusicFlag.SURROUND2, False)
            case MusicSurroundOption.MODE1:
                self._setflags(MusicFlag.SURROUND, True)
                #self._setflags(MusicFlag.SURROUND2, False) #IBASS did it itself
            case MusicSurroundOption.MODE2:
                #self._setflags(MusicFlag.SURROUND, False)
                self._setflags(MusicFlag.SURROUND2, True)
        
    @property
    def ft2mod(self) -> bool:
        ''' Use FastTracker 2 .mod playback '''
        return self._getflag(MusicFlag.FT2MOD)
    @ft2mod.setter
    def ft2mod(self, value:bool):
        self._setflags(MusicFlag.FT2MOD, value)

    @property
    def pt1mod(self) -> bool:
        ''' Use ProTracker 1 .mod playback '''
        return self._getflag(MusicFlag.PT1MOD)
    @ft2mod.setter
    def pt1mod(self, value:bool):
        self._setflags(MusicFlag.PT1MOD, value)

    @property
    def posreset(self) -> bool:
        ''' Stop all notes when seeking '''
        return self._getflag(MusicFlag.POSRESET)
    @posreset.setter
    def posreset(self, value:bool):
        self._setflags(MusicFlag.POSRESET, value)

    @property
    def posresetex(self) -> bool:
        ''' Stop all notes and reset BPM/etc when seeking '''
        return self._getflag(MusicFlag.POSRESETEX)
    @posresetex.setter
    def posresetex(self, value:bool):
        self._setflags(MusicFlag.POSRESETEX, value)

    @property
    def stopback(self) -> bool:
        ''' Stop when a backward jump effect is played '''
        return self._getflag(MusicFlag.STOPBACK)
    @stopback.setter
    def stopback(self, value:bool):
        self._setflags(MusicFlag.STOPBACK, value)

    #speaker flags

#endregion