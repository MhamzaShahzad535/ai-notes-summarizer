# AI Notes Summarizer API

AI Notes Summarizer API is a backend application built with FastAPI that allows users to create notes, securely log in, generate AI summaries using Google Gemini, and download a PDF report containing their notes and summaries.

This project was created as part of the Backend AI Engineering capstone project.

## Problem

Students and professionals often have long notes that take time to reread.

This application stores notes and uses AI to generate short summaries so that users can understand the most important information more quickly.

## 10x Claim

AI Notes Summarizer reduces the time needed to review long notes by generating concise summaries in seconds.

## Main Features

* User registration
* User login with JWT authentication
* Protected API endpoints
* Create and retrieve notes
* Store notes permanently using SQLite
* Generate AI summaries using Google Gemini
* Validate AI input and output
* Log LLM token usage and estimated cost
* Generate downloadable PDF reports

## Technologies

* Python
* FastAPI
* SQLite
* SQLAlchemy
* JWT Authentication
* Google Gemini API
* ReportLab
* Pydantic
* Uvicorn

## Capstone Concepts

| Concept         | Implementation                                          |
| --------------- | ------------------------------------------------------- |
| API Endpoints   | FastAPI endpoints in `main.py`                          |
| Database        | SQLite with SQLAlchemy in `database.py` and `models.py` |
| Authentication  | JWT authentication in `auth.py`                         |
| LLM Integration | Gemini summarization in `llm.py`                        |
| Reporting       | PDF report generation in `report.py`                    |

## LLM Validation and Cost Logging

The AI summarization feature validates the note before sending it to Gemini.

The application also validates that Gemini returns a usable summary.

Each Gemini request logs:

* Model name
* Input tokens
* Output tokens
* Thinking tokens
* Total tokens
* Estimated paid-tier cost

Usage information is stored in:

```text
llm_usage.csv
```

Example:

```text
timestamp,model,prompt_tokens,output_tokens,thinking_tokens,total_tokens,estimated_paid_cost_usd
2026-09-14T16:51:04.829782+00:00,gemini-3.5-flash-lite,43,20,0,63,0.00006290
```

## Project Structure

```text
ai-notes-summarizer/
│
├── main.py
├── auth.py
├── database.py
├── models.py
├── schemas.py
├── llm.py
├── report.py
├── llm_usage.csv
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/MhamzaShahzad535/ai-notes-summarizer.git
cd ai-notes-summarizer
```

Create a virtual environment:

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Gemini API Key

Create a Gemini API key using Google AI Studio.

Set the API key as an environment variable.

### Windows PowerShell

```powershell
$env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

Do not store your API key directly inside the source code.

## Run the Application

Start the FastAPI server:

```powershell
uvicorn main:app --reload
```

Open Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Register

```text
POST /register
```

Example:

```json
{
  "email": "user@example.com",
  "password": "test123"
}
```

### Login

```text
POST /login
```

Returns a JWT access token.

### Create Note

```text
POST /notes
```

Authentication is required.

Example:

```json
{
  "title": "Deep Learning",
  "content": "Deep learning uses neural networks with multiple layers to learn complex patterns from data."
}
```

### Get Notes

```text
GET /notes
```

Authentication is required.

### Summarize Note

```text
POST /notes/{note_id}/summarize
```

Example:

```text
POST /notes/1/summarize
```

Example response:

```json
{
  "id": 1,
  "title": "Deep Learning",
  "summary": "Deep learning utilizes multi-layered neural networks. These networks are designed to learn complex patterns from data."
}
```

### Generate PDF Report

```text
GET /report
```

This generates and downloads:

```text
AI_Notes_Report.pdf
```

The report contains the original notes and their AI-generated summaries.

## 5-Minute Demo

1. Start the API with `uvicorn main:app --reload`.
2. Open `http://127.0.0.1:8000/docs`.
3. Register a user using `/register`.
4. Login using `/login`.
5. Copy the returned JWT token.
6. Click **Authorize** in Swagger and enter the token.
7. Create a note using `/notes`.
8. View saved notes using `GET /notes`.
9. Generate a summary using `/notes/{note_id}/summarize`.
10. Generate and download the PDF using `/report`.

## Security

* Passwords are hashed before they are stored.
* Protected endpoints require JWT authentication.
* The Gemini API key is stored in an environment variable.
* Secrets are not committed to GitHub.
* Local SQLite database files are ignored by Git.

## Non-Goal

This project does not include a complex frontend or mobile application.

The goal of the project is to demonstrate a simple working backend system with authentication, database persistence, AI integration, validation, cost logging, and PDF reporting.

## Future Improvements

Possible future improvements include:

* Allow each user to access only their own notes
* Add update and delete note endpoints
* Add a frontend interface
* Add automated tests
* Deploy the API online

## Author

Muhammad Hamza Shahzad

