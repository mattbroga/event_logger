from flask import Flask, render_template, request
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#app = Flask(__name__)
app = Flask(__name__, static_url_path='/static', static_folder='static')

# Database configuration
engine = create_engine('sqlite:///button_logs.db')  # Adjust for your preferred database
Base = declarative_base()

class ButtonLog(Base):
    __tablename__ = 'button_logs'
    id = Column(Integer, primary_key=True)
    button_name = Column(String)
    timestamp = Column(DateTime)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        button_name = request.form['button_name']
        timestamp = datetime.now()

        # Log to database
        session = Session()
        log_entry = ButtonLog(button_name=button_name, timestamp=timestamp)
        session.add(log_entry)
        session.commit()
        session.close()

        # Log to text file
        with open('logs/button_logs.txt', 'a') as log_file:
            log_file.write(f"{timestamp} - Button '{button_name}' clicked\n")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
