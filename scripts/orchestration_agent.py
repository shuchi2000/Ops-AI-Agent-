import json
import os
from transformers import pipeline

def handle_query(query):
    # Load the intent examples from the JSON file
    intent_examples = {
        "client_program": [
            "Which learners are enrolled in client X's program?",
            "List programs mapped to each learner",
        ],
        "attendance": [
            "What is the attendance of learner John?",
            "Show me attendance data for March",
        ],
        "content_progress": [
            "Which learners have completed module 2?",
            "How many learners are in progress with the content?",
        ],
        "progress_report": [
            "Give me the progress status of each learner",
            "Who hasn't completed the required modules yet?",
        ],
        "score_report": [
            "What are the scores for learners in the final test?",
            "Show me the average score per learner",
        ]
    }

    # Initialize the zero-shot classifier
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    # Function to get the most likely intent based on the query
    def get_intent(query):
        # Flatten all example questions into a list of labels
        labels = []
        for intent, examples in intent_examples.items():
            labels.extend(examples)  # Add all example questions for each intent
        
        # Perform zero-shot classification
        result = classifier(query, labels)

        # Match the most likely label to an intent
        matched_label = result['labels'][0]
        
        # Map the matched label back to the intent
        for intent, examples in intent_examples.items():
            if matched_label in examples:
                return intent  # Return the matching intent
        
        return "Unknown"  # If no match is found, return Unknown

    # Function to map the intent to the corresponding file path
    def route_to_file(intent):
        file_mapping = {
            "client_program": "client_program_learner.csv",
            "attendance": "learner_attendence.csv",
            "content_progress": "progress_content_deploy.csv",
            "progress_report": "progress_report.csv",
            "score_report": "score_report.csv"
        }

        # Base directory
        base_dir = r"C:\Users\shuchismita_mallick.Shuchismita\GenAI-Projects\Operation AI Agent\data"

        # Use os.path.join() to correctly construct the full file path
        return os.path.join(base_dir, file_mapping.get(intent, 'default_file.csv'))

    # Get the intent from the query
    intent = get_intent(query)

    # Get the file path for the identified intent
    file_path = route_to_file(intent)

    # Return the intent and corresponding file path
    return {
        "intent": intent,
        "file_path": file_path
    }
