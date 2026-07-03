import pytest
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier

from pytrain_grader import load_solution, get_attr


def _f(name):
    return get_attr(load_solution(), name)


def data():
    return make_classification(
        n_samples=250,
        n_features=6,
        n_informative=4,
        class_sep=1.2,
        random_state=7,
    )


def test_cv_mean_score_matches_5fold():
    X, y = data()
    got = _f("cv_mean_score")(DecisionTreeClassifier(random_state=0), X, y)
    expected = float(cross_val_score(DecisionTreeClassifier(random_state=0), X, y, cv=5).mean())
    assert isinstance(float(got), float)
    assert float(got) == pytest.approx(expected)


def test_cv_mean_score_other_model():
    from sklearn.neighbors import KNeighborsClassifier

    X, y = data()
    got = _f("cv_mean_score")(KNeighborsClassifier(n_neighbors=3), X, y)
    expected = float(cross_val_score(KNeighborsClassifier(n_neighbors=3), X, y, cv=5).mean())
    assert float(got) == pytest.approx(expected)


def test_tune_knn_returns_fitted_search():
    X, y = data()
    gs = _f("tune_knn")(X, y)
    assert hasattr(gs, "best_params_") and hasattr(gs, "cv_results_"), (
        "return the FITTED GridSearchCV object itself"
    )


def test_tune_knn_grid_is_exactly_the_spec():
    X, y = data()
    gs = _f("tune_knn")(X, y)
    tried = sorted(p["n_neighbors"] for p in gs.cv_results_["params"])
    assert tried == [1, 3, 5, 7, 9]


def test_tune_knn_best_is_sensible():
    X, y = data()
    gs = _f("tune_knn")(X, y)
    assert gs.best_params_["n_neighbors"] in {1, 3, 5, 7, 9}
    assert 0.65 <= float(gs.best_score_) <= 1.0


def test_tune_knn_can_predict():
    X, y = data()
    gs = _f("tune_knn")(X, y)
    preds = gs.predict(X[:7])
    assert len(preds) == 7
