/* Southeast Asia as a Predictive Mirror — Visualization
 * Renders Chart.js charts for each hypothesis based on JSON data files.
 */

// ---------- Chart.js global defaults ----------
Chart.defaults.font.family = "'Inter', 'Noto Sans JP', sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.color = '#1a1a1a';
Chart.defaults.borderColor = '#e5e5e5';
Chart.defaults.scale.grid.color = '#f0f0f0';
Chart.defaults.scale.grid.drawTicks = false;

const COLOR_L = '#2563eb';
const COLOR_R = '#dc2626';
const COLOR_NEU = '#6b7280';
const COLOR_HL = '#f59e0b';

const COUNTRY_ORDER = ['SG', 'BN', 'MY', 'TH', 'ID', 'VN', 'PH', 'KH', 'LA', 'MM'];

const COUNTRY_NAME_JA = {
  VN: 'ベトナム',
  ID: 'インドネシア',
  PH: 'フィリピン',
  TH: 'タイ',
  MY: 'マレーシア',
  SG: 'シンガポール',
  KH: 'カンボジア',
  LA: 'ラオス',
  MM: 'ミャンマー',
  BN: 'ブルネイ'
};

function countryFull(code) {
  return COUNTRY_NAME_JA[code] ? `${code} (${COUNTRY_NAME_JA[code]})` : code;
}

// Defensive: set innerHTML only if element exists (used across multi-page tabs)
function setFinding(id, html) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = html;
}

const BACKBONE_COLOR = {
  central_bank: '#0891b2',  // cyan
  platform:     '#dc2626',  // red
  bank:         '#7c3aed',  // purple
  telco:        '#f59e0b',  // amber
  unknown:      '#9ca3af'
};

// ---------- Intersection Observer for fade-in ----------
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('section:not(.hero)').forEach(s => observer.observe(s));

// ---------- TOC active highlight ----------
const tocLinks = document.querySelectorAll('.toc a');
const sections = document.querySelectorAll('section');
const tocObserver = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const id = e.target.id;
      tocLinks.forEach(a => {
        a.classList.toggle('active', a.getAttribute('href') === '#' + id);
      });
    }
  });
}, { threshold: 0.4 });
sections.forEach(s => tocObserver.observe(s));

// ---------- Data loader ----------
async function loadAll() {
  const files = ['A_findex', 'B_concentration', 'C_disasters', 'D_remittance', 'E_comparison'];
  const data = {};
  for (const f of files) {
    try {
      const r = await fetch(`data/${f}.json`);
      if (r.ok) data[f] = await r.json();
      else console.warn(`Failed to load ${f}.json: ${r.status}`);
    } catch (err) {
      console.warn(`Error loading ${f}.json:`, err);
    }
  }
  return data;
}

// ---------- Helpers ----------
function makeScatter(canvasId, points, opts = {}) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  return new Chart(ctx, {
    type: 'scatter',
    data: {
      datasets: [{
        label: opts.label || 'ASEAN10',
        data: points,
        backgroundColor: opts.color || COLOR_L,
        borderColor: opts.color || COLOR_L,
        pointRadius: 7,
        pointHoverRadius: 10
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ctx => {
              const p = ctx.raw;
              return `${countryFull(p.label)}: (${p.x}, ${p.y})${p.note ? ' — ' + p.note : ''}`;
            }
          }
        }
      },
      scales: {
        x: { title: { display: true, text: opts.xLabel || '', color: COLOR_NEU } },
        y: { title: { display: true, text: opts.yLabel || '', color: COLOR_NEU } }
      }
    },
    plugins: [{
      id: 'labels',
      afterDatasetsDraw(chart) {
        const { ctx } = chart;
        const meta = chart.getDatasetMeta(0);
        ctx.save();
        ctx.font = '600 11px JetBrains Mono, monospace';
        ctx.fillStyle = COLOR_NEU;
        meta.data.forEach((point, i) => {
          const p = chart.data.datasets[0].data[i];
          ctx.fillText(p.label, point.x + 10, point.y - 8);
        });
        ctx.restore();
      }
    }]
  });
}

