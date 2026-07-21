Vibe_Code_Assignement_Inmind

Part 3:
Write a simple Python CLI chat bot, do NOT use any web frameworks it NEEDS to use the openai python lybrary and NEEDS to connect to my local Ollama server running on http://localhost:11434 with qwen2.5-coder:7b model. Store the conversation history in the correct format and save the files exactly to C:\Users\elcha\Documents\GitHub\Vibe_Code_Assignement_Inmind\chatbot.py
(that was the first prompt i wrote and it got me the closest result to what i wanted but used deprecated openai functions i had to fix myself)

Write a Simple Python CLI chat bot, do NOT use any web frameworks it NEEDS to use CURRENTLY SUPPORTED  openai python library YPU MUST USE response = client.chat.completions.create for the response format it also NEEDS TO connect to my local ollama server on http://localhost:11434 with qwen2.5-coder:7b model. it MUST STORE conversation history IN THE CORRECT FORMAT AND FEED IT BACK TO THE MODEL ON EACH QUERY and save the script you write EXACTLY TO C:\Users\elcha\Documents\GitHub\Vibe_Code_Assignement_Inmind\chatbot.py (you have permission to save to that file) (this was my attempt at forcing it to use supported syntax but it didnt work)


The agent saved me time by writing the correct code steps for the task i demanded and the correct code logic for saving history and making the bot work. However debugging the errors was very hard as it was almost instantly dropping context and hallucinating when i sent it the error messages. Another problem was that it is trained on old data which had deprecated openai functions so the weights were heavily favored towards functions that arent supported anymore and i had to fix that myself(Trying to force it into using the correct functions in the prompt resulted in unusable code that was very wrong). The last small issue was that it kept my convestations variable initialization inside the function which would lead to wiping history everytime so i took it out.

Part 4:
This is the output of the code:
TASK 1: Zero-Shot vs Few-Shot (Sentiment)

Zero-Shot 
  Input:  The battery life on this phone is absolutely incredible, I love it!
  Output: Positive

  Input:  The delivery was late and the box arrived completely crushed.
  Output: The sentiment of this sentence is negative.

  Input:  The product works fine, nothing special but no complaints either.
  Output: The sentiment of the sentence "The product works fine, nothing special but no complaints either." is neutral. The statement indicates that the product functions as expected without any issues or disappointments, but it lacks enthusiasm or praise beyond basic functionality.

 Few-Shot (3 examples) 
  Input:  The battery life on this phone is absolutely incredible, I love it!
  Output: Positive

  Input:  The delivery was late and the box arrived completely crushed.
  Output: Negative

  Input:  The product works fine, nothing special but no complaints either.
  Output: Neutral


 TASK 2: Parameter Exploration (Temperature & Top-p)

 temperature=0
  Run 1: The ocean glows with a golden hue as the sun dips below the horizon, painting the waves in a mesmerizing display of orange and pink light.
  Run 2: The ocean glows with a golden hue as the sun dips below the horizon, painting the waves in a mesmerizing display of orange and pink light.

 temperature=0.7 
  Run 1: The ocean sparkles with a golden hue as the sun dips below the horizon, painting the waves in strokes of orange and pink.
  Run 2: The sky and sea blend into a golden glow as the sun dips below the horizon, painting the waters with strokes of orange and pink that seem to ripple outward in waves of light.

 temperature=1.2 
  Run 1: The skies ignite in brilliant oranges and pinks as the sun descends, casting long shadows and shimmering waves on the vast expanse of indigo sea that stretches endlessly before them.
  Run 2: As the sun sets, a golden glow spreads across the calm ocean's surface, reflecting off the horizon and turning the water into a mesmerizing swirl of amber, turquoise, and navy blues.

 temperature=0.7, top_p=0.5 
  Run 1: The ocean glows with a golden hue as the sun dips below the horizon, painting the waves in shades of orange and pink.
  Run 2: The ocean sparkles with a golden hue as the sun dips below the horizon, painting the waves in a breathtaking display of orange and pink light.


 TASK 3: Structured JSON Output (Entity Extraction)

  Input:  My name is Sara and I am 25 years old. I work as a software engineer in Beirut.
  Output: {
  "name": "Sara",
  "age": 25,
  "occupation": "software engineer",
  "city": "Beirut"
}
  Valid JSON? YES

  Input:  John Smith, age 40, is a chef from New York City.
  Output: {
  "name": "John Smith",
  "age": 40,
  "occupation": "chef",
  "city": "New York City"
}
  Valid JSON? YES

  Input:  Maria Garcia is 31 and teaches mathematics at a university in Madrid.
  Output: {
  "name": "Maria Garcia",
  "age": 31,
  "occupation": "mathematics teacher",
  "city": "Madrid"
}
  Valid JSON? YES

  All valid: YES

  In task 1, Using few shot prompting forced the model to answer in the format we want exactly unlike the zero shot one where it responded with random filler and explanations we dont need or care abt.

  In task 2,increasing the temperature increases the creativity of the model, we went from 0 (exact same output, fully deterministic) to 1.2 (diffrent outputs, more creativity)
  adding top_p=0.5 made it only able to choose words from the top words of which probabilities add up to 50% so it can only choose words from the top 50% making the randomness more controlled.

  In Task 3, enforcing a JSON structure forced the local model to extract the exact fields we need without creating or deleting random keys.