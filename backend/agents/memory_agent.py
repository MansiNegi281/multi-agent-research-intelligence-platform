class MemoryAgent:

    def __init__(self):
        self.history = []

    def add(self, question, answer):

        self.history.append(
            {
                "question": question,
                "answer": answer
            }
        )

        # Keep only last 5 interactions
        if len(self.history) > 5:
            self.history.pop(0)

    def get_context(self):

        if not self.history:
            return ""

        context = ""

        for chat in self.history:

            context += f"""
User: {chat['question']}

Assistant: {chat['answer']}

"""

        return context

    def clear(self):
        self.history = []