function makeBar(canvasId, labels, values, opts = {}) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: opts.label || '',
        data: values,
        backgroundColor: opts.colors || labels.map(() => opts.color || COLOR_L),
        borderColor: opts.colors || labels.map(() => opts.color || COLOR_L),
        borderWidth: 0
      }]
    },
    options: {
      indexAxis: opts.horizontal ? 'y' : 'x',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ctx => `${countryFull(ctx.label)}: ${ctx.parsed[opts.horizontal ? 'x' : 'y']}${opts.unit || ''}`
          }
        }
      },
      scales: {
        x: { title: { display: !!opts.xLabel, text: opts.xLabel || '' } },
        y: { title: { display: !!opts.yLabel, text: opts.yLabel || '' } }
      }
    }
  });
}

function getCountry(data, code, field) {
  if (!data || !data.data || !data.data[code]) return null;
  return data.data[code][field];
}

// ---------- Render each hypothesis ----------

function renderA1(d) {
  if (!d.A_findex || !d.E_comparison) return;
  const findex = d.A_findex.data;
  const points = [];
  COUNTRY_ORDER.forEach(c => {
    const mm = findex[c]?.mobile_money_pct;
    const ba = findex[c]?.bank_account_pct;
    if (mm != null && ba != null) {
      points.push({ x: ba, y: mm, label: c });
    }
  });
  makeScatter('chart-A1', points, {
    xLabel: 'Bank Account Ownership (%)',
    yLabel: 'Mobile Money Account (%)',
    color: COLOR_L
  });

  // Compute leapfrog strength as mm - ba (when positive)
  const sorted = points.map(p => ({ ...p, gap: p.y - p.x })).sort((a,b) => b.gap - a.gap);
  const top = sorted[0];
  document.getElementById('finding-A1').innerHTML = top
    ? `銀行口座を経由せずモバイルマネーが先行している度合いが最大なのは <strong>${top.label}</strong> (差分 ${top.gap.toFixed(1)}pt)。リープフロッグ強度の代理指標。`
    : 'データが揃わず計算不能。';
}

function renderA2(d) {
  if (!d.A_findex || !d.B_concentration) return;
  const findex = d.A_findex.data;
  const conc = d.B_concentration.data;
  const points = [];
  COUNTRY_ORDER.forEach(c => {
    const mm = findex[c]?.mobile_money_pct;
    const tshare = conc[c]?.top_share_pct;
    if (mm != null && tshare != null) {
      points.push({ x: mm, y: tshare, label: c, note: conc[c].top_provider });
    }
  });
  makeScatter('chart-A2', points, {
    xLabel: 'Mobile Money Penetration (%)',
    yLabel: 'Top Provider Market Share (%)',
    color: COLOR_R
  });

  // Naive correlation
  const n = points.length;
  if (n >= 3) {
    const mx = points.reduce((s, p) => s + p.x, 0) / n;
    const my = points.reduce((s, p) => s + p.y, 0) / n;
    const num = points.reduce((s, p) => s + (p.x - mx) * (p.y - my), 0);
    const dx = Math.sqrt(points.reduce((s, p) => s + (p.x - mx) ** 2, 0));
    const dy = Math.sqrt(points.reduce((s, p) => s + (p.y - my) ** 2, 0));
    const r = num / (dx * dy);
    document.getElementById('finding-A2').innerHTML =
      `普及度とトップシェアの相関係数 r = <strong>${r.toFixed(2)}</strong>。${r > 0.3 ? '便利と集中の正相関を示唆 → L と R が同時に増えている可能性。' : '明確な相関なし。データ追加で再検証要。'}`;
  } else {
    document.getElementById('finding-A2').innerHTML = 'データ点不足で相関計算不能。';
  }
}

function renderB1(d) {
  if (!d.B_concentration) return;
  const conc = d.B_concentration.data;
  const grouped = { central_bank: [], platform: [], bank: [], telco: [], unknown: [] };
  COUNTRY_ORDER.forEach(c => {
    const t = conc[c]?.backbone_type || 'unknown';
    grouped[t] = grouped[t] || [];
    grouped[t].push(c);
  });
  const labels = Object.keys(grouped).filter(k => grouped[k].length > 0);
  const values = labels.map(k => grouped[k].length);
  const colors = labels.map(k => BACKBONE_COLOR[k]);

  makeBar('chart-B1', labels.map(k => k.replace('_', ' ').toUpperCase()), values, {
    colors,
    yLabel: 'Number of Countries',
    unit: ' countries'
  });

  const breakdown = labels.map(k => `<strong>${k}</strong>: ${grouped[k].join(', ')}`).join(' / ');
  document.getElementById('finding-B1').innerHTML =
    `${breakdown}。Telco backbone (M-Pesa型) は ASEAN-10 で実質的に消滅。`;
}

