import streamlit as st
import numpy as np
import plotly.graph_objs as go

# Page configuration
st.set_page_config(layout="wide", page_icon="🌟", page_title="Optimizer Playground")

# Custom CSS for enhanced aesthetics
st.markdown("""
<style>
.stContainer {
    border-radius: 15px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    background: linear-gradient(145deg, #1e1e2e, #16161f);
    transition: all 0.3s ease;
}
.stContainer:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 15px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# Title - Centered Up -> True
st.markdown("""
    <h1 style='font-family:system-ui; text-align:center; margin-top:-50px; 
    margin-bottom:30px; font-size:2.5rem; color:white'>
    ☀️ Optimizer Playground
    </h1>
    """, unsafe_allow_html=True)

# 2 columns with adjusted width
col1, col2 = st.columns([0.2, 0.8], gap="medium")

# Defining the content of col1 - Hyperparameters Zone
with col1:
    with st.container(border=True):
        # Algorithm selection using tags
        tags = ["Stochastic Gradient Descent", "SGD with momentum","Nestrov Momentum","Adam","RMSProp","AdaGrad"]
        selected_algo = st.selectbox('Algorithm', tags, index=0,
                                     help="Choose an optimization algorithm")
        learning_rate = st.slider('Learning Rate', 0.01, 1.0, 0.09, step=0.01,
                               help="Choose a Learning Rate")
        # Interactive controls
        x_min, x_max = st.slider('X Range', -200, 200, (-20, 20), step=20,
                               help="Adjust the domain for X values")
        y_min, y_max = st.slider('Y Range', -200, 200, (-10, 10), step=1,
                               help="Adjust the domain for Y values")
        resolution = st.slider('Grid Resolution', 20, 200, 100, step=10,
                             help="Number of points in each dimension")
        
        # Surface complexity control
        complexity = st.slider('Terrain Complexity', 1, 10, 5, 
                             help="Controls the overall complexity of the landscape")
        feature_type = st.multiselect('Feature Types', 
                                     ['Peaks', 'Valleys', 'Plateaus', 'Ridges', 'Saddles'],
                                     default=['Peaks', 'Valleys', 'Plateaus'],
                                     help="Select the types of features to include")
        
        init_type =st.selectbox('Initialisation Type',
                                  ['Random'],
                                  help='Select a initialisation method')
        
        # Visualization settings
        colorscale = st.selectbox('Color Scale', ['Viridis', 'Plasma', 'Inferno', 'Jet', 'Turbo'])
        show_contour = st.checkbox('Show Contour Projection', True)
        rotate_3d = st.checkbox('Enable 3D Rotation', True)
        
        # Random seed for reproducibility
        seed = st.number_input('Random Seed', 0, 10000, 42, 
                              help="Set a seed for reproducible landscapes")

# Defining the content of col2 - Graph Zone
with col2:
    # Playground Container with increased height and aesthetic styling
    with st.container(border=False, height=800):
        # Set random seed for reproducibility
        np.random.seed(seed)
        
        # Define grid
        num_points = resolution
        x_vals = np.linspace(x_min, x_max, num_points)
        y_vals = np.linspace(y_min, y_max, num_points)
        X, Y = np.meshgrid(x_vals, y_vals)
        
        # Start with a base surface
        Z = np.zeros_like(X)
        
        # Scale factor based on complexity
        scale_factor = complexity / 3.0
        
        # Add complicated features based on selected types
        
        # 1. Add Perlin-like noise for natural terrain
        if complexity > 1:
            freq = 0.1 * complexity
            for i in range(3):  # Multiple octaves
                phase_x = np.random.rand() * 10
                phase_y = np.random.rand() * 10
                Z += (np.sin((X + phase_x) * freq) * np.cos((Y + phase_y) * freq)) * (1.0 / (i + 1)) * scale_factor
                freq *= 2
        
        # 2. Add peaks and valleys
        if 'Peaks' in feature_type or 'Valleys' in feature_type:
            num_features = np.random.randint(3, 7) * complexity // 3
            for _ in range(num_features):
                center_x = np.random.uniform(x_min*0.8, x_max*0.8)
                center_y = np.random.uniform(y_min*0.8, y_max*0.8)
                width = np.random.uniform(1, 4) * scale_factor
                height = np.random.uniform(1, 3) * scale_factor
                
                # Determine if it's a peak or valley
                if 'Peaks' in feature_type and 'Valleys' in feature_type:
                    is_peak = np.random.choice([True, False])
                elif 'Peaks' in feature_type:
                    is_peak = True
                else:
                    is_peak = False
                
                amplitude = height if is_peak else -height
                
                # Create feature with varying steepness
                steepness = np.random.uniform(0.5, 2.5)
                dist = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
                feature = amplitude * np.exp(-(dist**steepness) / (2 * width**2))
                Z += feature
        
        # 3. Add plateaus
        if 'Plateaus' in feature_type:
            num_plateaus = np.random.randint(1, 4) * complexity // 3
            for _ in range(num_plateaus):
                center_x = np.random.uniform(x_min*0.8, x_max*0.8)
                center_y = np.random.uniform(y_min*0.8, y_max*0.8)
                width = np.random.uniform(2, 6) * scale_factor
                height = np.random.uniform(1, 2) * scale_factor
                
                # Create plateau with sharp edges
                dist = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
                plateau = height * (1 - np.tanh(dist - width))
                Z += plateau
        
        # 4. Add ridges
        if 'Ridges' in feature_type:
            num_ridges = np.random.randint(1, 3) * complexity // 3
            for _ in range(num_ridges):
                angle = np.random.uniform(0, np.pi)
                offset = np.random.uniform(-5, 5)
                height = np.random.uniform(1, 3) * scale_factor
                width = np.random.uniform(0.5, 2) * scale_factor
                
                # Create ridge
                ridge_dist = np.abs(X * np.cos(angle) + Y * np.sin(angle) - offset)
                ridge = height * np.exp(-ridge_dist**2 / (2 * width**2))
                Z += ridge
        
        # 5. Add saddle points
        if 'Saddles' in feature_type:
            num_saddles = np.random.randint(1, 3) * complexity // 4
            for _ in range(num_saddles):
                center_x = np.random.uniform(x_min*0.8, x_max*0.8)
                center_y = np.random.uniform(y_min*0.8, y_max*0.8)
                a = np.random.uniform(0.1, 0.5) * scale_factor
                b = np.random.uniform(0.1, 0.5) * scale_factor
                
                # Create saddle point
                X_shifted = X - center_x
                Y_shifted = Y - center_y
                angle = np.random.uniform(0, np.pi/2)
                X_rotated = X_shifted * np.cos(angle) - Y_shifted * np.sin(angle)
                Y_rotated = X_shifted * np.sin(angle) + Y_shifted * np.cos(angle)
                saddle = a * X_rotated**2 - b * Y_rotated**2
                Z += saddle
        
        # Apply a final scaling to ensure the surface is visible
        Z_range = np.max(Z) - np.min(Z)
        if Z_range < 1:
            Z *= 2 / Z_range
        
        # Plot
        fig = go.Figure(data=[go.Surface(
            z=Z,
            x=X,
            y=Y,
            colorscale=colorscale.lower(),
            lighting=dict(
                ambient=0.5,
                diffuse=0.6,
                specular=0.2,
                roughness=0.9,
                fresnel=0.1
            ),
            contours={
                'z': {'show': show_contour, 'usecolormap': False, 'highlightcolor': 'white','width': 6, 'size': 36}
            },
            opacity=1
        )])

        # Dark mode & hide scale
        fig.update_layout(
            template='plotly_dark',
            margin=dict(l=0, r=0, t=0, b=0),
            height=700,
            width=1000,
            scene=dict(
                camera=dict(eye=dict(x=1.2, y=1.2, z=1.2)),
                xaxis_title='X Axis',
                yaxis_title='Y Axis',
                zaxis_title='Z Axis'
            )
        )
        
        np.save('X.npy',X)
        np.save('Y.npy',Y)
        np.save('Z.npy',Z)

        fig.update_traces(showscale=False)  # Hide color bar for clean look
        

            
        # Render Plotly chart
        st.plotly_chart(fig, use_container_width=True)