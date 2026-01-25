# Benkyo Backend

REST API server for the Benkyo Japanese Language Learning application.

## Tech Stack

- **Framework:** Flask 2.1
- **Database:** MongoDB Atlas
- **Authentication:** JWT (PyJWT)
- **Storage:** Google Cloud Storage
- **Password Hashing:** Argon2

## Setup Instructions

### Prerequisites

- Python 3.11+ (tested with Python 3.13)
- pip
- MongoDB Atlas account
- Google Cloud Storage credentials (for file uploads)

### Installation

1. **Clone and create virtual environment:**

   ```bash
   git clone <repository-url>
   cd benkyo-backend
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**

   Create a `.env` file in the root directory:

   ```env
   DB_USERNAME=your_mongodb_username
   DB_PASSWORD=your_mongodb_password
   DB_NAME=your_database_name
   TOKEN_PASS=your_jwt_secret_key
   PORT=5001
   ```

4. **Start the server:**

   ```bash
   python application.py
   ```

   The API will be available at `http://localhost:5001`

### Notes

- On macOS, port 5000 is used by AirPlay Receiver. Use port 5001 instead.
- Ensure MongoDB credentials are URL-encoded if they contain special characters.

## Project Structure

```
benkyo-backend/
├── application.py          # Flask app entry point & route definitions
├── jap_dev/
│   ├── formatters/         # Response data formatters
│   ├── helpers/            # Authentication, DB connection, utilities
│   ├── queries/            # Database query functions
│   ├── responses/          # API response builders
│   ├── schemas/            # Request validation schemas
│   └── views/              # Route handlers (controllers)
├── requirements.txt
└── wsgi.py                 # WSGI entry point for production
```

## API Reference

All endpoints (except `/login` and `/`) require a valid JWT token in the `Authorization` header.

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Returns `{"status": "ok"}` |

---

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/login` | Authenticate user and get JWT |
| GET | `/session` | Validate current session |
| GET | `/users` | Get user info |
| POST | `/users` | Create new user |

#### POST `/login`

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "id": "user_id",
  "username": "string",
  "type": "admin|regular",
  "jwt": "token_string",
  "exp": 1234567890
}
```

---

### Words (Vocabulary)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/words` | List words with pagination & filtering |
| POST | `/words` | Create a new word |
| PUT | `/words` | Update a word |
| DELETE | `/words` | Delete a word |
| GET | `/words/search` | Search for a specific word |
| POST | `/words/<word_id>/related` | Add a related word relationship |
| DELETE | `/words/<word_id>/related/<related_word_id>` | Remove a relationship |
| GET | `/words/csv` | Export words as CSV |
| GET | `/words/csv/jlpt` | Export JLPT words as CSV |

#### GET `/words`

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `group` | string | Filter by collection (e.g., `jlpt_n3`) |
| `filter_by` | string | Search term |
| `page_size` | integer | Results per page |
| `page_number` | integer | Page number |
| `order_field` | string | Field to sort by |
| `order_direction` | string | `asc` or `desc` |

#### GET `/words/search`

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `word` | string | Search by word text |
| `word_id` | string | Search by word ID |
| `group` | string | Get random word from collection |

#### POST `/words/<word_id>/related`

**Request Body:**
```json
{
  "relatedWordId": "string",
  "type": "related|synonym|antonym",
  "tags": ["formal", "casual", "spoken", "written"],
  "note": "optional note"
}
```

Creates a bidirectional relationship between two words.

---

### Kanji

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/kanjis` | List kanji with pagination |
| POST | `/kanjis` | Create a new kanji |
| PUT | `/kanjis` | Update a kanji |
| GET | `/kanjis/search` | Search for a specific kanji |
| GET | `/kanjis/exists` | Check if kanji exists |
| GET | `/kanjis/csv` | Export kanji as CSV |
| GET | `/kanjis/components` | Get kanji components |
| GET | `/kanjis/components/irregular` | Get irregular components |
| POST | `/kanjis/components/irregular` | Add irregular component |
| GET | `/kanjis/radicals` | Get kanji radicals |

---

### Collections

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/collections` | List all collections |
| POST | `/collections` | Create a new collection |
| GET | `/collections/search` | Search for a collection |

---

### Grammar (Clauses)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/clauses` | List grammar clauses |
| POST | `/clauses` | Create a new clause |
| PUT | `/clauses` | Update a clause |
| DELETE | `/clauses` | Delete a clause |
| GET | `/clauses/search` | Search for a clause |

---

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message description"
}
```

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Missing or invalid JWT |
| 404 | Not Found - Resource doesn't exist |

## Development

### Running with Docker

```bash
docker build -t benkyo-backend .
docker run -p 5001:5001 --env-file .env benkyo-backend
```

### Database Snapshots

Database snapshots are stored in `/snapshots/` for backup purposes.

### Scripts

Utility scripts are in `/scripts/` (gitignored) for data migrations and analysis.
