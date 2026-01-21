import streamlit as st
from agents import AgentManager
from utils.logger import logger
from utils.file_validator import file_upload_section
from dotenv import load_dotenv

load_dotenv()

def main():
    st.set_page_config(page_title= "Historical Agent AI System", layout="wide")
    st.title("Historical-Agent AI system with Description and Validation")

    st.sidebar.title("Select Task")
    task = st.sidebar.selectbox("Choose Task:",[
            "Summarize Historical Text",
            "Write and Refine Historical Article",
            "Find events on a given Year/Century"
        ]
    )

    agent_manager = AgentManager(max_retries=2,verbose=True)

    if task == "Summarize Historical Text":
        summarize_section(agent_manager)

    elif task == "Write and Refine Historical Article":
        write_and_refine_article_section(agent_manager)

    elif task == "Find events on a given Year/Century":
        historical_events_finder(agent_manager)

def summarize_section(agent_manager):
    st.header("Summarize Historical Text")
    
    # Add input method selection
    input_method = st.radio("Choose input method:", ["Type Text", "Upload File"], key="summarize_input")
    
    text = None
    
    if input_method == "Type Text":
        text = st.text_area("Enter historical text to summarize:", height=200, key="summarize_text")
    else:
        # File upload
        content, filename = file_upload_section(
            label="Upload a historical text file",
            help_text="Upload .txt, .md, .pdf, .docx, or .csv files",
            key="summarize_file"
        )
        if content:
            text = content
            with st.expander("📄 View uploaded content"):
                st.text_area("File content:", value=text, height=200, disabled=True)
    
    if st.button("Summarize"):
        if text:
            main_agent = agent_manager.get_agent("summarize")
            validator_agent = agent_manager.get_agent("summarize_validator")
            with st.spinner("Summarizing..."):
                try:
                    summary = main_agent.execute(text)
                    st.subheader("Summary:")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Error: {e}")
                    logger.error(f"SummarizeAgent Error: {e}")
                    return

            with st.spinner("Validating summary..."):
                try:
                    validation = validator_agent.execute(original_text=text, summary=summary)
                    st.subheader("Validation:")
                    st.write(validation)
                except Exception as e:
                    st.error(f"Validation Error: {e}")
                    logger.error(f"SummarizeValidatorAgent Error: {e}")
        else:
            st.warning("Please enter some text or upload a file to summarize.")

def write_and_refine_article_section(agent_manager):
    st.header("Write and Refine Historical Article")
    
    topic = st.text_input("Enter the topic for the historical article:")
    
    # Add option for outline input
    outline_method = st.radio("Outline input method:", ["Type Outline", "Upload File"], key="outline_input")
    
    outline = None
    
    if outline_method == "Type Outline":
        outline = st.text_area("Enter an outline (optional):", height=150, key="outline_text")
    else:
        content, filename = file_upload_section(
            label="Upload an outline file (optional)",
            help_text="Upload .txt, .md, or .docx files",
            key="outline_file"
        )
        if content:
            outline = content
            with st.expander("📄 View uploaded outline"):
                st.text_area("Outline content:", value=outline, height=150, disabled=True)
    
    if st.button("Write and Refine Article"):
        if topic:
            writer_agent = agent_manager.get_agent("write_article")
            refiner_agent = agent_manager.get_agent("refiner")
            validator_agent = agent_manager.get_agent("validator")
            with st.spinner("Writing article..."):
                try:
                    draft = writer_agent.execute(topic, outline)
                    st.subheader("Draft Article:")
                    st.write(draft)
                except Exception as e:
                    st.error(f"Error: {e}")
                    logger.error(f"WriteArticleAgent Error: {e}")
                    return

            with st.spinner("Refining article..."):
                try:
                    refined_article = refiner_agent.execute(draft)
                    st.subheader("Refined Article:")
                    st.write(refined_article)
                except Exception as e:
                    st.error(f"Refinement Error: {e}")
                    logger.error(f"RefinerAgent Error: {e}")
                    return

            with st.spinner("Validating article..."):
                try:
                    validation = validator_agent.execute(topic=topic, article=refined_article)
                    st.subheader("Validation:")
                    st.write(validation)
                except Exception as e:
                    st.error(f"Validation Error: {e}")
                    logger.error(f"ValidatorAgent Error: {e}")
        else:
            st.warning("Please enter a topic for the historical article.")

def historical_events_finder(agent_manager):
    st.header("Find events on a given Year/Century")
    
    # Add input method selection
    input_method = st.radio("Choose input method:", ["Type Date", "Upload File"], key="events_input")
    
    year_century = None
    
    if input_method == "Type Date":
        year_century = st.text_area("Enter Year/Century to get important events:", height=100, key="events_text")
    else:
        # File upload - useful if user has multiple dates/years
        content, filename = file_upload_section(
            label="Upload a file with years/centuries",
            help_text="Upload .txt or .csv file with dates",
            key="events_file"
        )
        if content:
            year_century = content
            with st.expander("📄 View uploaded dates"):
                st.text_area("File content:", value=year_century, height=100, disabled=True)
    
    if st.button("Find Events"):
        if year_century:
            main_agent = agent_manager.get_agent("historical_events")
            validator_agent = agent_manager.get_agent("historical_events_validator")
            with st.spinner("Searching events..."):
                try:
                    historical_events = main_agent.execute(year_century)
                    st.subheader("Historical Events:")
                    st.write(historical_events)
                except Exception as e:
                    st.error(f"Error: {e}")
                    logger.error(f"HistoricalEventAgent Error: {e}")
                    return

            with st.spinner("Validating historical events..."):
                try:
                    validation = validator_agent.execute(year_century=year_century, historical_events=historical_events)
                    st.subheader("Validation:")
                    st.write(validation)
                except Exception as e:
                    st.error(f"Validation Error: {e}")
                    logger.error(f"EventsFinderValidatorAgent Error: {e}")
        else:
            st.warning("Please enter Year/Century or upload a file.")

if __name__ == "__main__":
    main()