# Estudos — *Machine Learning: Guia de Referência Rápida* (Matt Harrison) · concluído

> **A melhor forma de estudar um livro técnico é ler e praticar ao mesmo tempo.**
> Leia um trecho, feche o livro e escreva o código com as próprias mãos. Só depois compare com o original.

Este repositório registra como estudei *Machine Learning – Guia de Referência Rápida* (O'Reilly), capítulos 3 a 19, no **VS Code + Jupyter**.
Os notebooks oficiais do autor foram escritos para versões antigas do pandas e do scikit-learn e já não rodavam. O que está aqui é **o trabalho de atualização**: as correções e as ferramentas que fazem os notebooks do livro rodarem nas bibliotecas atuais e geram cadernos de prática.

## O método

1. **Ler** a seção indicada no PDF (cada caderno mostra a página).
2. **Praticar** num caderno com as células de código **vazias**, escrevendo o código sem olhar.
3. **Conferir** com o notebook do capítulo já corrigido para as bibliotecas atuais.
4. **Anotar** com as próprias palavras e registrar o progresso.

## Melhorias no código do livro

- `estudos/compat.py`: camada de compatibilidade que carrega os dados locais (o link original do Titanic deixou de funcionar e o dataset Boston saiu do scikit-learn) e ajusta APIs que mudaram.
- `estudos/_ferramentas/fixes.json` + `fixes.py`: correções célula a célula nos notebooks originais, para APIs removidas ou renomeadas no pandas 2.x, no scikit-learn 1.x e em outras bibliotecas.
- `build_nbs.py`: gera os notebooks corrigidos, com a página do PDF em cada seção.
- `gerar_praticar.py`: gera os cadernos de prática com as células vazias, sem sobrescrever o que já foi escrito.
- `run_nbs.py`: executa todos os capítulos. **17 de 17 notebooks rodam sem erro** com Python 3.12.
- [Guia de Estudos (PDF)](estudos/Guia_de_Estudos_ML.pdf) para iniciantes.

## O que está aqui (e o que não está)

| Está aqui | Fica só na minha máquina |
|---|---|
| correções, scripts geradores, `compat.py`, guia, `requirements-estudos.txt`, configuração do VS Code | notebooks originais do autor e as versões corrigidas e de prática geradas a partir deles, e os dados baixados |

O código original está em [mattharrison/ml_pocket_reference](https://github.com/mattharrison/ml_pocket_reference), que não tem licença aberta. Por isso os notebooks derivados dele não são republicados aqui. Para reproduzir: clone o repositório do autor, copie para dentro dele a pasta `estudos/` daqui e siga `estudos/_ferramentas/LEIA-ME.txt`.

## Direitos autorais

O livro e os notebooks do autor **não** estão neste repositório. Para estudar, use a sua própria cópia.
As ferramentas, as correções e o guia são autorais e estão sob licença [MIT](LICENSE).
