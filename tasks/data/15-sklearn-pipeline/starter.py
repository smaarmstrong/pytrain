from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def build_pipeline():
    """Unfitted Pipeline: scaler -> classifier."""
    raise NotImplementedError


def split_fit_score(X, y):
    """Split (test_size=0.25, random_state=0), fit on train, return test accuracy."""
    raise NotImplementedError
