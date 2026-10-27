
import socket
import threading

dns = {
    "google.com": "142.250.0.1",
    "yahoo.com": "98.137.11.163"
}

def ask(port, domain):                      # forward query to next server
    s = socket.socket()
    s.connect(("127.0.0.1", port))
    s.send(domain.encode())
    reply = s.recv(1024).decode()
    s.close()
    return reply

def local(d):                               # recursive server (port 5000)
    print("LOCAL -> ROOT")
    return ask(5001, d)

def root(d):                                # port 5001
    print("ROOT  -> TLD")
    return ask(5002, d)

def tld(d):                                 # port 5002
    print("TLD   -> AUTH")
    return ask(5003, d)

def auth(d):                                # port 5003
    print("AUTH  found answer")
    return dns.get(d, "Not Found")

def handle(c, func):
    domain = c.recv(1024).decode()
    print("Query:", domain)
    c.send(func(domain).encode())           # answer goes back up the chain
    c.close()

def serve(port, func):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", port))
    s.listen()
    while True:
        c, addr = s.accept()
        threading.Thread(target=handle, args=(c, func)).start()

# start Root, TLD, Auth in background threads
for port, func in [(5001, root), (5002, tld), (5003, auth)]:
    threading.Thread(target=serve, args=(port, func), daemon=True).start()

print("Recursive DNS Server running")
serve(5000, local)                          # main server clients talk to
