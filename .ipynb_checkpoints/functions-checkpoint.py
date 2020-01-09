import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
import matplotlib.cm as cm

def plot_count_rating(words,ratings,counts):
    labels = words
    men_means = ratings
    women_means = counts

    x = np.arange(len(words))  # the label locations
    width = 0.35  # the width of the bars

    # Get a color map
    my_cmap = cm.get_cmap('Greens')

    # Get normalize function (takes data in range [vmin, vmax] -> [0, 1])
    my_norm = Normalize(vmin=1, vmax=5)

    fig, ax = plt.subplots(figsize=(16,9))
    # rects1 = ax.bar(x - width/2, men_means, width, label='Rating')
    rects2 = ax.bar(x + width/2, women_means, width, label='Ratings',color=my_cmap(my_norm(men_means)))

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Counts')
    ax.set_title('Word by rating and count')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()


    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


    # autolabel(rects1)
    autolabel(rects2)
    fig.tight_layout()

    plt.show()