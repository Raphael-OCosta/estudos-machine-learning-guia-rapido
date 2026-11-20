"""Gera praticar/capXX_*.ipynb: cadernos vazios por seção do livro, com a preparação pronta.

Uso (na raiz do curso):
  python estudos\\_ferramentas\\gerar_praticar.py . estudos\\_ferramentas\\fixes.json estudos\\_ferramentas\\secoes.json
Não sobrescreve cadernos que já existem (para não apagar o que você escreveu).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_nbs import TITULOS, URL_RE, slug  # noqa: E402

ROOT = Path(sys.argv[1]).resolve()
FIXES = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
SECOES = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))
OUT = ROOT / "praticar"
OUT.mkdir(exist_ok=True)

PAG = {3: 24, 4: 51, 5: 58, 6: 61, 7: 79, 8: 90, 9: 98, 10: 103, 11: 145, 12: 149, 13: 165,
       14: 178, 15: 209, 16: 217, 17: 223, 18: 254, 19: 268}

# Células do notebook original que viram a "preparação" de cada capítulo
# (o que o capítulo supõe que já existe: dados, funções auxiliares, treino/teste).
PREP = {4: [0], 5: [0], 6: [0, 1], 7: [0], 8: [0, 1], 9: [1], 10: [0], 11: [0], 12: [0], 13: [1],
        14: [1], 15: [0], 16: [0], 17: [1], 18: [1], 19: [1]}

# Linhas que já são exercício e saem da preparação
CORTAR = {4: ["df.isnull().mean() * 100"]}
# A partir deste trecho a célula já é exercício
CORTAR_DEPOIS = {11: "fig, ax = plt.subplots(figsize=(6, 4))\nvc_viz"}

NAO_RODA = {(10, "TPOT"): "O TPOT não roda hoje (veja o guia). Só leitura."}


def fix(ch, i, s):
    s = URL_RE.sub("url = compat.TITANIC  # arquivo local", s)
    s = s.replace("from sklearn.datasets import load_boston", "from compat import load_boston")
    for a, b in FIXES.get("_global", []):
        s = s.replace(a, b)
    fx = FIXES.get(f"{ch}:{i}", {})
    for a, b in fx.get("replace", []):
        s = s.replace(a, b)
    return fx.get("source", s)


def code(src=""):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": src}


def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src}


IMPORT_COMPAT = 'import sys\nsys.path.insert(0, "../estudos")  # onde fica o compat.py\nimport compat  # dados locais e ajustes para as bibliotecas atuais\n'

for n in range(3, 20):
    titulo = TITULOS[n]
    nome = f"cap{n:02d}_{slug(titulo)}.ipynb"
    destino = OUT / nome
    if destino.exists():
        print("já existe, mantido:", nome)
        continue
    orig = json.loads((ROOT / f"ch{n:02d}.ipynb").read_text(encoding="utf-8"))

    if n == 3:
        prep = IMPORT_COMPAT + "url = compat.TITANIC  # caminho do titanic3.xls (no livro é um link da internet)\n"
        prep_txt = "Só carrega os ajustes e define `url` com o arquivo do Titanic. **Todo o resto você escreve.**"
    else:
        partes = []
        for i in PREP[n]:
            s = fix(n, i, "".join(orig["cells"][i]["source"]))
            for corte in CORTAR.get(n, []):
                s = s.replace(corte, "")
            if n in CORTAR_DEPOIS:
                s = s.split(CORTAR_DEPOIS[n])[0].rstrip() + "\n"
            if n == 19:  # a partir da classe TitanicTransformer já é exercício
                s = s.split("class TitanicTransformer")[0].rstrip() + '\n\nurl = compat.TITANIC\ndf = pd.read_excel(url)\n'
            partes.append(s.strip())
        prep = IMPORT_COMPAT + "\n" + "\n\n".join(partes) + "\n"
        prep_txt = ("Igual ao começo do capítulo no livro: bibliotecas, dados"
                    + (", funções auxiliares e divisão treino/teste" if n not in (4, 5, 7) else "")
                    + ". Já vem pronta para você focar no assunto do capítulo.")

    cells = [
        md(f"# Capítulo {n} — {titulo} · prática\n\n"
           f"**Livro:** começa na página **{PAG[n]}** do PDF.\n\n"
           "**Como usar:**\n"
           "1. Rode a célula **Preparação** abaixo (`Shift+Enter`).\n"
           "2. Para cada seção, leia no livro e **digite o código** na célula vazia — não copie e cole.\n"
           "3. Precisa de mais espaço? Passe o mouse entre as células e clique em **+ Code** "
           "(ou **+ Markdown** para anotar com suas palavras).\n\n"
           f"**Travou?** Consulte `../estudos/{nome}` (código pronto e ajustado) "
           f"ou `../ch{n:02d}.ipynb` (resultados do autor)."),
        md(f"## Preparação\n{prep_txt}"),
        code(prep),
    ]
    for _lvl, sec, pag in SECOES[str(n)]:
        texto = f"## {sec} · PDF p. {pag}"
        if (n, sec) in NAO_RODA:
            texto += f"\n\n> {NAO_RODA[(n, sec)]}"
        cells += [md(texto), code()]
    cells.append(md("## Minhas anotações do capítulo\n\n- Aprendi:\n- Dúvidas:\n"))

    nb = {"cells": cells, "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3 (.venv)", "language": "python"},
                                        "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
    destino.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print("criado:", nome, f"({len(SECOES[str(n)])} seções)")
