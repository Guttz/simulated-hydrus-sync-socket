### Run
```
pip install -r requirements.txt
python app.py
```
### Functionality
The demo automatically launches a Flask server and creates a socket in the Namespace '/sync'
Connected clients to the Server Socket must use two fundamental methods:
```
@app.route('/add-modification-table', methods=['GET', 'POST'])
```
This receives a new row and sends a notification to the connected clients
Body example: {method: "GET", resource_url: "https://.../123-123-123"}
```
@app.route('/modification-table-diff')
```
This receives a PARAM with a **Job ID** and sends the table diff according to the last updated resource the Agent had.
GET Example: https://localhost:5000/modification-table-diff?agent_job_id=2
Obs.: If empty parameter, the endpoint returns the full table