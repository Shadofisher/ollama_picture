import subprocess
import argparse
import json

def run_command(command_file):
    # Read the command from the command file
    with open(command_file, 'r') as file:
        command = file.read().strip()
    
    # Execute the command and capture the output
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e.stderr}")
        return None

def parse_response(response):
    try:
        # Try to parse the response as JSON
        json_data = json.loads(response)
        
        # Extract the "content" section
        if 'message' in json_data:
            print("Content:", json_data["message"])
        else:
            print("No 'content' field found in the response.")
    except json.JSONDecodeError:
        print("Failed to decode JSON from the response.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a command from a file and parse the response.")
    parser.add_argument('command_file', type=str, help='Path to the command file containing the command to run.')

    args = parser.parse_args()
    
    # Run the command and get the response
    response = run_command(args.command_file)
    
    if response:
        parse_response(response)
