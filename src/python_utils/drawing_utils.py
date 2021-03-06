#!/usr/bin/env python

############################################################################
# Copyright (c) 2011-2013 Saint-Petersburg Academic University
# All Rights Reserved
# See file LICENSE for details.
############################################################################

import sys
import getopt
import os
import matplotlib
matplotlib.use('Agg')
import pylab
import numpy 
import matplotlib.pyplot as plt
from pylab import *

class GraphicalData:
    all_keys = list()
    nt_keys = list()
    max_cluster = 0
    min_cluster = sys.maxsize

class GraphicalSetting:
    xlabel = ""
    ylabel = ""
    title = ""
    output_filename = ""
    bins = ""
    label = ""
    histtype = ""
    xlog_scale = False
    ylog_scale = False
    draw_legend = False
    colors = ""
    legend_loc = 'upper right'
    show_xaxis = True
    show_yaxis = True
    xmin_shift = 0
    xmax_shift = 0
    ymin_shift = 0
    ymax_shift = 0
    align = ""
    marker = ""
    linestyle = ""

def ReadIntGraphicalData(filename):
    src = open(filename, "r")
    data = GraphicalData()
    data.all_keys = list()
    data.nt_keys = list()
    for line in src.readlines():
        new_size = int(line.strip('\n'))
        data.max_cluster = max(data.max_cluster, new_size)
        data.min_cluster = min(data.min_cluster, new_size)
        data.all_keys.append(new_size)
        if new_size > 1:
            data.nt_keys.append(new_size)
    src.close()
    return data

def ReadFloatGraphicalData(filename):
    src = open(filename, "r")
    data = GraphicalData()
    data.all_keys = list()
    data.nt_keys = list()
    for line in src.readlines():
        new_size = float(line)
        data.max_cluster = max(data.max_cluster, new_size)
        data.min_cluster = min(data.min_cluster, new_size)
        data.all_keys.append(new_size)
        if new_size > 1:
            data.nt_keys.append(new_size)
    src.close()
    return data

def GetGraphicalSettings(xlabel = "", ylabel = "", title = "", output_filename = "figure.png", bins = 100, label = "", histtype = "bar", xlog_scale = False, ylog_scale = False, draw_legend = False, colors = "", legend_loc = 'upper right', show_xaxis = True, show_yaxis = True, xmin_shift = 0, xmax_shift = 0, ymin_shift = 0, ymax_shift = 0, align = "mid", marker = ".", linestyle = ""):
    setting = GraphicalSetting()
    setting.xlabel = xlabel
    setting.ylabel = ylabel
    setting.title = title
    setting.output_filename = output_filename
    setting.histtype = histtype
    setting.xlog_scale = xlog_scale
    setting.ylog_scale = ylog_scale
    setting.label = label
    setting.bins = bins
    setting.draw_legend = draw_legend
    setting.colors = colors
    setting.legend_loc = legend_loc
    setting.show_xaxis = show_xaxis
    setting.show_yaxis = show_yaxis
    setting.xmin_shift = xmin_shift
    setting.xmax_shift = xmax_shift
    setting.ymin_shift = ymin_shift
    setting.ymax_shift = ymax_shift
    setting.align = align
    setting.marker = marker
    setting.linestyle = linestyle
    return setting

def GetMaxBinsNumber(labels_count):
    return 90 / labels_count

