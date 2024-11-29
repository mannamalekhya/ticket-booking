from flask import Flask, jsonify, request, render_template_string

# Flask is a lightweight web framework in Python that allows us to build web applications.
# It handles routing (URL paths) and provides tools to build APIs and dynamic websites.

app = Flask(__name__)  # Create a Flask application instance.

# Sample data to represent available movie shows
shows = [
    {"id": 1, "movie": "Inception", "time": "7:00 PM"},
    {"id": 2, "movie": "Interstellar", "time": "9:00 PM"},
]

# A list to store booked tickets (acts like a database for this application).
tickets = []

# HTML template for the user interface (a simple webpage to interact with the app)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Movie Ticket Booking</title>
    <style>
        /* Add some basic styling for the web page to look clean and modern */
        body {
            font-family: 'Arial', sans-serif;
            margin: 20px;
            background-color: #f4f4f9;
            color: #333;
            line-height: 1.6;
        }
        h1, h2 {
            text-align: center;
            color: #444;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        form {
            margin-bottom: 20px;
            padding: 15px;
            background: #f9f9fc;
            border: 1px solid #ddd;
            border-radius: 6px;
        }
        label {
            font-weight: bold;
        }
        input, select, button {
            width: 100%;
            margin-bottom: 10px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            background-color: #5cb85c;
            color: white;
            font-size: 16px;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #4cae4c;
        }
        ul {
            list-style: none;
            padding: 0;
        }
        ul li {
            margin-bottom: 10px;
            padding: 10px;
            background: #f9f9fc;
            border: 1px solid #ddd;
            border-radius: 6px;
        }
        .actions form {
            display: inline-block;
        }
        .actions button {
            background-color: #d9534f;
            margin-right: 5px;
        }
        .actions button.update {
            background-color: #0275d8;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Movie Ticket Booking</h1>

        <!-- View Shows -->
        <h2>Available Shows</h2>
        <ul id="shows">
            {% for show in shows %}
            <li>
                <strong>{{ show.movie }}</strong> at {{ show.time }} 
                <small>(Show ID: {{ show.id }})</small>
            </li>
            {% endfor %}
        </ul>

        <!-- Book Ticket -->
        <h2>Book a Ticket</h2>
        <form method="post" action="/book-ui">
            <label for="name">Your Name:</label>
            <input type="text" id="name" name="name" placeholder="Enter your name" required>
            <label for="show_id">Show ID:</label>
            <input type="number" id="show_id" name="show_id" placeholder="Enter Show ID" required>
            <button type="submit">Book Ticket</button>
        </form>

        <!-- View Tickets -->
        <h2>Booked Tickets</h2>
        <ul id="tickets">
            {% for ticket in tickets %}
            <li>
                <strong>{{ ticket.movie }}</strong> at {{ ticket.time }} <br>
                Ticket ID: {{ ticket.id }} | Name: {{ ticket.name }}
                <div class="actions">
                    <form method="post" action="/cancel-ui">
                        <input type="hidden" name="ticket_id" value="{{ ticket.id }}">
                        <button type="submit">Cancel</button>
                    </form>
                    <form method="post" action="/update-ui">
                        <input type="hidden" name="ticket_id" value="{{ ticket.id }}">
                        <input type="text" name="name" placeholder="New Name">
                        <input type="number" name="show_id" placeholder="New Show ID">
                        <button type="submit" class="update">Update</button>
                    </form>
                </div>
            </li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""


@app.route("/")
def home():
    """
    The main route that displays the HTML template for the booking system.
    `render_template_string` dynamically generates HTML with the current list of shows and tickets.
    """
    return render_template_string(HTML_TEMPLATE, shows=shows, tickets=tickets)


@app.route("/book-ui", methods=["POST"])
def book_ticket_ui():
    """
    Handles booking a ticket.
    Accepts user input (name and show ID) from the web form and adds the ticket to the list.
    """
    name = request.form.get("name")  # Fetch 'name' field from the form data
    show_id = int(
        request.form.get("show_id")
    )  # Fetch 'show_id' field and convert it to integer

    # Find the show corresponding to the given show ID
    show = next((s for s in shows if s["id"] == show_id), None)
    if not show:
        return "Show not found!", 404

    # Create a ticket entry
    ticket = {
        "id": len(tickets) + 1,  # Generate a unique ID for the ticket
        "name": name,
        "show_id": show_id,
        "movie": show["movie"],
        "time": show["time"],
    }
    tickets.append(ticket)  # Add the ticket to the list
    return home()  # Refresh the home page with the updated ticket list


@app.route("/cancel-ui", methods=["POST"])
def cancel_ticket_ui():
    """
    Cancels a ticket. Removes the ticket from the list based on its ID.
    """
    ticket_id = int(request.form.get("ticket_id"))  # Fetch the ticket ID to cancel
    global tickets
    tickets = [
        t for t in tickets if t["id"] != ticket_id
    ]  # Remove the ticket with the matching ID
    return home()


@app.route("/update-ui", methods=["POST"])
def update_ticket_ui():
    """
    Updates a ticket's name or show ID.
    Accepts new details from the form and modifies the ticket in the list.
    """
    ticket_id = int(request.form.get("ticket_id"))  # Fetch the ticket ID to update
    new_name = request.form.get("name")  # New name (optional)
    new_show_id = request.form.get("show_id")  # New show ID (optional)

    # Find the ticket to update
    ticket = next((t for t in tickets if t["id"] == ticket_id), None)
    if not ticket:
        return "Ticket not found!", 404

    # Update name and/or show details
    if new_name:
        ticket["name"] = new_name
    if new_show_id:
        new_show_id = int(new_show_id)
        show = next((s for s in shows if s["id"] == new_show_id), None)
        if show:
            ticket["show_id"] = new_show_id
            ticket["movie"] = show["movie"]
            ticket["time"] = show["time"]

    return home()


if __name__ == "__main__":
    app.run(debug=True)  # Start the Flask development server in debug mode
