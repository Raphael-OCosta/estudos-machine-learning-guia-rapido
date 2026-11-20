"""Gera fixes.json: correções por célula (chave "cap:índice_original") e trocas globais."""
import json
import sys

AVISO = "> ⚠️ **Ajuste para as bibliotecas atuais:** "
NAO_RODA = "> ⚠️ **Não roda hoje:** "


def comentado(src):
    return "\n".join("# " + l if l.strip() else "#" for l in src.splitlines())


F = {}

F["_global"] = [
    ['"max_features": "auto",', '"max_features": "sqrt",  # "auto" foi removido do scikit-learn'],
    [".pipe(pd.get_dummies, drop_first=True)", ".pipe(pd.get_dummies, drop_first=True, dtype=int)"],
    ["yellowbrick.features.importances", "yellowbrick.model_selection"],
    ['sns.scatterplot(\n    "PC1",\n    "PC2",', 'sns.scatterplot(\n    x="PC1",\n    y="PC2",'],
    ["agg_df.corr()", "agg_df.corr(numeric_only=True)"],
    ["roc_viz.score(X_test, y_test)", "roc_viz.fit(X_train, y_train)  # o Yellowbrick novo exige fit antes do score\nroc_viz.score(X_test, y_test)"],
    ["n_splits=10, random_state=42", "n_splits=10, shuffle=True, random_state=42"],
    [".fit_sample(", ".fit_resample("],
    ['affinity="euclidean"', 'metric="euclidean"'],
    ["RFE(model, 4)", "RFE(model, n_features_to_select=4)"],
    ['jointplot(\n    "age", "fare", data=', 'jointplot(\n    x="age", y="fare", data='],
    ['.agg("min,max,mean,sum".split(","))', '[df.select_dtypes("number").columns]  # só colunas numéricas (pandas 2)\n     .agg(["min", "max", "mean", "sum"])'],
    ["import dtreeviz.trees\n", "import dtreeviz\n"],
    ["dtreeviz.trees.dtreeviz(", "dtreeviz.model("],
    ["xgb.XGBClassifier(random_state=42)", "xgb.XGBClassifier(random_state=42, early_stopping_rounds=10)"],
    ["    early_stopping_rounds=10,\n", ""],
]

F["6:25"] = {"replace": [["new_df = X.copy()", "new_df = X.astype(float)  # radviz não aceita colunas True/False"]]}

F["7:5"] = {
    "note": NAO_RODA + "a função `scale_vars` era do **fastai v1**, que não existe mais. "
            "A célula abaixo faz o mesmo (padronizar média 0 e desvio 1) com o `StandardScaler` do scikit-learn.",
    "source": "X3 = X2.copy()\nfrom sklearn.preprocessing import StandardScaler\n"
              "X3[X3.columns] = StandardScaler().fit_transform(X3)\nX3.std()\nX3.mean()\n\n" + comentado(
                  "Código original do livro (fastai v1):\nX3 = X2.copy()\nfrom fastai.structured import scale_vars\nscale_vars(X3, mapper=None)"),
}

F["7:21"] = {
    "note": NAO_RODA + "`add_datepart` era do **fastai v1**. Abaixo, o mesmo resultado com pandas (`.dt`).",
    "source": 'dates = pd.DataFrame(\n    {\n        "A": pd.to_datetime(\n            ["9/17/2001", "Jan 1, 2002"], format="mixed"\n        )\n    }\n)\n'
              "d = dates.A.dt\n"
              "dates = dates.assign(\n    AYear=d.year, AMonth=d.month, AWeek=d.isocalendar().week,\n    ADay=d.day, ADayofweek=d.dayofweek, ADayofyear=d.dayofyear,\n"
              "    AIs_month_end=d.is_month_end, AIs_month_start=d.is_month_start,\n    AIs_quarter_end=d.is_quarter_end, AIs_quarter_start=d.is_quarter_start,\n"
              "    AIs_year_end=d.is_year_end, AIs_year_start=d.is_year_start,\n    AElapsed=dates.A.astype('int64') // 10**9,\n).drop(columns='A')\ndates.T",
}

DTV = AVISO + "o **dtreeviz 2** mudou a forma de chamar: agora é `dtreeviz.model(...)` e o desenho sai com `.view()`."
F["10:11"] = {"note": DTV, "source": 'import dtreeviz\nviz = dtreeviz.model(\n    dt,\n    X,\n    y,\n    target_name="survived",\n'
              '    feature_names=X.columns,\n    class_names=["died", "survived"],\n)\nviz.view()'}
F["14:13"] = {"note": DTV, "source": 'import dtreeviz\ndtr3 = DecisionTreeRegressor(max_depth=2)\ndtr3.fit(bos_X_train, bos_y_train)\n'
              'viz = dtreeviz.model(\n    dtr3,\n    bos_X,\n    bos_y,\n    target_name="price",\n    feature_names=bos_X.columns,\n)\nviz.view()'}
F["5:3"] = {"note": AVISO + "o pyjanitor mudou os parâmetros do `coalesce`.", "source":'jn.coalesce(\n    Xbad,\n    "A",\n    "  sales numbers ",\n    target_column_name="val",\n)'}
F["8:4"] = {"note": NAO_RODA + "`rfpimp.feature_dependence_matrix` quebrou com o scikit-learn novo. Leia no livro; código comentado.",
            "source": comentado("import rfpimp\nrfpimp.plot_dependence_heatmap(\n    rfpimp.feature_dependence_matrix(X_train),\n"
                                "    value_fontsize=12,\n    label_fontsize=14,\n    figsize=(8, 8)\n)")}
