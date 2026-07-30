"""
Find shape mismatches between GET DIRECT CONSTANTS/DATA/LOOKUPS reads in EPS.mdl
and the CSV files they read.

Read-only: does not modify any repository files.

Usage:
    "%LOCALAPPDATA%\\Programs\\Python\\Python313\\python.exe" check_getdirect_shapes.py
Run from (or pass --repo) the EPS repo root, e.g.:
    C:\\Users\\DanOBrien\\Models\\EPS\\US\\eps-us
"""
import argparse
import csv
import io
import os
import re
import sys

SKETCH_MARKER = "\\\\\\---///"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def col_letter_to_index(letters):
    """'A' -> 0, 'B' -> 1, ... 'Z' -> 25, 'AA' -> 26, ..."""
    letters = letters.strip().upper()
    n = 0
    for ch in letters:
        if not ('A' <= ch <= 'Z'):
            raise ValueError(f"bad column letters: {letters!r}")
        n = n * 26 + (ord(ch) - ord('A') + 1)
    return n - 1


def split_cell(cell):
    """'B2' -> ('B', 2); 'B2*' -> ('B', 2, transposed=True)."""
    transposed = cell.endswith('*')
    c = cell[:-1] if transposed else cell
    m = re.match(r'^([A-Za-z]+)(\d+)$', c.strip())
    if not m:
        raise ValueError(f"unparseable cell ref: {cell!r}")
    return m.group(1), int(m.group(2)), transposed


def read_csv_rows(path):
    """Return list of rows (list of str fields), using csv.reader so quoted
    commas are respected. Returns None if file can't be read/decoded."""
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            with open(path, "r", encoding=enc, newline="") as f:
                text = f.read()
            break
        except (UnicodeDecodeError, LookupError):
            text = None
            continue
    else:
        return None
    if text is None:
        return None
    rows = list(csv.reader(io.StringIO(text)))
    # Drop fully-blank trailing rows (all fields empty/whitespace)
    while rows and all((c or "").strip() == "" for c in rows[-1]):
        rows.pop()
    return rows


class FileShapeCache:
    """Caches parsed CSV rows per file path so each file is read once."""

    def __init__(self, repo_root):
        self.repo_root = repo_root
        self._cache = {}

    def get(self, rel_path):
        if rel_path not in self._cache:
            abs_path = os.path.join(self.repo_root, rel_path)
            if not os.path.isfile(abs_path):
                self._cache[rel_path] = None
            else:
                self._cache[rel_path] = read_csv_rows(abs_path)
        return self._cache[rel_path]

    def exists(self, rel_path):
        return os.path.isfile(os.path.join(self.repo_root, rel_path))


def actual_data_shape(rows, start_row, start_col_letter):
    """Given parsed CSV rows (1-indexed conceptually, rows[0] is row 1),
    a data-start row number (e.g. 2) and start column letter (e.g. 'B'),
    return (actual_rows, actual_cols):
      actual_rows = number of non-blank rows from start_row to end of file
      actual_cols = number of fields in the first data row, counting from
                    start_col_letter's column index, trimming trailing blanks
    Returns (None, None) if rows is None or start_row is beyond file end.
    """
    if rows is None:
        return None, None
    start_idx = start_row - 1  # 0-indexed
    if start_idx >= len(rows):
        return 0, 0
    data_rows = rows[start_idx:]
    # actual_rows: count rows that have at least one non-blank field
    actual_rows = sum(1 for r in data_rows if any((c or "").strip() != "" for c in r))
    # actual_cols from first data row
    first_row = data_rows[0]
    col_idx = col_letter_to_index(start_col_letter)
    tail = first_row[col_idx:] if col_idx < len(first_row) else []
    # trim trailing blanks
    while tail and (tail[-1] or "").strip() == "":
        tail.pop()
    actual_cols = len(tail)
    return actual_rows, actual_cols


