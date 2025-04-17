import os
from langchain_experimental.agents import create_csv_agent
from langchain_anthropic import ChatAnthropic
from orchestration_agent import handle_query

# Initialize the LLM (Claude 3)
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

def agent(prompt):
    """
    This function handles the incoming prompt, fetches the corresponding file path based on intent,
    and returns the answer by utilizing the agent.
    """
    # Get the file path based on the intent extracted from the query
    file_path = handle_query(prompt)['file_path']
    
    # Check if the file exists at the determined path
    if os.path.exists(file_path):
        # File exists, create the CSV agent
        agent = create_csv_agent(
            llm=llm, 
            path=file_path, 
            verbose=True, 
            allow_dangerous_code=True, 
            handle_parsing_errors=True
        )
        
        # Use the agent to answer the query
        answer = agent.run(prompt)
        
        return answer
    else:
        # File does not exist, return an error message
        return "Sorry, we don't have any information regarding this."

# Example usage
if __name__ == "__main__":
    query = "What is the status of content progress?"  # Example query
    result = agent(query)
    print(result)
