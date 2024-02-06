# URL Shortener Service

A simple URL shortener service built with Flask.

## Features

- Shorten long URLs to easily share.
- Delete short URLs.
- Log and track HTTP requests.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes.

### Prerequisites

- Python 3.10
- Flask 3.0.1

### Installation

1. Clone the repository:

   ```git clone https://github.com/yourusername/url-shortener.git```

2. Change into the project directory:
   ```cd url-shortener```
3. Install dependencies:
   ```pip install -r requirements.txt```

### Usage

1. Run the Flask application:
   ```python app.py```
2. Access the application in your web browser:
   ```http://127.0.0.1:5000/```
3. Use the API endpoints:

- Create a short URL:
  ```
  PUT /api/url
    {"url": "https://example.com/somepath"}
    ```
- Delete a short URL:
  ```DELETE /api/url/ABC123 ```

### API Endpoints

- Create Short URL

    - Endpoint: PUT /api/url
    - Request JSON:```  {"url": "https://example.com/somepath"}```
    - Response:```{"url": "http://127.0.0.1:5000/ABC123"}```

 - Delete Short URL

    - Endpoint: DELETE /api/url/ABC123 
    - Response: ```OK```

### Logging
All HTTP requests are logged. You can find the logs in the access.log file.