def DrawHistogram(keys, histogram_setting):
    n = 0
    bins = []
    patches = []

    if len(keys) == 0:
        print("Histogram is empty!")
        return

    matplotlib.rc('xtick', labelsize=14) 
    matplotlib.rc('ytick', labelsize=14) 

    if histogram_setting.colors != "":
        n, bins, patches = pylab.hist(keys, histtype = histogram_setting.histtype, bins = histogram_setting.bins, label = histogram_setting.label, color = histogram_setting.colors, cumulative=False, linewidth=1)
    else:
        n, bins, patches = pylab.hist(keys, histtype = histogram_setting.histtype, bins = histogram_setting.bins, label = histogram_setting.label, cumulative=False, linewidth=1)
    
    if histogram_setting.xlog_scale:
        pylab.gca().set_xscale("log")    
    if histogram_setting.ylog_scale:
        pylab.gca().set_yscale("log")
    if histogram_setting.draw_legend:
        pylab.legend(loc = histogram_setting.legend_loc)
    plt.xlabel(histogram_setting.xlabel, fontsize = 16)
    plt.ylabel(histogram_setting.ylabel, fontsize = 16)
    plt.title(histogram_setting.title, fontsize = 16)
    plt.savefig(histogram_setting.output_filename)
    plt.gcf().clear()    

    return n, bins, patches

def DrawClusterSizesHist(histograms, histlabel, basename):
    max_cluster = 0
    nt_keys = list()
    all_keys = list()
    for h in histograms:
        max_cluster = max(max_cluster, h.max_cluster)
        nt_keys.append(h.nt_keys)
        all_keys.append(h.all_keys)

    hist_fname1 = basename + "comparative_nt_clusters_sizes.png"

    setting_nt = GetGraphicalSettings(xlabel = 'Clusters size', ylabel = 'Clusters number', title = "", output_filename = hist_fname1, bins = max_cluster / 2, label = histlabel, histtype = 'bar', xlog_scale = True, ylog_scale = False, draw_legend = True)  
    DrawHistogram(nt_keys, setting_nt)

    hist_fname2 = basename + "comparative_all_clusters_sizes.png"

    setting_all = GetGraphicalSettings(xlabel = 'Clusters size', ylabel = 'Clusters number', title = "", output_filename = hist_fname2, bins = max_cluster / 2, label = histlabel, histtype = 'bar', xlog_scale = True, ylog_scale = False, draw_legend = True)
    DrawHistogram(all_keys, setting_all)

    return [hist_fname1, hist_fname2]

def MaxValue(x) :
    x_max = 0
    for i in range(0, len(x)):
        x_max = max(x_max, x[i])
    return x_max

def MinValue(x) :
    x_min = sys.maxsize
    for i in range(0, len(x)):
        x_min = min(x_min, x[i])
    return x_min

def AverageValue(x):
    x_avg = 0
    for i in range(len(x)):
        x_avg += x[i]
    return x_avg / len(x)

def DrawMultiplePlot(x, y, setting):

    from scipy.interpolate import spline

    x_max = 0
    x_min = sys.maxsize
    for i in range(0, len(x)):
        x_max = max(x_max, MaxValue(x[i]))
        x_min = min(x_min, MinValue(x[i]))

    y_max = 0
    y_min = sys.maxsize
    for i in range(0, len(y)):
        y_max = max(y_max, MaxValue(y[i]))
        y_min = min(y_min, MinValue(y[i]))

    for i in range(0, len(x)):
        xnew = x[i] #numpy.linspace(MinValue(x[i]), MaxValue(x[i]), 300)
        ynew = y[i] #spline(x[i], y[i], xnew)
        if setting.colors != "":
            pylab.plot(xnew, ynew, color = setting.colors[i], label = setting.label[i])
        else:            
            pylab.plot(xnew, ynew, label = setting.label[i])
        matplotlib.pyplot.xlim(xmin = x_min - 1, xmax = x_max + 1)
    pylab.grid(True, which="both")

    pylab.xlim([x_min - setting.xmin_shift, x_max + setting.xmax_shift])
    pylab.ylim([y_min - setting.ymin_shift, y_max + setting.ymax_shift])

    if setting.xlog_scale:
        pylab.gca().set_xscale("log")
    if setting.ylog_scale:
        pylab.gca().set_yscale('log')
    if setting.draw_legend:
        pylab.legend(loc = setting.legend_loc)

    frame = plt.gca()

    frame.axes.get_yaxis().set_visible(setting.show_yaxis)
    frame.axes.get_xaxis().set_visible(setting.show_xaxis)

    plt.xlabel(setting.xlabel)
    plt.ylabel(setting.ylabel)
    plt.title(setting.title)
    plt.savefig(setting.output_filename)
    plt.gcf().clear()   

