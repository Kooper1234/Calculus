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

# Function to find points of intersection
def find_intersections(f1, f2):
    x = sp.symbols('x')
    intersections = sp.solve(f1 - f2, x)
    real_intersections = [i.evalf() for i in intersections if i.is_real]
    return sorted(real_intersections)

# Function to verify and cross-check results
def verify_results(sympy_result, numerical_result, tolerance=1e-5):
    if abs(sympy_result - numerical_result) < tolerance:
        return True
    return False

# Function to plot the functions and the area between them
def plot_functions_and_area(f1, f2, a, b, n):
    x = sp.symbols('x')
    f1_lambdified = sp.lambdify(x, f1, 'numpy')
    f2_lambdified = sp.lambdify(x, f2, 'numpy')
    x_vals = np.linspace(a, b, 1000)
    y_vals_f1 = f1_lambdified(x_vals)
    y_vals_f2 = f2_lambdified(x_vals)
    
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals_f1, label=str(f1), color='blue')
    ax.plot(x_vals, y_vals_f2, label=str(f2), color='red')
    ax.fill_between(x_vals, y_vals_f1, y_vals_f2, where=(y_vals_f1 > y_vals_f2), interpolate=True, color='gray', alpha=0.5)

    ax.set_title('Functions Plot and Area Enclosed')
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.legend()
    st.pyplot(fig)

st.title('Area Enclosed by Two Functions')

# Instructions for entering the functions
st.write("Enter the functions to integrate in terms of x. Use '**' for exponentiation, e.g., '((-3**(x+1.893))+8)**2-((3**(x-10))**2)'")

# Input for functions
f1_input = st.text_input('Enter the first function (f1) to integrate (in terms of x):', '((-3**(x+1.893))+8)**2')
f2_input = st.text_input('Enter the second function (f2) to integrate (in terms of x):', '((3**(x-10))**2)')
f1 = sp.sympify(f1_input)
f2 = sp.sympify(f2_input)

# Find points of intersection
try:
    intersections = find_intersections(f1, f2)
    st.write(f'Points of intersection: {intersections}')
except Exception as e:
    st.error(f"An error occurred while finding intersections: {e}")

# Input for interval
a = st.number_input('Enter the lower limit of integration (a):', value=0.0)
b = st.number_input('Enter the upper limit of integration (b):', value=1.0)

# Calculate the definite integral of the area between the functions
if st.button('Calculate Area Between Functions'):
    try:
        area_sympy = calculate_integral(f1 - f2, a, b)
        st.write(f'The area between {f1_input} and {f2_input} from {a} to {b} is (symbolic):')
        st.latex(f'\\int_{{{a}}}^{{{b}}} ({sp.latex(f1)} - {sp.latex(f2)}) \, dx = {area_sympy}')

        area_numerical = numerical_integral(f1 - f2, a, b)
        st.write(f'The area between {f1_input} and {f2_input} from {a} to {b} is (numerical): {area_numerical}')

        # Verify and cross-check results
        if verify_results(area_sympy, area_numerical):
            st.success('The symbolic and numerical results match within tolerance.')
        else:
            st.warning('The symbolic and numerical results do not match. Please verify the input functions.')
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Input for Riemann sum
method = st.selectbox('Choose Riemann sum method:', ['left', 'right'])
n = st.number_input('Enter the number of subintervals (n):', value=10, step=1)

# Calculate the Riemann sum approximation and plot
if st.button('Plot Functions and Area'):
    try:
        plot_functions_and_area(f1, f2, a, b, n)
    except Exception as e:
        st.error(f"An error occurred: {e}")
