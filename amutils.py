import enum
import sys
from typing import TextIO, Union

import arrays
import basic
import csv
from arrays import Strings
from basic import Errmess


class Coltype(enum.Enum):
    bool = 0
    float = 1
    string = 2


class Colname:
    def __init__(self, s: str):
        self.m_string = s
        self.assert_ok()

    def assert_ok(self):
        assert isinstance(self.m_string, str)
        assert self.m_string != ""

    def string(self) -> str:
        return self.m_string


class Column:
    def __init__(self, ct: Coltype, items: any):
        self.m_coltype = ct
        self.m_list = items
        self.assert_ok()

    def assert_ok(self):
        assert isinstance(self.m_coltype, Coltype)
        if self.m_coltype == Coltype.bool:
            assert isinstance(self.m_list, arrays.Bools)
            self.m_list.assert_ok()
        elif self.m_coltype == Coltype.float:
            assert isinstance(self.m_list, arrays.Floats)
            self.m_list.assert_ok()
        elif self.m_coltype == Coltype.string:
            assert isinstance(self.m_list, arrays.Strings)
            self.m_list.assert_ok()
        else:
            basic.my_error("bad column type")

    def num_rows(self) -> int:
        return self.m_list.len()

    def value_as_string(self, r: int) -> str:
        if self.coltype() == Coltype.string:
            return self.strings().string(r)
        elif self.coltype() == Coltype.float:
            return self.floats().value_as_string(r)
        else:
            assert self.coltype() == Coltype.bool
            return self.bools().value_as_string(r)

    def coltype(self) -> Coltype:
        return self.m_coltype

    def strings(self) -> arrays.Strings:
        assert self.coltype() == Coltype.string
        return self.m_list

    def floats(self) -> arrays.Floats:
        assert self.coltype() == Coltype.float
        return self.m_list

    def bools(self) -> arrays.Bools:
        assert self.coltype() == Coltype.bool
        return self.m_list

    def string(self, r: int) -> str:
        return self.strings().string(r)

    def float(self, r: int) -> float:
        return self.floats().float(r)

    def bool(self, r: int) -> bool:
        return self.bools().bool(r)


class NamedColumn:
    def __init__(self, cn: Colname, col: Column):
        self.m_colname = cn
        self.m_column = col
        self.assert_ok()

    def assert_ok(self):
        assert isinstance(self.m_colname, Colname)
        self.m_colname.assert_ok()
        assert isinstance(self.m_column, Column)
        self.m_column.assert_ok()

    def colname(self) -> Colname:
        return self.m_colname

    def column(self) -> Column:
        return self.m_column


class Colnames:
    def __init__(self, cs: list[Colname]):
        self.m_colnames = cs
        self.assert_ok()

    def contains_duplicates(self) -> bool:
        return self.strings().contains_duplicates()

    def strings(self) -> arrays.Strings:
        result = arrays.strings_empty()
        for i in range(0, self.len()):
            result.add(self.string(i))
        return result

    def assert_ok(self):
        for cn in self.m_colnames:
            assert isinstance(cn, Colname)
            cn.assert_ok()

    def add(self, cn: Colname):
        self.m_colnames.append(cn)

    def len(self) -> int:
        return len(self.m_colnames)

    def string(self, i: int) -> str:
        return self.colname(i).string()

    def colname(self, i: int) -> Colname:
        assert 0 <= i < self.len()
        return self.m_colnames[i]


def colnames_empty() -> Colnames:
    return Colnames([])


class Datset:
    def __init__(self, ncs: list[NamedColumn]):
        self.m_named_columns = ncs
        self.assert_ok()

    def string(self, r: int, c: int) -> str:
        return self.column(c).string(r)

    def float(self, r: int, c: int) -> float:
        return self.column(c).float(r)

    def bool(self, r: int, c: int) -> bool:
        return self.column(c).bool(r)

    def assert_ok(self):
        for nc in self.m_named_columns:
            assert isinstance(nc, NamedColumn)
            nc.assert_ok()
        assert not self.colnames().contains_duplicates()

    def colnames(self) -> Colnames:
        result = colnames_empty()
        for nc in self.m_named_columns:
            result.add(nc.colname())
        return result

    def pretty_string(self) -> str:
        return self.strings_array().pretty_string()

    def strings_array(self) -> arrays.StringsArray:
        result = arrays.strings_array_empty()
        result.add(self.colnames().strings())
        for r in range(0, self.num_rows()):
            result.add(self.row_as_strings(r))

        return result

    def num_rows(self) -> int:
        assert self.num_cols() > 0
        return self.column(0).num_rows()

    def num_cols(self) -> int:
        return self.colnames().len()

    def row_as_strings(self, r: int) -> arrays.Strings:
        result = arrays.strings_empty()
        for c in range(0, self.num_cols()):
            result.add(self.value_as_string(r, c))
        return result

    def value_as_string(self, r: int, c: int) -> str:
        return self.column(c).value_as_string(r)

    def column(self, c: int) -> Column:
        return self.named_column(c).column()

    def named_column(self, c: int) -> NamedColumn:
        assert 0 <= c < self.num_cols()
        return self.m_named_columns[c]

    def explain(self):
        print(self.pretty_string())


