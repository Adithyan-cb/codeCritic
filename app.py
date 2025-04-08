import streamlit as st
from dotenv import load_dotenv
from database import get_db,CodeReview
from sqlalchemy.orm import Session
from codecritic import codeCritic


# creating a uploader using streamlit
st.title("Code Critic")

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

        # save the review in database
        db: Session = next(get_db())
        db_review = CodeReview(uploaded_code=code_content,
                               suggestions=suggestions)
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        st.success("Code review saved to history!")

# sidebar to show review history
st.sidebar.header("Review History")

db: Session = next(get_db())
past_reviews = db.query(CodeReview).order_by(CodeReview.timestamp.desc()).limit(5).all() # Display last 5 reviews

if past_reviews:
    for review in past_reviews:
        with st.sidebar.expander(f"Review on {review.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"):
            st.subheader("Uploaded Code:")
            st.code(review.uploaded_code)
            st.subheader("Suggestions:")
            st.markdown(review.suggestions)
else:
    st.sidebar.info("No past code reviews yet.")