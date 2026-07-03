import pytest
from sklearn.datasets import make_classification
from sklearn.pipeline import Pipeline

from pytrain_grader import load_solution, get_attr


def _f(name):
    return get_attr(load_solution(), name)


def data():
    X, y = make_classification(
        n_samples=400,
        n_features=8,
        n_informative=5,
        n_redundant=1,
        class_sep=1.5,
        random_state=42,
    )
    # Wildly different feature scales: a pipeline without a scaler suffers.
    X = X.copy()
    X[:, 0] *= 1000.0
    X[:, 3] *= 250.0
    return X, y


def test_build_pipeline_is_a_pipeline():
    pipe = _f("build_pipeline")()
    assert isinstance(pipe, Pipeline), "build_pipeline must return a sklearn Pipeline"
    assert len(pipe.steps) >= 2, "the pipeline needs a scaler step AND a model step"


def test_pipeline_is_unfitted_and_trainable():
    X, y = data()
    pipe = _f("build_pipeline")()
    pipe.fit(X, y)
    preds = pipe.predict(X[:10])
    assert len(preds) == 10
    assert set(int(p) for p in preds) <= {0, 1}


def test_pipeline_fits_well_despite_scales():
    X, y = data()
    pipe = _f("build_pipeline")()
    pipe.fit(X, y)
    assert float(pipe.score(X, y)) >= 0.8


def test_split_fit_score_threshold():
    X, y = data()
    score = _f("split_fit_score")(X, y)
    assert isinstance(float(score), float)
    assert 0.75 <= float(score) <= 1.0


def test_split_fit_score_is_deterministic():
    X, y = data()
    f = _f("split_fit_score")
    assert float(f(X, y)) == pytest.approx(float(f(X, y)))
