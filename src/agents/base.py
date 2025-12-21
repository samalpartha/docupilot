
"""Base Agent definition using ERNIE"""

import os
from loguru import logger
import erniebot

# Initialize ERNIE - expecting credentials in env
erniebot.api_type = 'aistudio'
erniebot.access_token = os.getenv('ERNIE_ACCESS_TOKEN', '')

class BaseAgent:
    def __init__(self, name, role, model='ernie-3.5'):
        self.name = name
        self.role = role
        self.model = os.getenv('ERNIE_MODEL', 'ernie-3.5')
        self.system_prompt = f"You are {name}, a {role}."
        
    def set_system_prompt(self, prompt):
        self.system_prompt = prompt
        
    def run(self, message):
        """Send a message to the agent and get a response."""
        logger.info(f"🤖 {self.name} processing task...")
        
        try:
            # Construct messages with system prompt
            messages = [
                {'role': 'user', 'content': f"System Instruction: {self.system_prompt}\n\nTask: {message}"}
            ]
            
            # Use erniebot ChatCompletion
            response = erniebot.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.3
            )
            
            result = response.get_result()
            logger.debug(f"{self.name} output: {result[:100]}...")
            return result
            
        except Exception as e:
            logger.error(f"Error in agent {self.name}: {e}")
            return f"Error executing task: {e}"
