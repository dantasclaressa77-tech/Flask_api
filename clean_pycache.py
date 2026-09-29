"""Remove todos os diretórios __pycache__ do projeto.

Uso:
    python clean_pycache.py          # ignora venv/.venv
    python clean_pycache.py --all    # inclui venv/.venv
"""

import shutil
import sys
from pathlib import Path

IGNORAR = {"venv", ".venv", ".git"}


def limpar(raiz: Path, incluir_venv: bool = False) -> int:
    removidos = 0
    for pasta in raiz.rglob("__pycache__"):
        if not pasta.is_dir():
            continue
        partes = set(pasta.relative_to(raiz).parts)
        if not incluir_venv and partes & IGNORAR:
            continue
        shutil.rmtree(pasta, ignore_errors=True)
        print(f"Removido: {pasta.relative_to(raiz)}")
        removidos += 1
    return removidos


if __name__ == "__main__":
    raiz = Path(__file__).resolve().parent
    total = limpar(raiz, incluir_venv="--all" in sys.argv)
    print(f"\n{total} pasta(s) __pycache__ removida(s).")
