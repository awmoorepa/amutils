import sys
import enum

class Coltype(enum.Enum):
    coltype_bool = 0
    coltype_float = 1
    coltype_string = 2

class Colname:
    def __init__(self,s: str):
        self.m_string = s
        self.assert_ok()


class Column:
    def __init__(self,ct: Coltype,items: list):
        self.m_coltype = ct
        self.m_list = items
        self.assert_ok()



class NamedColumn:
    def __init__(self,cn: Colname,col: Column):
        self.m_colname = cn
        self.m_column = col
        self.assert_ok()


class Datset:
    def __init__(self,ncs: list[NamedColumn]):
        self.m_named_columns = ncs
        self.assert_ok()


class Errmess:
    def __init__(self,is_ok: bool,s: str):
        self.is_ok = is_ok
        self.m_string = s
        self.assert_ok()


class Filename:
    def __init__(self,s: str):
        self.m_string = s
        self.assert_ok()


def errmess_ok()->Errmess:
    return Errmess(True,None)


def filename_from_string(fname: str)->tuple[Filename,Errmess]:
    return Filename(str),errmess_ok()


def datset_from_filename(fn: Filename)->tuple[Datset,Errmess]:
    ncs,em=named_columns_from_filename(fn)
    if em.is_error():
        return None,em

    return datset_from_named_columns(ncs)


def datset_from_string(fname: str)->tuple[Datset,Errmess]:
    fn,em = filename_from_string(fname)
    if em.is_error():
        return None,em

    return datset_from_filename(fn)


def load(fname: str) -> Datset:
    ds,em = datset_from_string(fname)
    if em.is_error():
        sys.exit(em.string())
    return ds