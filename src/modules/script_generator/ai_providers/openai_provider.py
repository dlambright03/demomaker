"""
OpenAI Provider implementation for Script Generation.

This module provides an implementation of the AI provider interface using OpenAI APIs.
"""

import base64
import json
import logging
import os
from typing import Any, Dict, List, Optional

import requests

from src.modules.script_generator.ai_providers.base_provider import BaseAIProvider

# Configure logging
logger = logging.getLogger(__name__)


class OpenAIProvider(BaseAIProvider):
    """OpenAI implementation for AI provider."""

    # OpenAI API endpoints
    CHAT_COMPLETION_URL = "https://api.openai.com/v1/chat/completions"
    VISION_URL = "https://api.openai.com/v1/chat/completions"

    # Default models
    DEFAULT_CHAT_MODEL = "gpt-3.5-turbo"
    DEFAULT_VISION_MODEL = "gpt-4-vision-preview"

    # Timeout in seconds
    DEFAULT_TIMEOUT = 30

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the OpenAI provider.

        Args:
            config: Optional configuration dictionary
        """
        super().__init__("OpenAI", config)
        self._chat_model = config.get("chat_model", self.DEFAULT_CHAT_MODEL)
        self._vision_model = config.get("vision_model", self.DEFAULT_VISION_MODEL)
        self._timeout = config.get("timeout", self.DEFAULT_TIMEOUT)
        self._session = None

    def _validate_config(self) -> None:
        """Validate the configuration parameters."""
        if not self._api_key and not os.environ.get("OPENAI_API_KEY"):
            raise ValueError(
                "OpenAI API key not provided in config or environment variables"
            )

    def _initialize_client(self) -> None:
        """Initialize the requests session for OpenAI API calls."""
        self._session = requests.Session()
        api_key = self._api_key or os.environ.get("OPENAI_API_KEY")
        self._session.headers.update(
            {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        )

    def analyze_image_content(self, image_data: bytes) -> Dict[str, Any]:
        """
        Analyze image content using OpenAI's vision model.

        Args:
            image_data: Binary image data to analyze

        Returns:
            Dictionary containing analysis results (objects, text, etc.)
        """
        if not self.is_available():
            raise RuntimeError("OpenAI provider is not initialized")

        try:
            # Encode image data to base64
            base64_image = base64.b64encode(image_data).decode("utf-8")

            # Create the message payload
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an image analysis assistant. Analyze the provided image and extract the following information: "
                        "1. Objects: List all visible objects with their approximate positions and sizes. "
                        "2. Text: All readable text in the image. "
                        "3. Colors: Dominant colors in the image with approximate percentages. "
                        "4. Composition: Overall layout and visual structure of the image. "
                        "5. Quality: Assessment of image resolution and clarity. "
                        "Provide the response as a structured JSON object with these categories. "
                        "Be precise and comprehensive in your analysis."
                    ),
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this image and provide a detailed analysis as JSON.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            },
                        },
                    ],
                },
            ]

            # Make the API request
            payload = {
                "model": self._vision_model,
                "messages": messages,
                "max_tokens": 1000,
                "response_format": {"type": "json_object"},
            }

            response = self._session.post(
                self.VISION_URL, json=payload, timeout=self._timeout
            )
            response.raise_for_status()
            result = response.json()

            # Extract and parse the JSON response
            content = result["choices"][0]["message"]["content"]
            analysis = json.loads(content)

            # Convert to standard format
            return {
                "objects": analysis.get("objects", []),
                "text": analysis.get("text", ""),
                "colors": analysis.get("colors", {}),
                "composition": analysis.get("composition", ""),
                "quality": analysis.get("quality", ""),
                "raw_analysis": analysis,
            }

        except Exception as e:
            logger.error(f"Error analyzing image with OpenAI: {str(e)}")
            raise

    def generate_script_from_images(
        self, image_analyses: List[Dict[str, Any]], description: str
    ) -> Dict[str, Any]:
        """
        Generate a script from a set of analyzed images.

        Args:
            image_analyses: List of image analysis results
            description: Description of the content for script generation

        Returns:
            Dictionary containing the generated script
        """
        if not self.is_available():
            raise RuntimeError("OpenAI provider is not initialized")

        try:
            # Create a structured prompt from the image analyses
            image_descriptions = []
            for idx, analysis in enumerate(image_analyses):
                objects_str = ", ".join(
                    [obj.get("name", "unknown") for obj in analysis.get("objects", [])]
                )
                text_str = analysis.get("text", "")
                image_descriptions.append(
                    f"Image {idx+1}:\n"
                    f"- Objects: {objects_str}\n"
                    f"- Text: {text_str}\n"
                    f"- Composition: {analysis.get('composition', '')}"
                )

            images_content = "\n\n".join(image_descriptions)

            # Create the message payload for script generation
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a professional script writer for creating engaging demo videos. "
                        "Your task is to create a script for a video based on a set of images and a description. "
                        "The script should be engaging, coherent, and suitable for a professional narration. "
                        "Each script segment should correspond to one image and include timing information. "
                        "Aim for 5-15 seconds per image, with enough detail to engage the viewer but not overwhelm them. "
                        "Your response should be a valid JSON object with the following structure:\n"
                        "{\n"
                        '  "title": "Title of the script",\n'
                        '  "total_duration": total_duration_in_seconds,\n'
                        '  "segments": [\n'
                        "    {\n"
                        '      "id": "segment-1",\n'
                        '      "image_index": 0,\n'
                        '      "duration": seconds_for_this_segment,\n'
                        '      "narration": "Text to be narrated for this segment"\n'
                        "    },\n"
                        "    ...\n"
                        "  ]\n"
                        "}"
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Create a demo script for the following images with this description: {description}\n\n"
                        f"Here are the image analyses:\n\n{images_content}"
                    ),
                },
            ]

            # Make the API request
            payload = {
                "model": self._chat_model,
                "messages": messages,
                "max_tokens": 2000,
                "temperature": 0.7,
                "response_format": {"type": "json_object"},
            }

            response = self._session.post(
                self.CHAT_COMPLETION_URL, json=payload, timeout=self._timeout
            )
            response.raise_for_status()
            result = response.json()

            # Extract and parse the JSON response
            content = result["choices"][0]["message"]["content"]
            script = json.loads(content)

            # Validate the script structure
            if "segments" not in script or not isinstance(script["segments"], list):
                raise ValueError("Invalid script format: missing or invalid segments")

            if "total_duration" not in script:
                # Calculate total duration if not provided
                script["total_duration"] = sum(
                    segment.get("duration", 0) for segment in script["segments"]
                )

            return script

        except Exception as e:
            logger.error(f"Error generating script with OpenAI: {str(e)}")
            raise

    def is_available(self) -> bool:
        """Check if the OpenAI provider is available."""
        try:
            # Check if API key is available
            api_key = self._api_key or os.environ.get("OPENAI_API_KEY")
            if not api_key:
                return False

            # Initialize session if not already done
            if self._session is None:
                self._initialize_client()

            return True
        except Exception as e:
            logger.error(f"Error checking OpenAI availability: {str(e)}")
            return False

    def initialize(self, api_key: Optional[str] = None, **kwargs) -> bool:
        """
        Initialize the OpenAI provider.

        Args:
            api_key: Optional API key for OpenAI
            kwargs: Additional configuration options

        Returns:
            True if initialization succeeded, False otherwise
        """
        try:
            # Set API key if provided
            if api_key:
                self._api_key = api_key

            # Update configuration if provided
            if "chat_model" in kwargs:
                self._chat_model = kwargs["chat_model"]
            if "vision_model" in kwargs:
                self._vision_model = kwargs["vision_model"]
            if "timeout" in kwargs:
                self._timeout = kwargs["timeout"]

            # Validate configuration
            self._validate_config()

            # Initialize client
            self._initialize_client()

            logger.info(f"OpenAI provider initialized with models: {self._chat_model}, {self._vision_model}")
            return True
        except Exception as e:
            logger.error(f"Error initializing OpenAI provider: {str(e)}")
            return False
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                },
            ]

            # Make the API request
            payload = {
                "model": self._vision_model,
                "messages": messages,
                "max_tokens": 1000,
                "response_format": {"type": "json_object"},
            }

            response = self._session.post(
                self.VISION_URL, json=payload, timeout=self._timeout
            )
            response.raise_for_status()

            # Extract and parse the response
            result = response.json()
            content = (
                result.get("choices", [{}])[0].get("message", {}).get("content", "{}")
            )

            # Parse the JSON string from content
            analysis = json.loads(content)

            # Format the result to match our expected structure
            return {
                "content": {
                    "objects": analysis.get("objects", []),
                    "text": analysis.get("text", ""),
                    "colors": analysis.get("colors", []),
                    "composition": analysis.get("composition", {}),
                },
                "quality": analysis.get("quality", {}),
            }

        except requests.RequestException as e:
            logger.error(f"Error making OpenAI Vision API request: {str(e)}")
            raise RuntimeError(f"Failed to analyze image with OpenAI: {str(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing OpenAI Vision API response: {str(e)}")
            raise RuntimeError(f"Failed to parse OpenAI response: {str(e)}")

    def generate_narrative(
        self,
        image_analyses: List[Dict[str, Any]],
        description: str,
        segment_index: int,
        is_first: bool = False,
        is_last: bool = False,
    ) -> str:
        """
        Generate narrative text for a script segment based on image analysis.

        Args:
            image_analyses: List of image analysis results
            description: Overall description of the demo
            segment_index: Index of the current segment
            is_first: Whether this is the first segment
            is_last: Whether this is the last segment

        Returns:
            Generated narrative text for the segment
        """
        if not self.is_available():
            raise RuntimeError("OpenAI provider is not initialized")

        try:
            # Get the current image analysis
            current_analysis = image_analyses[segment_index]

            # Create a prompt based on the segment position and content
            segment_type = (
                "introduction" if is_first else "conclusion" if is_last else "middle"
            )

            system_prompt = (
                "You are a professional demo video script writer. "
                "Your task is to create a narrative for a segment of a demo video based on the image content analysis provided. "
                f"This is a {segment_type} segment. "
                "Write a clear, engaging, and professional script segment that describes what's in the image. "
                "Use a friendly, conversational tone. If there are technical elements, explain them simply. "
                "Include smooth transitions to the next segment if this isn't the conclusion. "
                "Keep the narrative concise but informative."
            )

            # Format the objects for better context
            objects_str = ", ".join(
                [
                    obj.get("name", "")
                    for obj in current_analysis.get("content", {}).get("objects", [])
                ]
            )
            text_content = current_analysis.get("content", {}).get("text", "")

            user_prompt = (
                f"Generate a script segment for a demo video with the following description: '{description}'. "
                f"The image contains the following elements: {objects_str}. "
                f"Text visible in the image: '{text_content}'. "
                f"This is segment {segment_index + 1} of {len(image_analyses)}. "
            )

            if is_first:
                user_prompt += "This is the introduction segment. Start with a welcoming tone and introduce the topic."
            elif is_last:
                user_prompt += "This is the conclusion segment. Summarize key points and end with a call to action or closing thought."
            else:
                user_prompt += "This is a middle segment. Ensure smooth transition from the previous segment and to the next one."

            # Create the message payload
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            # Make the API request
            payload = {
                "model": self._chat_model,
                "messages": messages,
                "max_tokens": 500,
                "temperature": 0.7,
            }

            response = self._session.post(
                self.CHAT_COMPLETION_URL, json=payload, timeout=self._timeout
            )
            response.raise_for_status()

            # Extract the generated text
            result = response.json()
            narrative = (
                result.get("choices", [{}])[0].get("message", {}).get("content", "")
            )
            return narrative.strip()

        except requests.RequestException as e:
            logger.error(f"Error making OpenAI Chat API request: {str(e)}")
            raise RuntimeError(f"Failed to generate narrative with OpenAI: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating narrative with OpenAI: {str(e)}")
            raise RuntimeError(f"Failed to generate narrative: {str(e)}")

    @property
    def supports_image_analysis(self) -> bool:
        """
        Check if this provider supports direct image analysis.

        Returns:
            True as OpenAI supports image analysis via GPT-4 Vision
        """
        return True
