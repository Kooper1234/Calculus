import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# Function to calculate the definite integral using SymPy
def calculate_integral(f, a, b):
    x = sp.symbols('x')
    integral = sp.integrate(f, (x, a, b))
    return integral

# Function to calculate the definite integral using numerical methods (SciPy)
def numerical_integral(f, a, b):
    x = sp.symbols('x')
    f_lambdified = sp.lambdify(x, f, 'numpy')
    integral, _ = quad(f_lambdified, a, b)
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
    return riemann_sum, sample_points, heights

# Function to verify and cross-check results
def verify_results(sympy_result, numerical_result, tolerance=1e-5):
    if abs(sympy_result - numerical_result) < tolerance:
        return True
    return False

# Function to plot the function and Riemann sums
def plot_function_and_riemann(f, a, b, n, method='left'):
    x = sp.symbols('x')
    f_lambdified = sp.lambdify(x, f, 'numpy')
    x_vals = np.linspace(a, b, 1000)
    y_vals = f_lambdified(x_vals)
    
    riemann_sum_result, sample_points, heights = riemann_sum(f, a, b, n, method)
    width = (b - a) / n

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label=str(f), color='blue')
    for i in range(n):
        if method == 'left':
            rect_x = [sample_points[i], sample_points[i], sample_points[i] + width, sample_points[i] + width, sample_points[i]]
            rect_y = [0, heights[i], heights[i], 0, 0]
        else:
            rect_x = [sample_points[i] - width, sample_points[i] - width, sample_points[i], sample_points[i], sample_points[i] - width]
            rect_y = [0, heights[i], heights[i], 0, 0]
        ax.fill(rect_x, rect_y, 'gray', edgecolor='black', alpha=0.5)
    
    ax.set_title('Function Plot and Riemann Sum Approximation')
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.legend()
    st.pyplot(fig)

st.title('Definite Integral and Riemann Sum Approximation')

# Instructions for entering the function
st.write("Enter the function to integrate in terms of x. Use '**' for exponentiation, e.g., '((-3**(x+1.893))+8)**2-((3**(x-10))**2)'")

# Input for function
f_input = st.text_input('Enter the function to integrate (in terms of x):', '((-3**(x+1.893))+8)**2-((3**(x-10))**2)')
f = sp.sympify(f_input)

# Input for interval
a = st.number_input('Enter the lower limit of integration (a):', value=0.0)
b = st.number_input('Enter the upper limit of integration (b):', value=1.0)

# Calculate the definite integral
if st.button('Calculate Definite Integral'):
    try:
        integral = calculate_integral(f, a, b)
        st.write(f'The definite integral of {f_input} from {a} to {b} is (symbolic):')
        st.latex(f'\\int_{{{a}}}^{{{b}}} {sp.latex(f)} \, dx = {integral}')

        numerical_result = numerical_integral(f, a, b)
        st.write(f'The definite integral of {f_input} from {a} to {b} is (numerical): {numerical_result}')

        # Verify and cross-check results
        if verify_results(integral, numerical_result):
            st.success('The symbolic and numerical results match within tolerance.')
        else:
            st.warning('The symbolic and numerical results do not match. Please verify the input function.')
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Input for Riemann sum
method = st.selectbox('Choose Riemann sum method:', ['left', 'right'])
n = st.number_input('Enter the number of subintervals (n):', value=10, step=1)

# Calculate the Riemann sum approximation and plot
if st.button('Calculate Riemann Sum Approximation'):
    try:
        riemann_sum_result, sample_points, heights = riemann_sum(f, a, b, n, method)
        st.write(f'The {method} Riemann sum approximation of {f_input} from {a} to {b} with {n} subintervals is:')
        st.write(riemann_sum_result)

        plot_function_and_riemann(f, a, b, n, method)
    except Exception as e:
        st.error(f"An error occurred: {e}")
