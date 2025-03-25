from agno.agent import Agent, RunResponse
from agno.models.together import Together
from agno.tools.arxiv import ArxivTools
from tools.paper_download_tool import download_arxiv_papers
from dotenv import load_dotenv
import os

load_dotenv()

# Define the summarization agent
summarization_agent = Agent(
    name="summarization-agent",
    model=Together(id="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", api_key=os.getenv("TOGETHER_API_KEY")),
    tools=[ArxivTools(), download_arxiv_papers],
    role="Download papers from arXiv and save them for further processing.",
    description=
    '''
        You are a summarization agent that will fetch papers from arXiv based on a given topic and maximum number of papers.
        You will extract the metadata, summary, and a list of source links of the papers and download them in pdf format.
    ''',
    instructions=[
        "Search for the latest and most relevant research papers on the given topic from arXiv.",
        "If the number of papers is not specified, fetch 5 by default.",
        "Extract the metadata, summary, and a list of source links of the papers for downloading.",
        "For each paper, extract the following metadata: title, abstract, authors, publication date, keywords, and source link.",
        "Download the papers in pdf format for processing by other agents.",
        "Your response should include a list of the extracted papers including the following information for each paper:"
        "1. Metadata: Title, Authors, Abstract,Publication Date, Keywords, Source Link",
        "2. Summary: Abstract or a concise summary of the paper",
        "3. Paths to the downloaded papers for further processing",
        "The information for each paper must be included in the following format.",
            "Title: [Title of the Paper]",
            "Authors: [Authors of the Paper]",
            "Abstract: [Abstract of the Paper]",
            "Publication Date: [Date of Publication]",
            "Keywords: [Keywords of the Paper]",
            "Source Link: [Source Link of the Paper]",
            "Summary: [Summary of the Paper]",
            "PDF Path: [Path to the Downloaded Paper]"
    ],
    markdown=True,
    show_tool_calls=True,
    debug_mode=True
)
