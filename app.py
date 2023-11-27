import streamlit as st
import json
from main import debit
from main import waterheight
from main import water_above_roof
from main import critical_height
from main import equivalent_load
from main import flat_roof
from main import curved_roof
from main import sloped_roof_bi_al
from main import sloped_roof_sm_al
from main import curved_and_sloped_roof_bi_al
from main import curved_and_sloped_roof_sm_al
from main import critical_stifness

st.header("roof overflow design for steel roofs")

st.sidebar.header("roof overflow")

area_value = st.sidebar.number_input("roof area in (m^2)",50)
n_value = st.sidebar.number_input("number of water overflows",1)

Area = area_value 

n = n_value 

debit_latex, debit_value = debit(Area, n)
st.write(" water debit in m^3/s")
st.latex(debit_latex)

height_A_value=st.sidebar.number_input("height start of overflow above roof (mm)",30)
width_value = st.sidebar.number_input("width of overflow (mm)",200)
height_value = st.sidebar.number_input("height of overflow in (mm) ",20)

width_overload=width_value
height_aboveroof=height_A_value
Qhi=debit_value
height_of_overload=height_value

dndi_latex, dndi_value= waterheight(width_overload,Qhi)
st.write("waterheight in mm")
st.latex(dndi_latex)
Dndi=dndi_value
dhw_latex,dhw_value=water_above_roof(Dndi,height_aboveroof)
st.write("total height in mm")
st.latex(dhw_latex)
hcrit_latex,hcrit_value=critical_height(height_aboveroof,height_of_overload)
st.write("critical waterheight in mm ")
st.latex(hcrit_latex)

hcrit=height_aboveroof+height_of_overload-30



ho=height_value
hnd=height_A_value
dhw=Dndi+hnd
equload_latex,equload_value=equivalent_load(dhw)
st.write("equivalent load in kN/m^2 ")
st.latex(equload_latex) 
import plotly.graph_objects as go
fig=go.Figure()
fig.add_trace(go.Scatter(x=[0,70,70,100,100,0], y=[0,0,hnd,hnd,dhw,dhw], fill="toself",fillcolor="lightblue", line=dict(color="lightblue"),showlegend=False))
fig.add_trace(go.Scatter(x=[0,100,100,70,70,0,0,None,70,100,100,70,70], y=[-30,-30,hnd,hnd,0,0,-30,None,hnd+ho,hnd+ho,hnd+ho+ho,hnd+ho+ho,hnd+ho], fill="toself",fillcolor="grey", line=dict(color="black"),showlegend=False))
fig.add_trace(go.Scatter(x=[0,100,], y=[hcrit,hcrit],mode="lines", line=dict(color="black", dash="dash"),showlegend=False))
x1, y1 = 70, 30 + hnd
x2, y2 = 100, 30 + hnd


x_point, y_point = 65, hnd+3
label_text = f"<span style='color:black; font-weight:bold;'>hnd = {hnd}mm</span>"

# Add an annotation for the point
fig.add_annotation(
    text=label_text,  # Text label for the point
    x=x_point,  # X-coordinate of the point
    y=y_point,  # Y-coordinate of the point
    showarrow=False,  # Display an arrow pointing to the annotation
    arrowhead=1,  # Specify the arrowhead style
    
)
x_point, y_point = 30, hcrit+3
if hcrit>dhw_value:
    label_text2 =f" <span style='color:black; font-weight:bold;'>hcrit =maximum available waterheight  {hcrit}mm</span>"
else:
    label_text2 = f"<span style='color:red; font-weight:bold;'>maximum water height exceeded!! make overflow wider or higher</span>"

# Add an annotation for the point
fig.add_annotation(
    text=label_text2,  # Text label for the point
    x=x_point,  # X-coordinate of the point
    y=y_point,  # Y-coordinate of the point
    showarrow=False,  # Display an arrow pointing to the annotation
    arrowhead=1,  # Specify the arrowhead style
)
x_point, y_point = 65, round(dhw,0)+3
label_text1 = f"<span style='color:black; font-weight:bold;'>dhw = {round(dhw,0)}mm</span>"

