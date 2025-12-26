# SmartEducation

**Version:** 0.2.0

## Overview
SmartEducation is a premium AI-powered educational dashboard and resource management platform.

## Key Features
- **Modern Dashboard:** Glassmorphism UI with interactive stats (Hours Spent, Completion, etc.).
- **User Activity Framework:** Real-time tracking of user interactions, logins, and learning milestones.
- **AI Bookmark System:** Intelligent resource categorization and ranking based on learning goals.
- **Session Resumption:** "Welcome Back" logic that prompts users to resume their last significant activity.
- **Secure Authentication:** Integrated JWT authentication with OTP-based registration and password reset.

## Tech Stack
- **Backend:** Flask (Python) with SQLAlchemy & JWT.
- **Frontend:** Vanilla JS, CSS3 (Glassmorphism), FontAwesome.
- **Database:** SQLite (SQLAlchemy ORM).


## Configuration

The application uses environment variables for configuration. Create a `.env` file in the root directory or set these variables in your deployment environment.

### Required Variables
- `SECRET_KEY`: Secret key for Flask sessions.
- `JWT_SECRET_KEY`: Secret key for JWT authentication.
- `MAIL_USERNAME` / `MAIL_PASSWORD`: Credentials for the mail server.
- `TWILIO_ACCOUNT_SID` / `TWILIO_AUTH_TOKEN`: Credentials for Twilio SMS.

### Development Defaults
If not set, the application defaults to development values (e.g., `dev-secret-key-change-in-production`). The application automatically validates the presence of these variables on startup in production mode (`DEBUG=False`).

### Constants
Hardcoded values and URLs are centralized in `app/constants.py`.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd SmartEducation
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
  ```bash
  venv\Scripts\activate
  ```
- macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
python app.py
```

## Project Structure
```
SmartEducation/
├── README.md
├── requirements.txt
├── .gitignore
├── app.py
└── ...
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License.

## Contact
For questions or feedback, please reach out to the development team.
