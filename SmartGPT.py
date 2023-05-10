import tkinter as tk
from tkinter import font
from openai_api_chat_completion import OpenAIChatCompletion
import hydra
from omegaconf import DictConfig, OmegaConf
import datetime
import os
from io import StringIO
import logging
from hydra.utils import get_original_cwd, to_absolute_path

# Initialize StringIO object
log_capture_string = StringIO()

# Configure logging
log = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", stream=log_capture_string)
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

@hydra.main(config_path="config", config_name="config")
class SmartGPT:
    """
    A class for handling the GUI of the chat interface.
    """
    def __init__(self, cfg: DictConfig):
        """
        Initialize the SmartGPT class with the OpenAI API key and the configuration.

        Args:
            cfg (DictConfig): Configuration for the OpenAIChatCompletion class.
        """
        self.cfg = cfg
        self.openai_api_key = cfg.LLM
        self.chat_api = OpenAIChatCompletion(self.cfg.LLM)

    def create_gui(self):
        """
        Create the GUI for the chat interface.
        """

        def on_submit():
            query = query_widget.get()
            hint = hint_widget.get()
            if query:
                output_text_widget.config(state=tk.NORMAL)
                output_text_widget.insert(tk.END, "You: " + query + "\n")
                output_text_widget.config(state=tk.DISABLED)
                query_widget.delete(0, tk.END)

                # Process the query using the EfficientGPT class and display the responses at each step
                for response in self.process_user_input(query, hint):
                    output_text_widget.config(state=tk.NORMAL)
                    output_text_widget.insert(tk.END, response + "\n")
                    output_text_widget.config(state=tk.DISABLED)
                    output_text_widget.see(tk.END)

        def on_clear():
            query_widget.delete(0, tk.END)
            hint_widget.delete(0, tk.END)
            output_text_widget.config(state=tk.NORMAL)
            output_text_widget.delete("1.0", tk.END)
            output_text_widget.config(state=tk.DISABLED)
            self.chat_api.conversation = [{"role": "system", "content": "You are a helpful assistant with high expertise in all matters."}]

        root = tk.Tk()
        root.title("SmartGPT GUI")

        text_font = font.Font(size=18)

        query_label = tk.Label(root, text="Enter your question, query or task:")
        query_label.pack()

        query_widget = tk.Entry(root, width=250)
        query_widget.pack()
        query_widget.insert(0, "I have a 20 liter jug and a 5 liter jug. I want to measure 5 liters. How can i do it?")

        hint_label = tk.Label(root, text="Enter your hint:")
        hint_label.pack()
        hint_widget = tk.Entry(root, width=250)
        hint_widget.pack()
        hint_widget.insert(0,"Who said you must use both jugs? What if you just fill in the 5-liter jug and you are done!")

        submit_button = tk.Button(root, text="Submit", command=on_submit)
        submit_button.pack()

        clear_button = tk.Button(root, text="Clear", command=on_clear)
        clear_button.pack()

        output_text_widget = tk.Text(root, wrap=tk.WORD, font=text_font, state=tk.DISABLED)
        output_text_widget.pack(expand=True, fill=tk.BOTH)

        root.mainloop()

    def generate_chain_of_thought_prompt(self, user_input):
        """
        This function generates the chain of thought prompt for the assistant's response.
        
        Args:
            user_input (str): The user's input message.

        Returns:
            str: The chain of thought prompt.
        """
        # The prompt is a formatted string that includes the user's input
        # and an initial response from the assistant.
        chain_of_thought_prompt = f"Question: {user_input}. Let's work this out in a step by step way to be sure we have the right answer. Answer "
        
        # Log the generated prompt for debugging purposes
        log.info(f"chain_of_thought_prompt: {chain_of_thought_prompt}")
        
        return chain_of_thought_prompt

    def generate_self_reflection_prompt(self):
        """
        This function generates a self-reflection prompt for the assistant to analyze and criticize the responses.
        
        Args:
            user_message (str): The user's input message.
            responses (list): A list of assistant's responses to the user's message.

        Returns:
            str: The self-reflection prompt.
        """
        # The prompt is created by concatenating the user's message and the assistant's responses
        # self_reflection_prompt = f'"Question:{user_message}"\n\n' + "\nAnswer options:".join(responses)
        
        # An additional instruction is added for the assistant to analyze and criticize the responses
        self_reflection_prompt = "You are an expert researcher tasked with investigating the three answer options above. List all the flaws and faulty logic of each answer option. Be detailed, thorough and very analytical. Let's think step by step. Answer:"
        
        # Log the generated prompt for debugging purposes
        log.info(f"self_reflection_prompt: {self_reflection_prompt}")
        
        return self_reflection_prompt

    def generate_final_selection_prompt(self):
        """
        This function generates a final selection prompt for the assistant to choose the best response,
        improve it, and provide the improved answer.

        Args:
            user_message (str): The user's input message.
            responses (list): A list of assistant's responses to the user's message.
            reflection_responses (list): A list of the assistant's self-reflection responses.

        Returns:
            str: The final selection prompt.
        """
        # The prompt is created by concatenating the user's message, the assistant's responses, and the reflection responses
        #final_selection_prompt = f'Question:{user_message}\n\nAnswer options:' + "\n".join(responses) + "\nResearcher analysis:" + reflection_response
        
        # An additional instruction is added for the assistant to choose and improve the best response
        final_selection_prompt = "You are noe an expert resolver tasked with 1) Based on the analysis above, resolve which of the answer options is the best, 2) Improve that answer, and 3) You must respond with the improved answer in full. Let's work this out in a step by step way to be sure we have the right answer. Your improved answer is:"
        
        # Log the generated prompt for debugging purposes
        log.info(f"final_selection_prompt: {final_selection_prompt}")
        
        return final_selection_prompt
    
    def save_results(self, user_input, final_output):
        """
        This function saves the user's input and the model's final output to a file.

        Args:
            user_input (str): The user's input.
            final_output (str): The model's final output.
        """
        # Specify the directory where results will be saved
        results_dir = os.path.join(get_original_cwd(), "results")

        # If the directory doesn't exist, create it
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Create a timestamp for the results file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # The filename for the results file includes the timestamp
        results_filename = f"result_{timestamp}.txt"

        # Write the user's input and the model's final output to the results file
        with open(os.path.join(results_dir, results_filename), "w") as results_file:
            results_file.write(f"User Input: {user_input}\n")
            results_file.write(f"Logs:\n{log_capture_string.getvalue()}\n")
            results_file.write(f"Final Output: {final_output}")

        # Log the name of the file where results were saved
        log.info(f"Results saved to file: {results_filename}")

    def display_results(self, user_input, final_output, output_text_widget):
        """
        This function displays the user's input, logs, and the model's final output in a GUI text widget.

        Args:
            user_input (str): The user's input.
            final_output (str): The model's final output.
            output_text_widget (tkinter.Text): The tkinter Text widget where results will be displayed.
        """
        # Enable the text widget to insert text
        output_text_widget.config(state=tk.NORMAL)

        # Insert the user's input, logs, and the model's final output
        output_text_widget.insert(tk.END, f"User Input: {user_input}\n")
        output_text_widget.insert(tk.END, f"Logs:\n{log_capture_string.getvalue()}\n")
        output_text_widget.insert(tk.END, f"Final Output: {final_output}\n")

        # Disable the text widget to prevent the user from modifying the displayed text
        output_text_widget.config(state=tk.DISABLED)

    def process_user_input(self, user_input, hint):
        """
        This function processes the user input and generates the assistant's response.
        
        Args:
            user_input (str): The user's input message.

        Yields:
            str: The assistant's responses at each step of the process.
        """
        chain_of_thought_prompt = self.generate_chain_of_thought_prompt(user_input)
        yield f"Chain_of_thought_prompt: {chain_of_thought_prompt}"
        
        chain_of_thought_responses = []
        for i in range(3):
            message = {"role": "user", "content": chain_of_thought_prompt + str(i + 1) + ":"}
            answer_option = self.chat_api.get_chatgpt_response(message=message)
            chain_of_thought_responses.append(f"Answer Option {i + 1}: {answer_option}")
            yield f"Option {i + 1}: {answer_option}"

        self_reflection_prompt = self.generate_self_reflection_prompt()        
        message = {"role": "user", "content": self_reflection_prompt}
        yield f"Self-reflection Prompt: {message}"
        reflection_outputs = self.chat_api.get_chatgpt_response(message=message)
        yield f"Self-reflection: {reflection_outputs}"

        final_selection_prompt = self.generate_final_selection_prompt()
        message = {"role": "user", "content": final_selection_prompt}
        final_output = self.chat_api.get_chatgpt_response(message=message)        
        yield f"Final Assistant: {final_output}"
        
        # It never really works so I just want to see what happens if I just give an hint 
        message = {"role": "user", "content": hint}
        resolution = self.chat_api.get_chatgpt_response(message=message)
        yield f"resolution: {resolution}"
        
        log.info(f"Full Conversation: {self.chat_api.conversation}")
    
    def run(self):
        self.create_gui()


@hydra.main(config_path="config", config_name="config")
def main(cfg: DictConfig):
    chatgpt_app = SmartGPT(cfg)
    chatgpt_app.run()

if __name__ == "__main__":
    main()