# Add an annotation for the point
fig.add_annotation(
    text=label_text1,  # Text label for the point
    x=x_point,  # X-coordinate of the point
    y=y_point,  # Y-coordinate of the point
    showarrow=False,  # Display an arrow pointing to the annotation
    arrowhead=1,  # Specify the arrowhead style
)

fig.update_layout(
    xaxis=dict(showgrid=False),  # Remove x-axis gridlines
    yaxis=dict(showgrid=False),  # Remove y-axis gridlines
    paper_bgcolor='rgba(0,0,0,0)',  # Set transparent background
    plot_bgcolor='rgba(0,0,0,0)'  # Set transparent plot background
)
fig.update_xaxes(showline=False, showticklabels=False)  # Remove x-axis
fig.update_yaxes(showline=True, showticklabels=True, side="right")  # Show y-axis on the right

fig.layout.height = 600
fig.layout.width = 600
fig

# Load data from the merged_output.json file
with open('merged_output.json') as f:
    data = json.load(f)

# Extract beam types from the keys of the loaded data
beam_types = list(data.keys())

# Display a selectbox for beam type selection
#selected_beam = st.sidebar.selectbox("Select Beam Type:", beam_types)

st.sidebar.header("beam setup")
# List of roof types
roof_types = ["flat roof", "curved", "sloped", "curved and sloped"]

# Display a selectbox for roof type selection
selected_roof = st.sidebar.selectbox("Select Beam Type:", roof_types)
roof_type=selected_roof
# Conditional input fields based on roof type
if selected_roof == "curved" or selected_roof == "curved and sloped":
    z_value = st.sidebar.number_input("curvature value Z in mm:", min_value=0.0)
else:
    z_value = None

if selected_roof == "sloped" or selected_roof == "curved and sloped":
    al_value = st.sidebar.number_input("slope value  al in mm at end of beam:", min_value=0.0)
else:
    al_value = None

al=al_value
z=z_value



if roof_type == "flat roof":
    result = flat_roof(dhw)
elif roof_type == "curved":
    result = curved_roof(dhw, z)
elif roof_type == "sloped":
    if dhw > al:
        result = sloped_roof_bi_al(dhw, al, z)
    else:
        result = sloped_roof_sm_al(dhw, al, z)
elif roof_type == "curved and sloped":
    if dhw > al:
        result = curved_and_sloped_roof_bi_al(dhw, al, z)
    else:
        result = curved_and_sloped_roof_sm_al(dhw, al, z)
else:
    raise ValueError("Invalid roof_type value")
d_value=result

d_value_latex,d_value=result
st.write("reduced waterheight d in  mm ")
st.latex(d_value_latex)

# List of roof types
roof_stifness = ["simply supported", "one side semi fixed", "one side fully fixed", "two sides semi fixed","two sides fully fixed"]

# Display a selectbox for roof type selection
selected_stifness = st.sidebar.selectbox("Select Beam Type:", roof_stifness)
stiff_type=selected_stifness

if selected_stifness ==" simply supported":
    fac=1
elif selected_stifness =="one side semi fixed":
    fac=0.7
elif selected_stifness =="one side fully fixed":
    fac=0.4
elif selected_stifness =="two sides semi fixed":
    fac=0.4
elif selected_stifness =="two sides fully fixed":
    fac=0.2   

# Arrange them horizontally using columns
col1, col2, col3 = st.columns(3)

# Place each input field in a separate column without extra rows
with col2:
    input1=st.text_input("l in m", value="1")

with col1:
    selected_beam = st.selectbox("Select Beam Type:", beam_types)

with col3:
    input2=st.text_input("h.o.h. in m", value="1")