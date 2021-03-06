from typing import Union


def is_power_of_two(n: int) -> bool:
    assert n >= 0
    while n > 1:
        if (n & 1) == 1:
            return False
        n = n >> 1

    return True


def my_error(s: str):
    print(f'*** AWM code signals error: {s}')
    assert False


class Errmess:
    def __init__(self, is_ok: bool, s: str):
        self.m_is_ok: bool = is_ok
        self.m_string: str = s
        self.assert_ok()

    def is_error(self):
        return not self.m_is_ok

    def assert_ok(self):
        assert isinstance(self.m_is_ok, bool)
        assert isinstance(self.m_string, str)
        assert self.m_is_ok == (self.m_string == "")

    def is_ok(self):
        return self.m_is_ok

    def string(self) -> str:
        if self.is_ok():
            return 'ok'
        else:
            return self.m_string


def errmess_ok() -> Errmess:
    return Errmess(True, "")


def errmess_error(s: str) -> Errmess:
    return Errmess(False, s)


class Character:
    def __init__(self, single_character_string: str):
        assert len(single_character_string) == 1
        self.m_byte = ord(single_character_string)
        self.assert_ok()

    def assert_ok(self):
        assert isinstance(self.m_byte, int)
        assert 0 <= self.m_byte < 0x7F

    def string(self) -> str:
        return chr(self.m_byte)

    def is_char(self, single_character_string: str) -> bool:
        assert len(single_character_string) == 1
        return self.m_byte == ord(single_character_string)


def character_create(single_character_string: str) -> Character:
    return Character(single_character_string)


def character_from_string(s: str, i: int) -> Character:
    assert 0 <= i < len(s)
    return Character(s[i])


def float_from_string(s: str) -> Union[tuple[float, bool], tuple[None, bool]]:
    try:
        x = float(s)
        return x, True
    except ValueError:
        return None, False


def string_denotes_true(s: str) -> bool:
    if len(s) == 0:
        return False

    c = s[0]
    if c == 't' or c == 'T':
        lo = s.lower()
        return lo == 't' or lo == "true"
    else:
        return False


def string_denotes_false(s: str) -> bool:
    if len(s) == 0:
        return False

    c = s[0]
    if c == 'f' or c == 'F':
        lo = s.lower()
        return lo == 'f' or lo == "false"
    else:
        return False


def bool_from_string(s: str) -> Union[tuple[bool, bool], tuple[None, bool]]:
    if string_denotes_true(s):
        return True, True
    elif string_denotes_false(s):
        return False, True
    else:
        return None, False


def character_space() -> Character:
    return character_create(' ')


def character_newline():
    return character_create('\n')


def loosely_equals(x: float, y: float) -> bool:
    scale = max(abs(x), abs(y), 1e-3)
    diff = abs(x - y) / scale
    return diff < 1e-5


def string_is_float(s: str) -> bool:
    f, ok = float_from_string(s)
    return ok


def string_is_bool(s: str) -> bool:
    b, ok = bool_from_string(s)
    return ok


def n_spaces(n: int) -> str:
    result = ""
    for i in range(0, n):
        result = result + " "
    return result


def string_from_bool(b: bool) -> str:
    if b:
        return "true"
    else:
        return "false"


def string_from_bytes(bys: bytes)->str:
    return bys.decode("utf-8")
