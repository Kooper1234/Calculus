import streamlit as st
import sympy as sp
import numpy as np

# Function to calculate the definite integral
def calculate_integral(f, a, b):
    x = sp.symbols('x')
    integral = sp.integrate(f, (x, a, b))
    return integral

# Function to calculate the Riemann sum approximation
def riemann_sum(f, a, b, n, method='left'):
    x = sp.symbols('x')
    f_lambdified = sp.lambdify(x, f, 'numpy')
    width = (b - a) / n
    if method == 'left':
        sample_points = np.linspace(a, b - width, n)
    else:
        sample_points = np.linspace(a + width, b, n)
    heights = f_lambdified(sample_points)
    riemann_sum = np.sum(heights * width)
    return riemann_sum

st.title('Definite Integral and Riemann Sum Approximation')

# Input for function
f_input = st.text_input('Enter the function to integrate (in terms of x):', 'x**2')
f = sp.sympify(f_input)

# Input for interval
a = st.number_input('Enter the lower limit of integration (a):', value=0.0)
b = st.number_input('Enter the upper limit of integration (b):', value=1.0)

# Calculate the definite integral
if st.button('Calculate Definite Integral'):
    integral = calculate_integral(f, a, b)
    st.write(f'The definite integral of {f_input} from {a} to {b} is:')
    st.latex(f'\\int_{{{a}}}^{{{b}}} {sp.latex(f)} \, dx = {integral}')

# Input for Riemann sum
method = st.selectbox('Choose Riemann sum method:', ['left', 'right'])
n = st.number_input('Enter the number of subintervals (n):', value=10, step=1)

# Calculate the Riemann sum approximation
if st.button('Calculate Riemann Sum Approximation'):
    riemann_sum_result = riemann_sum(f, a, b, n, method)
    st.write(f'The {method} Riemann sum approximation of {f_input} from {a} to {b} with {n} subintervals is:')
    st.write(riemann_sum_result)
