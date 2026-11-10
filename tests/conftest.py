import sys
from pathlib import Path

# A raiz do repositório no caminho, para `import exemplos` funcionar também com `pytest` sem `python -m`.
RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))
