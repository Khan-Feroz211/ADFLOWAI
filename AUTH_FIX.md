# Authentication Fix - Quick Start Guide

## Issues Fixed:
1. ✅ Database URL corrected to use SQLite (was trying PostgreSQL)
2. ✅ Database session management improved
3. ✅ Accounts now properly stored and persisted

## How to Test:

### 1. Start the server:
```bash
python app.py
```

### 2. Test Registration (in another terminal):
```bash
curl -X POST http://localhost:5000/api/v1/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"john\",\"email\":\"john@example.com\",\"password\":\"Test1234\",\"full_name\":\"John Doe\"}"
```

### 3. Test Login:
```bash
curl -X POST http://localhost:5000/api/v1/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"john\",\"password\":\"Test1234\"}"
```

### 4. Or use the test script:
```bash
python test_auth.py
```

## Password Requirements:
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter  
- At least 1 number

## Database Location:
All accounts are stored in: `adflowai_dev.db`

## What Was Wrong:
The `.env` file had `DATABASE_URL=postgresql://...` but PostgreSQL wasn't running. 
The app was trying to connect to a non-existent database, causing registration/login to fail.

Now it uses SQLite which works out of the box!
