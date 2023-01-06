from pprint import pp
import re
from re._constants import _NamedIntConstant
from re._parser import parse, SubPattern

# OP CODES
FAILURE: int = getattr(re._constants, "FAILURE")
SUCCESS: int = getattr(re._constants, "SUCCESS")
ANY: int = getattr(re._constants, "ANY")
ANY_ALL: int = getattr(re._constants, "ANY_ALL")
ASSERT: int = getattr(re._constants, "ASSERT")
ASSERT_NOT: int = getattr(re._constants, "ASSERT_NOT")
AT: int = getattr(re._constants, "AT")
BRANCH: int = getattr(re._constants, "BRANCH")
CATEGORY: int = getattr(re._constants, "CATEGORY")
CHARSET: int = getattr(re._constants, "CHARSET")
BIGCHARSET: int = getattr(re._constants, "BIGCHARSET")
GROUPREF: int = getattr(re._constants, "GROUPREF")
GROUPREF_EXISTS: int = getattr(re._constants, "GROUPREF_EXISTS")
IN: int = getattr(re._constants, "IN")
INFO: int = getattr(re._constants, "INFO")
JUMP: int = getattr(re._constants, "JUMP")
LITERAL: int = getattr(re._constants, "LITERAL")
MARK: int = getattr(re._constants, "MARK")
MAX_UNTIL: int = getattr(re._constants, "MAX_UNTIL")
MIN_UNTIL: int = getattr(re._constants, "MIN_UNTIL")
NOT_LITERAL: int = getattr(re._constants, "NOT_LITERAL")
NEGATE: int = getattr(re._constants, "NEGATE")
RANGE: int = getattr(re._constants, "RANGE")
REPEAT: int = getattr(re._constants, "REPEAT")
REPEAT_ONE: int = getattr(re._constants, "REPEAT_ONE")
SUBPATTERN: int = getattr(re._constants, "SUBPATTERN")
MIN_REPEAT_ONE: int = getattr(re._constants, "MIN_REPEAT_ONE")
ATOMIC_GROUP: int = getattr(re._constants, "ATOMIC_GROUP")
POSSESSIVE_REPEAT: int = getattr(re._constants, "POSSESSIVE_REPEAT")
POSSESSIVE_REPEAT_ONE: int = getattr(re._constants, "POSSESSIVE_REPEAT_ONE")
GROUPREF_IGNORE: int = getattr(re._constants, "GROUPREF_IGNORE")
IN_IGNORE: int = getattr(re._constants, "IN_IGNORE")
LITERAL_IGNORE: int = getattr(re._constants, "LITERAL_IGNORE")
NOT_LITERAL_IGNORE: int = getattr(re._constants, "NOT_LITERAL_IGNORE")
GROUPREF_LOC_IGNORE: int = getattr(re._constants, "GROUPREF_LOC_IGNORE")
IN_LOC_IGNORE: int = getattr(re._constants, "IN_LOC_IGNORE")
LITERAL_LOC_IGNORE: int = getattr(re._constants, "LITERAL_LOC_IGNORE")
NOT_LITERAL_LOC_IGNORE: int = getattr(re._constants, "NOT_LITERAL_LOC_IGNORE")
GROUPREF_UNI_IGNORE: int = getattr(re._constants, "GROUPREF_UNI_IGNORE")
IN_UNI_IGNORE: int = getattr(re._constants, "IN_UNI_IGNORE")
LITERAL_UNI_IGNORE: int = getattr(re._constants, "LITERAL_UNI_IGNORE")
NOT_LITERAL_UNI_IGNORE: int = getattr(re._constants, "NOT_LITERAL_UNI_IGNORE")
RANGE_UNI_IGNORE: int = getattr(re._constants, "RANGE_UNI_IGNORE")
MIN_REPEAT: int = getattr(re._constants, "MIN_REPEAT")
MAX_REPEAT: int = getattr(re._constants, "MAX_REPEAT")

# AT CODES
AT_BEGINNING: int = getattr(re._constants, "AT_BEGINNING")
AT_END: int = getattr(re._constants, "AT_END")

