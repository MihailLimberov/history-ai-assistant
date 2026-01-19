from .agent_base import AgentBase

class EventsFinderValidatorAgent(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="EventsFinderValidatorAgent",max_retries= max_retries,verbose = verbose)

    def execute(self,year_century,historical_events):
        system_message = "You are an expert AI assistant that validates the events that happened on a current year/century."
        user_content = (
            "Given the original data and the historical events, verify that the brief summary of the events is indeed correct.\n"
            "Provide a brief analysis and rate the summary of the events on a scale from 1 to 5, where 5 indicates an excellent quality.\n\n"
            f"Given year/century: \n{year_century}\n\n"
            f"Historical Events in that year/century: \n{historical_events}\n\n"
            "Validation"
        )

        messages = [
            {"role" : "system", "content": system_message},
            {"role" : "user" , "content" : user_content}
        ]    
        validation = self.call_openai(messages,max_tokens= 512)
        return validation