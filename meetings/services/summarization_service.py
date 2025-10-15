"""
Summarization Service for Meeting Summarizer application.

This module provides AI-powered meeting summarization using OpenAI's GPT-4.
It analyzes transcripts and extracts executive summaries, key decisions,
action items, and discussion topics.

Created on: October 13, 2025
"""

from openai import OpenAI
from django.conf import settings
import json
import logging
from typing import Dict, List, Optional, Any

# Set up logging
logger = logging.getLogger(__name__)

# Comprehensive prompt template for meeting analysis
SUMMARY_PROMPT = """You are an AI assistant specialized in analyzing meeting transcripts.

Analyze the following meeting transcript and extract:

1. **Executive Summary**: A concise 3-4 sentence overview of the entire meeting
2. **Key Decisions**: Important decisions made during the meeting (as array of strings)
3. **Action Items**: Specific tasks identified with details (as array of objects with: task, assignee, priority, deadline)
4. **Discussion Topics**: Main themes and topics discussed (as array of strings)
5. **Participants**: List of people who participated in the meeting (extract names mentioned in the transcript)
6. **Insights**: Key insights, learnings, or observations from the meeting (as array of strings)

Return your analysis in this exact JSON format:
{{
  "executive_summary": "...",
  "key_decisions": ["decision 1", "decision 2"],
  "action_items": [
    {{"task": "...", "assignee": "...", "priority": "high/medium/low", "deadline": "YYYY-MM-DD or null"}}
  ],
  "discussion_topics": ["topic 1", "topic 2"],
  "participants": ["person 1", "person 2"],
  "insights": ["insight 1", "insight 2"]
}}

Transcript:
{transcript}

Return ONLY the JSON, no additional text."""


