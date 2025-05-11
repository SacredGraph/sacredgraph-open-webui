# OpenWebUI Outseta Proxy

This proxy server verifies Outseta JWT tokens and injects trusted headers for OpenWebUI authentication.

## Setup

1. Install dependencies:

```bash
npm install
```

2. Create a `.env` file in the project root with the following variables:

```
PORT=3000
OUTSETA_DOMAIN=your-domain.outseta.com
```

Replace `your-domain.outseta.com` with your actual Outseta domain.

## Usage

1. Start the proxy server:

```bash
npm start
```

2. The proxy will run on `http://localhost:3000` and forward requests to OpenWebUI running on `http://localhost:5173`.

3. When a request comes in:
   - The proxy checks for an Outseta JWT token in the `token` cookie
   - If the token is valid, it extracts the user's email and name
   - These are injected as `x-user-email` and `x-user-name` headers
   - The request is forwarded to OpenWebUI
   - If the token is invalid or missing, the user is redirected to `http://localhost:5173/auth`

## Development

To run in development mode with auto-reload:

```bash
npm run dev
```

## Configuration

The proxy can be configured through environment variables:

- `PORT`: The port the proxy server will listen on (default: 3000)
- `OUTSETA_DOMAIN`: Your Outseta domain (required)

## Cookie Requirements

The proxy expects the Outseta JWT token to be present in a cookie named `token`. This cookie should be set by your Outseta authentication flow.
