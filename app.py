import os
import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, render_template, request
from datetime import datetime

# Firebase initialization
try:
    cred = credentials.Certificate('firebase_credentials.json')  # Adjust path if needed
    firebase_admin.initialize_app(cred, {
      'databaseURL': 'https://event-logger-cf33a-default-rtdb.firebaseio.com/'
    })
except ValueError:
    # Handle invalid JSON format
    print("Error: Invalid firebase_credentials.json file format.")
except FileNotFoundError:
    # Handle missing file
    print("Error: firebase_credentials.json file not found.")


ref = db.reference('/')  # Get a reference to the root of your database


#app = Flask(__name__)
app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        game_name = request.form['game_name']  # Get the game name from the form
        button_name = request.form['button_name']
        timestamp = datetime.utcnow().isoformat()

        # Log to Firebase Realtime Database
        game_ref = ref.child('games').child(game_name)  # Reference to the game
        game_ref.push().set({  # Push a new event under the game
            'button_name': button_name,
            'timestamp': timestamp
        })

    # Retrieve button logs from Firebase
    button_logs_ref = db.reference('button_logs')  # Reference to 'button_logs'
    button_logs = button_logs_ref.get()  # Get all button logs as a dictionary

    return render_template('index.html', button_logs=button_logs)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
