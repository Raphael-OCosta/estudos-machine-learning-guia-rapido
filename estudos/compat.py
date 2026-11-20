"""Ajustes para rodar o código do livro (2019) com as bibliotecas atuais.

Os notebooks da pasta `estudos` fazem `import compat` na primeira célula.
Você não precisa mexer neste arquivo.
"""
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import scipy
from sklearn.utils import Bunch

DADOS = Path(__file__).resolve().parent.parent / "dados"
TITANIC = DADOS / "titanic3.xls"

# scikit-plot ainda chama scipy.interp, que saiu do SciPy.
if not hasattr(scipy, "interp"):
    scipy.interp = np.interp

# O Yellowbrick 1.5 reconhece o tipo do modelo pelo atributo _estimator_type,
# que o scikit-learn 1.6+ deixou de definir nas classes base.
from sklearn.base import ClassifierMixin, ClusterMixin, RegressorMixin

for _mixin, _tipo in ((ClassifierMixin, "classifier"), (RegressorMixin, "regressor"), (ClusterMixin, "clusterer")):
    if not hasattr(_mixin, "_estimator_type"):
        _mixin._estimator_type = _tipo

# Menos poluição na saída das células.
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)


def load_boston():
    """Substitui sklearn.datasets.load_boston (removido no scikit-learn 1.2)."""
    df = pd.read_csv(DADOS / "boston.csv")
    X = df.drop(columns="MEDV")
    return Bunch(
        data=X.to_numpy(dtype=float),
        target=df["MEDV"].to_numpy(dtype=float),
        feature_names=np.array(X.columns),
        frame=df,
    )
