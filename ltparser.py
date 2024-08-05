from os.path import exists

# Number of columns expected in ltfile
LOOKUPCOLUMNS = 3

class LTParser:

    lt = dict()

    def __init__(self, ltfile):
        if (not exists(ltfile)):
            raise IOError('File does not exist', ltfile)
        with open(ltfile, 'r') as ltfile_handle:
            for line in ltfile_handle:
                if line.startswith('#'):
                    continue
                fields = line.split(",")
                if (len(fields) != LOOKUPCOLUMNS):
                    raise ValueError("File is not formatted as a lookuptable")
                port, proto, tag = int(fields[0].split()[0]), fields[1].split()[0].lower(), fields[2].split()[0].upper()
                if (port not in self.lt):
                    self.lt[port] = {}
                self.lt[port][proto] = tag
        if (not self.lt):
            raise EOFError('No lookup tables could be built from', ltfile)


    def find_tag(self, port, proto):
        '''Returns a tag corresponding to the port and proto provided, otherwise returns None if there are no matches'''
        if (port in self.lt and proto in self.lt[port]):
            return self.lt[port][proto]
        return None
    