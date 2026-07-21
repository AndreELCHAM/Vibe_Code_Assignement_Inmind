import openai
from datetime import datetime
conversation = []# model had this inside the chat with bot function which would wipe memory
# Configuration
'''this is deprecated syntax that gave me an error saying so (original model output)
openai.api_base = 'http://localhost:11434/v1'  # Change this to point to your Qwen2.5-coder:7b model API
openai.api_key = 'ollama'  # Set your OpenAI API key here if required
'''
#this is the new syntax

client = openai.OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
model_name = 'qwen2.5-coder:7b'  #orignial output also had the name wrong here

# Conversation history
def save_history(conversation):
    with open('C:/Users/elcha/Documents/GitHub/Vibe_Code_Assignement_Inmind/chatbot_history.txt', 'a') as file:
       for turn in conversation:
        file.write(str(turn) + '\n')
# Chatbot function
def chat_with_bot(query):
    conversation.append({'role': 'user', 'content': query})  # Log the user interaction

    try:#was originally openai.Completion.create and engine= which is also deprecated
        response = client.chat.completions.create(
            model=model_name,
            messages=conversation,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,).choices[0].message.content.strip()
        conversation.append({'role': 'assistant', 'content': response})  # Log the bot response
        print(response)
    except Exception as e:
        conversation.append({'role': 'assistant', 'content': f'Error: {str(e)}'})
        print(f'An error occurred: {e}')
        save_history(conversation)
        
if __name__ == '__main__':
    while True:
        query = input('> ')  # Get user input
        if query.lower() in ('exit', 'quit', 'q'):  # Exit the loop to end the conversation
            break
        chat_with_bot(query)