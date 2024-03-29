import streamlit as st
import startup


def main():
    st.title("Using MetaGPT for Product Innovation")
    user_input = st.text_area("Input: ", height=150)

    if user_input:
        st.write("Sending to LLM API:")
        st.write(user_input)

    #startup.main()
        
if __name__ == "__main__":
    main()