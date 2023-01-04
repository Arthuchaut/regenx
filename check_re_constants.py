import re
from re._constants import *
from re._parser import parse, SubPattern
from re._compiler import compile, _compile, _code, dis

def main():
    raw_pattern = "[A-Z\d]+ ABC \w+"
    sub_pattern: SubPattern = parse(raw_pattern)
    # # print(sub_pattern)
    # # sub_pattern.dump()

    # # code = []
    # # _compile(code, sub_pattern, 0)
    # # print(code)

    code = _code(sub_pattern, 0)
    dis(code)

if __name__ == "__main__":
    main()