"""Bayplan HUL: keep only the HUL containers (HAL/HAC/HAS -> HUL) for the chosen ports.

Usage:
    python bayplan_hul.py [folder] [--ports LCH,BKK] [--agents HAL,HAC,HAS,HUL]

Reads the one .asc file in <folder>/input (or Input), writes
<folder>/output/<name>_HUL_<PORTS>.asc. Same rules as index.html.
"""
import argparse
import re
import sys
from pathlib import Path

REMARK_START = "***Refer to the following remark."
CONTAINER_RE = re.compile(r"^\d{6} [A-Z]{4}\d{7} ")
TEMP_RE = re.compile(r"(-?\d+)\d([CF])")


def agent_of(line):
    return line[19:22]


def port_of(line):  # PUSBKK -> BKK
    return line[30:33]


def fix_temp(line):
    # -250C -> -25C (one space after C keeps the column width)
    a, b = 52, 80
    return line[:a] + TEMP_RE.sub(r"\1\2 ", line[a:b], count=1) + line[b:]


def convert(text, agents, ports):
    eol = "\r\n" if "\r\n" in text else "\n"
    out = []
    st = {"total": 0, "kept": 0, "dropped": 0, "reefer": 0, "by_port": {}}
    tail = False
    for line in re.split(r"\r?\n", text):
        if not tail and line.startswith(REMARK_START):
            tail = True
        if tail or not CONTAINER_RE.match(line):
            out.append(line)
            continue
        st["total"] += 1
        if agent_of(line) not in agents or port_of(line) not in ports:
            st["dropped"] += 1
            continue
        new = line[:19] + "HUL" + line[22:]
        if new[44:46] == "RF":  # reefer type code at col 45
            fixed = fix_temp(new)
            if fixed != new:
                st["reefer"] += 1
            new = fixed
        st["kept"] += 1
        st["by_port"][port_of(new)] = st["by_port"].get(port_of(new), 0) + 1
        out.append(new)
    return eol.join(out), st


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", nargs="?", default=".")
    ap.add_argument("--ports", default="LCH,BKK")
    ap.add_argument("--agents", default="HAL,HAC,HAS,HUL")
    args = ap.parse_args()

    root = Path(args.folder)
    inp = next((root / d for d in ("input", "Input") if (root / d).is_dir()), None)
    if not inp:
        sys.exit(f"ไม่พบโฟลเดอร์ input ใน {root}")
    files = sorted(p for p in inp.iterdir() if p.is_file() and p.suffix.lower() == ".asc")
    if len(files) != 1:
        sys.exit(f"ต้องมีไฟล์ .asc 1 ไฟล์ใน {inp} (พบ {len(files)})")
    src = files[0]

    split = lambda s: {x for x in re.split(r"[\s,]+", s.upper()) if x}
    ports = split(args.ports)
    text, st = convert(src.read_bytes().decode("latin-1"), split(args.agents), ports)

    out_dir = root / "output"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"{src.stem}_HUL_{'-'.join(sorted(ports))}{src.suffix}"
    out.write_bytes(text.encode("latin-1"))

    by_port = " · ".join(f"{p} {n}" for p, n in sorted(st["by_port"].items())) or "-"
    print(f"ไฟล์งาน   : {src.stem}")
    print(f"ตู้ทั้งหมด : {st['total']}")
    print(f"เก็บไว้    : {st['kept']}  ({by_port})")
    print(f"ตัดทิ้ง    : {st['dropped']}")
    print(f"RF ลด TEMP: {st['reefer']}")
    print(f"ผลลัพธ์    : {out}")


if __name__ == "__main__":
    main()
