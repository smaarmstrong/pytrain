import matplotlib.pyplot as plt


def make_dashboard(x, trend, volume):
    fig, (top, bottom) = plt.subplots(2, 1)
    top.plot(x, trend)
    top.set_title("Trend")
    top.set_ylabel("level")
    bottom.bar(x, volume)
    bottom.set_title("Volume")
    bottom.set_ylabel("count")
    return fig
