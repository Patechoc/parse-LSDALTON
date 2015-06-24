#!/usr/bin/env python

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import plotly.plotly as py
from plotly.graph_objs import *
from decimal import *


def pdf(x, mean, var):
    """Probability density function of the Normal distribution"""
    std = math.sqrt(var)
    return 1 / (std * (math.sqrt(2 * math.pi))) * (math.e ** -(((x - mean) ** 2) / (2 * var)))

def pdf_values(mean, var, label=None, FROM_X=None, TO_X=None, NUMBER_OF_SAMPLES=None):
    """Plot the probability density function of
    the Normal distribution for the given mean and variance"""
    std = math.sqrt(var)
    context = Context(prec=2, rounding=ROUND_UP)
    if FROM_X == None:
        FROM_X = int(context.create_decimal_from_float(mean - 3.*std))
    if TO_X == None:
        TO_X   = int(context.create_decimal_from_float(mean + 3.*std))
    if NUMBER_OF_SAMPLES == None:
        NUMBER_OF_SAMPLES = 1000 # The more samples the smoother :)
    # Take NUMBER_OF_SAMPLES numbers evenly from [FROM_X, TO_X]
    xs = np.linspace(FROM_X, TO_X, NUMBER_OF_SAMPLES)
    ys = [pdf(x, mean, var) for x in xs]
    #label = r"$\mu={0: .1f}, \sigma^2={1: .1f}$".format(mean, var)
    #label = "mu={0: .1f}, sigma={1: .1f}".format(mean, var)
    name = "$\mu = {0:+.2E}, \quad \sigma^2 = {1:+.2E}$".format(mean, var)
    if label != None:
        name = label
    return [xs, ys, name]


def plot_Matplotlib(gaussians, title=None, FROM_X=None, TO_X=None, xlabel=None):
    # gaussians = [{'mean':2.1e-05, 'variance':9.6e-10, 'name':'test1'},
    #              {'mean':0., 'variance':1.},
    #              {'mean':0., 'variance':5.},
    #              {'mean':-2., 'variance':0.5}]
    LINE_WIDTH = 3
    xMinD = gaussians[0]["mean"]
    xMaxD = gaussians[0]["mean"]
    for gaussian in gaussians:
        std = math.sqrt(gaussian["variance"])
        xMinD = min(xMinD, gaussian["mean"]-3.*std)
        xMaxD = max(xMaxD, gaussian["mean"]+3.*std)

    # context = Context(prec=2, rounding=ROUND_UP)
    # print "xMinD, xMaxD\n"
    # print "{}\t{}\n".format(xMinD, xMaxD)
    # xMinI = int(context.create_decimal_from_float(xMinD))
    # xMaxI = int(context.create_decimal_from_float(xMaxD))
    # print "xMinI, xMaxI\n"
    # print "{}\t{}\n".format(xMinI, xMaxI)
    # #print xMax
    if FROM_X == None:
        FROM_X = xMinD
    if TO_X == None:
        TO_X   = xMaxD
    ### Plot the curves with different means and variances
    fig, ax = plt.subplots()
    if xlabel != None:
        ax.set_xlabel(xlabel)
    for gaussian in gaussians:
        if 'name' in gaussian.keys():
            [xs, ys, label] = pdf_values(gaussian["mean"],
                                         gaussian["variance"],
                                         label=gaussian["name"],
                                         FROM_X=FROM_X, TO_X=TO_X)
        else:
            [xs, ys, label] = pdf_values(gaussian["mean"],
                                         gaussian["variance"],
                                         FROM_X=FROM_X, TO_X=TO_X)

        ax.tick_params(axis='y',
                       left='off',
                       right='off',
                       labelleft='off',
                       labelright='off',
                       direction='out',
                       length=6,
                       width=2,
                       colors='r')
        ax.plot(xs, ys, label=label, linewidth=LINE_WIDTH)
        #    # Configure the x-axis size
    plt.xlim((FROM_X, TO_X))
    #plt.ticklabel_format(axis='x', style='sci', scilimits=(-0,0))
    ax.get_xaxis().set_major_formatter(plt.LogFormatter(10,  labelOnlyBase=False))
    if title != None:
        #fig.suptitle(title, fontsize=20)
        fig.suptitle(title)
    #plt.xlabel('xlabel', fontsize=18)
    #plt.ylabel('ylabel', fontsize=16)
    plt.grid() # Toggle the axes grid
    plt.legend() # Show a legend
    # plt.show() # Show the actual plot
    #return fig
    return [fig, ax]


def plot_Plotly(gaussians, title=None, FROM_X=None, TO_X=None, xlabel=None):
    #py.sign_in('DemoAccount', 'lr1c37zw81')
    # Plot the curves with different means and variances
    lines = []
    #for gaussian in gaussians:
    #    lines.append(Scatter(x=res[0], y=res[1]) for res in pdf_values(gaussian["mean"], gaussian["variance"]))
    xMinD = gaussians[0]["mean"]
    xMaxD = gaussians[0]["mean"]
    for gaussian in gaussians:
        std = math.sqrt(gaussian["variance"])
        xMinD = min(xMinD, gaussian["mean"]-3.*std)
        xMaxD = max(xMaxD, gaussian["mean"]+3.*std)

    if FROM_X == None:
        FROM_X = xMinD
    if TO_X == None:
        TO_X   = xMaxD

    for gaussian in gaussians:
        if 'name' in gaussian.keys():
            [xs, ys, label] = pdf_values(gaussian["mean"],
                                         gaussian["variance"],
                                         label=gaussian["name"],
                                         FROM_X=FROM_X, TO_X=TO_X)
        else:
            [xs, ys, label] = pdf_values(gaussian["mean"],
                                         gaussian["variance"],
                                         FROM_X=FROM_X, TO_X=TO_X)

        lines.append(Scatter(x=xs, y=ys, name=label))
        #    lines = [ Scatter(x=res[0], y=res[1]) for res in pdf_values(gaussian["mean"], gaussian["variance"]) for gaussian in gaussians]
        #    #print lines
    titre = ""
    if title != None:
        titre = title

    data = Data(lines)
    layout = Layout(
        title = titre,
#        showlegend=True,
#        autosize=True,
#        width=1310,
#        height=712,
        xaxis=XAxis(
            range=[FROM_X, TO_X],
            exponentformat='E',
            # type='linear',
            # autorange=False,
            showlegend=True,
            showgrid=True,
            showline=False,
            # nticks=0.1,
            # ticks='',
            ticks='outside',
            # dtick=1
        ),
        yaxis=YAxis(
            #range=[-0.01, 1.01],
            type='linear',
            autorange=True,
            showgrid=False,
            showline=False,
            # nticks=0.1,
            # dtick=0.1
            ticks='',
            showticklabels=False,
        ),
        # legend=Legend(
        #     borderwidth=0,
        #     xanchor='auto'
        # )
    )

    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename=titre)
    return plot_url


if __name__ == "__main__":
    gaussians = [{'mean':2.1e-05, 'variance':9.6e-10, 'name':'test1'},
                 {'mean':0., 'variance':1.},
                 {'mean':0., 'variance':5.},
                 {'mean':-2., 'variance':0.5}]
    # [fig, ax] = plot_Matplotlib(gaussians,
    #                 title="xLim from -5 to 5",
    #                 FROM_X=-5,
    #                 TO_X=5,
    #                 xlabel="some distance (in $\AA$)")
    [fig, ax] = plot_Matplotlib(gaussians, title="no specific x-limits")
    plt.show()

    plot_Plotly(gaussians, title="Titre TEST")
