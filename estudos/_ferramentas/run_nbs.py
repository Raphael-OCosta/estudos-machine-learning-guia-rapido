"""Executa os notebooks de estudos e lista as células com erro (não salva os notebooks)."""
import json
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient

pasta = Path(sys.argv[1])
alvo = sys.argv[2:] or None
rel = {}
for f in sorted(pasta.glob("cap*.ipynb")):
    if alvo and not any(a in f.name for a in alvo):
        continue
    nb = nbformat.read(f, as_version=4)
    t = time.time()
    client = NotebookClient(nb, timeout=420, kernel_name="python3", allow_errors=True,
                            resources={"metadata": {"path": str(pasta)}})
    try:
        client.execute()
    except Exception as e:  # timeout etc.
        rel[f.name] = [{"cell": -1, "erro": f"{type(e).__name__}: {str(e)[:300]}"}]
        print(f.name, "FALHOU", e, flush=True)
        continue
    errs = []
    for i, c in enumerate(nb.cells):
        if c.cell_type != "code":
            continue
        for o in c.get("outputs", []):
            if o.get("output_type") == "error":
                errs.append({"cell": i, "erro": f"{o['ename']}: {o['evalue'][:300]}",
                             "src": c.source[:160]})
    rel[f.name] = errs
    print(f"{f.name}: {len(errs)} erro(s) em {time.time() - t:.0f}s", flush=True)
Path(pasta.parent / "relatorio_execucao.json").write_text(json.dumps(rel, ensure_ascii=False, indent=1), encoding="utf-8")
