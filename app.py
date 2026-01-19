import streamlit as st
from agents import AgentManager
from utils.logger import logger
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
    text = st.text_area("Enter historical text to summarize:", height=200)
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
            st.warning("Please enter some text to summarize.")

def write_and_refine_article_section(agent_manager):
    st.header("Write and Refine Historical Article")
    topic = st.text_input("Enter the topic for the historical article:")
    outline = st.text_area("Enter an outline (optional):", height=150)
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
    year_century = st.text_area("Enter Year/Century to get important events:", height=100)
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
            st.warning("Please enter Year/Century.")

if __name__ == "__main__":
    main()
