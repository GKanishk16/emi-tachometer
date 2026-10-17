"""Build a self-contained three-page HTML dashboard preview from DuckDB.
Author: Kanishk Gupta
"""
from __future__ import annotations

from datetime import date
from html import escape
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'powerbi' / 'dashboard_preview.html'


def query_rows(connection: duckdb.DuckDBPyConnection, sql: str):
    return connection.execute(sql).fetchall()


def rate_chart(title: str, description: str, rows, category_col: int = 0,
               count_col: int = 1, rate_col: int = 2, max_rate: float = 40.0) -> str:
    """Render accessible, directly labeled SVG bars with rate and cohort size."""
    width, height = 720, 340
    left, right, top, bottom = 64, 22, 28, 90
    plot_w, plot_h = width - left - right, height - top - bottom
    slot = plot_w / max(len(rows), 1)
    bar_w = min(68, slot * 0.52)
    parts = [f'<section class="viz-panel"><h2>{escape(title)}</h2><p class="sub">{escape(description)}</p>',
             f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}. {escape(description)}">']
    for tick in range(0, int(max_rate) + 1, 10):
        y = top + plot_h - plot_h * tick / max_rate
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" stroke="#e3e8ee"/>')
        parts.append(f'<text x="{left-10}" y="{y+4:.1f}" text-anchor="end" class="axis">{tick}%</text>')
    parts.append(f'<text x="16" y="{top+plot_h/2:.1f}" text-anchor="middle" class="axis-title" transform="rotate(-90 16 {top+plot_h/2:.1f})">Default rate</text>')
    for index, row in enumerate(rows):
        label = escape(str(row[category_col]))
        count = int(row[count_col])
        rate = float(row[rate_col]) * 100
        x = left + index * slot + (slot - bar_w) / 2
        bar_h = plot_h * rate / max_rate
        y = top + plot_h - bar_h
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bar_h:.1f}" rx="4" fill="#167d73"><title>{label}: {rate:.2f}% default rate; {count:,} loans</title></rect>')
        parts.append(f'<text x="{x+bar_w/2:.1f}" y="{y-9:.1f}" text-anchor="middle" class="value">{rate:.1f}%</text>')
        cx = x + bar_w / 2
        parts.append(f'<text x="{cx:.1f}" y="{top+plot_h+23}" text-anchor="middle" class="xlabel">{label}</text>')
        parts.append(f'<text x="{cx:.1f}" y="{top+plot_h+43}" text-anchor="middle" class="count">n={count:,}</text>')
    parts.append('</svg></section>')
    return ''.join(parts)


def metric(label: str, value: str, note: str) -> str:
    return (f'<div class="metric"><span>{escape(label)}</span><strong>{escape(value)}</strong>'
            f'<small>{escape(note)}</small></div>')


