#!/usr/bin/env python3
"""Buduje PDF z dokumentu LaTeX przy uzyciu silnika Tectonic.

Tectonic to samowystarczalny silnik LaTeX (pojedyncza binarka), ktory nie
wymaga instalacji systemowej ani uprawnien administratora i sam dociaga
potrzebne pakiety. Binarka lezy w .tools/tectonic.exe (albo w PATH).

Uzycie:
    python build.py            # kompiluje main.tex -> main.pdf
    python build.py plik.tex   # kompiluje wskazany plik .tex
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def find_tectonic() -> str:
    """Zwraca sciezke do binarki Tectonica: najpierw .tools/, potem PATH."""
    local = ROOT / ".tools" / ("tectonic.exe" if os.name == "nt" else "tectonic")
    if local.is_file():
        return str(local)
    on_path = shutil.which("tectonic")
    if on_path:
        return on_path
    sys.exit(
        "Nie znaleziono Tectonica. Oczekiwano .tools/tectonic.exe "
        "lub polecenia 'tectonic' w PATH."
    )


def main(argv: list[str]) -> int:
    tex = Path(argv[1]) if len(argv) > 1 else ROOT / "main.tex"
    if not tex.is_file():
        sys.exit(f"Nie znaleziono pliku: {tex}")

    tectonic = find_tectonic()
    cmd = [tectonic, "-X", "compile", str(tex)]
    print(">", " ".join(cmd))
    result = subprocess.run(cmd, cwd=str(tex.parent))
    if result.returncode == 0:
        print(f"\nOK: wygenerowano {tex.with_suffix('.pdf')}")
    else:
        print("\nBLAD: kompilacja nie powiodla sie.", file=sys.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
