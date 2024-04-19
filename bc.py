import socket
import struct

def get_rpi_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
        print("Could not extract IP address", Exception)
    finally:
        st.close()
    return IP



multicast_group = '232.1.1.1'
server_address = ('', 1235)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)

group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    data, _ = sock.recvfrom(1024)
    decoded = data.decode('utf-8')
    tweet_split = decoded.split(',')
    tweet_type = tweet_split[0].strip()