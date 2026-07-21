import sys, io, json, textwrap, openai
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

client = openai.OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen2.5-coder:7b"

def query(messages, temperature=0.7, top_p=1.0, max_tokens=256):
    response = client.chat.completions.create(
        model=MODEL, messages=messages,
        temperature=temperature, top_p=top_p, max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()


test_sentences = [
    "The battery life on this phone is absolutely incredible, I love it!",
    "The delivery was late and the box arrived completely crushed.",
    "The product works fine, nothing special but no complaints either.",
]

print("\nTASK 1: Zero-Shot vs Few-Shot (Sentiment)")

print("\nZero-Shot ")
for s in test_sentences:
    result = query([{"role": "user", "content": f"What is the sentiment of this sentence? '{s}'"}], temperature=0)
    print(f"  Input:  {s}")
    print(f"  Output: {result}\n")

print(" Few-Shot (3 examples) ")
few_shot_examples = [
    {"role": "user", "content": "What is the sentiment of this sentence? 'This restaurant has the best pasta I have ever tasted!'"},
    {"role": "assistant", "content": "Positive"},
    {"role": "user", "content": "What is the sentiment of this sentence? 'Terrible customer service, I waited over an hour.'"},
    {"role": "assistant", "content": "Negative"},
    {"role": "user", "content": "What is the sentiment of this sentence? 'The movie was okay, not great but not bad.'"},
    {"role": "assistant", "content": "Neutral"},
]
for s in test_sentences:
    result = query([*few_shot_examples, {"role": "user", "content": f"What is the sentiment of this sentence? '{s}'"}], temperature=0)
    print(f"  Input:  {s}")
    print(f"  Output: {result}\n")


print("\n TASK 2: Parameter Exploration (Temperature & Top-p) ")

param_prompt = [
    {"role": "system", "content": "You are a creative writing assistant."},
    {"role": "user", "content": "Write a single sentence describing what the ocean looks like at sunset."},
]

configs = [
    {"label": "temperature=0   ",  "temperature": 0,   "top_p": 1.0},
    {"label": "temperature=0.7 ",        "temperature": 0.7, "top_p": 1.0},
    {"label": "temperature=1.2 ", "temperature": 1.2, "top_p": 1.0},
    {"label": "temperature=0.7, top_p=0.5 ", "temperature": 0.7, "top_p": 0.5},
]

for cfg in configs:
    print(f"\n {cfg['label']} ")
    for run in range(1, 3):
        result = query(param_prompt, temperature=cfg["temperature"], top_p=cfg["top_p"])
        print(f"  Run {run}: {result}")


print("\n\n TASK 3: Structured JSON Output (Entity Extraction)")

json_sentences = [
    "My name is Sara and I am 25 years old. I work as a software engineer in Beirut.",
    "John Smith, age 40, is a chef from New York City.",
    "Maria Garcia is 31 and teaches mathematics at a university in Madrid.",
]

json_system = textwrap.dedent("""\
    You are a structured-data extractor.
    From the user's sentence, extract personal information and return
    ONLY a valid JSON object with these exact keys:

    {"name": "<full name>", "age": <integer>, "occupation": "<job title>", "city": "<city>"}

    Rules:
    - Return ONLY the JSON object.
    - Use the exact key names shown above.
    - age must be an integer, not a string.
    - If a field is missing, use null.
""")

all_valid = True
for s in json_sentences:
    raw = query([{"role": "system", "content": json_system}, {"role": "user", "content": s}], temperature=0, max_tokens=200)
    print(f"\n  Input:  {s}")
    print(f"  Output: {raw}")
    try:
        parsed = json.loads(raw)
        print(f"  Valid JSON? YES")
    except json.JSONDecodeError:
        cleaned = raw
        if "```" in raw:
            cleaned = raw.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
            cleaned = cleaned.strip()
        try:
            parsed = json.loads(cleaned)
            print(f"  Valid JSON? YES")
        except json.JSONDecodeError:
            print(f"  Valid JSON? NO")
            all_valid = False

print(f"\n  All valid: {'YES' if all_valid else 'NO'}")


