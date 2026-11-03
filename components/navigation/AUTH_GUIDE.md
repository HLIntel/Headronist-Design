# Authentication boundary

Headronist supplies sign-in/sign-out UI patterns only, not an identity provider. Use a vetted server-side OIDC/OAuth integration with appropriate PKCE, secure HttpOnly cookies, CSRF protection, session expiration and revocation, and rate limiting. Never store credentials or access tokens in design manifests. Provide accessible loading, error, recovery, expiration and signed-out states. The host app must implement the real logout action.