def subscript_family_size_from_csv(cache, rel_path, start_col_letter, start_row):
    rows = cache.get(rel_path)
    if rows is None:
        return None
    col_idx = col_letter_to_index(start_col_letter)
    count = 0
    for r in rows[start_row - 1:]:
        val = r[col_idx] if col_idx < len(r) else ""
        if (val or "").strip() == "":
            break
        count += 1
    return count


# ---------------------------------------------------------------------------
# Parsing EPS.mdl
# ---------------------------------------------------------------------------

CURLY_COMMENT_RE = re.compile(r"\{[^}]*\}")
# Vensim numeric-range shorthand for subscript elements, e.g. "(Hour0-Hour23)"
# or "(pass1-pass20)" expands to 24 / 20 individual elements respectively.
RANGE_ELEMENT_RE = re.compile(r"^\(([A-Za-z_ ]*)(\d+)\s*-\s*([A-Za-z_ ]*)(\d+)\)$")


def count_element_list(tokens):
    """Given a list of already comma-split, whitespace-stripped element
    tokens (curly-brace comments already removed), return the total
    element count, expanding any "(prefixN-prefixM)" range shorthand."""
    total = 0
    for tok in tokens:
        if not tok:
            continue
        m = RANGE_ELEMENT_RE.match(tok)
        if m:
            _p1, n1, _p2, n2 = m.groups()
            total += int(n2) - int(n1) + 1
        else:
            total += 1
    return total

GET_DIRECT_CONSTANTS_RE = re.compile(
    r"GET DIRECT CONSTANTS\(\s*'([^']*)'\s*,\s*'([^']*)'\s*,\s*'([^']*)'\s*\)"
)
GET_DIRECT_DATAISH_RE = re.compile(
    r"GET DIRECT (DATA|LOOKUPS)\(\s*'([^']*)'\s*,\s*'([^']*)'\s*,\s*'([^']*)'\s*,\s*'([^']*)'\s*\)"
)
GET_DIRECT_SUBSCRIPT_RE = re.compile(
    r"GET DIRECT SUBSCRIPT\(\s*'([^']*)'\s*,\s*'([^']*)'\s*,\s*'([^']*)'\s*,\s*'([^']*)'\s*,\s*'([^']*)'\s*\)"
)


