from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.neighbors import KNeighborsClassifier


def cv_mean_score(model, X, y):
    return float(cross_val_score(model, X, y, cv=5).mean())


def tune_knn(X, y):
    grid = {"n_neighbors": [1, 3, 5, 7, 9]}
    gs = GridSearchCV(KNeighborsClassifier(), grid, cv=5, n_jobs=1)
    gs.fit(X, y)
    return gs
