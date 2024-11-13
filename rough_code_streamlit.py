import streamlit as st
from gpt_researcher import GPTResearcher
import asyncio

async def gpt_res(query, q_type = 1):
    """
    This is a sample script that shows how to run a research report.
    """
    # Report Type
    report_type = "custom_report"
    inner_query = """
                    Show me the details for the above mentioned oil regarding their price forcast for upcoming months with the following rules
                    ->Heading: Display each oil type entered by the user as a heading.
                    ->Summary: Under each heading, provide a bullet-point summary with concise insights 
                    (under 200 words) on the price trends and relevant factors for that oil type. 
                    Focus on recent trends, key drivers, and brief historical context if available.
                    ->References: Include a "References" section below each summary with the URLs of the sources used to gather the data for that oil."""
    
    prompt = query + inner_query
    # return prompt
    
    # prompt = query +  """
    #             Show me the details for the above mentioned oil with the following rules
    #             - Heading should be the oil name
    #             -below the head will be the summary of above mentioned oil Prices and trends in bullet format
    #             -the data should be concise and less than 200 words
    #             - Below that, the sources should be mentioned in reference section
    #             """
    report_source = "static"
    pdf_source = "local"
    # sources = ['https://vespertool.com/news/india-palm-oil-prices-have-reached-their-peak/']
    sources = [
        'https://vespertool.com/news/india-palm-oil-prices-have-reached-their-peak/',
        'https://vespertool.com/news/palm-oil-hits-yearly-high/',
        'https://vespertool.com/news/eudr-compliant-crude-palm-oil-benchmark-rises/',
        'https://vespertool.com/news/palm-maintains-tight-spread-with-soy/',
        'https://vespertool.com/news/palm-oil-higher-freight-rates-improved-production/'
    ]

    # Initialize the researcher
    if q_type == 0:
        researcher = GPTResearcher(query=prompt, report_type=report_type, config_path=None)
    if q_type == 1:
        researcher = GPTResearcher(query=prompt, report_source=report_source, source_urls=sources, report_type=report_type)
    if q_type == 2:
        researcher = GPTResearcher(query=prompt, report_source=pdf_source, report_type=report_type)
    # Conduct research on the given query
    await researcher.conduct_research()
    # Write the report
    report = await researcher.write_report()
    
    return report

st.title("OilPrice Insight")


# Input from the user
query = st.text_input("Enter oil names to analyze their price trends")
# query_type = 0
report = ''

# Button to submit the query
if st.button("Run General Internet Search – Analyze content broadly across the internet"):
    report = asyncio.run(gpt_res(query, q_type= 0))
if st.button("Analyze Preset URLs – Focus analysis on specified, user-defined web links"):
    report = asyncio.run(gpt_res(query,  q_type= 1))
if st.button("Analyze Local PDF Documents – Conduct analysis on PDF research files stored locally."):
    report = asyncio.run(gpt_res(query, q_type= 2)) 
st.write(report)