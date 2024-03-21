## Flask Application Design for Identifying Cheapest Compute Engine VM Instances

### HTML Files

**index.html**

- Main HTML file for the web application.
- Contains the user interface (UI) for displaying the list of regions and the cheapest VM instances along with their hourly prices.
- Utilizes Flask's Jinja2 templating engine to dynamically render the data from the Python backend.

### Routes

**app.py**

- Python script that defines the routes and provides the logic for the web application.
- Includes the following routes:
    - **Root Route (/):**
        - Handles GET requests to the root URL.
        - Fetches the list of GCP regions and the cheapest VM instance type for each region from the Cloud API.
        - Passes the data to the index.html template for rendering.
    - **API Endpoint (/api/instances):**
        - Handles GET requests to fetch the data in JSON format.
        - Provides an interface for external systems to access the application's data.
    - **Region Checker (/region-checker):**
        - Handles POST requests to check if a new region has been added to GCP.
        - Updates the application's internal data if a new region is detected.
        - Can be triggered by Cloud Functions or other automated mechanisms to ensure automatic updates.