class Filename:
    def __init__(self, s: str):
        self.m_string = s
        self.assert_ok()

    def assert_ok(self):
        assert isinstance(self.m_string, str)
        assert self.string() != ""

    def open(self, readwrite: str) -> Union[tuple[None, bool], tuple[TextIO, bool]]:
        try:
            f = open(self.string(), readwrite)
        except FileNotFoundError:
            return None, False

        return f, True

    def string(self) -> str:
        return self.m_string


def is_legal_filename(f_name: str) -> bool:
    return len(f_name) > 0


def filename_from_string(f_name: str) -> Union[tuple[Filename, Errmess], tuple[None, bool]]:
    if is_legal_filename(f_name):
        return Filename(f_name), basic.errmess_ok()
    else:
        return None, False


class RowIndexedSmat:
    def __init__(self, first_row: arrays.Strings):
        self.m_row_to_col_to_string = []
        self.m_row_to_col_to_string.append(first_row)
        self.assert_ok()

    def assert_ok(self):
        assert arrays.is_list_of_instances_of_strings_class(self.m_row_to_col_to_string)
        assert self.num_rows() > 0
        assert self.num_cols() > 0

    def num_cols(self) -> int:
        assert self.num_rows() > 0
        return self.m_row_to_col_to_string[0].len()

    def column(self, c: int) -> arrays.Strings:
        assert 0 <= c < self.num_cols()
        result = arrays.strings_empty()
        for r in range(0, self.num_rows()):
            result.add(self.string(r, c))
        return result

    def num_rows(self) -> int:
        return len(self.m_row_to_col_to_string)

    def add(self, ss: arrays.Strings):
        assert self.num_cols() == ss.len()
        self.m_row_to_col_to_string.append(ss)

    def string(self, r: int, c: int) -> str:
        assert 0 <= r < self.num_rows()
        assert 0 <= c < self.num_cols()
        return self.m_row_to_col_to_string[r].string(c)

    def strings_from_row(self, r: int) -> arrays.Strings:
        assert 0 <= r < self.num_rows()
        return self.m_row_to_col_to_string[r]


def row_indexed_smat_transpose(ris: RowIndexedSmat) -> RowIndexedSmat:
    assert ris.num_cols() > 0

    result = row_indexed_smat_singleton(ris.column(0))

    for c in range(1, ris.num_cols()):
        result.add(ris.column(c))

    result.assert_ok()
    return result


class Smat:
    def __init__(self, row_to_col_to_string: RowIndexedSmat):
        self.m_row_to_col_to_string = row_to_col_to_string
        self.m_col_to_row_to_string = row_indexed_smat_transpose(row_to_col_to_string)
        self.assert_ok()

    def assert_ok(self):
        assert isinstance(self.m_row_to_col_to_string, RowIndexedSmat)
        self.m_row_to_col_to_string.assert_ok()
        assert isinstance(self.m_row_to_col_to_string, RowIndexedSmat)
        self.m_col_to_row_to_string.assert_ok()

        assert self.m_row_to_col_to_string.num_rows() == self.m_col_to_row_to_string.num_cols()
        assert self.m_row_to_col_to_string.num_cols() == self.m_col_to_row_to_string.num_rows()

        for r in range(0, self.num_rows()):
            for c in range(0, self.num_cols()):
                assert self.m_row_to_col_to_string.string(r, c) == self.m_col_to_row_to_string.string(c, r)

    def num_rows(self) -> int:
        return self.m_row_to_col_to_string.num_rows()

    def num_cols(self) -> int:
        return self.m_row_to_col_to_string.num_cols()

    def column(self, c: int) -> arrays.Strings:
        result = arrays.strings_empty()
        for r in range(0, self.num_rows()):
            result.add(self.string(r, c))
        return result

    def string(self, r: int, c: int) -> str:
        return self.row(r).string(c)

    def row(self, r: int) -> arrays.Strings:
        assert 0 <= r < self.num_rows()
        return self.m_row_to_col_to_string.strings_from_row(r)