class SummarizationService:
    """
    Service class for generating AI-powered meeting summaries using GPT-4.
    
    This service provides methods for:
    - Generating comprehensive meeting summaries
    - Extracting action items
    - Validating summary structure
    
    Attributes:
        api_key (str): OpenAI API key
        client (OpenAI): OpenAI client instance
        model (str): GPT model name
    
    Example:
        >>> service = SummarizationService()
        >>> summary = service.generate_summary(transcript_text)
        >>> print(summary['executive_summary'])
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI client with API key.
        
        Args:
            api_key (str, optional): OpenAI API key. If not provided,
                                    uses settings.OPENAI_API_KEY
        
        Raises:
            ValueError: If API key is not provided and not found in settings
        """
        self.api_key = api_key or getattr(settings, 'OPENAI_API_KEY', None)
        
        if not self.api_key:
            logger.error("OpenAI API key not found in settings or parameters")
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY in settings "
                "or pass api_key parameter."
            )
        
        # Get base URL for OpenAI-compatible APIs (like Llama Maverick)
        base_url = getattr(settings, 'OPENAI_BASE_URL', None)
        
        # Initialize client with or without custom base URL
        if base_url:
            self.client = OpenAI(api_key=self.api_key, base_url=base_url)
            logger.info(f"SummarizationService initialized with custom base_url: {base_url}")
        else:
            self.client = OpenAI(api_key=self.api_key)
            logger.info("SummarizationService initialized with default OpenAI endpoint")
        
        # Use Llama model or GPT model from settings
        self.model = getattr(settings, 'OPENAI_GPT_MODEL', 'meta-llama/llama-3.1-8b-instruct')
        
        logger.info(f"SummarizationService initialized with model: {self.model}")
    
    def generate_summary(self, transcript_text: str) -> Dict[str, Any]:
        """
        Generate AI-powered summary from meeting transcript.
        
        This method uses GPT-4 to analyze the transcript and extract:
        - Executive summary
        - Key decisions
        - Action items with assignees and deadlines
        - Discussion topics
        
        Args:
            transcript_text (str): The meeting transcript text to analyze
        
        Returns:
            dict: Structured summary data with keys:
                - executive_summary (str): Brief overview
                - key_decisions (list): List of decisions made
                - action_items (list): List of tasks with details
                - discussion_topics (list): Main topics discussed
        
        Raises:
            ValueError: If transcript is empty or invalid
            Exception: If API call fails or JSON parsing fails
        
        Example:
            >>> service = SummarizationService()
            >>> summary = service.generate_summary(transcript)
            >>> print(f"Summary: {summary['executive_summary']}")
            >>> for decision in summary['key_decisions']:
            ...     print(f"- {decision}")
        """
        logger.info("Starting summary generation")
        
        # Validate input
        if not transcript_text or not transcript_text.strip():
            error_msg = "Transcript text cannot be empty"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        max_retries = 3
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Create prompt using template
                prompt = SUMMARY_PROMPT.format(transcript=transcript_text)
                
                logger.info(f"Sending request to {self.model} for summary generation (attempt {attempt + 1}/{max_retries})")
                logger.debug(f"Transcript length: {len(transcript_text)} characters")
                
                # Call OpenAI API
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a meeting analysis expert specializing in extracting insights from meeting transcripts."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,  # Low temperature for consistency
                    max_tokens=2000,
                    response_format={"type": "json_object"}  # Ensure JSON response
                )
                
                # Extract response content
                response_content = response.choices[0].message.content
                
                # Check if response is empty
                if not response_content or not response_content.strip():
                    error_msg = "Received empty response from API"
                    logger.error(error_msg)
                    logger.debug(f"Full response object: {response}")
                    raise Exception(error_msg)
                
                logger.debug(f"Received response: {response_content[:200]}...")
                
                # Parse JSON response with fallback extraction
                try:
                    summary_dict = json.loads(response_content)
                except json.JSONDecodeError as json_err:
                    # Try to extract JSON from response if wrapped in text
                    logger.warning(f"Initial JSON parse failed: {str(json_err)}")
                    logger.debug(f"Attempting to extract JSON from response...")
                    
                    import re
                    # Try to find JSON object in the response
                    json_match = re.search(r'\{[\s\S]*\}', response_content)
                    if json_match:
                        try:
                            summary_dict = json.loads(json_match.group(0))
                            logger.info("Successfully extracted JSON from response")
                        except json.JSONDecodeError as json_err2:
                            error_msg = f"Failed to parse extracted JSON: {str(json_err2)}"
                            logger.error(error_msg)
                            logger.debug(f"Invalid JSON content: '{response_content[:500]}'")
                            raise Exception(error_msg) from json_err2
                    else:
                        error_msg = f"Failed to parse JSON response: {str(json_err)}"
                        logger.error(error_msg)
                        logger.debug(f"Invalid JSON content: '{response_content[:500]}'")
                        raise Exception(error_msg) from json_err
                
                # Validate summary structure
                if not self.validate_summary_structure(summary_dict):
                    error_msg = "Summary structure validation failed - missing required keys"
                    logger.error(error_msg)
                    logger.debug(f"Invalid structure: {summary_dict}")
                    raise Exception(error_msg)
                
                # Log success
                logger.info(
                    f"Summary generation completed successfully. "
                    f"Decisions: {len(summary_dict.get('key_decisions', []))}, "
                    f"Action items: {len(summary_dict.get('action_items', []))}, "
                    f"Topics: {len(summary_dict.get('discussion_topics', []))}"
                )
                
                return summary_dict
            
            except Exception as e:
                last_error = e
                logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in 2 seconds...")
                    import time
                    time.sleep(2)
                continue
        
        # All retries failed - return a basic summary instead of crashing
        logger.error(f"Summary generation failed after {max_retries} attempts: {str(last_error)}")
        logger.warning("Returning fallback summary due to repeated failures")
        
        # Return a minimal valid summary structure
        fallback_summary = {
            "executive_summary": "Summary generation encountered errors. The meeting transcript was processed but detailed analysis could not be completed. Please review the transcript directly.",
            "key_decisions": [],
            "action_items": [],
            "discussion_topics": [],
            "participants": [],
            "insights": []
        }
        
        return fallback_summary
    
    def extract_action_items(self, summary_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract and format action items from summary dictionary.
        
        This method validates and formats action items from the AI-generated
        summary, ensuring each item has the required fields.
        
        Args:
            summary_dict (dict): The summary dictionary containing action_items
        
        Returns:
            list: List of formatted action items, each containing:
                - task (str): The action item description
                - assignee (str): Person assigned to the task
                - priority (str): Priority level (high/medium/low)
                - deadline (str or None): Due date in YYYY-MM-DD format
        
        Example:
            >>> service = SummarizationService()
            >>> summary = service.generate_summary(transcript)
            >>> action_items = service.extract_action_items(summary)
            >>> for item in action_items:
            ...     print(f"{item['task']} - {item['assignee']}")
        """
        logger.info("Extracting action items from summary")
        
        # Get action items from summary
        action_items = summary_dict.get('action_items', [])
        
        if not action_items:
            logger.warning("No action items found in summary")
            return []
        
        # Validate and format each action item
        formatted_items = []
        required_fields = ['task', 'assignee', 'priority']
        
        for idx, item in enumerate(action_items):
            # Check required fields
            missing_fields = [field for field in required_fields if field not in item]
            
            if missing_fields:
                logger.warning(
                    f"Action item {idx} missing fields: {missing_fields}. "
                    f"Item: {item}"
                )
                continue
            
            # Format the item
            formatted_item = {
                'task': item['task'],
                'assignee': item.get('assignee', 'Unassigned'),
                'priority': item.get('priority', 'medium').lower(),
                'deadline': item.get('deadline')  # Can be None
            }
            
            # Validate priority value
            if formatted_item['priority'] not in ['high', 'medium', 'low']:
                logger.warning(
                    f"Invalid priority '{formatted_item['priority']}' for action item. "
                    f"Setting to 'medium'"
                )
                formatted_item['priority'] = 'medium'
            
            formatted_items.append(formatted_item)
        
        logger.info(f"Extracted {len(formatted_items)} valid action items")
        return formatted_items
    
    def validate_summary_structure(self, summary_dict: Dict[str, Any]) -> bool:
        """
        Validate that summary dictionary has all required keys.
        
        Args:
            summary_dict (dict): The summary dictionary to validate
        
        Returns:
            bool: True if all required keys exist, False otherwise
        
        Example:
            >>> service = SummarizationService()
            >>> is_valid = service.validate_summary_structure(summary_data)
            >>> if not is_valid:
            ...     print("Invalid summary structure")
        """
        required_keys = [
            'executive_summary',
            'key_decisions',
            'action_items',
            'discussion_topics'
        ]
        
        # Check if all required keys exist
        missing_keys = [key for key in required_keys if key not in summary_dict]
        
        if missing_keys:
            logger.error(f"Summary validation failed. Missing keys: {missing_keys}")
            return False
        
        # Additional validation: check types
        if not isinstance(summary_dict['executive_summary'], str):
            logger.error("executive_summary must be a string")
            return False
        
        if not isinstance(summary_dict['key_decisions'], list):
            logger.error("key_decisions must be a list")
            return False
        
        if not isinstance(summary_dict['action_items'], list):
            logger.error("action_items must be a list")
            return False
        
        if not isinstance(summary_dict['discussion_topics'], list):
            logger.error("discussion_topics must be a list")
            return False
        
        logger.debug("Summary structure validation passed")
        return True
