# -*- coding: utf-8 -*-

# Copyright (C) 2013 Michael Hogg

# This file is part of BMDanalyse - See LICENSE.txt for information on usage and redistribution

# Fix to ensure that the matplotlib legend updates whenever the user 
# makes any change to the curves

from matplotlib.backends.qt4_editor.figureoptions import *

def figure_edit(axes, parent=None):
    """Edit matplotlib figure options"""
    sep = (None, None) # separator

    has_curve = len(axes.get_lines()) > 0

    # Get / General
    xmin, xmax = axes.get_xlim()
    ymin, ymax = axes.get_ylim()
    general = [('Title', axes.get_title()),
               sep,
               (None, "<b>X-Axis</b>"),
               ('Min', xmin), ('Max', xmax),
               ('Label', axes.get_xlabel()),
               ('Scale', [axes.get_xscale(), 'linear', 'log']),
               sep,
               (None, "<b>Y-Axis</b>"),
               ('Min', ymin), ('Max', ymax),
               ('Label', axes.get_ylabel()),
               ('Scale', [axes.get_yscale(), 'linear', 'log'])
               ]

    if has_curve:
        # Get / Curves
        linedict = {}
        for line in axes.get_lines():
            label = line.get_label()
            if label == '_nolegend_':
                continue
            linedict[label] = line
        curves = []
        linestyles = LINESTYLES.items()
        markers = MARKERS.items()
        curvelabels = sorted(linedict.keys())
        for label in curvelabels:
            line = linedict[label]
            curvedata = [
                         ('Label', label),
                         sep,
                         (None, '<b>Line</b>'),
                         ('Style', [line.get_linestyle()] + linestyles),
                         ('Width', line.get_linewidth()),
                         ('Color', col2hex(line.get_color())),
                         sep,
                         (None, '<b>Marker</b>'),
                         ('Style', [line.get_marker()] + markers),
                         ('Size', line.get_markersize()),
                         ('Facecolor', col2hex(line.get_markerfacecolor())),
                         ('Edgecolor', col2hex(line.get_markeredgecolor())),
                         ]
            curves.append([curvedata, label, ""])

    datalist = [(general, "Axes", "")]
    if has_curve:
        datalist.append((curves, "Curves", ""))
        
    def apply_callback(data):
        """This function will be called to apply changes"""
        if has_curve:
            general, curves = data
        else:
            general, = data
            
        # Set / General
        title, xmin, xmax, xlabel, xscale, ymin, ymax, ylabel, yscale = general
        axes.set_xscale(xscale)
        axes.set_yscale(yscale)
        axes.set_title(title)
        axes.set_xlim(xmin, xmax)
        axes.set_xlabel(xlabel)
        axes.set_ylim(ymin, ymax)
        axes.set_ylabel(ylabel)
        
        if has_curve:
            # Set / Curves
            for index, curve in enumerate(curves):
                line = linedict[curvelabels[index]]
                label, linestyle, linewidth, color, \
                    marker, markersize, markerfacecolor, markeredgecolor = curve
                line.set_label(label)
                line.set_linestyle(linestyle)
                line.set_linewidth(linewidth)
                line.set_color(color)
                if marker is not 'none':
                    line.set_marker(marker)
                    line.set_markersize(markersize)
                    line.set_markerfacecolor(markerfacecolor)
                    line.set_markeredgecolor(markeredgecolor) 

    ### Fix begins here - By Michael Hogg 14/2/2013. Adopted from Dave Giesen's fix on Nabble   
            # Recalculate the color and style of legend artists.  Don't think this  
            # would work in all circumstances. But it does work for a figure with a  
            # single subplot which has multiple lines
            figure = axes.get_figure()
            all_axes = figure.get_axes()
            for axesSubplot in all_axes:
                legend = axesSubplot.get_legend()
                handles, labels = axesSubplot.get_legend_handles_labels()
                # Location and title are altered by the _init_legend_box 
                # function, so preserve the current values
                loc   = legend._loc
                title = legend.get_title().get_text()
                if title == 'None': title = None
                # This function recalculates colors and styles
                legend._init_legend_box(handles, labels)
                legend._loc = loc
                legend.set_title(title)
    ### Fix ends here
            
        # Redraw
        figure = axes.get_figure()
        figure.canvas.draw()
        
    data = formlayout.fedit(datalist, title="Figure options", parent=parent,
                            icon=get_icon('qt4_editor_options.svg'), apply=apply_callback)
    if data is not None:
        apply_callback(data)