F["10:33"] = {"note": AVISO + "`median()` agora precisa de `numeric_only=True` quando há colunas de texto.",
              "replace": [["cat_df.fillna(cat_df.median())", "cat_df.fillna(cat_df.median(numeric_only=True))"]]}

F["10:35"] = {"note": NAO_RODA + "o **auto-sklearn** só funciona no Linux. Leia no livro; o código fica comentado como referência.",
              "source": comentado("from autosklearn.classification import (\n    AutoSklearnClassifier,\n)\nasc = AutoSklearnClassifier(\n    time_left_for_this_task=240\n)\nasc.fit(X_train, y_train)\nasc.score(X_test, y_test)")}
F["10:36"] = {"note": NAO_RODA + "o **TPOT** mudou completamente desde o livro e é muito lento. Leia no livro; código comentado.",
              "source": comentado("from tpot import TPOTClassifier\ntc = TPOTClassifier(generations=2)\ntc.fit(X_train, y_train)\ntc.score(X_test, y_test)")}
F["10:37"] = {"source": comentado('tc.export("tpot_exported_pipeline.py")')}

F["13:11"] = {
    "note": NAO_RODA + "o **pdpbox** não instala mais. O scikit-learn tem o mesmo gráfico de dependência parcial: `PartialDependenceDisplay`.",
    "source": 'from sklearn.inspection import PartialDependenceDisplay\nfeat_name = "age"\nfig, ax = plt.subplots(figsize=(6, 4))\n'
              'PartialDependenceDisplay.from_estimator(\n    rf5, X.astype(float), [feat_name], kind="both", ax=ax\n)',
}
F["13:12"] = {
    "source": 'features = ["fare", "sex_male"]\nfig, ax = plt.subplots(figsize=(6, 5))\n'
              'PartialDependenceDisplay.from_estimator(\n    rf5, X.astype(float), [tuple(features)], ax=ax\n)',
}
F["12:18"] = {
    "note": NAO_RODA + "o `ClassPredictionError` do Yellowbrick 1.5 quebrou com o scikit-learn novo. "
            "Abaixo, o mesmo gráfico (acertos e erros por classe) feito com pandas.",
    "source": 'fig, ax = plt.subplots(figsize=(6, 3))\npd.crosstab(\n    pd.Series(y_test.values, name="real").map({0: "died", 1: "survived"}),\n'
              '    pd.Series(dt.predict(X_test), name="previsto").map({0: "died", 1: "survived"}),\n'
              ').plot.bar(stacked=True, ax=ax)\nax.set_title("Class Prediction Error")\n\n'
              + comentado("Código original do livro:\ncpe_viz = ClassPredictionError(\n    dt, classes=[\"died\", \"survived\"]\n)\ncpe_viz.score(X_test, y_test)\ncpe_viz.poof()"),
}
F["13:15"] = {
    "note": AVISO + "o **shap** novo devolve um único array (linhas × colunas × classes). A linha extra abaixo volta ao formato do livro (uma lista por classe).",
    "replace": [["shap_vals = s.shap_values(X_test)\n",
                 "shap_vals = s.shap_values(X_test)\nif getattr(shap_vals, 'ndim', 0) == 3:  # formato novo -> formato do livro\n"
                 "    shap_vals = [shap_vals[:, :, i] for i in range(shap_vals.shape[2])]\n"]],
}

F["15:8"] = {
    "note": AVISO + "o `statsmodels` agora exige uma coluna constante no teste de Breusch-Pagan (`add_constant`).",
    "replace": [["hb = sms.het_breuschpagan(resids, bos_X_test)",
                 "import statsmodels.api as sm\nhb = sms.het_breuschpagan(resids, sm.add_constant(bos_X_test))"]],
}

F["17:13"] = {"replace": [['circle_kwargs["legend"] = legend', 'circle_kwargs["legend_label"] = legend'],
                          ["fig.circle(", "fig.scatter("],
                          ["        tools=[", "        tools=["]]}
F["17:15"] = {
    "note": NAO_RODA + "o **scprep** exige um pandas antigo. Abaixo, um gráfico 3D equivalente (parado) com matplotlib.",
    "source": 'fig = plt.figure(figsize=(8, 6))\nax = fig.add_subplot(projection="3d")\n'
              'ax.scatter(X_pca[:, 0], X_pca[:, 1], X_pca[:, 2], c=y, cmap="Spectral")\n'
              'ax.set(xlabel="Principal Component 1", ylabel="Principal Component 2", zlabel="Principal Component 3")',
}
F["17:27"] = {
    "note": AVISO + "`phate.plot.scatter2d` saiu do PHATE 2; o gráfico abaixo faz o mesmo com matplotlib.",
    "source": 'fig, ax = plt.subplots(figsize=(6, 4))\nax.scatter(X_phate[:, 0], X_phate[:, 1], c=y, alpha=0.5, cmap="Spectral")',
}

F["19:10"] = {"note": AVISO + "no livro esta célula usa um `X` que não existe neste capítulo; trocado por `df`.",
              "source": "df.isna().any()"}
F["19:11"] = {"note": AVISO + "erro de digitação do livro: a pipeline se chama `spca_pipe`.",
              "replace": [["X_pca = pca_pipe.fit_transform", "X_pca = spca_pipe.fit_transform"]]}
F["19:12"] = {"replace": [["pca_pipe.named_steps", "spca_pipe.named_steps"]]}

json.dump(F, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(F), "entradas")
