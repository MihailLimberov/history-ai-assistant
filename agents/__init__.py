from .summarize_tool import SummarizeTool
from .write_article_tool import WriteArticleTool
from .events_finder_tool import EventsFinderTool
from .summary_validator_agent import SummarizeValidatorAgent
from .write_article_validator_agent import WriteArticleValidatorAgent
from .events_finder_validator_agent import EventsFinderValidatorAgent
from .refiner_agent import RefinerAgent
from .validator_agent import ValidatorAgent

class AgentManager:
    def __init__(self,max_retries=2,verbose=True):
        self.agents = {
            "summarize": SummarizeTool(max_retries=max_retries,verbose=verbose),
            "write_article": WriteArticleTool(max_retries=max_retries,verbose=verbose),
            "historical_events": EventsFinderTool(max_retries = max_retries, verbose = verbose),#...
            "summarize_validator": SummarizeValidatorAgent(max_retries=max_retries,verbose=verbose),
            "write_article_validator":WriteArticleValidatorAgent(max_retries=max_retries,verbose=verbose),
            "historical_events_validator": EventsFinderValidatorAgent(max_retries=max_retries,verbose=verbose),#...
            "refiner": RefinerAgent(max_retries=max_retries,verbose=verbose),
            "validator": ValidatorAgent(max_retries=max_retries,verbose=verbose)
        }
    def get_agent(self,agent_name):
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found")
        return agent
