#!/usr/bin/env python 

import sys, os, re
import argparse
import compare_LSDALTON_outputs as compLS
import plotly_boxPlot_RMSgradDiff_benchmark_set
import tabulate_stats_benchmark_set
import plotly_gaussians_gradDiff_stats_benchmark_set


if __name__ == "__main__":
    ''' Heavy plot on plotly to show gradient difference elementwise!! '''
    # plotly_boxPlot_RMSgradDiff_benchmark_set.run()  

    ''' csv tables to share raw data'''
    tabulate_stats_benchmark_set.run()
    #plotly_gaussians_gradDiff_stats_benchmark_set.run()
