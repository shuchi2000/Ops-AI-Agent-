import pandas as pd
from datetime import datetime

# Function to fetch program codes under each client
def fetch_program_codes(Client_name):
    # Read the CSV file
    df = pd.read_csv(r"C:\Users\shuchismita_mallick.Shuchismita\GenAI-Projects\Operation AI Agent\data\client_program_learner.csv")
    
    # Assuming the file has columns: 'client_name' and 'program_code'
    if 'Client_name' not in df.columns or 'code' not in df.columns:
        raise ValueError("CSV file must contain 'client_name' and 'program_code' columns")
    
    # Group by client_name and collect program codes
    client = df[df['Client_name']== Client_name]
    code = client['code'].unique()
    code = list(code)
    
    return code

import pandas as pd

# Function to fetch program codes and additional information under each client
def fetch_program_info(Client_name, Program_code):
    # Read the CSV file
    df = pd.read_csv(r"C:\Users\shuchismita_mallick.Shuchismita\GenAI-Projects\Operation AI Agent\data\client_program_learner.csv")
    
    # Assuming the file has columns: 'Client_name', 'program_code', 'created_at', 'owner', 'spoc', and 'learner_id'
    if 'Client_name' not in df.columns or 'code' not in df.columns:
        raise ValueError("CSV file must contain 'Client_name' and 'program_code' columns")
    
    # Filter by client and program code
    client_program = df[(df['Client_name'] == Client_name) & (df['code'] == Program_code)]
    
    if client_program.empty:
        raise ValueError(f"No program found for {Client_name} with the code {Program_code}")

    # Extracting required details
    created_at = datetime.strptime(client_program['Program_created_at'].iloc[0], '%Y-%m-%d %H:%M:%S.%f').date()
    owner = client_program['owner_emails'].iloc[0].strip('[]')
    spoc = client_program['spoc_emails'].iloc[0].strip('[]')
    total_learners = client_program['learner_id'].nunique()  # Assuming learner_id column represents each learner uniquely
    
    program_info = {
        'Program Created At': created_at,
        'Owner mail id:': owner,
        'Spoc mail id': spoc,
        'Tota Learners': total_learners
    }
    
    return program_info

    
# Example usage (uncomment if you want to run standalone)
client_programs = fetch_program_codes("Fractal Analytics")
client_programs

