import sys

def test():
    return True

if __name__ == '__main__':
    arg = sys.argv[1]
    if arg.lower() == 'test':
        test()
    else:
        raise RuntimeError('Unknown argument: %s' % arg)
