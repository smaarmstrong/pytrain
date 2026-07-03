import matplotlib.pyplot as plt


def make_figure(x, y):
    fig, ax = plt.subplots()
    ax.plot(x, y, label="signal")
    ax.set_title("Signal over time")
    ax.set_xlabel("t")
    ax.set_ylabel("value")
    ax.legend()
    return fig