def load_equation_text(mdl_path):
    with open(mdl_path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    marker_idx = text.find(SKETCH_MARKER)
    if marker_idx == -1:
        raise RuntimeError("Could not find sketch-section marker; refusing to guess.")
    eq_text = text[:marker_idx]
    # Collapse Vensim line-continuations: backslash + newline + leading
    # whitespace on the continuation line is removed entirely (no space
    # inserted -- source already embeds any needed space before the '\').
    eq_text = re.sub(r"\\\r?\n[ \t]*", "", eq_text)
    return eq_text


def flatten(block):
    return " ".join(block.split())


def parse_subscript_families(blocks, cache):
    """Returns dict: family_name -> (size, source_description)
    Only considers blocks that look like `Name: elem, elem, ... [-> Target]`
    with no '=' before the first '~' (i.e. not an equation)."""
    families = {}
    decl_re = re.compile(r"^([^:=\n]+):\s*(.*)$", re.DOTALL)
    for b in blocks:
        # Quick reject: equation blocks always contain '=' before any '~'.
        pre_tilde = b.split('~', 1)[0]
        if '=' in pre_tilde:
            continue
        if ':' not in pre_tilde:
            continue
        flat = flatten(b)
        m = decl_re.match(flat)
        if not m:
            continue
        name = m.group(1).strip()
        rest = m.group(2)
        if not name or not re.match(r"^[A-Za-z]", name):
            continue
        # Cut comment/annotation part (starts at first '~')
        body = rest.split('~', 1)[0]

        subscript_m = GET_DIRECT_SUBSCRIPT_RE.search(body)
        if subscript_m:
            file_, delim, first_cell, last_cell, prefix = subscript_m.groups()
            try:
                col_letters, row_num, _ = split_cell(first_cell)
            except ValueError:
                families[name] = (None, f"unparseable first_cell {first_cell!r} in {file_}")
                continue
            size = subscript_family_size_from_csv(cache, file_, col_letters, row_num)
            if size is None:
                families[name] = (None, f"FILE NOT FOUND: {file_}")
            else:
                families[name] = (size, f"GET DIRECT SUBSCRIPT {file_} col {col_letters} from row {row_num}")
            continue

        # Explicit element list, possibly with '-> mapping target' and
        # '{comment}' annotations containing commas.
        body_wo_map = body.split('->', 1)[0]
        body_clean = CURLY_COMMENT_RE.sub("", body_wo_map)
        elems = [e.strip() for e in body_clean.split(',')]
        elems = [e for e in elems if e]
        if elems:
            count = count_element_list(elems)
            families[name] = (count, "explicit list")
    return families


def family_size(name, families):
    """Return size for a subscript token appearing in an LHS bracket list.
    If `name` matches a known family, return its size (or None if that
    family's size itself could not be determined). Otherwise it's treated
    as a FIXED element (specific member, not a family) -> size 1."""
    if name in families:
        size, _src = families[name]
        return size  # may be None (family size unknown -> propagate)
    return 1


def parse_lhs(flat_before_call):
    """Given the flattened text preceding a 'GET DIRECT ...(' call, strip a
    trailing '=' / ':=' / ':INTERPOLATE::=' (and any ':EXCEPT: [...]' clause,
    which per repo scan never co-occurs with GET DIRECT anyway) and return
    (name, subs_list_or_None)."""
    s = flat_before_call.strip()
    # Strip trailing '=' and any ':' / 'INTERPOLATE' immediately before it.
    m = re.search(r"(:INTERPOLATE:)?:?=\s*$", s)
    if not m or not s.endswith('='):
        return None, None
    s = s[:m.start()].rstrip()
    bracket_m = re.search(r"^(?P<name>[^\[]+?)\s*\[(?P<subs>[^\]]*)\]\s*$", s)
    if bracket_m:
        name = bracket_m.group('name').strip()
        subs_raw = bracket_m.group('subs')
        subs = [x.strip() for x in subs_raw.split(',')]
        return name, subs
    # No brackets -> scalar
    name = s.strip()
    if name:
        return name, []
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=os.getcwd(), help="EPS repo root")
    ap.add_argument("--mdl", default="EPS.mdl", help="model filename relative to repo root")
    ap.add_argument("--info-cap", type=int, default=40)
    args = ap.parse_args()

    repo_root = os.path.abspath(args.repo)
    mdl_path = os.path.join(repo_root, args.mdl)
    if not os.path.isfile(mdl_path):
        print(f"ERROR: model file not found: {mdl_path}")
        sys.exit(1)

    cache = FileShapeCache(repo_root)

    eq_text = load_equation_text(mdl_path)
    blocks = eq_text.split('|')

    families = parse_subscript_families(blocks, cache)

    critical = []
    info = []
    parse_failures = []
    missing_files = []
    unresolved_family_calls = []

    n_get_direct_blocks = 0

    for b in blocks:
        if 'GET DIRECT' not in b:
            continue
        # Subscript-family declaration blocks are already handled above;
        # skip re-processing them here.
        pre_tilde = b.split('~', 1)[0]
        if 'GET DIRECT SUBSCRIPT' in b and '=' not in pre_tilde:
            continue

        n_get_direct_blocks += 1
        flat = flatten(b)

        const_m = GET_DIRECT_CONSTANTS_RE.search(flat)
        dataish_m = GET_DIRECT_DATAISH_RE.search(flat)

        if const_m:
            call_start = const_m.start()
            kind = "CONSTANTS"
            file_, delim, cell = const_m.groups()
        elif dataish_m:
            call_start = dataish_m.start()
            kind = dataish_m.group(1)  # DATA or LOOKUPS
            file_, delim, timerow, cell = dataish_m.groups()[1:]
        else:
            parse_failures.append(("UNRECOGNIZED GET DIRECT FORM", flat[:200]))
            continue

        lhs_text = flat[:call_start]
        name, subs = parse_lhs(lhs_text)
        if name is None:
            parse_failures.append(("LHS PARSE FAILURE", flat[:200]))
            continue

        if not cache.exists(file_):
            missing_files.append((name, file_))
            continue

        try:
            col_letters, row_num, transposed = split_cell(cell)
        except ValueError as e:
            parse_failures.append((f"CELL PARSE FAILURE ({e})", flat[:200]))
            continue

        rows = cache.get(file_)
        act_rows, act_cols = actual_data_shape(rows, row_num, col_letters)
        if act_rows is None:
            missing_files.append((name, file_))
            continue

        # Resolve family sizes for each subscript token. A token that is a
        # known subscript-family name contributes its family size and
        # participates in the row/col split below. A token that is NOT a
        # known family name is a FIXED element (a specific member, e.g.
        # "electricity if" rather than the family "Industrial Fuel") --
        # per the spec it still contributes size 1 to any row/col PRODUCT,
        # but it must NOT occupy the "last subscript" slot that determines
        # the row/col split for CONSTANTS: e.g. Foo[Industry Category,
        # Industrial Process,electricity if] with a fixed last element is
        # physically laid out as (Industry Category) rows x (Industrial
        # Process) cols in the CSV, not "(Industry Category x Industrial
        # Process) rows x 1 col". So for the CONSTANTS split we use only
        # the family (non-fixed) subscripts, in their original relative
        # order. For DATA/LOOKUPS (pure product, no row/col split) using
        # all subs vs. only family subs is equivalent since fixed tokens
        # contribute a factor of 1 either way.
        sizes = []          # all subs, fixed -> 1 (used for DATA/LOOKUPS product)
        family_sizes = []   # only real family subs, in order (used for CONSTANTS split)
        unresolved = False
        for s in subs:
            sz = family_size(s, families)
            if sz is None:
                unresolved = True
            sizes.append(sz)
            if s in families:
                family_sizes.append(sz)

        if unresolved:
            unresolved_family_calls.append((name, file_, subs))
            continue

        if kind == "CONSTANTS":
            if not family_sizes:  # scalar, or all subs were fixed elements
                exp_rows, exp_cols = 1, 1
            elif transposed:
                exp_rows = family_sizes[-1]
                exp_cols = 1
                for x in family_sizes[:-1]:
                    exp_cols *= x
            else:
                exp_rows = 1
                for x in family_sizes[:-1]:
                    exp_rows *= x
                exp_cols = family_sizes[-1]

            row_bad = act_rows < exp_rows
            col_bad = act_cols < exp_cols
            row_extra = act_rows > exp_rows
            col_extra = act_cols > exp_cols

            entry = dict(
                var=name, file=file_, cell=cell, kind=kind,
                exp=(exp_rows, exp_cols), act=(act_rows, act_cols),
            )
            if row_bad or col_bad:
                entry["severity"] = "CRITICAL"
                critical.append(entry)
            elif row_extra or col_extra:
                entry["severity"] = "INFO"
                info.append(entry)

        else:  # DATA / LOOKUPS
            exp_rows = 1
            for x in sizes:
                exp_rows *= x
            entry = dict(
                var=name, file=file_, cell=cell, kind=kind,
                exp=(exp_rows, None), act=(act_rows, act_cols),
            )
            if act_rows < exp_rows:
                entry["severity"] = "CRITICAL"
                critical.append(entry)
            elif act_rows > exp_rows:
                entry["severity"] = "INFO"
                info.append(entry)

    # -----------------------------------------------------------------
    # Sanity anchors
    # -----------------------------------------------------------------
    anchor_ok = True
    whm_size = families.get('PEaWHRP WM Row', (None, None))[0]
    if whm_size != 175:
        print(f"ANCHOR FAIL: PEaWHRP WM Row family size = {whm_size}, expected 175")
        anchor_ok = False
    ifam = families.get('Industrial Fuel', (None, None))[0]
    ipro = families.get('Industrial Process', (None, None))[0]
    if ifam != 12:
        print(f"ANCHOR FAIL: Industrial Fuel family size = {ifam}, expected 12")
        anchor_ok = False
    if ipro != 11:
        print(f"ANCHOR FAIL: Industrial Process family size = {ipro}, expected 11")
        anchor_ok = False
    if anchor_ok:
        print(f"Sanity anchors OK (PEaWHRP WM Row=175, Industrial Fuel=12, Industrial Process=11)")
    print()

    # -----------------------------------------------------------------
    # Report
    # -----------------------------------------------------------------
    print(f"Parsed {len(blocks)} equation blocks; {n_get_direct_blocks} GET DIRECT data/const/lookup calls "
          f"(+ {len(families)} subscript families found, of which some via GET DIRECT SUBSCRIPT).")
    print(f"CRITICAL mismatches: {len(critical)}")
    print(f"INFO (actual > expected, likely harmless): {len(info)}")
    print(f"Missing files referenced: {len(missing_files)}")
    print(f"Calls with unresolved family sizes: {len(unresolved_family_calls)}")
    print(f"Parse failures: {len(parse_failures)}")
    print()

    print("=" * 100)
    print("CRITICAL MISMATCHES (actual rows/cols < expected -- likely run blockers)")
    print("=" * 100)
    if not critical:
        print("(none)")
    for e in critical:
        exp_r, exp_c = e["exp"]
        act_r, act_c = e["act"]
        exp_str = f"{exp_r}x{exp_c}" if exp_c is not None else f"{exp_r} rows"
        act_str = f"{act_r}x{act_c}" if e["kind"] == "CONSTANTS" else f"{act_r} rows"
        print(f"[CRITICAL] {e['var']}  <=  {e['file']} '{e['cell']}' ({e['kind']})")
        print(f"           expected {exp_str}   actual {act_str}")

    print()
    print("=" * 100)
    print(f"INFO (actual > expected -- extra rows/cols, usually harmless; capped at {args.info_cap})")
    print("=" * 100)
    for e in info[:args.info_cap]:
        exp_r, exp_c = e["exp"]
        act_r, act_c = e["act"]
        exp_str = f"{exp_r}x{exp_c}" if exp_c is not None else f"{exp_r} rows"
        act_str = f"{act_r}x{act_c}" if e["kind"] == "CONSTANTS" else f"{act_r} rows"
        print(f"[INFO] {e['var']}  <=  {e['file']} '{e['cell']}' ({e['kind']})  expected {exp_str}  actual {act_str}")
    if len(info) > args.info_cap:
        print(f"... ({len(info) - args.info_cap} more INFO entries suppressed)")

    print()
    print("=" * 100)
    print("MISSING FILES (GET DIRECT call references a file that does not exist)")
    print("=" * 100)
    if not missing_files:
        print("(none)")
    for name, file_ in missing_files:
        print(f"[MISSING FILE] {name}  <=  {file_}")

    print()
    print("=" * 100)
    print("CALLS WITH UNRESOLVED SUBSCRIPT FAMILY SIZES (family size itself could not be determined)")
    print("=" * 100)
    if not unresolved_family_calls:
        print("(none)")
    for name, file_, subs in unresolved_family_calls:
        print(f"[UNRESOLVED] {name}  subs={subs}  file={file_}")

    print()
    print("=" * 100)
    print("PARSE FAILURES (GET DIRECT calls the parser could not fully analyze -- nothing silently skipped)")
    print("=" * 100)
    if not parse_failures:
        print("(none)")
    for reason, snippet in parse_failures:
        print(f"[PARSE FAILURE: {reason}] {snippet}")


if __name__ == "__main__":
    main()
