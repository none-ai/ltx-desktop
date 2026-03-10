# LTX Desktop

A modern Flask web application for LTX Desktop, featured on Product Hunt.

## Features

- **Home Page** - Welcome page with product highlights and call-to-action buttons
- **Features Page** - Detailed showcase of product capabilities
- **About Page** - Company mission and technology information
- **Contact Page** - Contact form for user feedback
- **API Endpoints** - RESTful API for application information
- **Rate Limiting** - Built-in rate limiting for API protection
- **Request Tracking** - Unique request ID for every API call

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/info` | GET | Application information |
| `/api/health` | GET | Health check endpoint |
| `/api/contact` | POST | Submit contact form |
| `/api/stats` | GET | Application statistics |
| `/api/features` | GET | List all features |
| `/api/routes` | GET | List all available routes |

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd ltx-desktop

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the App

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | 5000 |
| `FLASK_DEBUG` | Debug mode | True |
| `SECRET_KEY` | Flask secret key | dev-secret-key |

## Project Structure

```
ltx-desktop/
├── app.py              # Main application file
├── requirements.txt   # Python dependencies
├── templates/          # HTML templates
│   ├── base.html      # Base template
│   ├── home.html      # Home page
│   ├── features.html  # Features page
│   ├── about.html     # About page
│   └── contact.html  # Contact page
└── static/
    └── css/
        └── style.css  # Styling
```

## Technology Stack

- **Backend**: Flask 3.0
- **Frontend**: HTML5, CSS3
- **Python**: 3.8+

作者: stlin256的openclaw
