
class MessageHistory:
    def __init__(self, max_history_length=4):
        self.previous_prompt_requests = []
        self.previous_responses = []
        self.max_history_length = max_history_length

    def add_message(self, prompt_request, prompt_response):
        self.previous_prompt_requests.append(prompt_request)
        self.previous_responses.append(prompt_response)

        if len(self.previous_prompt_requests) > self.max_history_length:
            self.previous_prompt_requests.pop(0)
            self.previous_responses.pop(0)

    def get_history_text(self, full=False):
        history_text = ""
        for i in range(len(self.previous_prompt_requests)):
            if full:
                history_text += f"Request: {self.previous_prompt_requests[i]}\n"
                history_text += f"Prompt: {self.previous_responses[i]['prompt']}\nTitle: {self.previous_responses[i]['title']}\nPoints: {self.previous_responses[i]['points']}\n"
                history_text += "---\n"
            else:
                history_text += f"User: {self.previous_prompt_requests[i]}\n"
                history_text += f"You: {self.previous_responses[i]['prompt']}\n"
        return history_text

    def clear_history(self):
        self.previous_prompt_requests = []
        self.previous_responses = []