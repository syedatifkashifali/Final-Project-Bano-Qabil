import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Create a figure and axes
fig, ax = plt.subplots()

# Create a line object
line, = ax.plot([], [], 'ro')

# Define the animation function
def animate(i):
    # Generate some random data
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x + i / 10.0)

    # Update the line data
    line.set_data(x, y)

    # Redraw the canvas
    plt.draw()

# Create the animation object
ani = animation.FuncAnimation(fig, animate, frames=100, interval=100)

# Display the animation in Streamlit
st.markdown("## Animation Example")
st.pyplot(fig)
