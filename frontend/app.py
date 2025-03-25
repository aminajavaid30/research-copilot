import streamlit as st
import requests
import json

# Set Streamlit page configurations
st.set_page_config(page_title="AI Research Copilot", layout="wide")

# Initialize session state variables to maintain user input and results
if "result_json" not in st.session_state:
    st.session_state.result_json = None
if "research_topic" not in st.session_state:
    st.session_state.research_topic = ""
if "max_papers" not in st.session_state:
    st.session_state.max_papers = 5
if "selected_paper" not in st.session_state:
    st.session_state.selected_paper = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Define API URL for backend communication
API_URL = "http://127.0.0.1:8000"

# Sidebar UI for user inputs and controls
with st.sidebar:
    st.image("../images/research_copilot_logo.png", width=150)  # Display logo
    st.subheader("Search and Generate Literature Reviews")
    st.header("🔍 Search Papers")
    
    # Input fields for research topic and number of papers
    topic = st.text_input("Enter Research Topic:", key="topic_input", value=st.session_state.research_topic)
    max_papers = st.number_input("Number of Papers to Fetch:", min_value=1, max_value=10, value=st.session_state.max_papers, key="papers_input")
    
    col_btn1, col_btn2 = st.columns([2, 1])  # Layout for buttons
    
    with col_btn1:
        # Fetch papers button
        if st.button("Fetch Papers & Generate Review"):
            if topic:
                st.session_state.research_topic = topic
                try:
                    with st.spinner("Fetching papers from arXiv..."):
                        response = requests.post(API_URL+"/fetch_papers/", json={"topic": topic, "max_papers": max_papers})
                    
                    if response.status_code != 200:
                        st.error("Error: Invalid response from server.")
                        st.stop()
                    
                    # Parse response JSON
                    result_decoded = response.content.decode("utf-8")
                    st.session_state.result_json = json.loads(result_decoded)
                
                except json.JSONDecodeError:
                    st.error("Error: Received an unreadable response from the server.")
                    st.stop()
                except requests.exceptions.RequestException:
                    st.error("Error: Could not connect to the server.")
                    st.stop()
    
    with col_btn2:
        # Refresh button to clear results and reset inputs
        if st.button("🔄 Refresh"):
            st.session_state.result_json = None
            st.session_state.research_topic = ""
            st.session_state.max_papers = 5
            st.rerun()

# Display main application title
st.title("AI Research Copilot")

# Show instructions if no results are available
if st.session_state.result_json is None:
    st.info("Enter a research topic and click 'Fetch Papers & Generate Review' to get started.")

# Display results if available
if st.session_state.result_json:
    research_topic = st.session_state.research_topic.title()  # Capitalize topic words
    st.header(f"📖 Literature Review: {research_topic}")
    
    if "pdf_path" in st.session_state.result_json:
        pdf_path = st.session_state.result_json["pdf_path"]
        filename = f"{topic.replace(' ', '_')}_literature_review.pdf"
        
        # Layout for success message and download button
        col_success, col_download = st.columns([5, 1])
        
        with col_success:
            st.success("Literature Review Generated!")
        
        with col_download:
            st.download_button(label="📥 Download", 
                               data=open(pdf_path, "rb"), 
                               file_name=filename, 
                               mime="application/pdf")
    
    # Extract and display literature review details
    response = st.session_state.result_json.get("response")
    data = json.loads(response)
    papers = data.get("papers", [])
    conclusion = data.get("conclusion", "")
    references = data.get("references", [])
    
    if papers:
        # Iterate through each retrieved paper and display details
        for i, paper in enumerate(papers):
            with st.container():
                st.subheader(f"📄 {i+1}. {paper['title']}")
                st.markdown(f"**🖊️ Authors:** {paper['authors']}")
                st.markdown(f"**📅 Publication Date:** {paper['publication_date'][:10]}")
                st.markdown(f"**🔑 Keywords:** {paper['keywords']}")
                st.markdown("**📌 Summary:**")
                st.write(paper["summary"])
                st.markdown("**📝 Review:**")
                st.write(paper["review"])
                st.divider()
        
        # Display conclusion section
        st.subheader("🧐 Conclusion")
        st.write(conclusion)
        
        # Display references section
        st.subheader("📚 References")
        for ref in references:
            st.markdown(f"- {ref}")
    else:
        st.error("No papers found!")
