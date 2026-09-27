import os
import time

import streamlit as st
from dotenv import load_dotenv
from google import genai


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


# --------------------------------------------------
# STREAMLIT PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Laboratory Manual Assistant",
    page_icon="🤖",
    layout="centered"
)


# --------------------------------------------------
# APPLICATION HEADER
# --------------------------------------------------

st.title("🤖 LLM-Powered Application Portal")

st.caption(
    "Developed using Python, Streamlit and Google Gemini"
)


# --------------------------------------------------
# SIDEBAR CONFIGURATION
# --------------------------------------------------

st.sidebar.header("Gemini Model Configuration")

model_choice = st.sidebar.selectbox(
    "Select Gemini Model",
    [
        "gemini-3.5-flash-lite",
        "gemini-3.8-flash"
    ]
)


# --------------------------------------------------
# MAIN INPUT SECTION
# --------------------------------------------------

st.subheader("Text Utility Service")

user_prompt = st.text_area(
    "Enter your question or prompt:",
    placeholder="Type your prompt here..."
)


# --------------------------------------------------
# GENERATE RESPONSE BUTTON
# --------------------------------------------------

if st.button("🚀 Generate Response"):

    # Check API key
    if not api_key:

        st.error(
            "Gemini API key is not configured. "
            "Please check your .env file."
        )

    # Check user input
    elif not user_prompt.strip():

        st.warning(
            "Please enter a question or prompt."
        )

    else:

        # --------------------------------------------------
        # GEMINI API PROCESSING
        # --------------------------------------------------

        with st.spinner(
            "Generating response using Gemini..."
        ):

            try:

                # Create Gemini client
                client = genai.Client(
                    api_key=api_key
                )

                response = None

                # Automatic retry for temporary 503 errors
                for attempt in range(3):

                    try:

                        response = client.models.generate_content(
                            model=model_choice,
                            contents=user_prompt
                        )

                        break

                    except Exception as error:

                        error_message = str(error)

                        if "503" in error_message or "UNAVAILABLE" in error_message:

                            if attempt < 2:

                                wait_time = 2 ** attempt

                                st.info(
                                    f"Gemini is temporarily busy. "
                                    f"Retrying in {wait_time} seconds..."
                                )

                                time.sleep(wait_time)

                            else:

                                raise error

                        else:

                            raise error


                # --------------------------------------------------
                # DISPLAY RESPONSE
                # --------------------------------------------------

                if response and response.text:

                    st.success(
                        "Response generated successfully!"
                    )

                    st.markdown(
                        "### Generated Result"
                    )

                    st.info(
                        response.text
                    )

                else:

                    st.warning(
                        "Gemini returned an empty response."
                    )


            # --------------------------------------------------
            # ERROR HANDLING
            # --------------------------------------------------

            except Exception as error:

                st.error(
                    f"Gemini API Error: {error}"
                )