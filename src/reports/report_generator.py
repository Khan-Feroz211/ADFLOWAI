"""
ADFLOWAI - Report Generator
Generates PDF and Excel/CSV reports for campaigns
Uses only packages already in requirements.txt (no extra deps needed for CSV/HTML)
"""
import csv
import json
import io
import logging
from datetime import datetime
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Generates campaign reports in multiple formats:
    - CSV   (built-in, no deps)
    - JSON  (built-in, no deps)
    - HTML  (built-in, renders nicely, printable as PDF from browser)
    
    For real PDF/Excel install: pip install reportlab openpyxl
    """

    def generate_csv(self, campaigns: List[Dict], user_info: Dict) -> bytes:
        """Generate CSV report - works with Excel when opened"""
        output = io.StringIO()
        writer = csv.writer(output)

        # Header block
        writer.writerow(['ADFLOWAI Campaign Report'])
        writer.writerow([f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"])
        writer.writerow([f"Account: {user_info.get('username', 'N/A')}"])
        writer.writerow([f"Company: {user_info.get('company', 'N/A')}"])
        writer.writerow([])

        # Summary row
        total_budget = sum(c.get('total_budget', 0) for c in campaigns)
        total_spent  = sum(c.get('spent_budget', 0) for c in campaigns)
        total_impr   = sum(c.get('impressions', 0) for c in campaigns)
        total_clicks = sum(c.get('clicks', 0) for c in campaigns)
        total_conv   = sum(c.get('conversions', 0) for c in campaigns)

        writer.writerow(['SUMMARY'])
        writer.writerow(['Total Campaigns', len(campaigns)])
        writer.writerow(['Total Budget', f"${total_budget:,.2f}"])
        writer.writerow(['Total Spent',  f"${total_spent:,.2f}"])
        writer.writerow(['Total Impressions', f"{total_impr:,}"])
        writer.writerow(['Total Clicks',      f"{total_clicks:,}"])
        writer.writerow(['Total Conversions', f"{total_conv:,}"])
        writer.writerow(['Avg CTR', f"{(total_clicks/total_impr*100):.2f}%" if total_impr else '0%'])
        writer.writerow([])

        # Campaign detail header
        writer.writerow(['CAMPAIGN DETAILS'])
        writer.writerow([
            'ID', 'Name', 'Status', 'Objective',
            'Total Budget ($)', 'Spent ($)', 'Remaining ($)', 'Budget Used %',
            'Impressions', 'Clicks', 'Conversions',
            'CTR (%)', 'CPC ($)', 'CPA ($)', 'ROAS',
            'AI Score (%)', 'Start Date', 'Created At'
        ])

        for c in campaigns:
            budget   = c.get('total_budget', 0) or 0
            spent    = c.get('spent_budget', 0) or 0
            metrics  = c.get('metrics', {}) or {}
            impr     = metrics.get('impressions', c.get('impressions', 0)) or 0
            clicks   = metrics.get('clicks', c.get('clicks', 0)) or 0
            conv     = metrics.get('conversions', c.get('conversions', 0)) or 0

            writer.writerow([
                c.get('id', ''),
                c.get('name', ''),
                c.get('status', ''),
                c.get('objective', ''),
                f"{budget:.2f}",
                f"{spent:.2f}",
                f"{max(0, budget-spent):.2f}",
                f"{(spent/budget*100):.1f}%" if budget else '0%',
                impr, clicks, conv,
                f"{metrics.get('ctr', 0)*100:.2f}" if metrics.get('ctr') else '0',
                f"{metrics.get('cpc', 0):.2f}" if metrics.get('cpc') else '0',
                f"{metrics.get('cpa', 0):.2f}" if metrics.get('cpa') else '0',
                f"{metrics.get('roas', 0):.2f}" if metrics.get('roas') else '0',
                f"{(c.get('performance_score', 0)*100):.0f}",
                c.get('start_date', '')[:10] if c.get('start_date') else '',
                c.get('created_at', '')[:10] if c.get('created_at') else '',
            ])

        return output.getvalue().encode('utf-8-sig')  # utf-8-sig = Excel-compatible BOM

    def generate_json(self, campaigns: List[Dict], user_info: Dict) -> bytes:
        """Generate structured JSON report"""
        total_budget = sum(c.get('total_budget', 0) for c in campaigns)
        total_spent  = sum(c.get('spent_budget', 0) for c in campaigns)
        total_impr   = sum(c.get('impressions', 0) for c in campaigns)
        total_clicks = sum(c.get('clicks', 0) for c in campaigns)
        total_conv   = sum(c.get('conversions', 0) for c in campaigns)

        report = {
            'report_metadata': {
                'generated_at': datetime.utcnow().isoformat(),
                'generated_by': user_info.get('username'),
                'company': user_info.get('company'),
                'period': 'All time',
            },
            'summary': {
                'total_campaigns': len(campaigns),
                'total_budget': total_budget,
                'total_spent': total_spent,
                'budget_remaining': total_budget - total_spent,
                'total_impressions': total_impr,
                'total_clicks': total_clicks,
                'total_conversions': total_conv,
                'avg_ctr_pct': round(total_clicks/total_impr*100, 2) if total_impr else 0,
                'avg_performance_score': round(sum(c.get('performance_score',0) for c in campaigns)/len(campaigns), 3) if campaigns else 0,
            },
            'campaigns': campaigns,
        }
        return json.dumps(report, indent=2, default=str).encode('utf-8')

    def generate_html(self, campaigns: List[Dict], user_info: Dict) -> bytes:
        """
        Generate a beautiful printable HTML report.
        Users can open this in a browser and Ctrl+P → Save as PDF.
        """
        now = datetime.utcnow().strftime('%B %d, %Y at %H:%M UTC')
        total_budget = sum(c.get('total_budget', 0) for c in campaigns)
        total_spent  = sum(c.get('spent_budget', 0) for c in campaigns)
        total_conv   = sum(c.get('conversions', 0) for c in campaigns)
        total_impr   = sum(c.get('impressions', 0) for c in campaigns)
        total_clicks = sum(c.get('clicks', 0) for c in campaigns)
        avg_score    = sum(c.get('performance_score', 0) for c in campaigns)/len(campaigns) if campaigns else 0

        score_color = lambda s: '#00e88f' if s>=0.7 else '#ffd166' if s>=0.4 else '#ff4560'
        status_color = {'active':'#00e88f','paused':'#ffd166','stopped':'#ff4560','draft':'#8b97a8','completed':'#00d4ff'}

        rows = ''
        for c in campaigns:
            s = c.get('performance_score', 0)
            sc = score_color(s)
            stc = status_color.get(c.get('status',''), '#8b97a8')
            rows += f"""
            <tr>
              <td><strong>{c.get('name','')}</strong></td>
              <td><span style="background:{stc}22;color:{stc};padding:2px 10px;border-radius:20px;font-size:11px">{c.get('status','')}</span></td>
              <td>${c.get('total_budget',0):,.0f}</td>
              <td>${c.get('spent_budget',0):,.0f}</td>
              <td>{c.get('impressions',0):,}</td>
              <td>{c.get('clicks',0):,}</td>
              <td>{c.get('conversions',0):,}</td>
              <td style="color:{sc};font-weight:700">{s*100:.0f}%</td>
            </tr>"""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ADFLOWAI Campaign Report</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;600&family=Syne:wght@700;800&family=DM+Mono&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'DM Sans', sans-serif; background: #f8fafc; color: #1a202c; padding: 40px; }}
  .header {{ background: #080b12; color: white; padding: 32px 40px; border-radius: 16px; margin-bottom: 32px; display: flex; justify-content: space-between; align-items: center; }}
  .logo {{ font-family: 'Syne', sans-serif; font-size: 28px; font-weight: 800; color: #00d4ff; }}
  .meta {{ text-align: right; font-size: 13px; color: #8b97a8; line-height: 1.8; font-family: 'DM Mono', monospace; }}
  .stats {{ display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-bottom: 32px; }}
  .stat {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; }}
  .stat-label {{ font-size: 11px; color: #8b97a8; text-transform: uppercase; letter-spacing: 1.5px; font-family: 'DM Mono', monospace; margin-bottom: 6px; }}
  .stat-value {{ font-family: 'Syne', sans-serif; font-size: 24px; font-weight: 800; color: #080b12; }}
  .stat-sub {{ font-size: 12px; color: #8b97a8; margin-top: 4px; }}
  .section {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; margin-bottom: 24px; }}
  .section-title {{ padding: 16px 24px; border-bottom: 1px solid #e2e8f0; font-size: 11px; font-family: 'DM Mono', monospace; color: #8b97a8; text-transform: uppercase; letter-spacing: 2px; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th {{ padding: 10px 16px; text-align: left; font-size: 11px; font-family: 'DM Mono', monospace; color: #8b97a8; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #e2e8f0; font-weight: 500; }}
  td {{ padding: 12px 16px; font-size: 13px; border-bottom: 1px solid #f1f5f9; }}
  tr:last-child td {{ border-bottom: none; }}
  .footer {{ text-align: center; color: #8b97a8; font-size: 12px; font-family: 'DM Mono', monospace; margin-top: 32px; }}
  @media print {{ body {{ padding: 20px; background: white; }} }}
</style>
</head>
<body>
  <div class="header">
    <div>
      <div class="logo">ADFLOW<span style="color:#8b97a8">AI</span></div>
      <div style="color:#8b97a8;font-size:12px;font-family:'DM Mono',monospace;margin-top:4px;letter-spacing:2px">CAMPAIGN PERFORMANCE REPORT</div>
    </div>
    <div class="meta">
      <div>{user_info.get('company') or user_info.get('username','')}</div>
      <div>{now}</div>
      <div>{len(campaigns)} campaigns</div>
    </div>
  </div>

  <div class="stats">
    <div class="stat"><div class="stat-label">Total Budget</div><div class="stat-value">${total_budget:,.0f}</div><div class="stat-sub">Allocated</div></div>
    <div class="stat"><div class="stat-label">Total Spent</div><div class="stat-value">${total_spent:,.0f}</div><div class="stat-sub">{total_spent/total_budget*100:.0f}% utilized</div></div>
    <div class="stat"><div class="stat-label">Conversions</div><div class="stat-value">{total_conv:,}</div><div class="stat-sub">Total</div></div>
    <div class="stat"><div class="stat-label">Avg AI Score</div><div class="stat-value">{avg_score*100:.0f}%</div><div class="stat-sub">Performance</div></div>
  </div>

  <div class="section">
    <div class="section-title">Campaign Details</div>
    <table>
      <thead>
        <tr>
          <th>Campaign</th><th>Status</th><th>Budget</th><th>Spent</th>
          <th>Impressions</th><th>Clicks</th><th>Conversions</th><th>AI Score</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
  </div>

  <div class="footer">
    Generated by ADFLOWAI &nbsp;·&nbsp; AI-Powered Campaign Optimization &nbsp;·&nbsp; {now}
  </div>
</body>
</html>"""
        return html.encode('utf-8')
