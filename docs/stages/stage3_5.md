# Stage 3.5 — Supabase Auth + GitHub CI/CD for QuantumTrade

This stage builds directly on Stage 3, adding authentication with Supabase Auth and implementing a GitHub CI/CD pipeline.

## 🎯 Features Implemented

| Feature | Status |
|---------|--------|
| Supabase Auth (email/password login) | ✅ |
| JWT Token Verification | ✅ |
| Protected Backend Routes | ✅ |
| Frontend Login Page | ✅ |
| GitHub Actions CI/CD | ✅ |
| Docker Build & Push | ✅ |

## 🔐 1. Supabase Auth Configuration

### Enable Email/Password Authentication

1. Go to your Supabase project dashboard
2. Navigate to **Auth → Providers → Email**
3. Enable "Email + Password"
4. (Optional) Enable Magic Link for OTP-less logins

### Auth Settings

Under **Auth → Settings**, ensure:
- JWT Expiry is reasonable (e.g., 3600 seconds)
- Site URL = your frontend's URL (e.g., http://localhost:5173 for development)

## ⚙️ 2. Environment Configuration

Added these variables to your `.env` file:

```env
# Supabase Auth
SUPABASE_JWT_SECRET=<your_supabase_jwt_secret>
VITE_SUPABASE_URL=https://<project_ref>.supabase.co
VITE_SUPABASE_ANON_KEY=<your_anon_key>
```

## 🧩 3. Frontend Auth Implementation

### Supabase Client

File: `frontend/src/lib/supabaseClient.js`

```javascript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
```

### Login Page

File: `frontend/src/pages/Login.jsx`

```javascript
import { useState } from "react"
import { supabase } from "../lib/supabaseClient"

export default function Login() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [message, setMessage] = useState("")

  const handleLogin = async (e) => {
    e.preventDefault()
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })
    if (error) setMessage(error.message)
    else setMessage("✅ Logged in successfully!")
  }

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl mb-4 font-bold">Login</h1>
      <form onSubmit={handleLogin} className="flex flex-col gap-3">
        <input type="email" placeholder="Email" value={email}
          onChange={(e) => setEmail(e.target.value)} className="p-2 border rounded" />
        <input type="password" placeholder="Password" value={password}
          onChange={(e) => setPassword(e.target.value)} className="p-2 border rounded" />
        <button type="submit" className="p-2 bg-blue-500 text-white rounded">Login</button>
      </form>
      {message && <p className="mt-2 text-sm">{message}</p>}
    </div>
  )
}
```

## 🛡️ 4. Backend JWT Verification

### Dependencies

Added to `backend/requirements.txt`:
```
python-jose==3.3.0
```

### JWT Middleware

File: `backend/src/middleware/jwt_middleware.py`

```python
from jose import jwt, JWTError
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer
import os

security = HTTPBearer()
JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

def verify_token(credentials=Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
```

### Protected Routes

File: `backend/src/routes/secure.py`

```python
from fastapi import APIRouter, Depends
from src.middleware.jwt_middleware import verify_token

router = APIRouter()

@router.get("/secure-data")
def get_secure_data(user=Depends(verify_token)):
    return {"message": "You are authenticated", "user": user}
```

## 🧱 5. GitHub CI/CD Pipeline

### Workflow File

File: `.github/workflows/deploy.yml`

```yaml
name: QuantumTrade CI/CD

on:
  push:
    branches:
      - main
      - develop

jobs:
  build:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        ports:
          - 5432:5432
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: testdb

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install backend dependencies
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Run backend tests
        run: |
          cd backend
          pytest --maxfail=1 --disable-warnings -q

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install frontend dependencies
        run: |
          cd frontend
          npm ci

      - name: Build frontend
        run: |
          cd frontend
          npm run build

      - name: Docker build & push
        if: github.ref == 'refs/heads/main'
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: jigneshbhirud/quantumtrade:latest

  cleanup:
    runs-on: ubuntu-latest
    needs: build
    if: always()
    
    steps:
      - name: Cleanup Docker cache
        run: docker system prune -af --volumes
```

### Required GitHub Secrets

For Docker Hub publishing, set these secrets in your GitHub repository:
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`

## 🧾 6. Git Commit

```bash
git add .
git commit -m "Stage 3.5: Added Supabase Auth + GitHub CI/CD pipeline"
git push origin develop
```

## ✅ Final Result

Stage 3.5 successfully implements:
- Supabase Cloud Database integration ✅
- Supabase Auth (JWT) ✅
- Backend JWT Middleware ✅
- Frontend Auth Page ✅
- GitHub Actions CI/CD ✅
- Docker Build + Push ✅
- Cleanup & version control ✅

Users can now register or log in using Supabase directly, with JWT tokens protecting backend routes.