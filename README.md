# Lean Transfer Protocol Module
### Module for sending requests to LTP servers in python

LTP or Lean Transfer Protocol is a protocol made by me (jerryjhird) as a modular alternative to http

## Example:
```py
import ltp_py.base as ltp

srv = ltp.LTPServer("IP", PORT)

resp = ltp.ltp_send("PING", "/", server=srv)
if resp.status == 200:
    print("server online")
```