function renderB2(d) {
  if (!d.B_concentration) return;
  const conc = d.B_concentration.data;
  const labels = [...COUNTRY_ORDER].filter(c => conc[c]?.top_share_pct != null)
    .sort((a, b) => conc[b].top_share_pct - conc[a].top_share_pct);
  const values = labels.map(c => conc[c].top_share_pct);
  const colors = labels.map(c => BACKBONE_COLOR[conc[c].backbone_type] || COLOR_NEU);

  makeBar('chart-B2', labels, values, {
    colors,
    horizontal: true,
    xLabel: 'Top Provider Share (%)',
    unit: '%'
  });

  const top = labels[0];
  document.getElementById('finding-B2').innerHTML =
    `最も集中度が高いのは <strong>${top}</strong> (${conc[top].top_provider} ${conc[top].top_share_pct}%, ${conc[top].backbone_type})。単一プロバイダーの障害が国全体の決済を止めるリスク構造。`;
}

function renderD1(d) {
  if (!d.D_remittance) return;
  const rem = d.D_remittance.data;
  const labels = [...COUNTRY_ORDER].filter(c => rem[c]?.inward_pct_gdp != null)
    .sort((a, b) => rem[b].inward_pct_gdp - rem[a].inward_pct_gdp);
  const values = labels.map(c => rem[c].inward_pct_gdp);

  makeBar('chart-D1', labels, values, {
    color: COLOR_L,
    horizontal: true,
    xLabel: 'Inward Remittance / GDP (%)',
    unit: '%'
  });

  const top = labels[0];
  document.getElementById('finding-D1').innerHTML =
    `<strong>${top}</strong> が受取GDP比 ${rem[top].inward_pct_gdp}% で最大。海外労働市場の不調が国経済の急所になる構造。`;
}

function renderD2(d) {
  if (!d.D_remittance) return;
  const rem = d.D_remittance.data;
  const labels = [...COUNTRY_ORDER].filter(c => rem[c]?.inward_usd_b != null);
  const inward = labels.map(c => rem[c].inward_usd_b);
  const outward = labels.map(c => rem[c].outward_usd_b || 0);

  const ctx = document.getElementById('chart-D2');
  if (!ctx) return;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        { label: 'Inward ($B)', data: inward, backgroundColor: COLOR_L, borderWidth: 0 },
        { label: 'Outward ($B)', data: outward, backgroundColor: COLOR_R, borderWidth: 0 }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top', align: 'end' },
        tooltip: { callbacks: { label: ctx => `${ctx.dataset.label}: $${ctx.parsed.y}B` } }
      },
      scales: { y: { title: { display: true, text: 'USD Billion' } } }
    }
  });

  const thInward = rem.TH?.inward_usd_b || 0;
  const thOutward = rem.TH?.outward_usd_b || 0;
  document.getElementById('finding-D2').innerHTML =
    `<strong>Thailand</strong> は受取 $${thInward}B / 送出 $${thOutward}B の二重ハブ。CLM三国 (KH/LA/MM) の経済を媒介し、タイの規制1つで3国同時ショックの構造的リスク。`;
}

function renderC1(d) {
  if (!d.C_disasters) {
    document.getElementById('finding-C1').textContent = 'EM-DAT データ取得中。完了後に描画されます。';
    return;
  }
  const dis = d.C_disasters.data;
  const labels = [...COUNTRY_ORDER].filter(c => dis[c]?.total_disasters != null)
    .sort((a, b) => dis[b].total_disasters - dis[a].total_disasters);
  const values = labels.map(c => dis[c].total_disasters);

  makeBar('chart-C1', labels, values, {
    color: COLOR_L,
    horizontal: true,
    xLabel: 'Total Disasters (2005-2025)',
    unit: ' events'
  });

  const top = labels[0];
  document.getElementById('finding-C1').innerHTML =
    `<strong>${top}</strong> が過去20年で最多 (${dis[top].total_disasters}件)。${dis[top].worst_event || ''}`;
}

