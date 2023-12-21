import requests
import json

# Define the headers for the API request
headers = {
    "Content-Type": "application/json",
    "anthropic-version": "2023-06-01", 
}

host = 'http://localhost:3000'

def assistant_claude():
    # Define the API endpoint
    url = f"{host}/assistants"

    # Define the data for the API request
    data = {
        "instructions": "You are a personal math tutor. Write and run code to answer math questions.",
        "name": "Math Tutor",
        "tools": [{"type": "retrieval"}],
        "model": "claude-2.1"
    }

    # Make the API request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Print the response content
    print(response.content)

    # Then try to convert it to JSON
    try:
        print(response.json())
    except json.JSONDecodeError:
        print("The response is not a valid JSON string.")
    
    return response.json()

def assistant_mistral():
    # Define the API endpoint
    url = f"{host}/assistants"

    # Define the data for the API request
    data = {
        "instructions": "You are a personal math tutor. Write and run code to answer math questions.",
        "name": "Math Tutor",
        "tools": [{"type": "retrieval"}],
        "model": "open-orca/mistral-7b-openorca"
    }

    # Make the API request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Print the response content
    print(response.json())

    # Extract the assistant id from the response
    assistant_id = response.json()['id']
    print('Using assistant', assistant_id)
    
    return response.json()

def create_thread():
    url = f"{host}/threads"

    response = requests.post(url, headers=headers)

    print(response.json())
    thread_id = response.json()['id']
    print('Using thread', thread_id)
    
    return response.json()

def add_message_to_thread(thread_id):
    url = f"{host}/threads/{thread_id}/messages"

    data = {
        "role": "user",
        "content": "I need to solve the equation 3x + 11 = 14. Can you help me?"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    return response.json()

def run_assistant(thread_id, assistant_id):
    url = f"{host}/threads/{thread_id}/runs"

    data = {
        "assistant_id": assistant_id,
        "instructions": "Please solve the equation."
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.json())    
    return response.json()

def check_run_status(thread_id, run_response):
    url = f"{host}/threads/{thread_id}/runs/{run_response['id']}"

    response = requests.get(url, headers=headers)

    print(response.json())
    
    return response.json()

def display_response(thread_id):
    url = f"{host}/threads/{thread_id}/messages"

    response = requests.get(url, headers=headers)

    print(response.json())
    
    return response.json()

if __name__ == "__main__":
    assistant_response = assistant_mistral()
    print("Assistant interaction started.")
    thread_response = create_thread()
    thread_id = thread_response['id']
    print("Thread ID:", thread_id)

    message_response = add_message_to_thread(thread_id)
    print("Message added to thread.")
    run_response = run_assistant(thread_id, assistant_id=assistant_response['id'])
    print("Assistant ran.")
    status_response = check_run_status(thread_id, run_response)
    print("Run status checked.")
    display_response = display_response(thread_id)
    print(display_response)
    print("Assistant interaction completed.")

