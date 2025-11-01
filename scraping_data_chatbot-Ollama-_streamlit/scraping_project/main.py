import streamlit as st
from langchain import requests
from scrape import scrape_website,split_content,extract_body_content,extract_cleaned_body
from modeling import parse_using_ollama

st.title('AI WEB SCRAPER')
url = st.text_input("Enter the url ")
if st.button("Scrape the website"):
    st.write("Scraping the website....")
    source = scrape_website(url)
    body_content = extract_body_content(source)
    cleaned_content = extract_cleaned_body(body_content)


    st.session_state.dom_content = cleaned_content
    with st.expander("view cleaned content"):
       st.text_area("content: ",cleaned_content,height=300)


if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            # Parse the content with Ollama
            chunks = split_content(st.session_state.dom_content)
            parsed_result = parse_using_ollama(chunks, parse_description)
            st.write(parsed_result)





