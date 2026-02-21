# 🎯 ADFLOWAI - Demo Startup Guide

## 🚀 Quick Start (30 seconds)

### 1. Start Everything
```bash
cd ADFLOWAI-VSCODE
docker-compose up -d
```

### 2. Wait 30 seconds for services to start

### 3. Open Browser
```
http://localhost:3000
```

---

## 📋 Pre-Demo Checklist

### Before the Demo:
```bash
# 1. Pull latest code
git pull origin main

# 2. Start services
docker-compose up -d

# 3. Check all services are healthy
docker-compose ps

# 4. Verify API
curl http://localhost:5000/health

# 5. Open frontend
start http://localhost:3000
```

### Expected Output:
```
✅ adflowai_api        - Up (healthy)
✅ adflowai_frontend   - Up
✅ adflowai_postgres   - Up (healthy)
✅ adflowai_redis      - Up (healthy)
```

---

## 🎬 Demo Flow

### Step 1: Register Account (30 sec)
1. Go to http://localhost:3000
2. Click "Register"
3. Fill form:
   - Username: `demo_user`
   - Email: `demo@adflowai.com`
   - Password: `Demo1234`
4. Click "Register"

### Step 2: Create Campaign (1 min)
1. Click "New Campaign"
2. Fill details:
   - Name: "Summer Sale 2026"
   - Budget: $10,000
   - Platforms: Google Ads, Facebook, Instagram
   - Duration: 30 days
3. Click "Create Campaign"

### Step 3: Show Dashboard (30 sec)
1. Go to Dashboard
2. Show real-time metrics
3. Show AI optimization scores
4. Show platform comparison

### Step 4: Show AI Features (1 min)
1. Click on campaign
2. Show "AI Recommendations"
3. Click "Optimize Budget"
4. Show automatic reallocation

---

## 🛑 Stop After Demo

```bash
docker-compose down
```

---

## 🔧 Troubleshooting

### Frontend not loading?
```bash
docker-compose restart frontend
# Wait 30 seconds
```

### API not responding?
```bash
docker-compose logs api
docker-compose restart api
```

### Reset everything?
```bash
docker-compose down -v
docker-compose up -d --build
```

---

## 💡 Demo Tips

1. **Pre-create account** before demo to save time
2. **Have sample data** ready to show
3. **Keep terminal open** to show logs if needed
4. **Test 5 minutes before** the actual demo
5. **Have backup slides** in case of issues

---

## 📊 Key Features to Highlight

✅ Multi-platform campaign management  
✅ Real-time performance tracking  
✅ AI-powered budget optimization  
✅ Automatic campaign pause/resume  
✅ Cross-platform analytics  
✅ ROI predictions  

---

## 🎯 One-Liner Demo Start

```bash
cd ADFLOWAI-VSCODE && docker-compose up -d && timeout /t 30 && start http://localhost:3000
```

**That's it! You're ready to demo! 🚀**
