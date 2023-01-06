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
AT_BEGINNING_STRING = getattr(re._constants, "AT_BEGINNING_STRING")
AT_BOUNDARY = getattr(re._constants, "AT_BOUNDARY")
AT_NON_BOUNDARY = getattr(re._constants, "AT_NON_BOUNDARY")

# CATEGORY CODE
CATEGORY_DIGIT = getattr(re._constants, "CATEGORY_DIGIT")
CATEGORY_SPACE = getattr(re._constants, "CATEGORY_SPACE")
CATEGORY_WORD = getattr(re._constants, "CATEGORY_WORD")
CATEGORY_NOT_DIGIT = getattr(re._constants, "CATEGORY_NOT_DIGIT")
CATEGORY_NOT_SPACE = getattr(re._constants, "CATEGORY_NOT_SPACE")
CATEGORY_NOT_WORD = getattr(re._constants, "CATEGORY_NOT_WORD")
AT_END_STRING = getattr(re._constants, "AT_END_STRING")
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
EXISTS: int = _NamedIntConstant(504, "EXISTS")

CHAR_MAP: dict[int, str] = {
    AT_BEGINNING.name: r"^",
    AT_END.name: r"$",
    IN.name: r"[]",
    RANGE.name: r"-",
    SUBPATTERN.name: r"()",
    OR.name: r"|",
    MIN_ZERO.name: r"*",
    MIN_ONE.name: r"+",
    MINMAX.name: r"{}",
    CATEGORY_DIGIT.name: r"\d",
    CATEGORY_WORD.name: r"\w",
    EXISTS.name: r"?",
    NEGATE.name: r"^",
    ANY.name: r".",
    CATEGORY_NOT_DIGIT.name: r"\D",
    CATEGORY_NOT_SPACE.name: r"\S",
    CATEGORY_NOT_WORD.name: r"\W",
    AT_END_STRING.name: r"\Z",
    AT_BEGINNING_STRING.name: r"\A",
    AT_BOUNDARY.name: r"\b",
    AT_NON_BOUNDARY.name: r"\B",
}

def to_pattern(p_code) -> re.Pattern:
    def _wrap(p_code) -> str:
        p_str: str = ""

        for sub in p_code:
            op_code, params = sub
            
            if op_code is AT:
                p_str += CHAR_MAP[params.name]
            elif op_code is MAX_REPEAT:
                r_min, r_max, r_sub = params
                p_str += _wrap(r_sub)

                if r_max is MAXREPEAT:
                    p_str += CHAR_MAP[MIN_ZERO.name] if r_min == 0 else CHAR_MAP[MIN_ONE.name]
                elif r_min == r_max:
                    p_str += CHAR_MAP[MINMAX.name][0] + str(r_min) + CHAR_MAP[MINMAX.name][1]
                elif r_min == 0 and r_max == 1:
                    p_str += CHAR_MAP[EXISTS.name]
                else:
                    p_str += CHAR_MAP[MINMAX.name][0] + str(r_min) + "," + str(r_max) + CHAR_MAP[MINMAX.name][1]
            elif op_code is IN:
                if len(params) > 1 or params[0][0] is RANGE:
                    p_str += CHAR_MAP[IN.name][0]

                p_str += _wrap(params)

                if len(params) > 1 or params[0][0] is RANGE:
                    p_str += CHAR_MAP[IN.name][1]
            elif op_code is SUBPATTERN:
                if len(params[3]) > 1 or params[3][0][0] is BRANCH:
                    p_str += CHAR_MAP[SUBPATTERN.name][0]

                p_str += _wrap(params[3])

                if len(params[3]) > 1 or params[3][0][0] is BRANCH:
                    p_str += CHAR_MAP[SUBPATTERN.name][1]
            elif op_code is RANGE:
                p_str += chr(params[0]) + CHAR_MAP[RANGE.name] + chr(params[1])
            elif op_code is LITERAL:
                p_str += chr(params)
            elif op_code is CATEGORY:
                p_str += CHAR_MAP[params.name]
            elif op_code is BRANCH:
                p_str += CHAR_MAP[OR.name].join(_wrap(p) for p in params[1])
            elif params is None and (val := CHAR_MAP.get(op_code.name)):
                p_str += val
            else:
                print("**** NO MANAGED:", sub)

        return p_str
            
    return re.compile(_wrap(p_code))

def main():
    raw_pattern = r"^[A-Z]{2,4} [a-z]{3,4} " \
                  r"[0-9]{1,} [a-z0-9]{2} [a-z\d]+ " \
                  r"(hello){1} (world){2,4} ([abc]+[def]+)+ " \
                  r"\w \w+ \d \d+ \w* .+ " \
                  r"[^\d]+ \t\n\r\v\f" \
                  r"(A|B) (ABC|DEF) ((123|(45|[abcd]*))+)? Z$"
    other_pattern = r"Hello[\t\n\r\v\f]world"
    p_code: SubPattern = parse(raw_pattern)
    
    # print(p_code.dump())
    # pp(sub_pattern.data)
    # # print(sub_pattern)
    # # sub_pattern.dump()

    # code = []
    # _compile(code, sub_pattern, 0)
    # print(code)

    # code = _code(sub_pattern, 0)
    # dis(code)

    converted = to_pattern(p_code)
    print("*****Converted:", converted)
    # print("*****Match:", converted.match("Hello\t\n\r\v\fworld")) 


if __name__ == "__main__":
    main()
