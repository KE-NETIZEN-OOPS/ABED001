from flask import Flask, render_template, request, jsonify
import spacy
import re  # Import the 're' module
from datetime import datetime, timedelta

app = Flask(__name__)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Store client name, bookings, and conversation state
client_name = None
bookings = {}
conversation_state = {
    "in_progress": False,
    "department": None,
    "doctor": None,
    "date": None,
    "time": None
}

# Doctor schedule with specific days and times
doctor_schedule = {
    "dr. alice smith": {
        "department": "Cardiology",
        "availability": ["Monday", "Wednesday"],
        "hours": "9 AM - 1 PM"
    },
    "dr. bob jones": {
        "department": "Neurology",
        "availability": ["Tuesday", "Thursday"],
        "hours": "10 AM - 2 PM"
    },
    "dr. carol brown": {
        "department": "Pediatrics",
        "availability": ["Friday"],
        "hours": "11 AM - 3 PM"
    },
    "dr. david white": {
        "department": "Orthopedics",
        "availability": ["Wednesday", "Friday"],
        "hours": "8 AM - 12 PM"
    },
    "dr. emily green": {
        "department": "General Surgery",
        "availability": ["Monday", "Thursday"],
        "hours": "1 PM - 5 PM"
    }
}

# Symptoms and relevant guidance with suggested doctors
symptoms_treatments = {
    "fever": {
        "treatment": "Stay hydrated, rest, and take acetaminophen or ibuprofen. If it persists, book an appointment.",
        "department": "Pediatrics"
    },
    "cough": {
        "treatment": "Drink warm fluids, take cough syrup, and rest. If it continues for more than a week, see a doctor.",
        "department": "Pediatrics"
    },
    "headache": {
        "treatment": "Rest in a dark room, stay hydrated, and take ibuprofen or acetaminophen. If severe, book a visit.",
        "department": "Neurology"
    },
    "nausea": {
        "treatment": "Try ginger tea, eat light foods, and drink small sips of water. If ongoing, consult a doctor.",
        "department": "General Surgery"
    },
    "stomach pain": {
        "treatment": "Apply a warm compress, drink chamomile tea, and take antacids if necessary. Seek medical help if persistent.",
        "department": "General Surgery"
    },
    "burn": {
        "treatment": "Rinse with cool water, avoid popping blisters, and cover loosely. Seek medical attention for serious burns.",
        "department": "General Surgery"
    }
}

# Operating and visiting hours
opening_hours = "Our hospital is open from 8 AM to 8 PM, Monday to Saturday."
visiting_hours = "Visiting hours are from 9 AM to 8 PM every day."

departments = [info['department'].lower() for info in doctor_schedule.values()]

@app.route('/')
def home():
    return render_template('index.html')

def extract_entities(user_input):
    """Uses spaCy to extract entities like doctor names, dates, and departments."""
    doc = nlp(user_input)
    entities = {
        "doctor": None,
        "department": None,
        "date": None,
        "time": None
    }
    
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            if ent.text.lower() in doctor_schedule:
                entities["doctor"] = ent.text.lower()
        elif ent.label_ == "ORG":
            for department in departments:
                if department in ent.text.lower():
                    entities["department"] = department
        elif ent.label_ == "DATE":
            entities["date"] = ent.text
        elif ent.label_ == "TIME":
            entities["time"] = ent.text

    if entities["department"] is None:
        for department in departments:
            if department in user_input.lower():
                entities["department"] = department
    if entities["doctor"] is None:
        for doctor in doctor_schedule:
            if doctor in user_input.lower():
                entities["doctor"] = doctor
    
    return entities

# Function to find doctors by department
def find_doctors_by_department(department):
    found_doctors = []
    for doctor, info in doctor_schedule.items():
        if info["department"].lower() == department.lower():
            found_doctors.append(doctor)
    if found_doctors:
        response_text = f"Doctors in the {department} department:\n" + "\n".join(found_doctors)
        return response_text
    else:
        return f"No doctors found in the {department} department."

# Function to find the department in a string
def find_department(text):
    for department in departments:
        if re.search(rf"\b{department}\b", text, re.IGNORECASE):
            return department
    return None

