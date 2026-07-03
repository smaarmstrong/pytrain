# sklearn: scale-then-classify pipeline

In `solution.py`, implement two functions.

```python
def build_pipeline():
    """Return an UNFITTED sklearn Pipeline of at least two steps:
    a feature scaler (e.g. StandardScaler) followed by a classifier
    (e.g. LogisticRegression(max_iter=1000)).

    The graded data has features on wildly different scales, so the
    scaler is not decoration."""

def split_fit_score(X, y):
    """Split X, y with train_test_split(test_size=0.25, random_state=0),
    fit build_pipeline() on the training portion only, and return the
    accuracy on the held-out test portion as a plain float."""
```

The grader calls these with a seeded synthetic classification set
(a few hundred rows, two classes) and requires test accuracy >= 0.75 —
comfortable for any reasonable scaler + classifier.

Example:

```python
>>> pipe = build_pipeline()
>>> pipe.fit(X_train, y_train).predict(X_test)   # standard estimator API
array([...])
>>> 0.75 <= split_fit_score(X, y) <= 1.0
True
```
