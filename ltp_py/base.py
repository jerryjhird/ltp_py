from collections import namedtuple
import socket

LTPResponse = namedtuple("LTPResponse", ["status", "body"])
LTPServer = namedtuple("LTPServer", ["host", "port"])

def _ltp_decode(raw_data):
    if len(raw_data) < 8:
        raise ValueError("packet too short")

    if not raw_data.startswith(b"ltp0"):
        raise ValueError("invalid magic expected 'ltp0'")

    sep_idx = raw_data.find(b"\n\n")

    if sep_idx == -1:
        raise ValueError("missing header separator")

    header_part = raw_data[:sep_idx].decode("utf-8")
    parts = header_part.split(" ")

    if len(parts) < 2:
        raise ValueError("malformed response header")

    status_code = int(parts[1])
    body_bytes = raw_data[sep_idx + 2 :]

    return LTPResponse(status=status_code, body=body_bytes)

def ltp_send(method, path, body="", *, server):
    if isinstance(body, str):
        body_bytes = body.encode("utf-8")
    else:
        body_bytes = body

    packet = f"ltp1 {method} {path}\n\n".encode("utf-8") + body_bytes

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server.host, server.port))
        s.sendall(packet)
        raw_response = s.recv(4096)

    return _ltp_decode(raw_response)

def ltp_get_extensions(*, server):
    resp = ltp_send("EXT", "/", server=server)
    text = resp.body.decode("utf-8", errors="replace")

    return [ext.strip() for ext in text.splitlines() if ext.strip() and ext.strip() != "None" ]