# CATEGORY CODE
CATEGORY_DIGIT = getattr(re._constants, "CATEGORY_DIGIT")
CATEGORY_SPACE = getattr(re._constants, "CATEGORY_SPACE")
CATEGORY_WORD = getattr(re._constants, "CATEGORY_WORD")
CATEGORY_LINEBREAK = getattr(re._constants, "CATEGORY_LINEBREAK")
CATEGORY_LOC_WORD = getattr(re._constants, "CATEGORY_LOC_WORD")
CATEGORY_UNI_DIGIT = getattr(re._constants, "CATEGORY_UNI_DIGIT")
CATEGORY_UNI_SPACE = getattr(re._constants, "CATEGORY_UNI_SPACE")
CATEGORY_UNI_WORD = getattr(re._constants, "CATEGORY_UNI_WORD")
CATEGORY_UNI_LINEBREAK = getattr(re._constants, "CATEGORY_UNI_LINEBREAK")

# MISC CODES
MAXREPEAT: int = getattr(re._constants, "MAXREPEAT")
OR: int = _NamedIntConstant(500, "OR")
MIN_ZERO: int = _NamedIntConstant(501, "MIN_ZERO")
MIN_ONE: int = _NamedIntConstant(502, "MIN_ONE")
MINMAX: int = _NamedIntConstant(503, "MINMAX")

CHAR_MAP: dict[int, str] = {
    AT_BEGINNING.name: "^",
    AT_END.name: "$",
    IN.name: "[]",
    RANGE.name: "-",
    SUBPATTERN.name: "()",
    OR.name: "|",
    MIN_ZERO.name: "*",
    MIN_ONE.name: "+",
    MINMAX.name: "{}",
    CATEGORY_DIGIT.name: "\d",
    CATEGORY_WORD.name: "\w",
}

def to_str(pattern: SubPattern) -> str:
    str_p: str = ""

    for sub in pattern:
        op_code, params = sub
        
        if op_code is AT:
            str_p += CHAR_MAP[params.name]
        elif op_code is MAX_REPEAT:
            r_min, r_max, r_sub = params
            str_p += to_str(r_sub)

            if r_max is MAXREPEAT:
                str_p += CHAR_MAP[MIN_ZERO.name] if r_min == 0 else CHAR_MAP[MIN_ONE.name]
            elif r_min == r_max:
                str_p += CHAR_MAP[MINMAX.name][0] + str(r_min) + CHAR_MAP[MINMAX.name][1]
            else:
                str_p += CHAR_MAP[MINMAX.name][0] + str(r_min) + "," + str(r_max) + CHAR_MAP[MINMAX.name][1]
        elif op_code is IN:
            str_p += CHAR_MAP[IN.name][0] + to_str(params) + CHAR_MAP[IN.name][1]
        elif op_code is SUBPATTERN:
            str_p += CHAR_MAP[SUBPATTERN.name][0] + to_str(params[3]) + CHAR_MAP[SUBPATTERN.name][1]
        elif op_code is RANGE:
            str_p += chr(params[0]) + CHAR_MAP[RANGE.name] + chr(params[1])
        elif op_code is LITERAL:
            str_p += chr(params)
        elif op_code is CATEGORY:
            str_p += CHAR_MAP[params.name]
        else:
            print(sub)
            

    return str_p

def main():
    raw_pattern = r"^[A-Z]{2,4} [a-z]{3,4} " \
                  r"[0-9]{1,} [a-z0-9]{2} [a-z\d]+ " \
                  r"(hello){1} (world){2,4} ([abc]+[def]+)+ " \
                  r"\w \w+ \d \d+ \w* " \
                  r"(A|B) (ABC|DEF) ((123|45)+)? Z$"
    sub_pattern: SubPattern = parse(raw_pattern)
    
    print(sub_pattern.dump())
    # pp(sub_pattern.data)
    # # print(sub_pattern)
    # # sub_pattern.dump()

    # code = []
    # _compile(code, sub_pattern, 0)
    # print(code)

    # code = _code(sub_pattern, 0)
    # dis(code)

    print(to_str(sub_pattern))


if __name__ == "__main__":
    main()
