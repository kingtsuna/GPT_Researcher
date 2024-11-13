import streamlit as st
from gpt_researcher import GPTResearcher
import asyncio

async def gpt_res(query, q_type = 1):
    """
    This is a sample script that shows how to run a research report.
    """
    # Report Type
    report_type = "research_report"
    inner_query = """
                    Show me the details for the above mentioned oil regarding their price forcast for upcoming months with the following rules
                    ->Heading: Display each oil type entered by the user as a heading.
                    ->Summary: Under each heading, provide a bullet-point summary with concise insights 
                    (under 200 words) on the price trends and relevant factors for that oil type. 
                    Focus on recent trends, key drivers, and brief historical context if available.
                    ->References: Include a "References" section below each summary with the URLs of the sources used to gather the data for that oil."""
    
    # prompt = query + inner_query
    
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
 
        'https://www.ncbi.nlm.nih.gov/books/?term=Curcumin'
    ]

    # Initialize the researcher
    if q_type == 0:
        researcher = GPTResearcher(query=query, report_type=report_type, config_path=None)
    if q_type == 1:
        researcher = GPTResearcher(query=query, report_source=report_source, source_urls=sources, report_type=report_type)
    if q_type == 2:
        researcher = GPTResearcher(query=query, report_source=pdf_source, report_type=report_type)
    # Conduct research on the given query
    await researcher.conduct_research()
    # Write the report
    report = await researcher.write_report()
    
    return report

st.title("Medical Insights from Trusted Sources")


# Input from the user
query = st.text_input("Ask Your Question")
# query_type = 0
report = ''

# Button to submit the query
if st.button("Search on Untrusted Sources"):
    report = asyncio.run(gpt_res(query, q_type= 0))
if st.button("Search on Trusted Sources"):
    report = asyncio.run(gpt_res(query,  q_type= 1))
if st.button("Scan Local. (still working...)"):
    report = asyncio.run(gpt_res(query, q_type= 2)) 
st.write(report)