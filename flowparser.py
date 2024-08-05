from os.path import exists
import ltparser as LTP

# Number of columns expected in flowfile
LOOKUPCOLUMNS = 7
# Column Field Length - padding to use in columns
CFL = 10

class FlowParser:

    tcount = dict() # Tag count
    pcount = dict() # Port/Protocol count
    ltparser = None
    flowfile = None

    def __init__(self, ltfile, flowfile):
        self.ltparser = LTP.LTParser(ltfile=ltfile)
        if (not exists(flowfile)):
            raise IOError('File does not exist', flowfile)
        self.flowfile = flowfile
        
    def parse(self):
        '''Parses flowfile based on lookuptable into tag and port/proto counts'''
        with open(self.flowfile, 'r') as flow_handle:
            for line in flow_handle:
                if line.startswith('#'):
                    continue
                fields = line.split()
                if (len(fields) != LOOKUPCOLUMNS):
                    raise ValueError("File is not formatted as a lookuptable")
                port, proto = int(fields[4]), fields[1].lower()
                tag = self.ltparser.find_tag(port=port, proto=proto)
                if (tag == None):
                    tag = 'UNTAGGED'
                if (tag in self.tcount):
                    self.tcount[tag] += 1
                else:
                    self.tcount[tag] = 1
                if (port in self.pcount):
                    if proto in self.pcount[port]:
                        self.pcount[port][proto] += 1
                    else:
                        self.pcount[port][proto] = 1
                else:
                    self.pcount[port] = {}
                    self.pcount[port][proto] = 1


    def write_results(self, output_file):
        '''Neatly writes results to output_file'''
        if (not self.tcount or not self.pcount):
            raise ValueError('No results found. Was parse() called?')
        with open(output_file, 'w') as output:
            output.write(f'Tag Counts:\n\n{"Tag.":<{CFL}}{"Count":<{CFL}}\n\n')
            for tag in sorted(self.tcount):
                output.write(f'{tag:<{CFL}}{self.tcount[tag]:<{CFL}}\n\n')
            output.write('\n\nPort/Protocol Combination Counts:\n\n')
            output.write(f'{"Port.":<{CFL}}{"Protocol.":<{CFL}}{"Count":<{CFL}}\n\n')
            for port in sorted(self.pcount):
                for proto in sorted(self.pcount[port]):
                    output.write(f'{port:<{CFL}}{proto:<{CFL}}{self.pcount[port][proto]:<{CFL}}\n\n')