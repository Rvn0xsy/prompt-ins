# Indirect Prompt Injection Log Receiver Service

A Python Flask Web server for validating crawler agents' performance against **indirect prompt injection attacks**. The system uses UUID allocation mechanism and authentication log recording to help detect and evaluate agent behavior when facing indirect prompt injection attacks.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Dependencies](#dependencies)

## Features

| Route | Description |
|-------|-------------|
| `/` | Home page, assigns unique UUID to each client and renders page |
| `/page` | Alternative home page, same functionality as `/` |
| `/test` | Test page, used for testing auth route |
| `/auth` | Auth route, receives UUID and data parameters, records access logs |
| `/logs` | Log viewing page, displays all auth route access records |

### Core Features

- 🔐 **UUID Allocation**: Automatically generates unique identifiers for each client
- 📊 **Log Recording**: Records client IP, User-Agent, UUID, request data, etc.
- 🌐 **Web Interface**: Beautiful HTML interface with log viewing support
- 🔒 **Secure Logging**: Stores up to 1000 access records

## Project Structure

```
prompt-ins/
├── app.py              # Flask main application
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── index.html      # Home page template (UUID display)
│   ├── logs.html       # Log viewing page
│   └── test.html       # Test page
└── README.md           # Project documentation
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure SSL Certificates (Optional)

HTTPS requires SSL certificate files:
- Certificate file: `cert.pem`
- Key file: `key.pem`

Configuration options:
- Place certificate files in project root directory
- Or set environment variables:
  ```bash
  export SSL_CERT_FILE=/path/to/cert.pem
  export SSL_KEY_FILE=/path/to/key.pem
  ```

### 3. Run Server

```bash
python app.py
```

Server runs on `http://localhost:5000` by default

### 4. Usage Flow

1. Visit `http://localhost:5000` to get UUID
2. Click "Test Auth" button on test page to send auth request
3. Visit `http://localhost:5000/logs` to view log records

## API Documentation

### GET /

Home route, assigns UUID to client and renders page.

**Response**: HTML page with assigned UUID

---

### GET /page

Alternative home route, same functionality as `/`.

---

### GET /test

Test route, assigns UUID to client and provides test interface.

---

### GET /auth

Auth route, records access logs.

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `uuid` | string | Yes | Client UUID |
| `data` | string | No | Custom data |

**Response** (JSON):
```json
{
    "status": "success",
    "message": "Log recorded",
    "uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "data": "xxx"
}
```

---

### GET /logs

Log viewing page, displays all auth route access records.

**Response**: HTML page with log list

---

## Configuration

### Port Configuration

| Mode | Port | Protocol |
|------|------|----------|
| HTTP | 5000 | http:// |
| HTTPS | 8443 | https:// |

### Log Storage

- Maximum 1000 log records
- Oldest logs are automatically deleted when limit is exceeded
- Logs include: timestamp, IP, User-Agent, UUID, Data

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SSL_CERT_FILE` | SSL certificate file path | `cert.pem` |
| `SSL_KEY_FILE` | SSL key file path | `key.pem` |

## Dependencies

- **Python**: 3.7+
- **Flask**: 3.0.0+
- **Werkzeug**: 3.0.1+

Install dependencies:
```bash
pip install Flask==3.0.0 Werkzeug==3.0.1
```
