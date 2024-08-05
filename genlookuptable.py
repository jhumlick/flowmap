import random
import argparse as AP

parser = AP.ArgumentParser()
parser.add_argument('records', help='Number of flow log records to write.', type=int)
parser.add_argument('tagrange', help='Number of tags to use starting from 0.', type=int)
parser.add_argument('outfile', help='File to write out to.', type=str)
args = parser.parse_args()

protopt = ('tcp', 'udp')

with open(args.outfile, 'w') as output:
    for i in range(args.records):
        proto = protopt[random.randint(0, 1)]
        dst_port = random.randint(1, 49152)
        tagno = random.randrange(0, args.tagrange)
        output.write(f'{dst_port},{proto},sv_P{tagno}\n')

