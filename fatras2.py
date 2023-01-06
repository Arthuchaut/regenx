from collections.abc import Iterable

OPEN_PARENTHESIS: str = "("
CLOSE_PARENTHESIS: str = ")"

def _rel_index(pattern: list[str], from_index: int, orientation: int = 1) -> int:
    oc: int = 0
    cc: int = 0

    try:
        assert pattern[from_index] == OPEN_PARENTHESIS
    except:
        raise SyntaxError

    for i, char in enumerate(pattern[::orientation][from_index:]):
        oc += char == OPEN_PARENTHESIS
        cc += char == CLOSE_PARENTHESIS

        if oc == cc:
            return from_index + i
    
    raise SyntaxError


def with_fixed_sequence_len(pattern: Iterable[str]) -> str:
    sequence: list[str | None] = [None] * len(pattern)

    for i, char in enumerate(pattern):
        if char == OPEN_PARENTHESIS:
            close_index: int = _rel_index(pattern, i)
            sequence[i] = OPEN_PARENTHESIS
            sequence[close_index] = CLOSE_PARENTHESIS
        if char == CLOSE_PARENTHESIS:


    return "".join(sequence)

def with_dynamic_sequence_len(pattern: Iterable[str]) -> str:
    sequence: list[str | None] = []

    for i, char in enumerate(pattern):
        if char == OPEN_PARENTHESIS:
            close_index: int = _close_index(pattern, i)

            while len(sequence) - 1 < close_index:
                sequence.append(None)

            sequence[i] = OPEN_PARENTHESIS
            sequence[close_index] = CLOSE_PARENTHESIS

    return "".join(sequence)

def main() -> None:
    pattern: str = "(()(()))()"
    expected: str = "(()(()))()"

    result: str = with_fixed_sequence_len(pattern)
    assert result == expected
    result: str = with_dynamic_sequence_len(pattern)
    assert result == expected

if __name__ == "__main__":
    main()