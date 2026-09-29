````markdown
# TraceShield Backend

TraceShield is a blockchain investigation-support backend designed to
organize verified analytical information and generate structured
investigation reports.

The backend is built with Python, FastAPI, and Pydantic.

---

## Features

- Investigation data validation
- Structured investigation reports
- Transaction analysis representation
- Fund-flow representation
- Wallet relationship analysis
- Risk indicator representation
- Entity intelligence representation
- Investigation timeline
- Evidence references
- AI-assisted investigation explanations
- Optional LLM integration
- REST API
- Swagger API documentation

---

## Technology Stack

- Python
- FastAPI
- Pydantic
- Uvicorn
- Python-dotenv

---

## Project Structure

```text
backend/
│
├── app/
│   ├── __init__.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── investigation.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── investigation_input.py
│   │   └── investigation_report.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py
│   │   ├── llm_service.py
│   │   └── report_generator.py
│   │
│   └── main.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
````

---

## Installation

Open PowerShell and navigate to the backend directory:

```powershell
cd "C:\Users\asus\OneDrive\Desktop\Traceshield1\backend"
```

Create a virtual environment if required:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the backend directory.

Example:

```text
LLM_API_KEY=
LLM_MODEL=default-model
LLM_PROVIDER=not_configured
```

The LLM configuration can remain empty while the
basic TraceShield backend is being developed.

---

## Running the Backend

From the backend directory:

```powershell
python -m uvicorn app.main:app --reload
```

The backend will normally start at:

```text
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically provides Swagger documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Alternative ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

---

## Health Check

The backend provides a health endpoint:

```text
GET /health
```

Example response:

```json
{
    "status": "healthy",
    "service": "TraceShield Backend"
}
```

---

## Root Endpoint

```text
GET /
```

Example response:

```json
{
    "application": "TraceShield",
    "status": "running",
    "version": "1.0.0"
}
```

---

## Investigation API

The main investigation endpoint is:

```text
POST /investigation/generate
```

It accepts structured investigation information and generates
an `InvestigationReport`.

The input is validated using Pydantic models.

The report contains:

* Case information
* Investigation summary
* Transaction summary
* Major fund flows
* Wallet relationships
* Risk indicators
* Entity intelligence
* Investigation timeline
* Analytical interpretation
* Evidence references
* Limitations

---

## Design Principles

TraceShield follows an evidence-grounded architecture.

The AI layer:

* Uses supplied analytical information.
* Does not invent blockchain transactions.
* Does not invent wallet addresses.
* Does not create unsupported evidence.
* Does not independently determine wallet ownership.
* Does not establish criminal activity.
* Preserves evidence references.
* Clearly communicates limitations.

The generated report should always be reviewed against
the underlying evidence.

---

## Development

Run the application with auto-reload:

```powershell
python -m uvicorn app.main:app --reload
```

After modifying Python files, Uvicorn automatically reloads
the application during development.

---

## API Flow

```text
Investigation Data
       │
       ▼
InvestigationInput
       │
       ▼
Validation
       │
       ▼
AI Service
       │
       ▼
Report Generator
       │
       ▼
InvestigationReport
       │
       ▼
JSON API Response
```

---

## Current Scope

The current backend focuses on:

1. Investigation data validation
2. Investigation analysis representation
3. AI-assisted explanation
4. Structured report generation
5. REST API delivery

Blockchain data collection and external intelligence providers
can be connected to the system through additional services later.

---

## License

This project is developed for educational, research,
and investigation-support purposes.

````

### Create the file

You can create it directly from PowerShell using:

```powershell
notepad README.md
````

Paste the code above, save it, and close Notepad.

### Verify

Run:

```powershell
Get-Item README.md
```

Then:

```powershell
Get-Content README.md | Select-Object -First 10
```

You should see:

```text
# TraceShield Backend

TraceShield is a blockchain investigation-support backend designed to
organize verified analytical information and generate structured
investigation reports.
```

Once this is created successfully, **send me the result and we'll continue with File 17.**
