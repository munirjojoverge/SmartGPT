# ********************************************************
#                      Munir Jojo-Verge (c)
#                         May 10th 2023
# ********************************************************

import openai
from omegaconf import DictConfig
import tiktoken
import logging

# Configure logging
log = logging.getLogger(__name__)


class OpenAIChatCompletion:
    """
    A class for handling conversations with OpenAI's GPT-3.5-turbo model.
    """

    def __init__(self, cfg: DictConfig):
        """
        Initialize the OpenAIChatCompletion class with given configuration.

        Args:
            cfg (DictConfig): Configuration object containing necessary parameters.
        """
        self.model = cfg.model
        self.max_tokens = cfg.max_tokens
        self.temperature = cfg.temperature
        self.top_p = cfg.top_p
        self.frequency_penalty = cfg.frequency_penalty
        self.presence_penalty = cfg.presence_penalty
        self.stop = cfg.stop        
        self.token_limit = cfg.token_limit
        self.buffer_tokens = cfg.buffer_tokens
        self.conversation = [{"role": "system", "content": "You are a helpful assistant."}]        
        openai.api_key = cfg.openai_key

    def update_conversation(self, message: dict):
        """
        Update the conversation with a new message.

        Args:
            message (dict): Dictionary containing the role and content of the message.
                            Expected format: 
                            {"role": "<role>", "content": "<content>"}
                            where "<role>" is either "system", "user", or "assistant"
                            and "<content>" is the corresponding message content.

        Raises:
            TypeError: If the provided message is not a dictionary or if the dictionary 
                    does not contain the keys "role" and "content".
        """
        # Ensure that the message is a dictionary with the keys "role" and "content"
        if not isinstance(message, dict) or not {'role', 'content'}.issubset(message.keys()):
            raise TypeError('Message must be a dictionary with the keys "role" and "content".')
        
        log.info(message)
        
        # Append the new message to the conversation
        self.conversation.append(message)


    def count_tokens(self, text):
        """
        Count the number of tokens in the given text.

        Args:
            text (str): Text to count tokens in.

        Returns:
            int: Number of tokens in the text.
        """
        enc = tiktoken.encoding_for_model(self.model)
        tokens = enc.encode_ordinary(text)
        return len(tokens)

    def summarize_conversation(self):
        """
        Summarize the conversation using ChatGPT itself.
        """
        summary_prompt = "Summarize the following conversation: "
        conversation_text = " ".join(
            [
                f"{msg['role']}: {msg['content']}"
                for msg in self.conversation
                if "content" in msg
            ]
        )

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{summary_prompt}{conversation_text}"},
            ],
        )

        summarized_text = response.choices[0].message.content
        self.conversation = [{"role": "system", "content": summarized_text}]

    def truncate_and_summarize_conversation(self):
        """
        Truncate and summarize the conversation to fit within the token limit.
        """
        conversation_text = "".join(
            [msg["content"] for msg in self.conversation if "content" in msg]
        )
        conversation_tokens = self.count_tokens(conversation_text)
        log.info(f"Conversation tokens: {conversation_tokens}")

        while conversation_tokens > (
            self.token_limit - self.buffer_tokens - self.max_tokens
        ):
            # Remove the oldest user message
            user_message_indices = [
                i for i, msg in enumerate(self.conversation) if msg["role"] == "user"
            ]
            if user_message_indices:
                self.conversation.pop(user_message_indices[0])
            else:
                break  # If no user messages are left, exit the loop

            # Summarize the remaining conversation
            self.summarize_conversation()

            # Recalculate the conversation tokens
            conversation_text = "".join(
                [msg["content"] for msg in self.conversation if "content" in msg]
            )
            conversation_tokens = self.count_tokens(conversation_text)

    def truncate_conversation(self):
        """
        Truncate the conversation to fit within the token limit and create a new conversation
        with the task prompt and the last 3 sets of messages.
        """
        conversation_text = "".join(
            [msg["content"] for msg in self.conversation if "content" in msg]
        )
        conversation_tokens = self.count_tokens(conversation_text)
        log.info(f"Conversation tokens: {conversation_tokens}")

        if conversation_tokens > (
            self.token_limit - self.buffer_tokens - self.max_tokens
        ):
            # Get the first 2 messages with the system role and the question prompt and the last xx messages
            first_messages = self.conversation[:2]
            last_messages = self.conversation[-5:]

            # Create a new conversation with the task prompt and the last 3 sets of messages
            self.conversation = first_messages + last_messages

            # Recalculate the conversation tokens
            conversation_text = "".join(
                [msg["content"] for msg in self.conversation if "content" in msg]
            )
            conversation_tokens = self.count_tokens(conversation_text)
            log.info(f"New conversation tokens: {conversation_tokens}")    

    def get_chatgpt_response(self, message, ):
        """
        Get ChatGPT model response by processing the conversation.

        Returns:
            str: response returned by the ChatGPT model.
        """
        try:
            self.update_conversation(message)
            # self.truncate_and_summarize_conversation()
            self.truncate_conversation()

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.conversation,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                n=1,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
                stop=self.stop,
            )

            # Extract and return the response text
            response = " ".join([choice.message['content'].strip() for choice in response.choices])
            message = {"role": "assistant", "content": response}
            self.update_conversation(message)
            log.info(f"ChatGPT response: {response}")
            return response
        
        except openai.OpenAIError as e:
            # Log and handle API exceptions
            log.error(f"OpenAI API error: {e}")
            return "Error: Unable to get response from ChatGPT. Please check the logs for more details."
