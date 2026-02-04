import streamlit as st
import json
import plotly.graph_objects as go
from main import (
    debit,
    waterheight,
    water_above_roof,
    critical_height,
    equivalent_load,
    flat_roof,
    curved_roof,
    sloped_roof_bi_al,
    sloped_roof_sm_al,
    curved_and_sloped_roof_bi_al,
    curved_and_sloped_roof_sm_al,
    critical_stifness,
    mult_factor,
    N_factor,
    factored_equivalent_load,
)

# Function to fix LaTeX strings from handcalcs
def fix_latex(latex_str):
    """Fix common LaTeX syntax errors from handcalcs decorator"""
    if latex_str is None:
        return latex_str
    
    # Convert to string if needed
    latex_str = str(latex_str)
    
    # Remove $$ delimiters that handcalcs adds (Streamlit doesn't want them)
    latex_str = latex_str.replace('$$', '').strip()
    
    # Fix \& to & for alignment  
    latex_str = latex_str.replace('\\&', '&')
    
    # Fix math.pi references  
    latex_str = latex_str.replace('\\mathrm{math.pi}', '\\pi')
    latex_str = latex_str.replace('math.pi', '\\pi')
    
    # handcalcs uses ' ; \ ' as separator - the backslash is literal
    # Replace semicolon with double backslash for line break
    latex_str = latex_str.replace(' ; ', ' \\\\ ')
    
    return latex_str

# Quick test to verify LaTeX rendering works
with st.expander("🔧 LaTeX Test (click to expand)", expanded=False):
    st.write("Testing if LaTeX renders...")
    st.latex(r"E = mc^2")
    st.write("If you see E = mc² above, LaTeX works! If you see raw code, there's a problem with your Streamlit setup.")

# Streamlit layout
st.header("Water Overflow Design for Steel Roofs")
st.divider()
st.subheader("Calculation Program for Designing Roof Water Overflows According to NPR6703:2006 'Water Accumulation'")
st.divider()

st.sidebar.header("Roof Overflow")

# Input values
area_value = st.sidebar.number_input("Roof Area (m²)", 50, format='%d')
n_value = st.sidebar.number_input("Number of Water Overflows", 1)

# Assign input values
Area = area_value
n = n_value

st.write(f"Area: {area_value}m²")
st.write(f"Number of overflows per Area: {n_value}")

# Calculate water debit
debit_latex, debit_value = debit(Area, n)
st.write("Water debit (m³/s)")
st.latex(fix_latex(debit_latex))

# Water height calculations
height_A_value = st.sidebar.number_input("Height Start of Overflow Above Roof (mm)", 30)
width_value = st.sidebar.number_input("Width of Overflow (mm)", 200)
height_value = st.sidebar.number_input("Height of Overflow (mm)", 20)

width_overflow = width_value
height_above_roof = height_A_value
Qhi = debit_value
height_of_overflow = height_value

# Water height and critical height calculations
dndi_latex, dndi_value = waterheight(width_overflow, Qhi)
st.write("Water Height (mm)")
st.latex(fix_latex(dndi_latex))

Dndi = dndi_value
dhw_latex, dhw_value = water_above_roof(Dndi, height_above_roof)
st.write("Total Height (mm)")
st.latex(fix_latex(dhw_latex))

hcrit_latex, hcrit_value = critical_height(height_above_roof, height_of_overflow)
st.write("Critical Water Height (mm)")
st.latex(fix_latex(hcrit_latex))

# Additional calculations
hcrit = height_above_roof + height_of_overflow - 30
ho = height_value
hnd = height_A_value
dhw = Dndi + hnd
equload_latex, equload_value = equivalent_load(dhw)
st.write("Equivalent Load (kN/m²)")
st.latex(fix_latex(equload_latex))

# Plotting
fig = go.Figure()
fig.add_trace(go.Scatter(x=[0, 70, 70, 100, 100, 0], y=[0, 0, hnd, hnd, dhw, dhw], 
                         fill="toself", fillcolor="lightblue", line=dict(color="lightblue"), 
                         showlegend=False))
fig.add_trace(go.Scatter(x=[0, 100, 100, 70, 70, 0, 0, None, 70, 100, 100, 70, 70], 
                         y=[-30, -30, hnd, hnd, 0, 0, -30, None, hnd+ho, hnd+ho, hnd+ho+ho, hnd+ho+ho, hnd+ho], 
                         fill="toself", fillcolor="grey", line=dict(color="black"), 
                         showlegend=False))
fig.add_trace(go.Scatter(x=[0, 100], y=[hcrit, hcrit], mode="lines", 
                         line=dict(color="black", dash="dash"), showlegend=False))

x_point, y_point = 65, hnd + 3
label_text = f"<span style='color:black; font-weight:bold;'>hnd = {hnd}mm</span>"
fig.add_annotation(
    text=label_text,
    x=x_point,
    y=y_point,
    showarrow=False,
    arrowhead=1,
)

