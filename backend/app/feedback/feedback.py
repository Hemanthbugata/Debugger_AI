import logging

class FeedbackProcessor:
    def __init__(self):
        self._feedback_log = []

    def process(self, feedback: dict):
        logging.info(f"User feedback received: {feedback}")
        self._feedback_log.append(feedback)
        return {"status": "received"}