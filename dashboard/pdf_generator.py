from weasyprint import HTML
import datetime

def generate_cpv_report(cpv_data):
    """Generates a PDF report byte string from the current CPV data."""
    
    # 1. Business Logic
    cpv_5 = next((item for item in cpv_data if item["title"] == "CPV Value 5"), {"title": "CPV Value 5", "value": "N/A"})
    cheapest_cpv = min(cpv_data, key=lambda x: x["value"])

    # 2. HTML/CSS Template
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @page {{
                size: A4; margin: 20mm; background-color: #ffffff;
                @bottom-right {{
                    content: "Page " counter(page) " of " counter(pages);
                    font-family: sans-serif; font-size: 9pt; color: #94a3b8;
                }}
            }}
            body {{ font-family: sans-serif; color: #1e293b; line-height: 1.6; font-size: 11pt; }}
            .header {{
                background-color: #0f172a; color: #f8fafc; padding: 25px 20px;
                margin: -20mm -20mm 30px -20mm; border-bottom: 5px solid #3b82f6;
            }}
            .header h1 {{ margin: 0 0 5px 0; font-size: 24pt; }}
            .section-title {{ border-bottom: 2px solid #e2e8f0; color: #0f172a; font-size: 16pt; margin-top: 35px; page-break-after: avoid; }}
            .context-box {{ background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; border-radius: 6px; margin-bottom: 20px; }}
            .recommendation-box {{ background-color: #ecfdf5; border-left: 6px solid #10b981; padding: 20px; margin: 25px 0; page-break-inside: avoid; }}
            .recommendation-box h3 {{ color: #064e3b; margin-top: 0; }}
            .metric-highlight {{ font-size: 22pt; font-weight: bold; color: #10b981; display: block; margin: 10px 0; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 12px; border-bottom: 1px solid #e2e8f0; text-align: left; }}
            th {{ background-color: #f1f5f9; text-transform: uppercase; font-size: 10pt; }}
            .val-good {{ color: #10b981; font-weight: bold; }}
            .val-warn {{ color: #f59e0b; font-weight: bold; }}
            .val-bad {{ color: #ef4444; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Strategic Expansion Report</h1>
            <p>Acme Corporation | Generated: {datetime.date.today().strftime('%B %d, %Y')}</p>
        </div>

        <div class="context-box">
            <strong>Executive Summary:</strong> Following the successful initial investment via <strong>CPV Value 5</strong>, the objective is to strategically expand audience reach while minimizing acquisition costs.
        </div>

        <h2 class="section-title">Current State Analysis</h2>
        <p><strong>CPV Value 5</strong> is currently operating at a cost-per-value metric of <strong>{cpv_5['value']}</strong>. To maximize ROI on the upcoming expansion budget, we must pivot towards under-utilized, high-efficiency channels.</p>

        <div class="recommendation-box">
            <h3>Strategic Recommendation: Next Hit Target</h3>
            <p>The optimal path for audience expansion is:</p>
            <span class="metric-highlight">{cheapest_cpv['title']}</span>
            <p>At a current CPV of just <strong>{cheapest_cpv['value']}</strong>, this category represents the lowest barrier to entry and the highest potential for cost-effective scale.</p>
        </div>

        <h2 class="section-title">Complete Network Rankings</h2>
        <table>
            <thead><tr><th>Rank</th><th>Category Name</th><th>Current Value</th></tr></thead>
            <tbody>
    """

    # 3. Generate Table Rows
    for index, item in enumerate(cpv_data):
        val = item["value"]
        status_class = "val-bad" if val >= 75 else "val-warn" if val >= 40 else "val-good"
        row_style = "background-color: #ecfdf5;" if item["title"] == cheapest_cpv["title"] else ""
        
        html_content += f"""
            <tr style="{row_style}">
                <td>{index + 1}</td>
                <td><strong>{item['title']}</strong> { '(Current Investment)' if item['title'] == 'CPV Value 5' else '' }</td>
                <td class="{status_class}">{val}</td>
            </tr>"""

    html_content += "</tbody></table></body></html>"

    # 4. Compile HTML to PDF bytes
    return HTML(string=html_content).write_pdf()