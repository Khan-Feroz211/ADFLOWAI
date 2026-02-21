# 📊 ADFLOWAI - Export & Reports Guide

## ✅ Export Feature Status
**Working!** All export formats are functional.

---

## 📥 Available Export Formats

### 1. CSV (Excel Compatible)
```bash
GET /api/v1/reports/campaigns?format=csv
```
- Opens directly in Excel
- Contains summary + detailed campaign data
- UTF-8 with BOM for Excel compatibility

### 2. JSON (Structured Data)
```bash
GET /api/v1/reports/campaigns?format=json
```
- Machine-readable format
- Perfect for integrations
- Includes metadata + summary + campaigns

### 3. HTML (Printable Report)
```bash
GET /api/v1/reports/campaigns?format=html
```
- Beautiful formatted report
- Open in browser → Print → Save as PDF
- Professional design with charts

---

## 🔐 How to Export (With Authentication)

### From Frontend (Automatic)
1. Login to dashboard
2. Go to "Reports" section
3. Click "Export CSV" or "Export Report"
4. File downloads automatically

### From API (Manual)
```bash
# 1. Login first to get token
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"your_username","password":"your_password"}'

# 2. Copy the access_token from response

# 3. Export CSV
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "http://localhost:5000/api/v1/reports/campaigns?format=csv" \
  -o my_report.csv

# 4. Export HTML
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "http://localhost:5000/api/v1/reports/campaigns?format=html" \
  -o my_report.html

# 5. Export JSON
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "http://localhost:5000/api/v1/reports/campaigns?format=json" \
  -o my_report.json
```

---

## 📋 Report Contents

### Summary Section
- Total campaigns count
- Total budget allocated
- Total spent
- Total impressions, clicks, conversions
- Average CTR
- Average AI performance score

### Campaign Details
- Campaign ID & Name
- Status (active, paused, stopped)
- Budget breakdown
- Performance metrics (CTR, CPC, CPA, ROAS)
- AI optimization score
- Dates (start, created)

---

## 🎨 Frontend Integration

Add export buttons to your React components:

```javascript
import { campaignAPI } from '../services/api';

const ExportButton = () => {
  const handleExport = async (format) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(
        `http://localhost:5000/api/v1/reports/campaigns?format=${format}`,
        {
          headers: { 'Authorization': `Bearer ${token}` }
        }
      );
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `adflowai_report_${Date.now()}.${format}`;
      a.click();
    } catch (error) {
      console.error('Export failed:', error);
    }
  };

  return (
    <div>
      <button onClick={() => handleExport('csv')}>Export CSV</button>
      <button onClick={() => handleExport('html')}>Export Report</button>
      <button onClick={() => handleExport('json')}>Export JSON</button>
    </div>
  );
};
```

---

## 🐛 Common Issues & Fixes

### Issue: "401 Unauthorized"
**Fix**: Token expired, login again to get new token

### Issue: "Empty report"
**Fix**: Create some campaigns first, then export

### Issue: "CSV not opening in Excel"
**Fix**: File is UTF-8 with BOM, should work. Try "Open With" → Excel

### Issue: "Download not starting"
**Fix**: Check browser popup blocker settings

---

## 📊 Sample Report Output

### CSV Format:
```csv
ADFLOWAI Campaign Report
Generated: 2026-02-21 12:00 UTC
Account: demo_user
Company: Demo Corp

SUMMARY
Total Campaigns,5
Total Budget,$50,000.00
Total Spent,$32,450.00
Total Impressions,1,250,000
Total Clicks,45,000
Total Conversions,1,200
Avg CTR,3.60%

CAMPAIGN DETAILS
ID,Name,Status,Objective,Total Budget ($)...
1,Summer Sale,active,conversions,10000.00...
```

### HTML Format:
Beautiful formatted report with:
- Company header
- Summary cards with metrics
- Detailed campaign table
- Color-coded status badges
- AI performance scores
- Print-ready layout

---

## ✅ Testing Checklist

- [x] CSV export works
- [x] JSON export works  
- [x] HTML export works
- [x] Authentication required
- [x] UTF-8 encoding correct
- [x] Excel compatibility verified
- [x] Empty state handled
- [x] File naming with timestamp

**All export features are working!** 🎉
