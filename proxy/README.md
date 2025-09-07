# Python Proxy Server

This is a Python implementation of the proxy server that handles authentication and request forwarding. It's built using FastAPI and provides the same functionality as the Node.js version.

## Features

- JWT token verification using Outseta
- Request forwarding with header injection
- Cookie-based authentication
- Health check endpoint
- CORS support
- Environment variable configuration

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
PROXY_PORT=3000
OUTSETA_DOMAIN=your-outseta-domain
PROXY_FRONTEND_URL=http://localhost:5173
PROXY_TARGET=http://localhost:8081
```

## Running the Server

To start the server:

```bash
python main.py
```

The server will start on the configured port (default: 3000).

## API Endpoints

- `GET /health` - Health check endpoint
- `GET /` - Main proxy endpoint that handles authentication and request forwarding

## Development

The server uses FastAPI, which provides automatic API documentation. Once the server is running, you can access:

- Swagger UI: `http://localhost:3000/docs`
- ReDoc: `http://localhost:3000/redoc`