def DrawPlot(x, y, setting):

    matplotlib.rc('xtick', labelsize=14) 
    matplotlib.rc('ytick', labelsize=14) 
    if setting.colors != "":
        pylab.plot(x, y, setting.marker, color = setting.colors, label = setting.label)
    else:            
        pylab.plot(x, y, setting.marker, label = setting.label) 
    if setting.xlog_scale:        
        pylab.gca().set_xscale("log")
    if setting.ylog_scale:
        pylab.gca().set_yscale('log')
    if setting.draw_legend:
        pylab.legend(loc = setting.legend_loc)
    #matplotlib.pyplot.xlim(xmin = MinValue(x), xmax = MaxValue(x))

    frame = plt.gca()

    frame.axes.get_yaxis().set_visible(setting.show_yaxis)
    frame.axes.get_xaxis().set_visible(setting.show_xaxis)

    plt.xlabel(setting.xlabel, fontsize = 16)
    plt.ylabel(setting.ylabel, fontsize = 16)
    plt.title(setting.title, fontsize = 16)

    plt.savefig(setting.output_filename)
    plt.gcf().clear()   

def GetListByThreshold(item_list, thresh):
    return [item for item in item_list if item >= thresh]

def DrawVariuosClusterSizesHist(histograms, histlabel, size_thresholds, basename):
    if len(histograms) != len(histlabel):
        print("ERROR: # of labels != # of histograms")
        sys.exit(1)

    max_cluster = 0
    for h in histograms:
        max_cluster = max(max_cluster, h.max_cluster)

    output_fnames = list()
    for size in size_thresholds:
        hist_fname = basename + "_comp_hist_clusters_greater" + str(size) + ".png"
        keys = list()
        for h in histograms:
            keys.append(GetListByThreshold(h.all_keys, size))
        
        bins = (max_cluster - size) / 10
        xlog_scale = True
        if size >= 20:
            bins = (max_cluster - size) / 20
        if size >= 50:
            xlog_scale = False
            bins = (max_cluster - size) / 150

        settings = GetGraphicalSettings(xlabel = "Clusters size (>" + str(size) + ")", ylabel = 'Clusters number', title = "", output_filename = hist_fname, bins = bins, label = histlabel, histtype = 'bar', xlog_scale = xlog_scale, ylog_scale = False, draw_legend = True, legend_loc = 'lower right')  
        DrawHistogram(keys, settings)
        output_fnames.append(hist_fname)
 
    return output_fnames

def DrawSomaticMutations(X, Y, cdrs, settings):
    max_y = 0
    for y in Y:
        max_y = max(max_y, MaxValue(y))
    max_y += 1

    cdr_color = "#EFBEBE"
    # cdr1
    gca().add_patch(Rectangle((cdrs[0], 0), cdrs[1] - cdrs[0], max_y, facecolor= cdr_color, lw = 0))

    # cdr2
    gca().add_patch(Rectangle((cdrs[2], 0), cdrs[3] - cdrs[2], max_y, facecolor= cdr_color, lw = 0))

    # cdr3
    gca().add_patch(Rectangle((cdrs[4], 0), cdrs[5] - cdrs[4], max_y, facecolor= cdr_color, lw = 0))
    
    DrawMultiplePlot(X, Y, settings)

