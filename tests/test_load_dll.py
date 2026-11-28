import pytest
import basson

import sys

def test_unsupported_os(monkeypatch):
    monkeypatch.setattr(sys, 'platform', 'unsupported')
    with pytest.raises(ValueError) as e:
        basson.BASS()

        assert e == ValueError

def test_nonexistent_dll():
    with pytest.raises(Exception) as e:
        basson.BASS("nonexistent.dll")

        assert e == FileNotFoundError

def test_not_dll():
    with pytest.raises(Exception) as e: 

        match sys.platform:
                case "win32": name = "c:/Windows/explorer.exe"
                #case "darwin": name = "libbass.dylib" #FIXME
                #case "linux": name = "libbass.so" #FIXME
                case _: pytest.skip("Unsupported platform")

        assert e == OSError

def test_not_valid_dll():
    with pytest.raises(Exception) as e:
        match sys.platform:
            case "win32": name = "c:/Windows/System32/wow64.dll"
            #case "darwin": name = "libbass.dylib" #FIXME
            #case "linux": name = "libbass.so" #FIXME
            case _: pytest.skip("Unsupported platform")

        assert e == AttributeError

def test_load_dll_by_path():
    import pathlib

    match sys.platform:
        case "win32": name = "bass.dll"
        case "darwin": name = "libbass.dylib"
        case "linux": name = "libbass.so"
        case _: pytest.skip("Unsupported platform")

    path = pathlib.Path(pathlib.Path(sys.executable).parent / "bass" / name)
    if not path.exists(): pytest.skip("libbass.dylib not found")

    bass = basson.BASS(path)
    assert bass.GetVersion() != 0 
