from .agent_base import AgentBase

class EventsFinderTool(AgentBase):
    def __init__(self, max_retries, verbose=True):
        super().__init__(name="EventsFinderTool",max_retries= max_retries,verbose = verbose)

    def execute(self,year_century):
        messages = [
            {"role": "system", "content" : "You are an AI assistant that searches numerous events that happened on a given year/century."},
            {
                "role": "user",
                "content": (
                    "Find and provide brief summary of the most important events that happened on the given year/century:\n\n"
                    f"Given year/century {year_century}:\n\n"
                )
            }
        ]
        historical_events = self.call_openai(messages,max_tokens= 500)
        return historical_events