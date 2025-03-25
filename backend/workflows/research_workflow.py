from agno.agent import Agent
from agno.workflow import Workflow, RunResponse, RunEvent
from agno.storage.workflow.sqlite import SqliteWorkflowStorage
from agno.utils.pprint import pprint_run_response
from agno.utils.log import logger

from agents.summarization_agent import summarization_agent
from agents.review_generation_agent import review_generation_agent

# Define the ResearchCopilot workflow 
class ResearchCopilot(Workflow):
    summarization_agent: Agent = summarization_agent
    review_generation_agent: Agent = review_generation_agent

    def run(self, topic: str, max_papers: int = 5) -> RunResponse:
        """
            Executes the research workflow:
            1. Searches for research papers related to the topic.
            2. Generates a literature review based on the extracted papers.
        """
        logger.info(f"Generating a literature review of {max_papers} research papers from arXiv on: {topic}")

        # Step 1: Search arXiv for research papers on the topic and summarize them
        extracted_papers = self.get_extracted_papers(topic, max_papers)
        
        # If no extracted papers are found for the topic, end the workflow
        if extracted_papers is None:
            return RunResponse(
                event=RunEvent.workflow_completed,
                content=f"Sorry, could not find any research papers on the topic: {topic}",
            )           
        
        print("Extracted papers:", extracted_papers)

        # Step 2: Generate a literature review of the extracted papers
        literature_review: RunResponse = self.review_generation_agent.run(extracted_papers)
        if literature_review is None:
            return RunResponse(
                event=RunEvent.workflow_completed,
                content="Sorry, could not generate a literature review of the research papers.",
            )
        
        print("Literature review:", literature_review.content)
        return RunResponse(
            event=RunEvent.workflow_completed,
            content=literature_review.content,
        )

    def get_extracted_papers(self, topic: str, max_papers: int):
        """Get the search results for a topic."""

        MAX_ATTEMPTS = 3

        for attempt in range(MAX_ATTEMPTS):
            try:
                prompt = f"Search for {max_papers} most relevant papers on {topic}."
                summarizer_response: RunResponse = self.summarization_agent.run(prompt)

                # Validate response content
                if not summarizer_response or not summarizer_response.content:
                    logger.warning(f"Attempt {attempt + 1}/{MAX_ATTEMPTS}: Empty searcher response")
                    continue

                logger.info(f"Found papers on the topic {topic} in attempt {attempt + 1}")

                print("Extracted papers:", summarizer_response.content)
                return summarizer_response.content
            
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1}/{MAX_ATTEMPTS} failed: {str(e)}")

        logger.error(f"Failed to get extracted papers after {MAX_ATTEMPTS} attempts")
        return None
    

# Initialize the Research Copilot workflow with SQLite storage
research_workflow = ResearchCopilot(
    session_id=f"generate-literature-review",
    storage=SqliteWorkflowStorage(
        table_name="generate_literature_review_workflows",
        db_file="workflows/db/workflows.db",
    ),
)