def build(connection: duckdb.DuckDBPyConnection) -> None:
    total, defaults, default_rate, exposure, first_date, last_date = query_rows(connection, """
        SELECT COUNT(*), SUM(loan_default), AVG(loan_default::DOUBLE), SUM(disbursed_amount),
               MIN(disbursal_date), MAX(disbursal_date) FROM fact_loans
    """)[0]
    month_rows = query_rows(connection, """
        SELECT STRFTIME(vintage_month, '%b %Y'), COUNT(*), AVG(loan_default::DOUBLE)
        FROM fact_loans GROUP BY vintage_month ORDER BY vintage_month
    """)
    ltv_rows = query_rows(connection, """
        SELECT ltv_band, COUNT(*), AVG(loan_default::DOUBLE)
        FROM fact_loans GROUP BY ltv_band
        ORDER BY CASE ltv_band WHEN '<70%' THEN 1 WHEN '70-<80%' THEN 2 WHEN '80-<90%' THEN 3 ELSE 4 END
    """)
    bureau_rows = query_rows(connection, """
        SELECT bureau_score_band, COUNT(*), AVG(loan_default::DOUBLE)
        FROM fact_loans GROUP BY bureau_score_band
        ORDER BY CASE bureau_score_band WHEN 'No score' THEN 1 WHEN '<300' THEN 2 WHEN '300-499' THEN 3 WHEN '500-699' THEN 4 ELSE 5 END
    """)
    age_rows = query_rows(connection, """
        SELECT age_band, COUNT(*), AVG(loan_default::DOUBLE)
        FROM fact_loans GROUP BY age_band
        ORDER BY CASE age_band WHEN '<25' THEN 1 WHEN '25-34' THEN 2 WHEN '35-44' THEN 3 WHEN '45-54' THEN 4 ELSE 5 END
    """)
    employment_rows = query_rows(connection, """
        SELECT employment_type, COUNT(*), AVG(loan_default::DOUBLE)
        FROM fact_loans GROUP BY employment_type ORDER BY employment_type
    """)
    segment_rows = query_rows(connection, """
        SELECT risk_segment, COUNT(*), SUM(disbursed_amount), SUM(loan_default), AVG(loan_default::DOUBLE)
        FROM segmented_loans GROUP BY risk_segment
        ORDER BY CASE risk_segment WHEN 'Low' THEN 1 WHEN 'Medium' THEN 2 WHEN 'High' THEN 3 ELSE 4 END
    """)
    money = f'{float(exposure):,.0f}'
    pages = [
        ('overview', 'Portfolio Overview'),
        ('drivers', 'Risk Drivers'),
        ('segments', 'Early-Warning Segments'),
    ]
    tabs = ''.join(
        f'<button class="tab{" active" if i == 0 else ""}" type="button" role="tab" id="tab-{key}" aria-controls="page-{key}" aria-selected="{"true" if i == 0 else "false"}">{label}</button>'
        for i, (key, label) in enumerate(pages)
    )
    overview = f'''<section class="page" id="page-overview" role="tabpanel" aria-labelledby="tab-overview">
      <div class="metrics">{metric('Labeled loans', f'{total:,}', 'Training data')}{metric('Default rate', f'{default_rate*100:.2f}%', f'{defaults:,} labeled defaults')}{metric('Disbursed exposure', money, 'Source monetary units')}</div>
      <div class="context">Disbursals: {first_date} to {last_date} · Target: dataset first-EMI default label</div>
      <div class="charts">{rate_chart('Monthly cohort default rate', 'Default rate by disbursal vintage; loan count shown below each month.', month_rows, max_rate=30)}{rate_chart('Default rate by LTV band', 'The 90%+ band has only 1,219 loans; rates are not monotonic.', ltv_rows)}</div>
    </section>'''
    drivers = f'''<section class="page" id="page-drivers" role="tabpanel" aria-labelledby="tab-drivers" hidden>
      <div class="charts">{rate_chart('Bureau score band', 'No score is kept distinct; score bands show descriptive association only.', bureau_rows)}{rate_chart('Borrower age band', 'Age is shown for analysis and monitoring, not used in the risk rules.', age_rows)}{rate_chart('Employment type', 'Unknown employment values remain visible as their own group.', employment_rows)}</div>
    </section>'''
    table_rows = ''.join(
        f'<tr><th scope="row">{escape(name)}</th><td>{n:,}</td><td>{n/total:.1%}</td><td>{float(exp):,.0f}</td><td>{d:,}</td><td>{rate*100:.2f}%</td></tr>'
        for name, n, exp, d, rate in segment_rows
    )
    segments = f'''<section class="page" id="page-segments" role="tabpanel" aria-labelledby="tab-segments" hidden>
      <div class="charts">{rate_chart('Observed default rate by segment', 'Retrospective labels; threshold rules are hypotheses, not validated policy.', [(n, count, rate) for n,count,exp,d,rate in segment_rows])}</div>
      <section class="table-panel"><h2>Segment volume and exposure</h2><div class="table-wrap"><table><thead><tr><th>Risk segment</th><th>Loans</th><th>Portfolio share</th><th>Disbursed exposure</th><th>Defaults</th><th>Default rate</th></tr></thead><tbody>{table_rows}</tbody></table></div><p class="sub">Exposure is original disbursed principal, not outstanding balance or realized loss.</p></section>
      <p class="decision-note"><strong>Product decision:</strong> cutoffs are analyst-selected and require business, fairness, and prospective outcome validation before operational use.</p>
    </section>'''
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>EMI Tachometer Dashboard Preview</title>
<style>
:root{{--ink:#172b3d;--muted:#66788a;--paper:#f3f6f8;--surface:#fff;--line:#e0e7ec;--teal:#167d73;--teal-light:#dcefeb;--navy:#0f263a;--gold:#c68c35}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}.shell{{max-width:1280px;margin:0 auto;padding:28px 30px 42px}}header{{display:flex;justify-content:space-between;align-items:flex-start;gap:20px;margin-bottom:26px}}.brand{{display:flex;align-items:center;gap:14px}}.mark{{width:42px;height:42px;border-radius:12px;background:var(--navy);color:#fff;display:grid;place-items:center;font-weight:700;letter-spacing:.04em}}h1{{font-size:25px;line-height:1.2;margin:0 0 5px}}.subtitle,.context,.sub{{color:var(--muted)}}.subtitle{{margin:0}}.period{{padding:8px 12px;border:1px solid var(--line);border-radius:8px;background:var(--surface);font-size:13px;color:var(--muted)}}.tabs{{display:flex;gap:8px;border-bottom:1px solid var(--line);margin-bottom:22px;overflow:auto}}.tab{{border:0;border-bottom:3px solid transparent;background:none;color:var(--muted);padding:12px 14px;font:500 14px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;white-space:nowrap}}.tab.active{{color:var(--teal);border-color:var(--teal)}}.tab:focus-visible{{outline:3px solid #6aaea6;outline-offset:2px}}.metrics{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:0 0 12px}}.metric{{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px 18px;min-width:0}}.metric span,.metric small{{display:block;color:var(--muted)}}.metric strong{{display:block;font-size:26px;line-height:1.2;margin:7px 0;font-variant-numeric:tabular-nums}}.metric small{{font-size:12px}}.context{{font-size:13px;margin:12px 0 18px}}.charts{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}}#page-drivers .charts{{grid-template-columns:repeat(2,minmax(0,1fr))}}.viz-panel,.table-panel{{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:18px 18px 10px;min-width:0}}.viz-panel h2,.table-panel h2{{font-size:16px;margin:0 0 3px}}.sub{{font-size:12px;margin:0 0 8px}}svg{{width:100%;height:auto;display:block;overflow:visible}}.axis,.count{{font-size:11px;fill:#6a7b8b}}.axis-title,.xlabel{{font-size:12px;fill:#42566a}}.value{{font-size:12px;font-weight:600;fill:var(--ink)}}.table-panel{{margin-top:18px}}.table-wrap{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;font-size:13px}}th,td{{padding:11px 10px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}}th:first-child,td:first-child{{text-align:left}}thead th{{color:var(--muted);font-weight:600}}tbody th{{font-weight:600}}.decision-note{{border-left:3px solid var(--gold);padding:10px 14px;background:#fff9ee;margin:16px 0;color:#594521;font-size:13px}}[hidden]{{display:none!important}}@media(max-width:760px){{.shell{{padding:20px 16px 32px}}header{{display:block}}.period{{display:inline-block;margin-top:14px}}.metrics{{grid-template-columns:1fr}}.charts,#page-drivers .charts{{grid-template-columns:1fr}}}}
</style></head><body><main class="shell"><header><div class="brand"><div class="mark" aria-hidden="true">ET</div><div><h1>EMI Tachometer</h1><p class="subtitle">Vehicle loan portfolio analytics · L&amp;T training data</p></div></div><div class="period">Aug–Oct 2018 · {total:,} labeled loans</div></header>
<nav class="tabs" role="tablist" aria-label="Dashboard pages">{tabs}</nav>
{overview}{drivers}{segments}
<p class="sub" style="margin-top:18px">Descriptive analysis, not causal inference or production credit policy. The dataset has no repayment time series.</p>
</main><script>
const buttons = [...document.querySelectorAll('[role="tab"]')];
const panels = [...document.querySelectorAll('[role="tabpanel"]')];
buttons.forEach((button, index) => {{
  button.addEventListener('click', () => {{
    buttons.forEach((item, i) => {{ item.classList.toggle('active', i === index); item.setAttribute('aria-selected', String(i === index)); }});
    panels.forEach((panel, i) => {{ panel.hidden = i !== index; }});
  }});
  button.addEventListener('keydown', event => {{
    if (!['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
    event.preventDefault(); const next = (index + (event.key === 'ArrowRight' ? 1 : buttons.length - 1)) % buttons.length;
    buttons[next].focus(); buttons[next].click();
  }});
}});
</script></body></html>'''
    OUTPUT.write_text(html, encoding='utf-8')
    print(f'Built dashboard preview: {OUTPUT}')


def main() -> None:
    connection = duckdb.connect(str(ROOT / 'emi_tachometer.duckdb'), read_only=True)
    try:
        build(connection)
    finally:
        connection.close()


if __name__ == '__main__':
    main()
