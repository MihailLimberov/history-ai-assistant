from .agent_base import AgentBase

class WriteArticleValidatorAgent(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="WriteArticleValidatorAgent",max_retries= max_retries,verbose = verbose)

    def execute(self,topic,article):
        system_message = "You are an expert AI assistant that validates historical articles."
        user_content = (
            "Given the topic ant the historical article, evaluate whether the historical article comprehensively covers the topic, follow a logical stucture and maintains academic standarts.\n"
            "Provide a brief analysis and rate the article on a scale of 1 to 5, where 5 indicates an excellent quality.\n\n"
            f"Topic: {topic}\n\n"
            f"Article: \n{article}\n\n"
            "Validation"
        )

        messages = [
            {"role" : "system", "content": system_message},
            {"role" : "user" , "content" : user_content}
        ]    
        validation = self.call_openai(messages,max_tokens= 512)
        return validation