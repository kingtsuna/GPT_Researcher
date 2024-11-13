import streamlit as st
from gpt_researcher import GPTResearcher
import asyncio

# Function to handle research query
async def gpt_res(query, q_type=1):
    report_type = "custom_report"
    inner_query = """
                    Show me the details for the above mentioned oil with the following rules:
                    -> Heading: Display each oil type entered by the user as a heading.
                    -> Summary: Under each heading, provide a bullet-point summary with concise insights 
                    (under 200 words) on the price trends and relevant factors for that oil type. 
                    Focus on recent trends, key drivers, and brief historical context if available.
                    -> References: Include a "References" section below each summary with the URLs of the sources used to gather the data for that oil.
                   """
    prompt = query + inner_query
    
    # Define report sources
    report_source = "static"
    pdf_source = "local"
    sources = [
        'https://vespertool.com/news/india-palm-oil-prices-have-reached-their-peak/',
        'https://vespertool.com/news/palm-oil-hits-yearly-high/',
        'https://vespertool.com/news/eudr-compliant-crude-palm-oil-benchmark-rises/',
        'https://vespertool.com/news/palm-maintains-tight-spread-with-soy/',
        'https://vespertool.com/news/palm-oil-higher-freight-rates-improved-production/'
    ]

    # Initialize the researcher based on the query type
    if q_type == 0:
        researcher = GPTResearcher(query=prompt, report_type=report_type, config_path=None)
    elif q_type == 1:
        researcher = GPTResearcher(query=prompt, report_source=report_source, source_urls=sources, report_type=report_type)
    elif q_type == 2:
        researcher = GPTResearcher(query=prompt, report_source=pdf_source, report_type=report_type)

    await researcher.conduct_research()
    report = await researcher.write_report()
    
    return report

# Streamlit UI
st.title("Oil Price Insight Generator")
st.write("Analyze oil price trends and insights from various sources.")

# Query input section
st.subheader("Enter Details")
query = st.text_input("Enter oil names to analyze their price trends", placeholder="e.g., Palm Oil, Crude Oil, Soybean Oil")

# Display buttons with explanations for each type of search
st.subheader("Select Analysis Method")
st.write("Choose an analysis method based on the type of information you need.")

# Execute respective search function based on user selection
report = ''
if st.button("Analyze from Unconfirmed Sources"):
    st.write("**Analyzing content broadly across the internet...**")
    report = asyncio.run(gpt_res(query, q_type=1))

# if st.button("Analyze Preset URLs"):
#     st.write("**Focusing analysis on user-defined web links...**")
#     report = asyncio.run(gpt_res(query, q_type=1))

if st.button("Analyze From Confirmed Sources"):
    st.write("**Conducting analysis on confirmed sources...**")
    report = asyncio.run(gpt_res(query, q_type=2))

# Display the generated report
if report:
    st.subheader("Generated Report")
    st.write(report)
else:
    st.info("Your analysis report will appear here after selection.")
