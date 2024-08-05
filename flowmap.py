import argparse as AP
import flowparser as FLP

parser = AP.ArgumentParser()
parser.add_argument('ltfile', help='path to lookup table file.', type=str)
parser.add_argument('flfile', help='path to flow log file.', type=str)
parser.add_argument('output', help='name of output file to write out to.', type=str)
args = parser.parse_args()

flowparser = FLP.FlowParser(flowfile=args.flfile, ltfile=args.ltfile)
flowparser.parse()
flowparser.write_results(output_file=args.output)