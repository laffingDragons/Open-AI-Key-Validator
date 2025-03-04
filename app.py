import streamlit as st
from openai import OpenAI, AuthenticationError
import os
from dotenv import load_dotenv

def validate_openai_key(api_key):
    try:
        client = OpenAI(api_key=api_key)
        client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Key validation"}],
            timeout=10
        )
        return True
    except AuthenticationError:
        return False
    except Exception as e:
        st.error(f"Validation error: {str(e)}")
        return False

def main():
    load_dotenv()  # Load .env file if exists
    st.title("OpenAI API Key Validator")
    
    # Check existing environment variable first
    env_key = os.getenv("OPENAI_API_KEY")
    if env_key and validate_openai_key(env_key):
        st.success("✅ Environment key validated successfully!")
        return

    # Manual key input
    api_key = st.text_input("Enter OpenAI API Key:", type="password")
    
    if st.button("Validate Key"):
        if not api_key:
            st.warning("Please enter an API key")
            return
            
        with st.spinner("Validating..."):
            if validate_openai_key(api_key):
                st.success("✅ Valid API Key!")
                st.session_state.valid_key = True
                os.environ["OPENAI_API_KEY"] = api_key
            else:
                st.error("❌ Invalid API Key")

if __name__ == "__main__":
    main()
