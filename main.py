#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261120 (Python 3.13, stdlib only).

The image was drawn by render.py in this repository (PIL, run locally
when the entry was built) and is stored here as entry.png. This program
simply copies that image to the output directory, so both grading runs
write the same bytes with no network access.

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", OUT / "entry.png")
