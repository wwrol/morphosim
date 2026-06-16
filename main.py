from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import sim
import numpy as np
import pandas as pd

app = Dash(__name__)


app.layout = html.Div([
    html.H4('SIM'),
    dcc.Loading(dcc.Graph(id="graph"), type="cube")
])


ps = sim.ParticleSystem()
ps.add_source(np.array([0,0]),1)

df = pd.DataFrame()
SIM_LENGTH = 10000 #ms
STEP_SIZE = 10 #ms

for t in range(0,SIM_LENGTH,STEP_SIZE):
    ps.step(STEP_SIZE)
    df.loc[t,"time"] = t
    df.loc[t,"x"]=ps.xs[:0]
    df.loc[t,"y"]=ps.xs[:1]


@app.callback(
    Output("graph", "figure"))
def display_animated_graph():
    animation = px.scatter(
        df, x="x", y="y", animation_frame="time",size=10,
        range_x=[-10,10], range_y=[-10,10])
    return animation


app.run(debug=True)