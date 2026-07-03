# sklearn: CV & a tiny grid search

In `solution.py`, implement two functions.

```python
def cv_mean_score(model, X, y):
    """The mean of 5-fold cross-validation accuracy for `model` on (X, y),
    as a plain float. Use cv=5 with its default (unshuffled) fold split so
    the result is reproducible."""

def tune_knn(X, y):
    """Grid-search a KNeighborsClassifier over exactly this tiny grid:

        n_neighbors in [1, 3, 5, 7, 9]

    using GridSearchCV with cv=5 and n_jobs=1. Fit it on (X, y) and return
    the FITTED GridSearchCV object (so .best_params_, .best_score_,
    .cv_results_ and .predict all work)."""
```

Example:

```python
>>> gs = tune_knn(X, y)
>>> gs.best_params_["n_neighbors"] in [1, 3, 5, 7, 9]
True
>>> len(gs.cv_results_["params"])   # one candidate per grid point
5
```
