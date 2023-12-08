from flask import Flask, render_template, request, session, url_for, redirect, jsonify, flash;
from openai_logic import generate_best

app = Flask(__name__,static_folder = 'static', static_url_path = '/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_suggestions', methods=['POST'])
def generate_suggestions():
    data = request.get_json()
    interview_history = data.get('interview_history', '')
    prompt_type = data.get('prompt_type', '')
    #print(interview_history,prompt_type)
    #suggestions = get_question_suggestion(interview_history)
    suggestions = generate_best(interview_history, prompt_type)
    return jsonify({'suggestions': suggestions})

#def get_suggestions(interview_history):
#    return [evaluate_question_suggestion(interview_history)]
		
app.secret_key = 'some key that you will never guess'
app.config['MYSQL_CONNECT_TIMEOUT'] = 10
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    #public_url = ngrok.connect(port=5000)
    app.run('127.0.0.1', 5000, debug = True)
