"""
C2UI API layer - everything that talks to the original SFM.

    protocol.py   shared wire format (Python 2.7 *and* 3.x compatible)
    launcher.py   start / find the sfm.exe process
    bridge.py     Python 3 client used by the host UI (QTcpSocket based)
    agent/        Python 2.7 code that runs *inside* sfm.exe (JSON-RPC server)
    native/       optional C++ (pybind11) module for Win32 window embedding
"""
