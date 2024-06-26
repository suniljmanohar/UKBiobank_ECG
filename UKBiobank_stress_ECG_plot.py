import numpy as np
from matplotlib import pyplot as plt


""" Copyright 2023 Dr Sunil Manohar (sunil.manohar@cardiov.ox.ac.uk) """


V_SCALE = 5  # expected voltage scale in uV
T_SCALE = 0.002  # expected time scale in seconds (= 1/sampling_frequency)


def format_ecg_plot(graph, v_rescale=1, t_rescale=1, grids=True, minor_ticks=True):
    """ adds formatting to a plotted ECG to make it look conventional """
    v_min, v_max = -400 / v_rescale, 400 / v_rescale  # standard ECG graph is -400, 400
    graph.set_ylim([v_min, v_max])
    if grids:
        graph.minorticks_on()
        major_ticks_x = np.arange(graph.get_xlim()[0], graph.get_xlim()[1], 0.2 / T_SCALE/ t_rescale)
        minor_ticks_x = np.arange(graph.get_xlim()[0], graph.get_xlim()[1], 0.04 / T_SCALE/ t_rescale)
        big_squares = int((v_max - v_min) / 100)
        major_ticks_y = np.linspace(v_min, v_max, big_squares + 1)
        minor_ticks_y = np.linspace(v_min, v_max, 5 * big_squares + 1)
        graph.grid(which='major', linestyle='-', linewidth='0.5', color='red', alpha=0.6)
        graph.set_xticks(major_ticks_x)
        graph.set_yticks(major_ticks_y)
        if minor_ticks:
            graph.grid(which='minor', linestyle=':', linewidth='0.5', color='red', alpha=0.3)
            graph.set_xticks(minor_ticks_x, minor=True)
            graph.set_yticks(minor_ticks_y, minor=True)
        graph.tick_params(which='both', top=False, left=False, right=False, bottom=False)
    graph.set_yticklabels([])
    graph.set_xticklabels([])
    graph.set_axisbelow(True)


def plot_iso_ecg(iso_leads, md, save_to='', display=False):
    """ plots 12 isolated complexes in conventional ECG layout, no rhythm strip"""
    fig = plt.figure(figsize=(4, 8))
    grid = plt.GridSpec(3, 1, wspace=0)
    axs = [None for j in range(3)]
    for x in range(3):
        if x > 0:
            axs[x] = fig.add_subplot(grid[x, 0], sharey=axs[0])
        else:
            axs[x] = fig.add_subplot(grid[x, 0])
        axs[x].plot(iso_leads[x], 'k-')
        axs[x].set_title(md['lead order'][x])
        format_ecg_plot(axs[x])
    plt.suptitle(md['filename'])

    if save_to != '': plt.savefig(save_to + ' median.svg')
    if display: plt.show()
    plt.close()


def plot_long_ecg(lead_data, md, display=False, save_to=''):
    """ plots 12 long ECG leads vertically ordered. ecg[0] is np array of shape (n_leads, lead_length) with ECG waveforms.
    ecg[1] is ECG metadata dict containing 'filename', 'lead order' and 'r waves'. Returns None """

    n = lead_data.shape[0]
    fig = plt.figure(figsize=(10, 4))
    grid = plt.GridSpec(n, 1, hspace=0, wspace=0)
    axs = [None for i in range(n)]

    for i in range(n):
        axs[i] = fig.add_subplot(grid[i, 0])
        axs[i].plot(lead_data[i], 'k-', linewidth=0.7)
        axs[i].set_title(md['lead order'][i])
        format_ecg_plot(axs[i])

    fig.suptitle(md['filename'])
    if save_to != '': plt.savefig(save_to)
    if display: plt.show()
    plt.close()
