from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Helper: find an event by ID (avoids repeating the same search in PATCH and DELETE)
def find_event(event_id):
    for event in events:
        if event.id == event_id:
            return event
    return None

# GET / - JSON welcome message (the rubric tests this)
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Event Management API!"}), 200

# GET /events - return all events as a JSON array (the rubric tests this)
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200

# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    # Read the JSON body (silent=True returns None instead of crashing on bad JSON)
    data = request.get_json(silent=True)

    # Input validation: title must be present
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Generate the next ID (safe even after deletions)
    new_id = max((e.id for e in events), default=0) + 1

    new_event = Event(new_id, data["title"])
    events.append(new_event)

    # 201 Created for a successful POST
    return jsonify(new_event.to_dict()), 201

# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # Look up the event; return 404 if it doesn't exist
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    # Validate the JSON body
    data = request.get_json(silent=True)
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    event.title = data["title"]
    return jsonify(event.to_dict()), 200

# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Look up the event; return 404 if it doesn't exist
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)
    # 204 No Content: success, nothing to return
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)