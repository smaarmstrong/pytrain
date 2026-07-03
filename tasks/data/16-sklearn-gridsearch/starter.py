from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.neighbors import KNeighborsClassifier


def cv_mean_score(model, X, y):
    """Mean 5-fold CV accuracy as a float."""
    raise NotImplementedError


def tune_knn(X, y):
    """Fitted GridSearchCV over n_neighbors=[1, 3, 5, 7, 9], cv=5, n_jobs=1."""
    raise NotImplementedError
