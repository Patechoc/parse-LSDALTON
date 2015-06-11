#!/usr/bin/env python

import math
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
from plotly.graph_objs import *

LINE_WIDTH = 3

FROM_X = -6
TO_X = 6
NUMBER_OF_SAMPLES = 1000 # The more samples the smoother :)

def pdf(x, mean, var):
  """Probability density function of the Normal distribution"""
  std = math.sqrt(var)
  return 1 / (std * (math.sqrt(2 * math.pi))) * (math.e ** -(((x - mean) ** 2) / (2 * var)))

def pdf_values(mean, var, name=None):
  """Plot the probability density function of
  the Normal distribution for the given mean and variance"""
  # Take NUMBER_OF_SAMPLES numbers evenly from [FROM_X, TO_X]
  xs = np.linspace(FROM_X, TO_X, NUMBER_OF_SAMPLES)
  ys = [pdf(x, mean, var) for x in xs]
  #label = r"$\mu={0: .1f}, \sigma^2={1: .1f}$".format(mean, var)
  #label = "mu={0: .1f}, sigma={1: .1f}".format(mean, var)
  label = "$\mu = {0: .1f}, \sigma^2 = {1: .1f}$".format(mean, var)
  if name != None:
      label = name
  return [xs, ys, label]

def plot_Plotly(gaussians):
    #py.sign_in('DemoAccount', 'lr1c37zw81')
    # Plot the curves with different means and variances
    lines = []
    #for gaussian in gaussians:
    #    lines.append(Scatter(x=res[0], y=res[1]) for res in pdf_values(gaussian["mean"], gaussian["variance"]))
    for gaussian in gaussians:
        [xs, ys, label] = pdf_values(gaussian["mean"], gaussian["variance"])
        lines.append(Scatter(x=xs, y=ys, name=label))
        #    lines = [ Scatter(x=res[0], y=res[1]) for res in pdf_values(gaussian["mean"], gaussian["variance"]) for gaussian in gaussians]
        #    #print lines
    data = Data(lines)
    layout = Layout(
#        showlegend=True,
#        autosize=True,
#        width=1310,
#        height=712,
        xaxis=XAxis(
            range=[-6, 6],
            # type='linear',
            # autorange=False,
            # showline=False,
            # nticks=0.1,
            # ticks='',
            # dtick=1
        ),
        yaxis=YAxis(
            range=[-0.01, 1.01],
            # type='linear',
            # autorange=False,
            # showline=False,
            # nticks=0.1,
            # ticks='',
            # dtick=0.1
        ),
        # legend=Legend(
        #     borderwidth=0,
        #     xanchor='auto'
        # )
    )
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='Topology comparisons')


def plot_Matplotlib(gaussians):
    # Plot the curves with different means and variances
    fig, ax = plt.subplots()
    for gaussian in gaussians:
        [xs, ys, label] = pdf_values(gaussian["mean"], gaussian["variance"])
        ax.plot(xs, ys, label=label, linewidth=LINE_WIDTH)
    # Configure the x-axis size
    plt.xlim((FROM_X, TO_X))
    # Configure the y-axis size
    plt.ylim((-0.1, 1.1)) # Extend the y axis a bit to the top and bottom
    # Configure the x-axis labels
    plt.xticks(range(FROM_X + 1, TO_X)) # 1 tick for each integer in [FROM_X - 1, TO_X + 1]
    # Configure the y-axis labels to show values of [0, 1] with step size 0.1
    plt.yticks([i * 0.1 for i in xrange(11)])
    plt.grid() # Toggle the axes grid
    plt.legend() # Show a legend
    plt.show() # Show the actual plot

if __name__ == "__main__":
    gaussians = [{'mean':0., 'variance':0.2},
                 {'mean':0., 'variance':1.},
                 {'mean':0., 'variance':5.},
                 {'mean':-2., 'variance':0.5}]
    #plot_Matplotlib(gaussians)
    plot_Plotly(gaussians)
