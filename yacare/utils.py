import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def norm_nrg(a_):
    """
    Helper function for plot_registration()

    From caimain.base.rois by agiovann
    """
    a = a_.copy()
    dims = a.shape
    a = a.reshape(-1, order='F')
    indx = np.argsort(a, axis=None)[::-1]
    cumEn = np.cumsum(a.flatten()[indx]**2)
    cumEn /= cumEn[-1]
    a = np.zeros(np.prod(dims))
    a[indx] = cumEn
    return a.reshape(dims, order='F')


def plot_registration(spatial, matches, non_matches, template1,
                      template2, level=0.98,
                      percentile_lims = [50, 99], cmap='gray',
                      contour_colors = ('r','g'), contour_widths=(2,1),
                      figsize=(6,6),
                      text_size=12):
    """
    Show registration of components between sessions using output of register_ROIs()
    Adapted from caiman.base.rois.register_ROIs() by agiovann

    spatial: [A1, A2_aligned]
    matches: list of matches1, 2
    non_matches: list of non_matches 1, 2
    template1 is Cn as in register_ROIs
    template2 (None default) is if you want to plot second template in a second window for reference.
    level is for plotting contours
    percentile_lims (for getting limits of plot)-- often 99 to 99.9
    contour colors/widths are for the two sessions



    To consider:
        improve documentation
        Add contours to second template
    """
    color1 = contour_colors[0]
    color2 = contour_colors[1]
    width1 = contour_widths[0]
    width2 = contour_widths[1]

    A1 = spatial[0]
    A2 = spatial[1]
    dims = template1.shape

    masks_1 = np.reshape(A1.toarray(), dims + (-1,), order='F').transpose(2, 0, 1)
    masks_2 = np.reshape(A2.toarray(), dims + (-1,), order='F').transpose(2, 0, 1)

    """
    First plot template one and matches
    """
    # get percentile limits for template1
    lp, hp = np.nanpercentile(template1, percentile_lims)
    plt.figure(figsize = figsize)
    ax1 = plt.subplot(121)
    plt.imshow(template1, vmin=lp, vmax=hp, cmap=cmap)

    [plt.contour(norm_nrg(mm), levels=[level], colors=color1, linewidths=width1) for mm in masks_1[matches[0]]]
    [plt.contour(norm_nrg(mm), levels=[level], colors=color2, linewidths=width2) for mm in masks_2[matches[1]]]
    lines = [Line2D([0], [0], color=c, linewidth=2) for c in contour_colors]
    labels = ['A1', 'A2']
    plt.legend(lines, labels, fontsize = text_size-2)
    plt.title('Template1 Matches', fontsize=text_size)
    plt.axis('off')

    """
    Next, plot template one and MISmatches
    """
    plt.subplot(122, sharex = ax1, sharey = ax1)

    plt.imshow(template1, vmin=lp, vmax=hp, cmap=cmap)
    [plt.contour(norm_nrg(mm), levels=[level], colors=color1, linewidths=width1) for mm in masks_1[non_matches[0]]]
    [plt.contour(norm_nrg(mm), levels=[level], colors=color2, linewidths=width2) for mm in masks_2[non_matches[1]]]
    plt.legend(lines, labels, fontsize = text_size-2)
    plt.title('Template1 Mismatches', fontsize=text_size)
    plt.axis('off')

    # """
    # Template two with matches
    # """
    # lp2, hp2 = np.nanpercentile(template2, percentile_lims)
    # plt.subplot(223, sharex=ax1, sharey = ax1)
    # plt.imshow(template2, vmin=lp2, vmax=hp2, cmap=cmap)
    #
    # [plt.contour(norm_nrg(mm), levels=[level], colors=color1, linewidths=width1) for mm in masks_1[matches[0]]]
    # [plt.contour(norm_nrg(mm), levels=[level], colors=color2, linewidths=width2) for mm in masks_2[matches[1]]]
    # lines = [Line2D([0], [0], color=c, linewidth=2) for c in contour_colors]
    # labels = ['A1', 'A2']
    # plt.legend(lines, labels, fontsize = text_size)
    # plt.title('T2 Matches', fontsize=text_size)
    # plt.axis('off')
    #
    # """
    # Next, plot template two and MISmatches
    # """
    # plt.subplot(224, sharex = ax1, sharey = ax1)
    #
    # plt.imshow(template2, vmin=lp2, vmax=hp2, cmap=cmap)
    # [plt.contour(norm_nrg(mm), levels=[level], colors=color1, linewidths=width1) for mm in masks_1[non_matches[0]]]
    # [plt.contour(norm_nrg(mm), levels=[level], colors=color2, linewidths=width2) for mm in masks_2[non_matches[1]]]
    # plt.legend(lines, labels, fontsize = text_size)
    # plt.title('T2 Mismatches', fontsize=text_size)
    # plt.axis('off')
    return
