# 🎯 ADFLOWAI - Quick Reference

## 🚀 Start Everything
```bash
docker-compose up -d
```

## 🌐 Access URLs
- **Frontend**: http://localhost:3000
- **API**: http://localhost:5000
- **Health**: http://localhost:5000/health

## 🧪 Test Auth
```bash
# Register
curl -X POST http://localhost:5000/api/v1/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"test\",\"email\":\"test@test.com\",\"password\":\"Test1234\"}"

# Login
curl -X POST http://localhost:5000/api/v1/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"test\",\"password\":\"Test1234\"}"
```

## 📊 Check Status
```bash
docker-compose ps
docker-compose logs -f api
```

## 🛑 Stop Everything
```bash
docker-compose down
```

## 🔄 Rebuild
```bash
docker-compose up -d --build
```

## ✅ All Fixed
- ✅ Auth database config (SQLite → PostgreSQL in Docker)
- ✅ Accounts persist properly
- ✅ Docker deployment working
- ✅ Pushed to GitHub

**Repository**: https://github.com/Khan-Feroz211/ADFLOWAI.git
