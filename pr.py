import streamlit as st
import streamlit.components.v1 as stc

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def main():
    st.title("About Me")

    # Load Lottie animation
    lottie_hello = load_lottieurl("https://lottie.host/9ac568aa-70c3-4de6-a428-723d7e94497f/Pi0BW1dNnf.json")

    # Display Lottie animation
    st_lottie.lottie(
        lottie_hello,
        speed=1,
        reverse=False,
        loop=True,
        quality="low", # medium ; high
        height=400,
        width=None,
        key=None,
    )

    # Add your content
    st.write("""
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed cursus eu risus nec cursus. 
        Integer sit amet augue id enim scelerisque pharetra non et nulla. Nullam id faucibus enim. 
        Sed non libero vitae lorem consectetur efficitur.
    """)

    # Add an interactive "Read More" button
    if st.button("Read More"):
        st.write("""
            Fusce vitae libero vitae elit maximus tempus. Quisque sagittis augue sed metus sollicitudin, 
            vel volutpat tortor ultrices. Etiam iaculis libero vel est cursus, in lobortis neque tincidunt. 
            Donec accumsan tincidunt odio, non finibus sapien bibendum vel.
        """)

if __name__ == "__main__":
    main()
