# 🆓 Free Hosting Alternatives (Railway & Vercel Full)

## Best Options for ADFLOWAI

---

## Option 1: 🥇 Render.com (RECOMMENDED)
**Genuinely free, no credit card, easiest setup**

### Backend (Flask API):
1. Go to https://render.com → Sign up with GitHub
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub → Select **ADFLOWAI** repo
4. Settings:
   - **Name:** adflowai-api
   - **Runtime:** Docker
   - **Plan:** Free
5. Add environment variables:
   ```
   SECRET_KEY        = your-secret-key-here
   JWT_SECRET_KEY    = your-jwt-secret-here
   DATABASE_URL      = (copy from Render PostgreSQL below)
   REDIS_URL         = (copy from Render Redis below)
   ENVIRONMENT       = production
   ```
6. Click **"Create Web Service"**

### PostgreSQL Database (Free):
1. Click **"New +"** → **"PostgreSQL"**
2. Name: adflowai-db → Plan: **Free**
3. Copy the **Internal Database URL** → paste into DATABASE_URL above

### Redis (Free via Upstash):
1. Go to https://upstash.com → Sign up free
2. Create Redis database → Copy **REST URL**
3. Paste into REDIS_URL in Render

### Frontend (React):
1. Click **"New +"** → **"Static Site"**
2. Select ADFLOWAI repo
3. Settings:
   - **Root Directory:** frontend
   - **Build Command:** npm install && npm run build
   - **Publish Directory:** frontend/build
4. Add environment variable:
   ```
   REACT_APP_API_URL = https://adflowai-api.onrender.com
   ```

**Your URLs:**
- API: `https://adflowai-api.onrender.com`
- Frontend: `https://adflowai-frontend.onrender.com`

**⚠️ Free tier note:** Spins down after 15min inactivity, 
takes ~30sec to wake up. Fine for demos.

---

## Option 2: 🥈 Fly.io (Best Performance Free)
**$0 with generous free allowance, stays always on**

```powershell
# Install flyctl
# Windows: download from https://fly.io/docs/hands-on/install-flyctl/

# Login
flyctl auth login

# Go to your project folder
cd ADFLOWAI-VSCODE

# Deploy backend
flyctl launch --name adflowai-api
# Choose: Yes to Dockerfile, No to Postgres (add separately)

# Add Postgres
flyctl postgres create --name adflowai-db

# Attach database  
flyctl postgres attach adflowai-db

# Set secrets
flyctl secrets set SECRET_KEY=your-secret-key JWT_SECRET_KEY=your-jwt-secret

# Deploy
flyctl deploy
```

**Free allowance includes:**
- 3 shared VMs (enough for API + worker)
- 3GB storage
- 160GB outbound data/month
- PostgreSQL included

---

## Option 3: 🥉 Oracle Cloud Always Free
**Genuinely always free, no time limit, most powerful**

Best for production but takes 30 minutes to set up.

1. Go to https://oracle.com/cloud/free → Sign up (needs credit card but charges $0)
2. Create **VM.Standard.A1.Flex** instance (4 CPU, 24GB RAM - FREE!)
3. SSH in and run:

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Clone your repo
git clone https://github.com/Khan-Feroz211/ADFLOWAI.git
cd ADFLOWAI

# Create production .env
cat > .env << 'ENVEOF'
SECRET_KEY=generate-a-strong-random-key-here
JWT_SECRET_KEY=generate-another-strong-key-here
ENVIRONMENT=production
DEBUG=False
ENVEOF

# Start everything
docker-compose up -d

# Get your public IP from Oracle console
# Your app is live at http://YOUR_IP:5000
```

**Free forever: 4 CPU, 24GB RAM, 200GB storage**

---

## Option 4: GitHub Codespaces (Quick Demo)
**For quick demos only - free 60hrs/month**

1. Go to your GitHub repo
2. Click **"Code"** → **"Codespaces"** → **"Create codespace"**
3. In the terminal:
```bash
docker-compose up -d
```
4. Codespaces gives you a public URL automatically
5. Share that URL for demos

---

## Comparison Table

| Platform      | Free Tier     | Always On | Setup Time | Best For        |
|---------------|--------------|-----------|------------|-----------------|
| **Render**    | ✅ Yes        | ❌ No      | 10 min     | Quick demos     |
| **Fly.io**    | ✅ Yes        | ✅ Yes     | 20 min     | Real usage      |
| **Oracle**    | ✅ Forever    | ✅ Yes     | 30 min     | Production      |
| **Codespaces**| ⚠️ 60hr/mo   | ❌ No      | 5 min      | Quick show      |

---

## 🎯 My Recommendation

**Right now (demos/pitching):** Use **Render.com**
- Easiest, free, get a URL in 10 minutes
- Fine for showing investors - just open the app before the meeting

**When you get first customer:** Move to **Fly.io** or **Oracle Always Free**
- Always on, reliable, still free

**When you have 10+ customers:** Pay $6/mo DigitalOcean droplet
