# CHANGES.md

## Task: URL Shortener Service

This project was built from the ground up to deliver a fast, minimal, and fully functional URL shortener API, while staying within the scope and constraints of the assignment. I focused on clarity, reliability, and clean execution across all components.

---

## Key Problems Identified and Tackled

- No implementation existed for the required functionality
- No storage mechanism to manage URLs or track analytics
- No validation or safety checks around input
- No test coverage for critical API behaviors

---

## What I Built and Why

### Health Endpoints
Retained and preserved the `/` and `/api/health` routes to offer meaningful health check status. These are essential for service monitoring and debugging.

### URL Shortening (`POST /api/shorten`)
- Built an endpoint to receive and validate a long URL
- Generated collision-free short codes using randomness and retries
- Kept storage in-memory for simplicity and to align with assignment scope
- Designed the response structure to mirror real-world APIs like Bitly

### Redirection (`GET /<short_code>`)
- Implemented a direct redirect to the original URL
- Included click tracking per short code
- Added 404 handling for unknown codes

### Stats (`GET /api/stats/<short_code>`)
- Exposed metadata such as original URL, click count, and creation timestamp
- Formatted timestamps in ISO format for clean API usage
- Ensured thread-safe access using a global lock

### Architecture and Code Practices
- Organized all storage logic in `storage.py` for separation of concerns
- Encapsulated route logic cleanly in `main.py`
- Maintained clarity in function naming, route design, and flow control
- Respected the limits of the assignment by avoiding overengineering

---

## Trade-offs and Assumptions

- Used only in-memory storage for URL mappings, as specified
- Short codes are always 6 characters long for consistency and simplicity
- Did not include rate-limiting, logging, or persistent storage by design
- Considered test coverage more important than adding advanced features

---

## With More Time, I Would:

- Integrate Redis or SQLite for persistent storage
- Build expiration logic for short URLs
- Add authentication to allow users to manage their links
- Track user-agent data or referral source for each redirect
- Improve test coverage and add integration testing
- Deploy this to a cloud platform with a custom domain

---

## AI Usage Disclosure

I used ChatGPT to:
- Brainstorm initial structure and routing flow
- Speed up boilerplate generation
- Review edge cases and code clarity

Every piece of logic was reviewed, customized, and tested manually. The final result reflects my decisions and understanding of the problem, not just generated code.
