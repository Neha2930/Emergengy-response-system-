
from flask import Flask, request, jsonify
import datetime
import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

app = Flask(__name__)

# In-memory storage for user profiles and alert history
user_profiles = {}
alert_history = []

@app.route('/create_profile', methods=['POST'])
def create_profile():
    data = request.get_json()
    profile_name = data.get('name')

    if not profile_name:
        return jsonify({"error": "Profile name is required."}), 400

    if profile_name in user_profiles:
        return jsonify({"error": "Profile already exists."}), 400

    user_profiles[profile_name] = []
    return jsonify({"message": f"Profile created for {profile_name}."}), 201

@app.route('/add_contact', methods=['POST'])
def add_contact():
    data = request.get_json()
    profile_name = data.get('profile_name')
    contact = data.get('contact')

    if not profile_name or not contact:
        return jsonify({"error": "Profile name and contact are required."}), 400

    if profile_name not in user_profiles:
        return jsonify({"error": "Profile not found."}), 404

    user_profiles[profile_name].append(contact)
    return jsonify({"message": f"Contact {contact} added to {profile_name}."}), 201

@app.route('/send_alert', methods=['POST'])
def send_alert():
    data = request.get_json()
    profile_name = data.get('profile_name')
    alert_message = data.get('alert_message')

    if not profile_name or not alert_message:
        return jsonify({"error": "Profile name and alert message are required."}), 400

    if profile_name not in user_profiles:
        return jsonify({"error": "Profile not found."}), 404

    # Send SMS to all contacts
    contacts = user_profiles[profile_name]
    for contact in contacts:
        try:
            message = client.messages.create(
                body=f"🚨 Emergency Alert from {profile_name}: {alert_message}",
                from_=TWILIO_PHONE_NUMBER,
                to=contact
            )
            print(f"Message sent to {contact}: {message.sid}")
        except Exception as e:
            print(f"Error sending message to {contact}: {e}")

    # Log alert
    alert_record = {
        "timestamp": datetime.datetime.now().isoformat(),
        "profile_name": profile_name,
        "alert_message": alert_message
    }
    alert_history.append(alert_record)

    return jsonify({"message": "Alert sent successfully."}), 200

@app.route('/get_history', methods=['GET'])
def get_history():
    return jsonify(alert_history), 200

@app.route('/get_contacts/<profile_name>', methods=['GET'])
def get_contacts(profile_name):
    if profile_name not in user_profiles:
        return jsonify({"error": "Profile not found."}), 404

    contacts = user_profiles[profile_name]
    return jsonify({"contacts": contacts}), 200

if __name__ == '__main__':
    app.run(debug=True)
