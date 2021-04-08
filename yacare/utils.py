import numpy as np
import matplotlib.pyplot as plt

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


def plot_registration(spatial, matches, non_matches, template1, template2=None, level=0.98,
                      percentile_lims = [50, 99], cmap='gray',
                      contour_colors = ('r','g'), contour_widths=(2,1)):
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
        Add legend for first sessionn, second session.
        Might be nice to have template1/template 2 as a second row or second figure. 
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

    # get percentile limits for plot
    lp, hp = np.nanpercentile(template1, percentile_lims)



    if template2 is not None:
        plt.figure(figsize=(30, 10))
        ax1 = plt.subplot(131)
    else:
        plt.figure(figsize = (20,10))
        ax1 = plt.subplot(121)
    
    plt.imshow(template1, vmin=lp, vmax=hp, cmap=cmap)
    #print one
    
    [plt.contour(norm_nrg(mm), levels=[level], colors=color1, linewidths=width1) for mm in masks_1[matches[0]]]
    [plt.contour(norm_nrg(mm), levels=[level], colors=color2, linewidths=width2) for mm in masks_2[matches[1]]]
    plt.title('Matches')
    plt.axis('off')

    if template2 is not None:
        plt.subplot(132, sharex = ax1, sharey = ax1)        
    else:
        plt.subplot(122, sharex = ax1, sharey = ax1 )
    plt.imshow(template1, vmin=lp, vmax=hp, cmap=cmap)
    [plt.contour(norm_nrg(mm), levels=[level], colors=color1, linewidths=width1) for mm in masks_1[non_matches[0]]]
    [plt.contour(norm_nrg(mm), levels=[level], colors=color2, linewidths=width2) for mm in masks_2[non_matches[1]]]
    plt.title('Mismatches')
    plt.axis('off')
    
    if template2 is not None:
        lp2, hp2 = np.nanpercentile(template2, percentile_lims)
        plt.subplot(133, sharex=ax1, sharey = ax1)
        plt.imshow(template2, cmap=cmap)
    
    plt.tight_layout()

    return
