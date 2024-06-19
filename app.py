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
        button_name = request.form['button_name']
        timestamp = datetime.now().isoformat()  # ISO 8601 format is recommended for timestamps

        # Log to Firebase Realtime Database
        users_ref = ref.child('button_logs')  # Reference to the 'button_logs' node
        users_ref.push().set({
            'button_name': button_name,
            'timestamp': timestamp
        })

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
