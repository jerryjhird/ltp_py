import ltp_py.base as ltp

srv = ltp.LTPServer("127.0.0.1", 8080)

# PING
resp = ltp.ltp_send("PING", "/", server=srv)
if resp.status == 200:
    print("server online")

# EXT
extensions = ltp.ltp_get_extensions(server=srv)
print(f"server extensions: {extensions}")

while True:
    user_input = input("type a message: ")
    resp = ltp.ltp_send("POST", "/", body=user_input, server=srv)