def strings_from_filename(fn: Filename) -> Union[tuple[None, Errmess], tuple[Strings, Errmess]]:
    f, ok = fn.open('r')
    if not ok:
        return None, basic.errmess_error(f"Darn it. I can't open file {fn.string()} for reading")

    finished = False
    result = arrays.strings_empty()
    current_line = ""
    while not finished:
        c = f.read()
        if not c:
            finished = True
            if current_line != "":
                result.add(current_line)
        elif c == '\n':
            result.add(current_line)
            current_line = ""
        else:
            current_line += c

    f.close()
    return result, basic.errmess_ok()


def row_indexed_smat_singleton(first_row: arrays.Strings) -> RowIndexedSmat:
    return RowIndexedSmat(first_row)


def row_indexed_smat_unit(s: str) -> RowIndexedSmat:
    return row_indexed_smat_singleton(arrays.strings_singleton(s))


def row_indexed_smat_from_strings_array(ssa: arrays.StringsArray) -> Union[
        tuple[None, Errmess], tuple[RowIndexedSmat, Errmess]]:
    if not ssa:
        return None, basic.errmess_error(
            "Can't make a row indexed smat from an empty array of strings")

    result = row_indexed_smat_singleton(ssa.strings(0))
    for r in range(1, ssa.len()):
        ss = ssa.strings(r)
        if ss.len() != result.num_cols():
            return result, basic.errmess_error(
                f'first row of csv file has {result.num_cols()} items, but row {r} has {ss.len()} items')
        result.add(ss)

    return result, basic.errmess_ok()


def row_indexed_smat_from_strings(ss: arrays.Strings) -> Union[tuple[None, Errmess], tuple[RowIndexedSmat, Errmess]]:
    ssa, em = csv.strings_array_from_strings_csv(ss)

    print(f'ssa =\n{ssa.pretty_string()}')

    if em.is_error():
        return None, em

    return row_indexed_smat_from_strings_array(ssa)


def smat_from_row_indexed_smat(rsm: RowIndexedSmat) -> Smat:
    return Smat(rsm)


def smat_unit(s: str) -> Smat:
    return smat_from_row_indexed_smat(row_indexed_smat_unit(s))


def smat_from_strings(ss: arrays.Strings) -> Union[tuple[None, Errmess], tuple[Smat, Errmess]]:
    ris, em = row_indexed_smat_from_strings(ss)
    if em.is_error():
        return None, em

    return smat_from_row_indexed_smat(ris), basic.errmess_ok()


def smat_from_filename(fn: Filename) -> Union[tuple[None, Errmess], tuple[Smat, Errmess]]:
    ss, em = strings_from_filename(fn)
    if em.is_error():
        return None, em

    return smat_from_strings(ss)


def named_column_create(cn: Colname, c: Column) -> NamedColumn:
    return NamedColumn(cn, c)


def colname_create(s: str) -> Colname:
    return Colname(s)


def column_from_bools(bs: arrays.Bools) -> Column:
    return Column(Coltype.bool, bs)


def column_default() -> Column:
    return column_from_bools(arrays.bools_singleton(False))


def named_column_default() -> NamedColumn:
    return named_column_create(colname_create("default"), column_default())


def coltype_from_strings(ss: arrays.Strings) -> Coltype:
    assert ss.len() > 0
    could_be_floats = True
    could_be_bools = True

    for i in range(0, ss.len()):
        s = ss.string(i)
        if could_be_floats and not basic.string_is_float(s):
            could_be_floats = False
        if could_be_bools and not basic.string_is_bool(s):
            could_be_bools = False
        if not (could_be_bools or could_be_floats):
            return Coltype.string

    assert could_be_bools != could_be_floats

    if could_be_bools:
        return Coltype.bool
    else:
        return Coltype.float


def column_from_floats(fs: arrays.Floats) -> Column:
    return Column(Coltype.float, fs)


def column_of_type_strings(ss: arrays.Strings) -> Column:
    return Column(Coltype.string, ss)


def column_from_strings_choosing_coltype(ss: arrays.Strings) -> Column:
    ct = coltype_from_strings(ss)
    if ct == Coltype.bool:
        bs, ok = arrays.bools_from_strings(ss)
        assert ok
        return column_from_bools(bs)
    elif ct == Coltype.float:
        fs, ok = arrays.floats_from_strings(ss)
        assert ok
        return column_from_floats(fs)
    else:
        assert ct == Coltype.string
        return column_of_type_strings(ss)


