import streamlit as st
import pandas as pd

# Import the updated function to fetch program details
from program_details import fetch_program_info, fetch_program_codes
from agent_2 import agent  # Import the agent function

# Step 1: Ask for Client Name
st.title("Client Query Interface")

if 'client_submitted' not in st.session_state:
    st.session_state.client_submitted = False

if not st.session_state.client_submitted:
    client_name = st.text_input("Enter Client Name")
    if st.button("Submit Client Name"):
        if client_name:
            try:
                # Fetch program codes for the client using the function
                client_programs = fetch_program_codes(client_name)
                
                # Check if programs exist for the given client
                if client_programs:
                    st.session_state.client_name = client_name
                    st.session_state.client_submitted = True
                    st.session_state.client_programs = client_programs
                else:
                    st.warning("No program codes found for this client.")
            except ValueError as e:
                st.warning(str(e))  # Show error if there are issues with the CSV
        else:
            st.warning("Please enter a client name.")

# Step 2: Show Program Code select box for the selected client
if st.session_state.get('client_submitted', False):
    st.success(f"Client: {st.session_state.client_name}")
    
    # Use the list of program codes for the client in the select box
    program_code = st.selectbox("Select Program Code", st.session_state.client_programs)
    
    # Step 3: Fetch Program Information after program code is selected
    if program_code:
        try:
            # Fetch the program info only after the program code is selected
            program_info = fetch_program_info(st.session_state.client_name, program_code)
            
            # Display program info (only date and email ids)
            st.write("### Program Information")
            st.write(f"**Program Created At:** {program_info['Program Created At']}")
            st.markdown(f"**Owner Mail ID:** [{program_info['Owner mail id:']}]({program_info['Owner mail id:']})")
            st.markdown(f"**SPOC Mail ID:** [{program_info['Spoc mail id']}]({program_info['Spoc mail id']})")
            st.write(f"**Total Learners:** {program_info['Tota Learners']}")
        except ValueError as e:
            st.warning(str(e))  # Show error if no data found for program

    # Step 4: Query input
    query = st.text_area("Enter your query")

    if st.button("Submit Query"):
        if query.strip():
            st.write("### Submitted Details:")
            st.write(f"**Client:** {st.session_state.client_name}")
            st.write(f"**Program Code:** {program_code}")
            st.write(f"**Query:** {query}")
            
            # Step 5: Get the answer from the agent
            try:
                prompt = f"""
                Client: {st.session_state.client_name}
                Program: {program_code}
                Query: {query}
                """
                # Call the agent function with the query
                response = agent(prompt)
                
                # Display the agent's response
                st.write("### Agent's Response:")
                st.write(response)
                
            except Exception as e:
                st.warning(f"Error: {str(e)}")  # Show error if the agent fails

        else:
            st.warning("Please enter a query.")
