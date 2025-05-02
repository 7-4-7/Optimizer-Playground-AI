import time
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

#st.set_page_config(page_title="Basics of Streamlit", page_icon=":smiley:", layout="wide", initial_sidebar_state="expanded")
st.title('Basics of Streamlit')
st.write("""
         # My first app
         Hello **world!**
         """)

st.text('This is some text by Bharat Bhusan Biswal.')

# Creating a sidebar
st.sidebar.header('About')
st.sidebar.text('This is Streamlit tutorial.')

# Code 
st.code('''def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2

        # Check if target is at mid
        if arr[mid] == target:
            return mid
        # If target is greater, ignore the left half
        elif arr[mid] < target:
            left = mid + 1
        # If target is smaller, ignore the right half
        else:
            right = mid - 1

    # Target is not present in the array
    return -1

# Example usage
arr = [2, 3, 4, 10, 40]
target = 10
result = binary_search(arr, target)

if result != -1:
    print(f"Element is present at index {result}")
else:
    print("Element is not present in array")
''')

st.html('<h2 style="color:blue;">Hello Streamlit</h2>')

# Latex code
st.latex(r'''
         a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} = \sum_{k=0}^{n-1} ar^k = a \left(\frac{1-r^{n}}{1-r}\right)
         ''')

# Metric
st.metric("Metrix", "$100K", "-5%")

# Buttons
if st.button('Say hello'):
    st.write('Why hello there')

# Create a dummy dataframe
df = pd.DataFrame({
     'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})   
st.dataframe(df)

st.table(df)

# Charts
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])
st.line_chart(chart_data)

st.area_chart(chart_data)
#st.map(chart_data)
# Sample DataFrame with latitude and longitude points
data = {
    'lat': [37.7749, 40.7128, 34.0522],
    'lon': [-122.4194, -74.0060, -118.2437]
}
df_1= pd.DataFrame(data) 
# Display the map
st.map(df_1)

st.scatter_chart(chart_data)
# Plotly chart 3d 
# Create sample data for the 3D scatter plot
x_data = [1, 2, 3, 4, 5]
y_data = [10, 11, 12, 13, 14]
z_data = [5, 4, 3, 2, 1]

# Create a 3D scatter plot
fig = go.Figure(data=[go.Scatter3d(
    x=x_data,
    y=y_data,
    z=z_data,
    mode='markers',
    marker=dict(
        size=10,
        color=z_data,  # Set color to the z values
        colorscale='Viridis',  # Choose a colorscale
        opacity=0.8
    )
)])

# Set layout for the 3D plot
fig.update_layout(
    title='3D Scatter Plot Example',
    scene=dict(
        xaxis_title='X AXIS',
        yaxis_title='Y AXIS',
        zaxis_title='Z AXIS'
    )
)

# Use Streamlit to render the Plotly figure
st.plotly_chart(fig)

# Create sample data
x = np.linspace(-10, 10, 100)
y = np.linspace(-10, 10, 100)
x, y = np.meshgrid(x, y)
z = x**2 + y**2

# Create a 3D surface plot
fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])

# Update layout for larger display
fig.update_layout(
    title='3D Surface Plot of f(x, y) = x^2 + y^2',
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    ),
    width=800,
    height=800
)

# Use Streamlit to render the Plotly figure
st.plotly_chart(fig, use_container_width=False)



# Columns and tabs
col1, col2 = st.columns(2)
col1.write('This is column 1')
col2.write('This is column 2')

col1, col2, col3 = st.columns([3, 1, 1])
col1.write('Column 1 larger')
col2.write('Column 2')
col3.write('Column 3')

# Bottom-aligned columns
col1, col2,col3 = st.columns(3, vertical_alignment="bottom")

# You can also use "with" notation:
with col1:
    st.radio("Select one:", [1, 2,3])
with col2:
    st.radio("Select two:", [4, 5,6])
with col3:
    st.radio("Select three:", [7, 8,9])    

st.page_link("basics_st.py", label="Home")
#st.data_editor("Edit data", df)
st.checkbox("I agree")
st.feedback("thumbs")
st.error("Error")


st.success("Success")
st.pills("Tags", ["Sports", "Politics"])
#st.pills(["Python", "Streamlit", "Plotly"])

st.segmented_control("Filter", ["Open", "Closed"])
with st.chat_message("user"):
    st.write("Hello 👋")
    st.line_chart(np.random.randn(30, 3))

st.chat_input("Type a message")
#st.camera_input("Take a photo")
with st.container():
    st.chat_input("Say something")

with st.echo():
    st.write("Code will be executed and printed")    

with st.spinner(text="In progress"):
    time.sleep(1.5)
    st.success("Done")

# Show and update progress bar
bar = st.progress(50)
time.sleep(0.1)
bar.progress(100)

st.balloons()
st.snow()
st.toast("Warming up...")
st.info("Info message")
# tabs in st

tab1,tab2 = st.tabs(["Tab 1", "Tab 2"])
tab1.write("This is a tab 1")
tab2.write("This is a tab 2")

with st.expander("See explanation"):
    st.write("This is an expander. My explanation is here. I am trying to explain something.I am finding it difficult to explain.")


expand = st.expander("My label", icon=":material/info:")
expand.write("Inside the expander.")
pop = st.popover("Button label")
pop.checkbox("Show all")

# You can also use "with" notation:
with expand:
    st.radio("Select one:", [1, 2])    

# Define a fragment
@st.fragment
def fragment_function():
    def get_data():
        # Sample data generation
        return pd.DataFrame(
            np.random.randn(20, 3),
            columns=['a', 'b', 'c']
        )

    df = get_data()
    st.line_chart(df)
    st.button("Update")

fragment_function()


# Define a dialog function
@st.dialog("Welcome!")
def modal_dialog():
    st.write("Hello")
    st.button("skip")
    st.caption("This is a dialog box")

modal_dialog()