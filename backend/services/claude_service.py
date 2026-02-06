import anthropic
import json
import time
from config import Config


class ClaudeService:
    """Service for interacting with Claude API"""

    def __init__(self):
        """Initialize Claude client"""
        if not Config.CLAUDE_API_KEY:
            raise ValueError("CLAUDE_API_KEY not configured")

        self.client = anthropic.Anthropic(api_key=Config.CLAUDE_API_KEY)
        self.model = "claude-sonnet-4-5-20250929"  # Latest Sonnet 4.5
        self.max_retries = 3
        self.retry_delay = 2  # seconds

    def send_prompt(self, prompt, system_message="", max_tokens=4096, temperature=0.7):
        """
        Send a prompt to Claude and get response

        Args:
            prompt (str): The user prompt
            system_message (str): Optional system message
            max_tokens (int): Maximum tokens in response
            temperature (float): Temperature for response generation

        Returns:
            str: Claude's response text

        Raises:
            Exception: If API call fails after retries
        """
        for attempt in range(self.max_retries):
            try:
                messages = [{"role": "user", "content": prompt}]

                kwargs = {
                    "model": self.model,
                    "max_tokens": max_tokens,
                    "messages": messages,
                    "temperature": temperature
                }

                if system_message:
                    kwargs["system"] = system_message

                response = self.client.messages.create(**kwargs)

                # Extract text from response
                return response.content[0].text

            except anthropic.RateLimitError as e:
                if attempt < self.max_retries - 1:
                    wait_time = self.retry_delay * (2 ** attempt)  # Exponential backoff
                    print(f"Rate limit hit, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise Exception(f"Rate limit exceeded: {str(e)}")

            except anthropic.APIError as e:
                if attempt < self.max_retries - 1:
                    wait_time = self.retry_delay * (2 ** attempt)
                    print(f"API error, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise Exception(f"Claude API error: {str(e)}")

            except Exception as e:
                raise Exception(f"Unexpected error calling Claude: {str(e)}")

    def send_prompt_with_json(self, prompt, system_message=""):
        """
        Send prompt and expect JSON response

        Args:
            prompt (str): The user prompt
            system_message (str): Optional system message

        Returns:
            dict: Parsed JSON response

        Raises:
            Exception: If response is not valid JSON
        """
        response_text = self.send_prompt(prompt, system_message, temperature=0.3)

        try:
            # Try to extract JSON from response (handle markdown code blocks)
            json_text = response_text.strip()

            # Remove markdown code blocks if present
            if json_text.startswith('```'):
                lines = json_text.split('\n')
                # Remove first and last lines (``` markers)
                json_text = '\n'.join(lines[1:-1])
                # Remove language identifier if present
                if json_text.startswith('json'):
                    json_text = '\n'.join(json_text.split('\n')[1:])

            # Parse JSON
            return json.loads(json_text)

        except json.JSONDecodeError as e:
            # If JSON parsing fails, try to find JSON object in response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except:
                    pass

            raise Exception(f"Failed to parse JSON from Claude response: {str(e)}\nResponse: {response_text}")

    def test_connection(self):
        """
        Test connection to Claude API

        Returns:
            bool: True if connection successful
        """
        try:
            response = self.send_prompt("Hello, respond with just 'OK'", max_tokens=10)
            return True
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False
