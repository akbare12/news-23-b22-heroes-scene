#!/usr/bin/env python3
"""Copy entry.png to MAKEFUN_OUTPUT_DIR/entry.png.

The grader runs this program with a read-only repository and a writable
output directory, so the program must never write next to itself: the only
output is os.environ["MAKEFUN_OUTPUT_DIR"]/entry.png. The source image sits
next to this file and is copied verbatim, so both runs write identical bytes.
"""
import hashlib
import os
import shutil
import struct
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    with open(src, "rb") as fh:
        data = fh.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("error: entry.png is not a PNG", file=sys.stderr)
        return 1
    if len(data) > 1048576:
        print("error: entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        print("error: entry.png is not 1024x1024", file=sys.stderr)
        return 1
    shutil.copyfile(src, dst)
    with open(dst, "rb") as fh:
        out = fh.read()
    if hashlib.sha256(out).hexdigest() != hashlib.sha256(data).hexdigest():
        print("error: output bytes differ from entry.png", file=sys.stderr)
        return 1
    print("OK: wrote %s (%d bytes, sha256 %s)" % (dst, len(out), hashlib.sha256(out).hexdigest()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
