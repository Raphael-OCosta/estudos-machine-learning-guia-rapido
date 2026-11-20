"""Gera estudos/capXX_*.ipynb a partir dos notebooks originais do livro."""
import copy
import json
import re
import sys
from pathlib import Path


TITULOS = {
    3: "Classificação - Titanic (visão geral)", 4: "Dados ausentes", 5: "Limpeza dos dados",
    6: "Explorando os dados", 7: "Pré-processamento", 8: "Seleção de atributos",
    9: "Classes desbalanceadas", 10: "Classificação", 11: "Seleção do modelo",
    12: "Métricas de classificação", 13: "Explicando os modelos", 14: "Regressão",
    15: "Métricas de regressão", 16: "Explicando modelos de regressão",
    17: "Redução de dimensionalidade", 18: "Clustering", 19: "Pipelines",
}

URL_RE = re.compile(r'url = \(\s*"http://biostat\.mc\.vanderbilt\.edu/"\s*"wiki/pub/Main/DataSets/titanic3\.xls"\s*\)')


def slug(t):
    import unicodedata
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")


def code(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": src}


def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src}


if __name__ == "__main__":
    ROOT = Path(sys.argv[1])
    OUT = ROOT / "estudos"
    FIXES = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")) if len(sys.argv) > 2 else {}

    for f in sorted(ROOT.glob("ch*.ipynb")):
        n = int(f.stem[2:])
        nb = json.loads(f.read_text(encoding="utf-8"))
        cells = []
        for i, c in enumerate(nb["cells"]):
            c = copy.deepcopy(c)
            if c["cell_type"] == "code":
                c["outputs"], c["execution_count"] = [], None
                s = "".join(c["source"])
                s = URL_RE.sub("url = compat.TITANIC  # arquivo local (o link do livro saiu do ar)", s)
                s = s.replace("from sklearn.datasets import load_boston", "from compat import load_boston  # removido do scikit-learn; lê dados/boston.csv")
                s = s.replace("import pandas_profiling\n", "import ydata_profiling as pandas_profiling  # novo nome da biblioteca\n")
                for a, b in FIXES.get("_global", []):
                    s = s.replace(a, b)
                key = f"{n}:{i}"
                if key in FIXES:
                    fx = FIXES[key]
                    if "replace" in fx:
                        for a, b in fx["replace"]:
                            s = s.replace(a, b)
                    if "source" in fx:
                        s = fx["source"]
                    if "note" in fx:
                        cells.append(md(fx["note"]))
                c["source"] = s
            cells.append(c)
        titulo = TITULOS[n]
        head = [
            md(f"# Capítulo {n} — {titulo}\n\n"
               "Notebook de estudo adaptado do repositório do livro (Matt Harrison). "
               "O original, com as saídas do autor, está em `../ch{:02d}.ipynb`.\n\n"
               "**Como usar:** rode a célula de baixo primeiro (`Shift+Enter`) e depois vá descendo, "
               "uma célula por vez, comparando com o livro.".format(n)),
            code("import compat  # ajustes para as bibliotecas atuais (veja compat.py)"),
        ]
        nb["cells"] = head + cells
        nb["metadata"]["kernelspec"] = {"name": "python3", "display_name": "Python 3 (.venv)", "language": "python"}
        out = OUT / f"cap{n:02d}_{slug(titulo)}.ipynb"
        out.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
        print(out.name)