x_point, y_point = 30, hcrit + 3
if hcrit > dhw_value:
    label_text2 = f"<span style='color:black; font-weight:bold;'>hcrit = maximum available waterheight {hcrit}mm</span>"
else:
    label_text2 = f"<span style='color:red; font-weight:bold;'>maximum water height exceeded!! make overflow wider or higher</span>"

fig.add_annotation(
    text=label_text2,
    x=x_point,
    y=y_point,
    showarrow=False,
    arrowhead=1,
)

x_point, y_point = 65, round(dhw, 0) + 3
label_text1 = f"<span style='color:black; font-weight:bold;'>dhw = {round(dhw, 0)}mm</span>"
fig.add_annotation(
    text=label_text1,
    x=x_point,
    y=y_point,
    showarrow=False,
    arrowhead=1,
)

fig.update_layout(
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)
fig.update_xaxes(showline=False, showticklabels=False)
fig.update_yaxes(showline=True, showticklabels=True, side="right")

fig.layout.height = 600
fig.layout.width = 600
st.plotly_chart(fig)

st.divider()
st.subheader("Reduced waterheight based on roof type")

# Roof type selection
st.sidebar.header("Roof type")
roof_types = ["Flat Roof", "Curved", "Sloped", "Curved and Sloped"]
selected_roof = st.sidebar.selectbox("Select Roof Type:", roof_types)
roof_type = selected_roof.lower()

# Conditional input fields based on roof type
if "curved" in roof_type:
    z_value = st.sidebar.number_input("Curvature Value Z (mm):", min_value=0.0)
    st.write(f"Curved roof, curvature: {z_value}mm")
else:
    z_value = None

if "sloped" in roof_type:
    al_value = st.sidebar.number_input("Slope Value Al (mm at end of beam):", min_value=0.0)
    st.write(f"Sloped roof, slope: {al_value}mm")
else:
    al_value = None

al = al_value
z = z_value

# Roof type calculations
if roof_type == "flat roof":
    result = flat_roof(dhw)
elif roof_type == "curved":
    result = curved_roof(dhw, z)
elif roof_type == "sloped":
    result = sloped_roof_bi_al(dhw, al, z) if dhw > al else sloped_roof_sm_al(dhw, al, z)
elif roof_type == "curved and sloped":
    result = curved_and_sloped_roof_bi_al(dhw, al, z) if dhw > al else curved_and_sloped_roof_sm_al(dhw, al, z)
else:
    raise ValueError("Invalid roof_type value")

d_value_latex, d_value = result
st.write("Reduced Water Height d (mm)")
st.latex(fix_latex(d_value_latex))

# Additional calculations for critical stiffness
st.divider()
st.subheader("Calculation of the Critical Stiffness to determine the additional water load")

# Load data from the merged_output.json file
with open('merged_output.json') as f:
    data = json.load(f)

# Extract beam types from the keys of the loaded data
beam_types = list(data.keys())

st.sidebar.header("Beam Setup")

# Select beam type
selected_beam = st.sidebar.selectbox("Select Beam:", beam_types)
selected_Iy = data[selected_beam]["Iy"]
st.write(f"Beam {selected_beam} is Iy: {selected_Iy}m⁴")
I_y = selected_Iy
l = st.sidebar.number_input("Length (m)", 1)
hoh = st.sidebar.number_input("h.o.h. (m)", 1)

# Select support type
roof_stiffness = ["Simply Supported", "One Side Semi Fixed", "One Side Fully Fixed", 
                  "Two Sides Semi Fixed", "Two Sides Fully Fixed"]
selected_stiffness = st.sidebar.selectbox("Select Support Type:", roof_stiffness)
stiff_type = selected_stiffness.lower()

# Calculate critical stiffness
if stiff_type == "simply supported":
    fac = 1
elif stiff_type in ["one side semi fixed", "two sides semi fixed"]:
    fac = 0.7
elif stiff_type in ["one side fully fixed", "two sides fully fixed"]:
    fac = 0.4
else:
    raise ValueError("Invalid stiff_type value")

y_rep = 10
critical_stiffness_latex, critical_stiffness_value = critical_stifness(fac, hoh, l, y_rep)
st.write("Critical Stiffness")
st.latex(fix_latex(critical_stiffness_latex))

# Additional calculations
E = 210000
y_m = 1.3
mult_factor_latex, mult_factor_value = mult_factor(I_y, y_m, critical_stiffness_value, E)
st.write("Multiplication Factor")
st.latex(fix_latex(mult_factor_latex))

N_factor_latex, N_factor_value = N_factor(mult_factor_value)
st.latex(fix_latex(N_factor_latex))

factored_equivalent_load_latex, factored_equivalent_load_value = factored_equivalent_load(d_value, N_factor_value)
st.write("Factored Equivalent Load (kN/m²)")
st.latex(fix_latex(factored_equivalent_load_latex))
