import streamlit as st
import numpy as np
import plotly.graph_objs as go
from noise import pnoise2

# Page configuration
st.set_page_config(layout="wide", page_icon="🌟")

# Centered Title with better typography
st.markdown("""
    <h1 style='font-family:system-ui; text-align:center; margin-top:-50px; 
    margin-bottom:30px; font-size:2.5rem; color:white'>
    ⚙️ Optimizer Playground
    </h1>
    """, unsafe_allow_html=True)

# Create columns with adjusted proportions
col1, col2, col3 = st.columns([1.5, 3.7, 1.75], gap="medium")

with col1:
    with st.container(border=True):
        st.text_area("Function", value="f(x, y) = Complex Terrain", height=100,
                     help="A procedurally generated terrain-like function")
        
        tags = ["Gradient Descent", "Newton's Method", "Simulated Annealing", "Genetic Algorithm"]
        selected_algo = st.selectbox('Algorithm', tags, index=0,
                                     help="Choose an optimization algorithm")
        learning_rate = st.slider('Learning Rate', 0.01, 1.0, 0.09, step=0.01,
                                  help="Choose a Learning Rate")
        
        x_min, x_max = st.slider('X Range', -200, 200, (-20, 20), step=20,
                                 help="Adjust the domain for X values")
        y_min, y_max = st.slider('Y Range', -200, 200, (-10, 10), step=1,
                                 help="Adjust the domain for Y values")
        resolution = st.slider('Grid Resolution', 20, 200, 100, step=10,
                               help="Number of points in each dimension")
        
        st.markdown("#### 🎨 Visualization Options")
        colorscale = st.selectbox('Color Scale', ['Viridis', 'Plasma', 'Inferno', 'Jet', 'Cividis'])
        show_contour = st.checkbox('Show Contour Projection', True)
        rotate_3d = st.checkbox('Enable 3D Rotation', True)

with col2:
    with st.container(border=False):
        num_points = resolution
        x_vals = np.linspace(x_min, x_max, num_points)
        y_vals = np.linspace(y_min, y_max, num_points)
        X, Y = np.meshgrid(x_vals, y_vals)

        Z = np.zeros_like(X)
        scale = 2.0
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0

        for i in range(num_points):
            for j in range(num_points):
                Z[i, j] = pnoise2(X[i, j] / scale, Y[i, j] / scale, octaves=octaves,
                                  persistence=persistence, lacunarity=lacunarity)
        
        Z = (Z - Z.min()) / (Z.max() - Z.min()) * 10  

        fig = go.Figure(data=[go.Surface(
            z=Z, x=X, y=Y, colorscale=colorscale.lower(),
            contours={'z': {'show': show_contour, 'usecolormap': True, 'highlightcolor': 'white'}},
            lighting={'ambient': 0.4, 'diffuse': 0.6, 'specular': 0.2},
            colorbar=dict(len=0.3, thickness=20, y=0.5, yanchor='middle')
        )])

        fig.update_layout(
            scene=dict(
                xaxis_title='X', yaxis_title='Y', zaxis_title='Loss',
                camera=dict(eye=dict(x=1.8, y=1.8, z=0.8) if rotate_3d else dict(x=0, y=0, z=2.5)),
                aspectratio=dict(x=1.3, y=1.3, z=0.7),
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=943
        )
        
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")

with col3:
    with st.container(border=True, height=800):
        st.markdown("#### <span style='color: blue;'>Meera</span>", unsafe_allow_html=True)
        st.markdown("# <p style='color:white; text-align:center;font-size:25px;'> Get your optimisation doubts cleared with good visualization </p>", unsafe_allow_html=True)
        st.container(height=400, border=False)
        
        prompt = st.chat_input(placeholder="Type a message...")
        if prompt:
            st.write("You:", prompt)
            st.write("Bot: Hello! How can I help you today?")