def DrawMutationHistogram(pos, settings, chain_type = "HC"):
    cdr1_start = 0.25
    cdr1_end = 0.3
    cdr2_start = 0.41
    cdr2_end = 0.54
    cdr3_start = 0.79
    cdr3_end = .86

    if chain_type == 'LC':
        cdr1_start = 0.23
        cdr1_end = 0.29
        cdr2_start = 0.41
        cdr2_end = 0.49
        cdr3_start = 0.77
        cdr3_end = .86

    n, bins, patches = DrawHistogram(pos, settings)
    cdr_color = "#EFBEBE"
    plt.gca().add_patch(Rectangle((cdr1_start, 0), cdr1_end - cdr1_start, MaxValue(n) + 2, facecolor= cdr_color, lw = 0))
    plt.gca().add_patch(Rectangle((cdr2_start, 0), cdr2_end - cdr2_start, MaxValue(n) + 2, facecolor= cdr_color, lw = 0))
    plt.gca().add_patch(Rectangle((cdr3_start, 0), cdr3_end - cdr3_start, MaxValue(n) + 2, facecolor= cdr_color, lw = 0))
    DrawHistogram(pos, settings)

def DrawIdentityPercentageDistribution(histogram, histname):
    if not histogram:
        return
    bins = min(GetMaxBinsNumber(1), int((max(histogram) - min(histogram)) * 10))
    if bins == 0:
        bins = 1
    settings = GetGraphicalSettings(xlabel = 'Cluster identity, %', ylabel = 'Cluster number', 
        title = "", output_filename = histname, bins = bins, 
        histtype = 'bar', xlog_scale = False, ylog_scale = False, draw_legend = False, align = "left")
    DrawHistogram(histogram, settings)

def DrawIdentityToLengthDistribution(perc_identity, cluster_length, plotname):
    settings = GetGraphicalSettings(xlabel = 'Cluster identity, %', ylabel = 'Cluster length',
        title = "", output_filename = plotname,
        xlog_scale = False, ylog_scale = False, draw_legend = False, marker = "o", linestyle = "None")
    DrawPlot(perc_identity, cluster_length, settings)

def DrawAnyClusterSizesHist(histograms, histlabel, histname):
    if not any(histograms):
        return
    max_cluster = max(max(histograms[i]) for i in range(len(histograms)) if histograms[i])
    bins = min(GetMaxBinsNumber(len(histograms)), max_cluster / 2)
    if bins == 0:
        bins = 1
    settings_all = GetGraphicalSettings(xlabel = 'Cluster size', ylabel = 'Cluster number', 
        title = "", output_filename = histname, bins = bins, label = histlabel, 
        histtype = 'bar', xlog_scale = False, ylog_scale = False, draw_legend = True)
    DrawHistogram(histograms, settings_all)

def DrawClusterLengthsHist(histograms, histlabel, histname):
    if not any(histograms):
        return
    min_length = min(min(a) for a in histograms)
    max_length = max(max(a) for a in histograms)
    bins = min(GetMaxBinsNumber(len(histograms)), (max_length - min_length) / 10)
    settings_all = GetGraphicalSettings(xlabel = 'Cluster length', ylabel = 'Cluster number', 
        title = "", output_filename = histname, bins = bins, label = histlabel, 
        histtype = 'bar', xlog_scale = False, ylog_scale = False, draw_legend = True)
    DrawHistogram(histograms, settings_all)

def DrawClusterGroupsBarChart(data, labels, chartname):
    ind = numpy.arange(len(data[0]))
    width = 0.3
    colors = ["blue", "orange", "red"]
    fig, ax = plt.subplots()
    rects = [None] * len(labels)
    for i in range(len(data)):
        rects[i] = ax.bar(ind + width * i, data[i], width, color = colors[i])
    
    ax.set_ylabel('Cluster number')
    ax.set_xlabel('Shared percent')
    ax.set_xticks(ind + width * len(labels) / 2)
    ax.set_xticklabels([str(i * 10) + '%' for i in range(5, 11)])

    ax.legend([r[0] for r in rects], labels, loc = 'upper left')
    plt.savefig(chartname)
    plt.gcf().clear()
