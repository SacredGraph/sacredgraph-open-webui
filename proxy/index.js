const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const { jwtVerify, createRemoteJWKSet } = require('jose');
const cookieParser = require('cookie-parser');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

// Use cookie parser middleware
app.use(cookieParser());

// Outseta configuration
const OUTSETA_DOMAIN = process.env.OUTSETA_DOMAIN;
const JWKS_URL = `https://${OUTSETA_DOMAIN}/.well-known/jwks`;

// Middleware to verify JWT and inject headers
app.use(async (req, res, next) => {
	if (req.query.access_token) {
		res.cookie('Outseta.nocode.accessToken', req.query.access_token);
		res.redirect(process.env.FRONTEND_URL || 'http://localhost:5173/');
		return;
	}

	try {
		const token = req.cookies['Outseta.nocode.accessToken'];

		console.log('token', token);

		if (token) {
			const JWKS = createRemoteJWKSet(new URL(JWKS_URL));
			const { payload } = await jwtVerify(token, JWKS);

			console.log('payload', payload);

			req.headers['X-User-Id'] = payload['outseta:accountUid'];
			req.headers['X-User-Email'] = payload.email;
			req.headers['X-User-Name'] = payload.name.trim() || payload.email;

			console.log('headers', req.headers);
		}
	} catch (error) {
		console.error('JWT verification failed:', error);
	}

	next();
});

const target = process.env.TARGET || 'http://localhost:8081';

// Proxy configuration
const proxyOptions = {
	target,
	changeOrigin: true,
	ws: true, // Enable WebSocket support
	logLevel: 'debug'
};

app.use('/', createProxyMiddleware(proxyOptions));

// Start the server
app.listen(port, () => {
	console.log(`Proxy server running on http://localhost:${port}`);
	console.log(`Proxying requests to ${target}`);
});