function renderC2(d) {
  if (!d.C_disasters || !d.E_comparison) {
    document.getElementById('finding-C2').textContent = 'EM-DAT データ取得中。完了後に描画されます。';
    return;
  }
  const dis = d.C_disasters.data;
  const comp = d.E_comparison.data;
  const points = [];
  COUNTRY_ORDER.forEach(c => {
    const urban = comp[c]?.top_city_pop_pct;
    const loss = dis[c]?.total_loss_usd_b;
    if (urban != null && loss != null) {
      points.push({ x: urban, y: loss, label: c });
    }
  });
  makeScatter('chart-C2', points, {
    xLabel: 'Top City Population Share (%)',
    yLabel: 'Total Disaster Loss (USD Billion)',
    color: COLOR_R
  });

  document.getElementById('finding-C2').innerHTML =
    `都市集中度が高い国ほど災害1件あたりの経済被害が大きい傾向。コンパクト都市の便利 (L) が脆弱性 (R) として顕在化。`;
}

function normalizeColonial(s) {
  if (!s) return 'Unknown';
  const lower = s.toLowerCase();
  if (lower.includes('never') || lower.includes('non-coloniz') || lower.includes('independent') || lower.includes('buffer state')) return 'Independent';
  if (lower.includes('spanish') || lower.includes('american')) return 'Spanish/US';
  if (lower.includes('british')) return 'British';
  if (lower.includes('french')) return 'French';
  if (lower.includes('dutch')) return 'Dutch';
  return 'Other';
}

function renderE1(d) {
  if (!d.E_comparison) return;
  const comp = d.E_comparison.data;
  const colonyColor = {
    'British': '#1e40af',
    'French': '#b91c1c',
    'Dutch': '#ea580c',
    'Spanish/US': '#7c3aed',
    'Independent': '#16a34a',
    'Other': '#9ca3af',
    'Unknown': '#9ca3af'
  };
  const labels = [...COUNTRY_ORDER].filter(c => comp[c]?.internet_pct != null)
    .sort((a, b) => comp[b].internet_pct - comp[a].internet_pct);
  const values = labels.map(c => comp[c].internet_pct);
  const colors = labels.map(c => colonyColor[normalizeColonial(comp[c].colonial)] || COLOR_NEU);

  makeBar('chart-E1', labels, values, {
    colors,
    horizontal: true,
    xLabel: 'Internet Penetration (%)',
    unit: '%'
  });

  // legend in finding (using actual countries' normalized colonial origin)
  const used = new Set(labels.map(c => normalizeColonial(comp[c].colonial)));
  const legend = [...used]
    .map(k => `<span style="display:inline-block;width:10px;height:10px;background:${colonyColor[k]};border-radius:2px;margin-right:4px;vertical-align:middle;"></span>${k}`)
    .join(' &nbsp; ');
  document.getElementById('finding-E1').innerHTML =
    `植民地経路で色分け — ${legend}<br>British圏 (SG/MY/BN) が一貫して高水準、French圏 (VN/KH/LA) は中下位、Independent型 (TH) は中位。初期条件としての制度経路依存。`;
}

function renderE2(d) {
  if (!d.E_comparison) return;
  const comp = d.E_comparison.data;
  const points = [];
  COUNTRY_ORDER.forEach(c => {
    const elec = comp[c]?.electricity_pct;
    const mob = comp[c]?.mobile_per_100;
    if (elec != null && mob != null) {
      points.push({ x: elec, y: mob, label: c, note: comp[c].colonial });
    }
  });
  makeScatter('chart-E2', points, {
    xLabel: 'Electricity Access (%)',
    yLabel: 'Mobile Subscriptions per 100',
    color: COLOR_HL
  });

  const laos = points.find(p => p.label === 'LA');
  document.getElementById('finding-E2').innerHTML = laos
    ? `<strong>Laos</strong>: 電気 ${laos.x}% でモバイル契約 ${laos.y}/100 — 他国が110-170の中で唯一の異常値。リープフロッグ前提モデルが当てはまらないケース。`
    : 'Laos データなし。';
}

// ---------- Main ----------
(async function init() {
  const data = await loadAll();
  console.log('Loaded data:', Object.keys(data));

  // Conditionally render based on which charts exist in the current page.
  // Each page (index/finance/petri) hosts a different subset of canvases.
  const guarded = (id, fn) => {
    if (document.getElementById(id)) fn(data);
  };

  guarded('chart-A1', renderA1);
  guarded('chart-A2', renderA2);
  guarded('chart-B1', renderB1);
  guarded('chart-B2', renderB2);
  guarded('chart-C1', renderC1);
  guarded('chart-C2', renderC2);
  guarded('chart-D1', renderD1);
  guarded('chart-D2', renderD2);
  guarded('chart-E1', renderE1);
  guarded('chart-E2', renderE2);
})();
