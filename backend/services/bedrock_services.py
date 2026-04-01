import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NVIDIA_API_KEY")

def generate_response(prompt: str):
    try:
        url = "https://integrate.api.nvidia.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistralai/mistral-small-4-119b-2603",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 200,
            "temperature": 0.5
        }

        # Make the request
        res = requests.post(url, headers=headers, json=payload)
        
        # Print full response for debugging
        print("FULL RESPONSE:", res.text)  # Use .text instead of .json() first
        print("STATUS CODE:", res.status_code)
        
        # Check if request was successful
        if res.status_code != 200:
            print(f"API Error: {res.status_code}")
            return f"API Error: {res.status_code} - {res.text}"
        
        # Parse JSON
        data = res.json()
        
        # Check for error response format #1: "response" field with error
        if "response" in data and isinstance(data["response"], str) and "Error" in data["response"]:
            print(f"API Error Response: {data['response']}")
            return f"Error: {data['response']}"
        
        # Check for error response format #2: "error" field
        if "error" in data:
            print(f"API Error Response: {data['error']}")
            return f"Error: {data['error']}"
        
        # Validate response structure for success case
        if "choices" not in data:
            print(f"Unexpected response structure: {data.keys()}")
            return f"Error: Unexpected response structure. Keys: {list(data.keys())}"
        
        if len(data["choices"]) == 0:
            return "Error: No choices in response"
        
        if "message" not in data["choices"][0]:
            print(f"Choice structure: {data['choices'][0].keys()}")
            return f"Error: 'message' not found in choice. Available keys: {list(data['choices'][0].keys())}"
        
        if "content" not in data["choices"][0]["message"]:
            print(f"Message structure: {data['choices'][0]['message'].keys()}")
            return f"Error: 'content' not found in message. Available keys: {list(data['choices'][0]['message'].keys())}"
        
        # Extract the actual response
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return f"Request Error: {e}"
    except ValueError as e:
        print(f"JSON Parse Error: {e}")
        return f"JSON Parse Error: {e}"
    except KeyError as e:
        print(f"Key Error - Response structure issue: {e}")
        return f"Key Error: {e}"
    except Exception as e:
        print(f"Unexpected Error: {type(e).__name__} - {e}")
        return f"Error: {e}"


# Test the function
if __name__ == "__main__":
    test_prompt = "What is data block?"
    response = generate_response(test_prompt)
    print("\nFinal Response:")
    print(response)