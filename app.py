from flask import Flask, request, jsonify
import openai
import random

app = Flask(__name__)

# Configure OpenAI API Key
openai.api_key = "my-open-ai-keyyy"

# Sample starting scenarios
SCENARIOS = [
    "You wake up in a mysterious forest with no memory of how you got there. A shadow moves between the trees...",
    "You stand before the gates of a ruined castle. The wind howls as the doors creak open by themselves...",
    "The spaceship's alarms blare as you awaken from cryosleep. Something has gone terribly wrong..."
]

# Game state storage (In a real-world app, use a database)
game_sessions = {}

def generate_story(prompt, user_input):
    """Generate the next part of the story based on user input."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a dungeon master narrating an interactive RPG story."},
            {"role": "user", "content": prompt + "\nUser Action: " + user_input}
        ]
    )
    return response['choices'][0]['message']['content']

@app.route("/start", methods=["POST"])
def start_game():
    """Start a new game session."""
    user_id = request.json.get("user_id")
    scenario = random.choice(SCENARIOS)
    game_sessions[user_id] = scenario
    return jsonify({"story": scenario})

@app.route("/play", methods=["POST"])
def play():
    """Continue the game based on user input."""
    user_id = request.json.get("user_id")
    user_input = request.json.get("user_input")
    
    if user_id not in game_sessions:
        return jsonify({"error": "Game session not found. Start a new game."}), 400
    
    new_story = generate_story(game_sessions[user_id], user_input)
    game_sessions[user_id] += "\n" + user_input + "\n" + new_story
    
    return jsonify({"story": new_story})

@app.route('/api/game', methods=['POST'])
def start_game():
    data = request.json
    return jsonify({"message": f"Game started! Welcome, {data['player_name']}."})


if __name__ == "__main__":
    app.run(debug=True)