def named_column_from_strings(ss: arrays.Strings) -> Union[tuple[None, Errmess], tuple[NamedColumn, Errmess]]:
    if ss.len() < 2:
        return None, basic.errmess_error("A file with named columns needs at least two rows")

    rest = arrays.strings_without_first_n_elements(ss, 1)
    c = column_from_strings_choosing_coltype(rest)

    return named_column_create(colname_create(ss.string(0)), c), basic.errmess_ok()


def named_column_from_smat_column(sm: Smat, c: int) -> Union[tuple[None, Errmess], tuple[NamedColumn, Errmess]]:
    return named_column_from_strings(sm.column(c))


def named_columns_from_smat(sm: Smat) -> Union[tuple[None, Errmess], tuple[list[NamedColumn], Errmess]]:
    result = []
    for c in range(0, sm.num_cols()):
        nc, em = named_column_from_smat_column(sm, c)
        if em.is_error():
            return None, em
        result.append(nc)

    return result, basic.errmess_ok()


def named_columns_from_filename(fn: Filename) -> Union[tuple[None, Errmess], tuple[list[NamedColumn], Errmess]]:
    sm, em = smat_from_filename(fn)
    if em.is_error():
        return None, em

    return named_columns_from_smat(sm)


def colnames_from_list(ncs: list[NamedColumn]) -> Colnames:
    result = colnames_empty()
    for nc in ncs:
        result.add(nc.colname())
    return result


def named_column_singleton(colname_as_string: str, value_as_string: str) -> NamedColumn:
    cn = colname_create(colname_as_string)
    col = column_of_type_strings(arrays.strings_singleton(value_as_string))
    return named_column_create(cn, col)


def datset_singleton(colname_as_string: str, value_as_string) -> Datset:
    ncs = [named_column_singleton(colname_as_string, value_as_string)]
    ds, em = datset_from_named_columns(ncs)
    assert em.is_ok()
    return ds


def datset_from_named_columns(ncs: list[NamedColumn]) -> Union[tuple[None, Errmess], tuple[Datset, Errmess]]:
    cs = colnames_from_list(ncs)
    if cs.contains_duplicates():
        return None, basic.errmess_error('the csv has multiple columns with the same name')
    return Datset(ncs), basic.errmess_ok()


def datset_from_filename(fn: Filename) -> Union[tuple[None, Errmess], tuple[Datset, Errmess]]:
    ncs, em = named_columns_from_filename(fn)
    if em.is_error():
        return None, em

    return datset_from_named_columns(ncs)


def datset_from_string(f_name: str) -> Union[tuple[None, Errmess], tuple[Datset, Errmess]]:
    fn, em = filename_from_string(f_name)
    if em.is_error():
        return None, em

    return datset_from_filename(fn)


def load(f_name: str) -> Datset:
    ds, em = datset_from_string(f_name)

    print(f'em = {em.string()}')
    print(f'ds =\n{ds.pretty_string()}')

    if em.is_error():
        sys.exit(em.string())
    return ds


def datset_from_smat(sm: Smat) -> Union[tuple[None, Errmess], tuple[Datset, Errmess]]:
    ncs, em = named_columns_from_smat(sm)
    if em.is_error():
        return None, em

    return datset_from_named_columns(ncs)


def datset_from_strings_csv(ss: arrays.Strings) -> Union[tuple[None, Errmess], tuple[Datset, Errmess]]:
    sm, em = smat_from_strings(ss)
    if em.is_error():
        return None, em

    return datset_from_smat(sm)


def datset_from_multiline_string(s: str) -> Union[tuple[None, Errmess], tuple[Datset, Errmess]]:
    ss = arrays.strings_from_lines_in_string(s)
    return datset_from_strings_csv(ss)


def unit_test():
    s = """date,hour,person,is_happy\n
        4/22/22, 15, ann, True\n
        4/22/22, 15, bob bobson, True\n
        4/22/22, 16, jan, False\n
        4/22/22, 09, jan, True\n
        4/22/22, 12, ann, False\n"""

    ds, em = datset_from_multiline_string(s)

    print(f'em = {em.string()}')
    print(f'ds = \n{ds.pretty_string()}')

    assert ds.string(1, 0) == '4/22/22'
    assert ds.string(1,2)=='bob bobson'
    assert not ds.bool(2, 3)
    assert ds.num_rows() == 5
    assert ds.num_cols() == 4
