from fastapi import FastAPI
from pydantic import BaseModel
from agents.chat_agent import chat_agent
from workflows.research_workflow import research_workflow
from agno.agent import RunResponse
from knowledge.knowledge_base import pdf_knowledge_base
from utils import extract_metadata, save_paper_metadata, generate_pdf
import os

# Initialize FastAPI application
app = FastAPI()

# Define request model for research paper fetching
class ResearchRequest(BaseModel):
    topic: str  # Research topic to fetch papers for
    max_papers: int = 5  # Default number of papers to fetch

@app.post("/fetch_papers/")
async def fetch_papers(request: ResearchRequest):
    """
    Endpoint to fetch research papers and generate a literature review.
    Executes the research workflow and processes the retrieved papers.
    """
    print("Executing workflow...")
    
    # Run the research workflow to fetch relevant papers
    response: RunResponse = research_workflow.run(topic=request.topic, max_papers=request.max_papers)

    if response:
        # Extract metadata from the response
        metadata = extract_metadata(response.content)
        metadata_file = save_paper_metadata(request.topic, metadata)
        
        # Generate and save the literature review PDF
        generate_pdf(request.topic, response.content)
        pdf_path = os.path.join("../literature_reviews", f"{request.topic.replace(' ', '_')}_literature_review.pdf")

        return {
            "message": "Literature review generated!",
            "pdf_path": pdf_path,
            "response": response.content
        }
    else:
        return {"error": "No papers found"}
