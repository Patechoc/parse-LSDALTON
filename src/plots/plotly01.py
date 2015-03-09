#!/usr/bin/env python

import numpy as np
import plotly.plotly as py
from datetime import date
from plotly.graph_objs import *


today = date.today()
today_str = today.isoformat()


bleu  ="rgb( 31,119,180)" ## "color":"rgb(54,144,192)",
orange="rgb(255,127, 14)"
vert  ="rgb( 44,160, 40)"
rouge ="rgb(214, 39, 40)"
violet="rgb(148,103,189)"
colors=[bleu, orange, vert, rouge, violet]





## DATA

y0 = np.random.randn(50)
y1 = np.random.randn(50)+1

trace1 = Box(
    y=y0
)
trace4 = Box(
    y=y1,
    x='molecule 2'    
)

x = ['molecule 1', 'molecule 1', 'molecule 1', 'molecule 1', 'molecule 1', 
     'molecule 2', 'molecule 2', 'molecule 2', 'molecule 2', 'molecule 2']


trace1 = Box(
    y=[0.2, 0.2, 0.6, 1.0, 0.5, 0.4, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3], ## diff. gradient elems 
    x=x,## nb. atoms in molecule, ou molName
    name='KT3X', # ADMM functional combined with basis set choice
    marker=Marker(
        color='#3D9970'),
    boxpoints='all',
    jitter=0.4,
    pointpos=-0.0
)
trace2 = Box(
    y=[0.6, 0.7, 0.3, 0.6, 0.0, 0.5, 0.7, 0.9, 0.5, 0.8, 0.7, 0.2],
    x=x,
    name='B88X',
    marker=Marker(
        color='#FF4136'
    ),
    boxpoints='all',
    jitter=0.4,
    pointpos=-0.0

)
trace3 = Box(
    y=[0.1, 0.3, 0.1, 0.9, 0.6, 0.6, 0.9, 1.0, 0.3, 0.6, 0.8, 0.5],
    x=x,
    name='OPTX',
    marker=Marker(
        color='#FF851B'
    ),
    boxpoints='all',
    jitter=0.4,
    pointpos=-0.0
)



# trace2 = Scatter(
#     x=[0, 1, 2], # nb-atoms / name molecule
#     y=[3, 4, 6], # avg. difference over gradient difference
#     mode = 'markers',
#     name = 'monTrace2',
#     error_y=ErrorY(
#         type='data',
#         array=[1, 2, 3], # RMS norm
#         visible=True),
#     marker=Marker(
#         #color='#85144B',
#         size=8, )
# )

data = Data([trace1, trace2, trace3])

layout = Layout(
    title='ADMM impact on molecular gradient'+today_str,
    xaxis=XAxis(
        title='set of molecules',
        # titlefont=Font(
        #     family='Courier New, monospace',
        #     size=18,
        #     color='#7f7f7f'
        # )
    ),
    yaxis=YAxis(
        title='Errors in molecular gradient',
        zeroline=False,
        # titlefont=Font(
        #     family='Courier New, monospace',
        #     size=18,
        #     color='#7f7f7f'
        # )
    ),
    boxmode='group',
)


fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='ADMM2 Gradient differences')