@app.route('/get-response', methods=['POST'])
def get_response():
    global client_name, bookings, conversation_state
    user_input = request.form['user_input'].strip().lower()

    if client_name is None:
        # Greeting and Name Retrieval
        if "hello" in user_input or "hi" in user_input:
            return jsonify({"response": "Hello! I’m your hospital assistant. May I know your name?"})
        elif "name is" in user_input:
            client_name = user_input.split("name is")[-1].strip().capitalize()
            return jsonify({"response": f"Nice to meet you, {client_name}! How can I assist you today?"})
        else:
            return jsonify({"response": "Hello! May I know your name, please?"})

    if "book" in user_input or "appointment" in user_input or "schedule" in user_input:
        # Begin Appointment Booking
        conversation_state["in_progress"] = True
        conversation_state["department"] = None  # Reset department selection
        return jsonify({"response": "Great! Which department do you need an appointment with? Our departments include Cardiology, Neurology, Pediatrics, Orthopedics, and General Surgery."})

    # Check if Appointment is in Progress and Department is Required
    if conversation_state["in_progress"] and not conversation_state["department"]:
        department = find_department(user_input)
        if department:
            conversation_state["department"] = department  # Store selected department
            response_text = find_doctors_by_department(department)
            return jsonify({"response": f"Great, you chose the {department} department. " + response_text})
        else:
            return jsonify({"response": "Please specify a valid department like Cardiology, Neurology, Pediatrics, Orthopedics, or General Surgery."})

    # If the user has specified a department, ask for a date
    if conversation_state["in_progress"] and conversation_state["department"] and not conversation_state["date"]:
        entities = extract_entities(user_input)
        if entities["date"]:
            conversation_state["date"] = entities["date"]
            available_doctors = [
                doctor for doctor, details in doctor_schedule.items() 
                if details["department"].lower() == conversation_state["department"].lower() 
                and entities["date"].lower() in [day.lower() for day in details["availability"]]
            ]
            if available_doctors:
                conversation_state["doctor"] = available_doctors[0]
                return jsonify({
                    "response": f"Selected {available_doctors[0].title()} on {entities['date']}. Available hours are {doctor_schedule[available_doctors[0]]['hours']}. Please specify a time within these hours."
                })
            else:
                return jsonify({"response": f"No available doctors in {conversation_state['department']} on {entities['date']}. Please choose another date."})
        else:
            return jsonify({"response": "Please specify a date for your appointment."})

    # If the user has specified a doctor and date, ask for a time
    if conversation_state["in_progress"] and conversation_state["doctor"] and not conversation_state["time"]:
        entities = extract_entities(user_input)
        if entities["time"]:
            conversation_state["time"] = entities["time"]
            bookings[client_name] = {
                "department": conversation_state["department"],
                "doctor": conversation_state["doctor"].title(),
                "date": conversation_state["date"],
                "time": conversation_state["time"]
            }
            response_message = (f"Appointment successfully booked with {conversation_state['doctor'].title()} in {conversation_state['department']} "
                                f"on {conversation_state['date']} at {conversation_state['time']}. A reminder will be sent before the appointment. "
                                "Please confirm the date and time, and remember to keep time. If all is correct, you're all set!")

            # Reset conversation state after booking
            conversation_state = {"in_progress": False, "department": None , "doctor": None, "date": None, "time": None}
            return jsonify({"response": response_message})
        else:
            return jsonify({"response": "Please specify a time for your appointment."})

    # General inquiries about visiting hours or opening hours
    if "visiting hours" in user_input:
        return jsonify({"response": visiting_hours})

    if "opening hours" in user_input:
        return jsonify({"response": opening_hours})

    # Handling symptoms
    for symptom, details in symptoms_treatments.items():
        if symptom in user_input:
            return jsonify({"response": f"{details['treatment']} If the symptom persists, please consider booking an appointment with"})

    # Goodbye
    if "goodbye" in user_input or "bye" in user_input:
        return jsonify({"response": "Goodbye and have a good day! Thanks for visiting us."})

    # Other responses if no match
    return jsonify({"response": f"I'm sorry, {client_name}, I didn’t understand that. Could you try rephrasing?"})

if __name__ == '__main__':
    app.run(debug=True)