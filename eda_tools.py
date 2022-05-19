import numpy as np
import missingno as msno
import matplotlib.pyplot as plt
import seaborn as sns

def na_bar_plot(dataframe):
    fig, ax = plt.subplots(figsize = (18, 8))
    msno.bar(dataframe, ax=ax)
    ax.set_title("Ratio de complétude des variables", fontsize = 18, fontweight = "bold", pad=15)
    plt.show()

def easy_bar_plot(x, y, data, order=None, xlab=None, ylab=None, title=None, grid=True, 
                  values_over_bars=True, vob_offset=None, vob_rot=None, x_tick_rot=None, 
                  tight_layout=False, figsize=(18, 8)):
    
    fig, ax = plt.subplots(figsize = figsize)
    if order is None:
        order = np.sort(data[x].unique()) 
    sns.barplot(x=x, y=y, data=data, ax=ax, order=order)
    if xlab is not None:
        ax.set_xlabel(xlab, fontsize = 16, fontweight = "bold")
    if ylab is not None:
        ax.set_ylabel(ylab, fontsize = 16, fontweight = "bold")
    if title is not None:
        plt.suptitle(title, fontsize = 18, fontweight = "bold")

    if grid :
        plt.grid(b=True, which='major', axis='both', alpha = 0.3)
    
    if values_over_bars:
        if vob_offset is None:
            vob_offset = 0.015
        if vob_rot is None:
            vob_rot = 0
        if vob_rot > 0:
            ha="left"
        else:
            ha="center"
        pos=0
        for i, (q, val) in data.iterrows():
            if val > 0:
                ax.text(pos, val + vob_offset*data[y].max(), "{}".format(round(val)), 
                        ha=ha, fontsize = 12, fontweight = "bold", rotation=vob_rot, 
                       rotation_mode="anchor")
            pos += 1
    if x_tick_rot is not None:
        plt.xticks(rotation = x_tick_rot, ha="center")
    if tight_layout:
        fig.tight_layout()
    plt.show()
