from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    name = ""
    if request.method == 'POST':
        name = request.form['name'].strip().lower()
        with open('secrets.json') as f:
            data = json.load(f)
        message = data.get(name, "No secret message found for you.")
    return render_template('index.html', message=message, name=name)

@app.route('/update', methods=['POST'])
def update_secret():
    data = request.json
    name = data.get("name").strip().lower()
    message = data.get("message")

    with open('secrets.json', 'r') as f:
        secrets = json.load(f)

    secrets[name] = message

    with open('secrets.json', 'w') as f:
        json.dump(secrets, f, indent=4)

    return jsonify({"status": "success", "message": f"Secret for {name} updated."})

if __name__ == '__main__':
    app.run(debug=True)
