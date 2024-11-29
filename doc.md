---

## **Movie Ticket Booking API Documentation**

### **Base URL**
`http://127.0.0.1:5000`

---

### **1. View Shows**
**Description:** Retrieve a list of all available shows.

- **Endpoint:** `/shows`
- **HTTP Method:** `GET`
- **Request Body:** None
- **Response Format:**
  ```json
  {
    "shows": [
      {
        "id": 1,
        "movie": "Inception",
        "time": "7:00 PM"
      },
      {
        "id": 2,
        "movie": "Interstellar",
        "time": "9:00 PM"
      }
    ]
  }
  ```
- **Example Request:**
  ```bash
  curl -X GET http://127.0.0.1:5000/shows
  ```

---

### **2. Book a Ticket**
**Description:** Book a ticket for a specific show.

- **Endpoint:** `/book`
- **HTTP Method:** `POST`
- **Request Body:**
  ```json
  {
    "show_id": <show_id>,
    "name": "<your_name>"
  }
  ```
  - `show_id` (integer): The ID of the show to book.
  - `name` (string): The name of the person booking the ticket.

- **Response Format:**
  - Success:
    ```json
    {
      "message": "Ticket booked successfully",
      "ticket": {
        "id": <ticket_id>,
        "name": "<your_name>",
        "show_id": <show_id>,
        "movie": "<movie_name>",
        "time": "<show_time>"
      }
    }
    ```
  - Error:
    ```json
    {
      "error": "Show not found"
    }
    ```

- **Example Request:**
  ```bash
  curl -X POST -H "Content-Type: application/json" \
       -d '{"show_id": 1, "name": "Alice"}' \
       http://127.0.0.1:5000/book
  ```

---

### **3. View Booked Tickets**
**Description:** Retrieve a list of all booked tickets.

- **Endpoint:** `/tickets`
- **HTTP Method:** `GET`
- **Request Body:** None
- **Response Format:**
  ```json
  {
    "tickets": [
      {
        "id": 1,
        "name": "Alice",
        "show_id": 1,
        "movie": "Inception",
        "time": "7:00 PM"
      }
    ]
  }
  ```
- **Example Request:**
  ```bash
  curl -X GET http://127.0.0.1:5000/tickets
  ```

---

### **4. Cancel a Ticket**
**Description:** Cancel a booked ticket.

- **Endpoint:** `/cancel/<ticket_id>`
- **HTTP Method:** `DELETE`
- **Path Parameter:**
  - `ticket_id` (integer): The ID of the ticket to cancel.
- **Request Body:** None
- **Response Format:**
  - Success:
    ```json
    {
      "message": "Ticket canceled successfully"
    }
    ```
  - Error:
    ```json
    {
      "error": "Ticket not found"
    }
    ```

- **Example Request:**
  ```bash
  curl -X DELETE http://127.0.0.1:5000/cancel/1
  ```

---

### **5. Update a Ticket**
**Description:** Update an existing ticket's name or show ID.

- **Endpoint:** `/update/<ticket_id>`
- **HTTP Method:** `PUT`
- **Path Parameter:**
  - `ticket_id` (integer): The ID of the ticket to update.
- **Request Body:**
  ```json
  {
    "name": "<new_name>",
    "show_id": <new_show_id>
  }
  ```
  - `name` (string, optional): The updated name of the ticket holder.
  - `show_id` (integer, optional): The updated show ID for the ticket.

- **Response Format:**
  - Success:
    ```json
    {
      "message": "Ticket updated successfully",
      "ticket": {
        "id": <ticket_id>,
        "name": "<new_name>",
        "show_id": <new_show_id>,
        "movie": "<movie_name>",
        "time": "<show_time>"
      }
    }
    ```
  - Error:
    ```json
    {
      "error": "Ticket not found"
    }
    ```

- **Example Request:**
  ```bash
  curl -X PUT -H "Content-Type: application/json" \
       -d '{"name": "Bob", "show_id": 2}' \
       http://127.0.0.1:5000/update/1
  ```

---

### Error Handling
1. **Invalid Show ID:**
   - Status: `404 Not Found`
   - Response: `{"error": "Show not found"}`

2. **Invalid Ticket ID:**
   - Status: `404 Not Found`
   - Response: `{"error": "Ticket not found"}`

3. **Validation Errors:**
   - Status: `400 Bad Request`
   - Response: `{"error": "Validation error message"}`

---

### Notes
- The `ticket_id` is automatically generated and unique for each booking.
- The `show_id` must correspond to an existing show; otherwise, the API will return an error.
- All responses are in JSON format.
- Test the API using tools like **Postman**, **curl**, or integrate it with the provided minimal UI.

---