import streamlit as st
from dotenv import load_dotenv
from codecritic import codeCritic
import datetime

# creating a uploader using streamlit
title = """
        <h1 style="text-align:center; 
                   background: -webkit-linear-gradient(#3E196E,#D46C76,#FFC07C);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   font-family:monospace;
                   margin-left:1.5rem">
            CODE CRITIC
        </h1>
    """
st.markdown(title,unsafe_allow_html=True)

# session state to display history 
if "review_history" not in st.session_state:
    st.session_state["review_history"] = []

upload_file = st.file_uploader("Upload your code file",type=["py","js","cpp","c","txt"])
code_content = ""

if upload_file is not None:
    code_content  = upload_file.read().decode("utf-8")
    st.subheader("uploaded code:")
    with st.expander("click to see uploaded code."):
        st.code(code_content,language=upload_file.name.split('.')[-1])

# displaying code review when button is clicked
if code_content:
    if st.button("Get Review"):
        with st.spinner("Analysing your code..."):
            suggestions = codeCritic(code_content)
        st.subheader("Code Review:")
        with st.expander("click here to collapse.",expanded=True):
            st.markdown(suggestions)

        # save in session_state for displaying
        tm = datetime.datetime.now()
        st.session_state["review_history"].append({
            "uploaded_code":code_content,
            "suggestion":suggestions,
            "time": tm.strftime("%a-%d-%b-%y")
        })

        st.success("review save in history")

# sidebar to show review history using session_state
st.sidebar.header("Review History")

if st.session_state["review_history"]:
    for review in reversed(st.session_state["review_history"]):
        with st.sidebar.expander(f"review on:{review['time']}"):
            st.subheader("uploaded code")
            st.code(review["uploaded_code"])
            st.subheader("suggestion")
            st.markdown(review["suggestion"])
else:
    st.sidebar.info("No past code reviw in this session yet..")