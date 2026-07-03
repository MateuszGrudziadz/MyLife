# MyLife

MyLife is a full-stack web application designed to manage different areas of everyday life in one place.

The application currently includes personal finance management, reminders, a journal and well-being tracking. The dashboard combines data from different modules and presents statistics and summaries for the logged-in user.

## Technologies

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- JWT authentication

### Frontend
- React
- Vite
- Tailwind CSS
- Axios
- Recharts

## Main features

- user registration and login
- JWT authentication
- user-specific data
- personal finance management
- income and expense categories
- transaction history and statistics
- reminders
- journal and well-being tracking
- sleep, energy, mood and productivity statistics
- journal tags with a many-to-many database relationship
- dashboard combining data from multiple modules

## How to run the project

### 1. Clone the repository

```bash
git clone https://github.com/MateuszGrudziadz/MyLife.git
cd MyLife
```

### 2. Create the PostgreSQL database

Create a PostgreSQL database named:

```text
mylife_auth
```

### 3. Configure the backend

Go to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example` and configure your PostgreSQL connection:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/mylife
SECRET_KEY=YOUR_SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Start the backend:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 4. Start the frontend

Open a second terminal and go to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the application:

```bash
npm run dev
```

Open the address displayed by Vite, usually:

```text
http://localhost:5173
```

## Author

Mateusz Grudziądz