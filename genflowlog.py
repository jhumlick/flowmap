import random
import socket
import struct
import argparse as AP

parser = AP.ArgumentParser()
parser.add_argument('records', help='Number of flow log records to write.', type=int)
parser.add_argument('outfile', help='File to write out to.', type=str)
args = parser.parse_args()

protopt = ('tcp', 'udp')
diropt = ('ingress', 'egress')

with open(args.outfile, 'w') as output:
    for i in range(args.records):
        proto = protopt[random.randint(0, 1)]
        ip = socket.inet_ntoa(struct.pack('>I', random.randrange(1, 0xffffffff)))
        src_port = random.randint(49152, 65535) # ephemeral ports
        dst_port = random.randint(1, 49151)
        direction = diropt[random.randint(0,1)]
        output.write(f'3 {proto} {ip} {src_port} {dst_port} {direction} OK\n')

