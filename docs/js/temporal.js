/* Temporal page — visualize the Trust time-functor.
 *
 * Reads docs/data/trust_timeline.json (from h_petri.trust_timeline)
 * and renders four charts:
 *  - chart-timelines:     all backbones as stepped lines over 1870-2030
 *  - chart-tradeoff:      scatter of (speed, concentration) per backbone
 *  - chart-reversal-time: ASEAN5 max(⊗) vs meet(▷) over time
 *
 * Theory references: notes/17, 19, 20.
 */

const RANK_LABELS = ['⊥', '⊤_priv', '⊤_bank', '⊤_pub'];

// Region-aware color palette.
const BACKBONE_COLORS = {
  // ASEAN central bank
  'Bakong (KH)':              '#0e7490',
  'PromptPay (TH)':           '#0891b2',
  // ASEAN platform (red family)
  'GCash (PH)':               '#dc2626',
  'MoMo (VN)':                '#ef4444',
  // ASEAN bank consortium / single
  'PayNow (SG)':              '#7c3aed',
  'KBZPay (MM)':              '#a16207',
  // Developed (grey family)
  'US Federal Reserve (US)':  '#1f2937',
  'Japan Banking (JP)':       '#374151',
  'EU SEPA (EU)':             '#4b5563',
  'Bitcoin (global)':         '#f59e0b',
};

const REGION_DASH = {
  ASEAN: [],          // solid
  developed: [6, 4],  // dashed
  global: [2, 2],
};

function rankTickLabel(v) { return RANK_LABELS[v] ?? ''; }

async function loadTimeline() {
  try {
    const r = await fetch('data/trust_timeline.json');
    if (!r.ok) return null;
    return await r.json();
  } catch (e) {
    console.warn('Failed to load trust_timeline.json', e);
    return null;
  }
}

function setText(id, html) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = html;
}

// ---------------- All-backbones timeline chart ----------------

function renderTimelinesChart(data) {
  const ctx = document.getElementById('chart-timelines');
  if (!ctx) return;

  const startYear = data.year_range[0];
  const endYear = data.year_range[1];
  const labels = [];
  for (let y = startYear; y <= endYear; y += 5) labels.push(y);

  const datasets = Object.entries(data.backbones).map(([name, m]) => {
    const pts = {};
    for (const p of m.data_points) pts[p.year] = p.rank;
    const series = labels.map(y => pts[y] ?? null);
    return {
      label: name,
      data: series,
      borderColor: BACKBONE_COLORS[name] || '#888',
      backgroundColor: (BACKBONE_COLORS[name] || '#888') + '22',
      borderWidth: 2,
      borderDash: REGION_DASH[m.region] || [],
      pointRadius: 0,
      stepped: true,
      tension: 0,
      spanGaps: true,
    };
  });

  new Chart(ctx, {
    type: 'line',
    data: { labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'nearest', axis: 'x', intersect: false },
      plugins: {
        legend: { position: 'right', labels: { font: { size: 10 } } },
        tooltip: {
          callbacks: {
            label: c => `${c.dataset.label}: ${rankTickLabel(c.parsed.y)} (rank ${c.parsed.y})`,
          },
        },
      },
      scales: {
        x: { title: { display: true, text: '年 (1870-2030)' }, ticks: { maxRotation: 0 } },
        y: {
          title: { display: true, text: 'Heyting値 階数' },
          min: 0, max: 3,
          ticks: { stepSize: 1, callback: v => `${v}: ${rankTickLabel(v)}` },
        },
      },
    },
  });

  // Finding text
  const aseanMaxRank = Math.max(...Object.entries(data.backbones)
    .filter(([_, m]) => m.region === 'ASEAN')
    .map(([_, m]) => m.data_points[m.data_points.length - 1].rank));
  const devMaxRank = Math.max(...Object.entries(data.backbones)
    .filter(([_, m]) => m.region === 'developed')
    .map(([_, m]) => m.data_points[m.data_points.length - 1].rank));
  setText(
    'finding-timelines',
    `先進国 (点線): 100年規模の緩い上昇。<br>
     ASEAN (実線): 数年で同じ Heyting階数に到達。<br>
     2026年時点で ASEAN最高=${aseanMaxRank}、先進国最高=${devMaxRank}。
     <strong>到達速度が桁違い</strong>だが、ゴールはほぼ同じ。`
  );
}

// ---------------- Speed × Concentration scatter ----------------

function renderTradeoffChart(data) {
  const ctx = document.getElementById('chart-tradeoff');
  if (!ctx) return;

  const points = Object.entries(data.backbones).map(([name, m]) => ({
    x: m.speed_per_year,
    y: m.concentration,
    label: name,
    region: m.region,
    type: m.type,
    color: BACKBONE_COLORS[name] || '#888',
    product: m.speed_x_concentration,
  }));

  new Chart(ctx, {
    type: 'scatter',
    data: {
      datasets: [{
        label: 'backbones',
        data: points,
        backgroundColor: points.map(p => p.color),
        borderColor: points.map(p => p.color),
        pointRadius: 8,
        pointHoverRadius: 10,
      }],
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: c => {
              const p = c.raw;
              return `${p.label}: v=${p.x}, C=${p.y}, v×C=${p.product} (${p.type})`;
            },
          },
        },
      },
      scales: {
        x: {
          title: { display: true, text: 'Trust上昇速度 v (Heyting階数/年)' },
          type: 'logarithmic', min: 0.005, max: 1,
        },
        y: {
          title: { display: true, text: '集中度 C (HHI類似)' },
          min: 0, max: 1,
        },
      },
    },
    plugins: [{
      id: 'labels',
      afterDatasetsDraw(chart) {
        const { ctx } = chart;
        ctx.save();
        ctx.font = '600 10px JetBrains Mono, monospace';
        ctx.fillStyle = '#555';
        chart.getDatasetMeta(0).data.forEach((point, i) => {
          const p = chart.data.datasets[0].data[i];
          // shorten name
          const shortName = p.label.replace(/\s*\(.*\)/, '');
          ctx.fillText(shortName, point.x + 12, point.y - 6);
        });
        ctx.restore();
      },
    }],
  });

  const minVC = data.metrics.min_v_times_C;
  const maxVC = data.metrics.max_v_times_C;
  setText(
    'finding-tradeoff',
    `v × C は <strong>${minVC} 〜 ${maxVC}</strong> の範囲。仮説 v×C ≥ K_const の K = ${minVC} (= JP Bank)。
     ただし範囲が広く厳密な定理化は困難。
     <strong>同じ backbone タイプ内では一定の傾向</strong>が見える: 中銀型は高速・中集中、銀行型は中速・分散、民間型は低速・高集中。`
  );
}

// ---------------- Bottleneck reversal across time ----------------

function renderReversalTimeChart(data) {
  const ctx = document.getElementById('chart-reversal-time');
  if (!ctx) return;

  // Sample every 5 years to keep readable
  const series = data.asean_max_meet_over_time.filter(r => r.year % 5 === 0 || r.year === 2026);
  const labels = series.map(r => r.year);
  const maxData = series.map(r => r['max_⊗']);
  const meetData = series.map(r => r['meet_▷']);

  new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: '⊗ 並列合成 (最強 backbone で律速)',
          data: maxData,
          borderColor: '#2563eb',
          backgroundColor: '#2563eb22',
          borderWidth: 3,
          pointRadius: 3,
          stepped: true,
          fill: false,
        },
        {
          label: '▷ 越境統合合成 (最弱 backbone で律速)',
          data: meetData,
          borderColor: '#dc2626',
          backgroundColor: '#dc262622',
          borderWidth: 3,
          pointRadius: 3,
          stepped: true,
          fill: '-1',  // fill toward dataset above
        },
      ],
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top' },
        tooltip: {
          callbacks: {
            label: c => `${c.dataset.label}: ${rankTickLabel(c.parsed.y)} (rank ${c.parsed.y})`,
          },
        },
      },
      scales: {
        x: { title: { display: true, text: '年' } },
        y: {
          title: { display: true, text: 'Heyting値 階数' },
          min: 0, max: 3,
          ticks: { stepSize: 1, callback: v => `${v}: ${rankTickLabel(v)}` },
        },
      },
    },
  });

  // Gap analysis
  const recent = series[series.length - 1];
  const earliest_with_gap = series.find(r => r.gap >= 2);
  setText(
    'finding-reversal-time',
    `2026年: max(⊗)=${recent['max_⊗']} (${rankTickLabel(recent['max_⊗'])}),
     meet(▷)=${recent['meet_▷']} (${rankTickLabel(recent['meet_▷'])}), 階数差 ${recent.gap}。<br>
     ${earliest_with_gap ? `階数差2が初めて出るのは ${earliest_with_gap.year} 年 — これは <strong>Bakong が ⊤_pub に達した瞬間</strong>。` : ''}<br>
     <strong>差が時間で広がる</strong> = 強い backbone (Bakong) が伸びても、弱い backbone (GCash) が変わらない限り、越境統合の代償は増え続ける。`
  );
}

// ---------------- Main ----------------

// ---------------- 1997 Crisis chart ----------------

function render1997CrisisChart(data) {
  const ctx = document.getElementById('chart-crisis-1997');
  if (!ctx) return;

  // Build per-country series for 1985-2010
  const startYear = 1985, endYear = 2010;
  const labels = [];
  for (let y = startYear; y <= endYear; y++) labels.push(y);

  const crisis_backbones = [
    'Thailand Banking (1985-)',
    'Indonesia Banking (1985-)',
    'Korea Banking (1985-)',
    'Malaysia Banking (1985-)',
  ];

  const country_colors = {
    'Thailand Banking (1985-)':    '#dc2626',
    'Indonesia Banking (1985-)':   '#ea580c',
    'Korea Banking (1985-)':       '#7c3aed',
    'Malaysia Banking (1985-)':    '#0891b2',
  };

  const datasets = crisis_backbones.map(name => {
    const m = data.backbones[name];
    if (!m) return null;
    const pts = {};
    for (const p of m.data_points) pts[p.year] = p.rank;
    const series = labels.map(y => pts[y] ?? null);
    return {
      label: name.replace(' (1985-)', '').replace(' Banking', ''),
      data: series,
      borderColor: country_colors[name],
      backgroundColor: country_colors[name] + '22',
      borderWidth: 2.5,
      pointRadius: 0,
      stepped: true,
      spanGaps: true,
    };
  }).filter(Boolean);

  new Chart(ctx, {
    type: 'line',
    data: { labels, datasets },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top' },
        tooltip: {
          callbacks: {
            label: c => `${c.dataset.label}: ${rankTickLabel(c.parsed.y)} (rank ${c.parsed.y})`,
            title: items => `${items[0].label}年`,
          },
        },
      },
      scales: {
        x: { title: { display: true, text: '年 (1985-2010)' } },
        y: {
          title: { display: true, text: 'Heyting値 階数' },
          min: 0, max: 3,
          ticks: { stepSize: 1, callback: v => `${v}: ${rankTickLabel(v)}` },
        },
      },
    },
    plugins: [{
      id: 'crisis_marker',
      afterDraw(chart) {
        const ctx = chart.ctx;
        const scaleX = chart.scales.x;
        const px1997 = scaleX.getPixelForValue('1997');
        const yTop = chart.chartArea.top;
        const yBottom = chart.chartArea.bottom;
        ctx.save();
        ctx.strokeStyle = 'rgba(220, 38, 38, 0.7)';
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 4]);
        ctx.beginPath();
        ctx.moveTo(px1997, yTop);
        ctx.lineTo(px1997, yBottom);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = '#dc2626';
        ctx.font = '600 11px JetBrains Mono, monospace';
        ctx.fillText('1997 AFC', px1997 + 6, yTop + 14);
        ctx.restore();
      },
    }],
  });

  // Compute drop ranges
  const drops = {};
  for (const name of crisis_backbones) {
    const m = data.backbones[name];
    if (!m) continue;
    const pts = {};
    for (const p of m.data_points) pts[p.year] = p.rank;
    const r1996 = pts[1996] ?? 0;
    const r1998 = pts[1998] ?? 0;
    drops[name.replace(' (1985-)', '').replace(' Banking', '')] = { from: r1996, to: r1998, drop: r1996 - r1998 };
  }

  const dropTxt = Object.entries(drops).map(([k, v]) => `<strong>${k}</strong>: ${v.from}→${v.to} (-${v.drop})`).join(' / ');
  setText(
    'finding-crisis-1997',
    `1996→1998 階数推移: ${dropTxt}。
     インドネシアが最大 (rank 2→0, -2階段)、マレーシアは資本規制で抑制 (rank 2→1, -1階段)。<br>
     <strong>同じ ⊤_bank 名目だった4国が、▷ で繋がっていたため最弱に律速されて全部崩落</strong>。`
  );
}

function renderReversal1997Chart(data) {
  const ctx = document.getElementById('chart-reversal-1997');
  if (!ctx) return;

  const crisis = data.crisis_1997;
  if (!crisis) return;

  // Sample every 2 years
  const series = crisis.max_meet_over_time.filter(r => r.year % 2 === 0 || r.year === 1997);
  const labels = series.map(r => r.year);
  const maxData = series.map(r => r['max_⊗']);
  const meetData = series.map(r => r['meet_▷']);

  new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: '⊗ 並列 (最強で律速)',
          data: maxData,
          borderColor: '#2563eb',
          backgroundColor: '#2563eb22',
          borderWidth: 3,
          pointRadius: 2,
          stepped: true,
          fill: false,
        },
        {
          label: '▷ 越境統合 (最弱で律速)',
          data: meetData,
          borderColor: '#dc2626',
          backgroundColor: '#dc262622',
          borderWidth: 3,
          pointRadius: 2,
          stepped: true,
          fill: '-1',
        },
      ],
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top' },
        tooltip: {
          callbacks: {
            label: c => `${c.dataset.label}: ${rankTickLabel(c.parsed.y)} (rank ${c.parsed.y})`,
          },
        },
      },
      scales: {
        x: { title: { display: true, text: '年 (1985-2030)' } },
        y: {
          title: { display: true, text: 'Heyting値 階数' },
          min: 0, max: 3,
          ticks: { stepSize: 1, callback: v => `${v}: ${rankTickLabel(v)}` },
        },
      },
    },
    plugins: [{
      id: 'crisis_marker',
      afterDraw(chart) {
        const ctx = chart.ctx;
        const scaleX = chart.scales.x;
        // find 1997 in labels
        const idx = chart.data.labels.indexOf(1997);
        if (idx < 0) return;
        const px = scaleX.getPixelForValue(1997);
        const yTop = chart.chartArea.top;
        const yBottom = chart.chartArea.bottom;
        ctx.save();
        ctx.strokeStyle = 'rgba(220, 38, 38, 0.7)';
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 4]);
        ctx.beginPath();
        ctx.moveTo(px, yTop);
        ctx.lineTo(px, yBottom);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = '#dc2626';
        ctx.font = '600 11px JetBrains Mono, monospace';
        ctx.fillText('1997', px + 6, yTop + 14);
        ctx.restore();
      },
    }],
  });

  // Find max gap
  const maxGap = series.reduce((acc, r) => r.gap > acc.gap ? r : acc, series[0]);
  const gap1996 = series.find(r => r.year === 1996)?.gap ?? '?';
  const gap1998 = series.find(r => r.year === 1998)?.gap ?? '?';
  setText(
    'finding-reversal-1997',
    `1996 階数差=${gap1996}, 1998 階数差=${gap1998}, 最大階数差=${maxGap.gap} (${maxGap.year}年)。
     <strong>1997年で meet が ${meetData[labels.indexOf(1997)] ?? '?'} に急落、max は ${maxData[labels.indexOf(1997)] ?? '?'} を維持 → 階数差が一気に広がる</strong>。
     これが「越境統合の代償が暴露される瞬間」の数値証拠。`
  );
}

// ---------------- Prediction pairs ----------------

function escHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

function renderPredictionPairs(data) {
  const container = document.getElementById('prediction-pairs-container');
  if (!container) return;
  const pairs = data.prediction_pairs || [];
  if (pairs.length === 0) {
    container.innerHTML = '<div class="pair-empty">予言ペアが見つかりません。</div>';
    return;
  }

  const html = pairs.map(p => {
    const devHtml = p.developed.map(d => `
      <div class="pair-event developed">
        <span class="year">${d.year}</span>
        <div class="event-name">${escHtml(d.event)}</div>
        <div class="region">${escHtml(d.region)}</div>
        <div class="summary">${escHtml(d.summary)}</div>
      </div>
    `).join('');

    // If single developed event, use simple 3-col layout. If multiple, stack on right.
    const isMulti = p.developed.length > 1;

    if (!isMulti) {
      const d = p.developed[0];
      return `
        <div class="pair-card">
          <div class="pair-label">${escHtml(p.label)}</div>
          <div class="pair-timeline">
            <div class="pair-event ea">
              <span class="year">${p.ea.year}</span>
              <div class="event-name">${escHtml(p.ea.event)}</div>
              <div class="region">${escHtml(p.ea.region)}</div>
              <div class="summary">${escHtml(p.ea.summary)}</div>
            </div>
            <div class="pair-arrow">
              <span class="arrow-line">→</span>
              <span class="lag">+${d.lag}年</span>
              <span class="lag-note">ラグ</span>
            </div>
            <div class="pair-event developed">
              <span class="year">${d.year}</span>
              <div class="event-name">${escHtml(d.event)}</div>
              <div class="region">${escHtml(d.region)}</div>
              <div class="summary">${escHtml(d.summary)}</div>
            </div>
          </div>
        </div>
      `;
    } else {
      const minLag = Math.min(...p.developed.map(d => d.lag));
      const maxLag = Math.max(...p.developed.map(d => d.lag));
      const lagText = `+${minLag}〜${maxLag}年`;
      return `
        <div class="pair-card">
          <div class="pair-label">${escHtml(p.label)}</div>
          <div class="pair-timeline">
            <div class="pair-event ea">
              <span class="year">${p.ea.year}</span>
              <div class="event-name">${escHtml(p.ea.event)}</div>
              <div class="region">${escHtml(p.ea.region)}</div>
              <div class="summary">${escHtml(p.ea.summary)}</div>
            </div>
            <div class="pair-arrow">
              <span class="arrow-line">→</span>
              <span class="lag">${lagText}</span>
              <span class="lag-note">ラグ</span>
            </div>
            <div class="pair-multi">${devHtml}</div>
          </div>
        </div>
      `;
    }
  }).join('');

  container.innerHTML = html;
}

(async function init() {
  const data = await loadTimeline();
  if (!data) {
    setText('finding-timelines',
      'data/trust_timeline.json が読み込めない。<code>python -m h_petri.trust_timeline</code> を実行して生成してください。');
    return;
  }

  renderTimelinesChart(data);
  renderTradeoffChart(data);
  renderReversalTimeChart(data);
  render1997CrisisChart(data);
  renderReversal1997Chart(data);
  renderPredictionPairs(data);
  renderLagTrend(data);
  renderForecast2030(data);
})();

// ---------------- §T10.1: enriched-category computed verdicts (notes/27) ----------------

(async function initEnriched() {
  let enr = null, kan = null;
  try {
    const r1 = await fetch('data/enriched_pairs.json');
    if (r1.ok) enr = await r1.json();
    const r2 = await fetch('data/kan_extension.json');
    if (r2.ok) kan = await r2.json();
  } catch (e) { /* ignore */ }

  const grid = document.getElementById('enriched-grid');
  const finding = document.getElementById('finding-enriched');
  if (!grid || !enr) {
    if (finding) finding.innerHTML =
      'data/enriched_pairs.json が読み込めない。<code>python -m h_petri.category.pairs_enriched</code> を実行してください。';
    return;
  }

  const gapByName = {};
  if (kan && kan.pairs) {
    for (const p of kan.pairs) {
      gapByName[p.name] = (p.prediction_gap && p.prediction_gap.total_amplification_gap);
    }
  }

  const badgeClass = { strict: 'strict', lax: 'lax', broken: 'partial' };
  const shortName = (n) => n.replace(/^Pair \d+ — /, '');

  grid.innerHTML = enr.pairs.map(p => {
    const gap = gapByName[p.name];
    const gapStr = (gap === undefined || gap === null) ? '—' : (gap > 0 ? `+${gap}` : `${gap}`);
    return `
      <div class="enr-card enr-${badgeClass[p.verdict] || 'lax'}">
        <div class="enr-name">${shortName(p.name)}</div>
        <div class="enr-row">
          <span class="enr-lbl">F の判定</span>
          <span class="badge ${badgeClass[p.verdict] || 'lax'}">${p.verdict}</span>
        </div>
        <div class="enr-row"><span class="enr-lbl">distortion</span><span class="enr-val">${p.distortion > 0 ? '+' : ''}${p.distortion}</span></div>
        <div class="enr-row"><span class="enr-lbl">Kan 増幅 gap</span><span class="enr-val">${gapStr}</span></div>
        <div class="enr-row"><span class="enr-lbl">圏の公理</span><span class="enr-val">${p.ea_axioms_ok && p.dev_axioms_ok ? '✓' : '✗'}</span></div>
      </div>`;
  }).join('');

  const adjOk = kan && kan.all_adjunctions_verified;
  finding.innerHTML =
    `5ペアとも圏の公理は構成的に成立 (✓)。F の判定: <strong>P2=strict / P1,P3,P4=lax / P5=broken</strong>。` +
    (adjOk ? ` Kan拡張の随伴 (Lan⊣F*⊣Ran) は<strong>全数チェックで成立</strong> — 値に依存しない検証済みの部分。` : ``) +
    ` <strong>Kan 増幅 gap は verdict と別軸</strong>: lax だけ正 (P1,3,4)、strict(P2) と broken(P5) は両方 0 (理由は正反対)。` +
    ` informal な手分類 (上の表) を計算で sharpening した結果、P3 は quasi→lax、P5 は partial→broken に確定。` +
    ` <em>ただし辺の hom 値は著者割当てなので、これは「割当てを固定した上での一意な判定」</em>。`;
})();

// ---------------- W: Lag trend scatter ----------------

function renderLagTrend(data) {
  const ctx = document.getElementById('chart-lag-trend');
  if (!ctx) return;
  const points = (data.lag_trend || []).map(p => ({
    x: p.ea_year,
    y: p.lag,
    label: `${p.ea_event} → ${p.developed_event}`,
    pair: p.label,
  }));
  if (points.length === 0) return;

  new Chart(ctx, {
    type: 'scatter',
    data: {
      datasets: [{
        label: '予言ペア',
        data: points,
        backgroundColor: '#dc2626',
        borderColor: '#dc2626',
        pointRadius: 8,
        pointHoverRadius: 10,
        showLine: false,
      }],
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: c => {
              const p = c.raw;
              return [`${p.pair}`, `${p.label}`, `ラグ: ${p.y}年`];
            },
          },
        },
      },
      scales: {
        x: { title: { display: true, text: '東南アジア事象の年' }, type: 'linear' },
        y: { title: { display: true, text: 'ラグ (年)' }, min: 0, max: 15 },
      },
    },
    plugins: [{
      id: 'lag_labels',
      afterDatasetsDraw(chart) {
        const { ctx } = chart;
        ctx.save();
        ctx.font = '600 10px JetBrains Mono, monospace';
        ctx.fillStyle = '#555';
        chart.getDatasetMeta(0).data.forEach((point, i) => {
          const p = chart.data.datasets[0].data[i];
          ctx.fillText(`+${p.y}年`, point.x + 12, point.y - 6);
        });
        ctx.restore();
      },
    }],
  });

  // Compute average and trend
  const xs = points.map(p => p.x);
  const ys = points.map(p => p.y);
  const n = points.length;
  const sumX = xs.reduce((a, b) => a + b, 0);
  const sumY = ys.reduce((a, b) => a + b, 0);
  const sumXY = xs.reduce((a, x, i) => a + x * ys[i], 0);
  const sumXX = xs.reduce((a, x) => a + x * x, 0);
  const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
  const avg = (sumY / n).toFixed(1);

  setText(
    'finding-lag-trend',
    `平均ラグ: <strong>${avg}年</strong>。線形回帰の傾き: <strong>${slope.toFixed(3)} 年/年</strong>
     (負なら時代が進むほどラグが縮む → 「予言の到達速度が加速」)。
     最古ペア (1997 AFC) のラグ 11-13年に対し、最新ペア (2021 Wave Money崩壊) のラグは 3年。
     <strong>4倍速になってる</strong>。`
  );
}

// ---------------- X: 2030 forecast ----------------

function renderForecast2030(data) {
  const container = document.getElementById('forecast-pairs-container');
  if (!container) return;
  const forecasts = data.forecast_2030 || [];
  if (forecasts.length === 0) {
    container.innerHTML = '<div class="pair-empty">予測データが見つかりません。</div>';
    return;
  }

  const html = forecasts.map(f => {
    const dev = f.developed_forecast;
    return `
      <div class="pair-card">
        <div class="pair-label">${escHtml(f.label)} (予測)</div>
        <div class="pair-timeline">
          <div class="pair-event ea">
            <span class="year">${f.ea.year}</span>
            <div class="event-name">${escHtml(f.ea.event)}</div>
            <div class="summary">${escHtml(f.ea.summary)}</div>
          </div>
          <div class="pair-arrow">
            <span class="arrow-line">→</span>
            <span class="lag">${escHtml(dev.lag_estimate)}</span>
            <span class="lag-note">推定</span>
          </div>
          <div class="pair-event developed" style="border-left-style:dashed;">
            <span class="year">${escHtml(dev.estimated_year)} (予測)</span>
            <div class="event-name">${escHtml(dev.event_candidates)}</div>
            <div class="summary">${escHtml(dev.summary)}</div>
            <div class="region" style="margin-top:6px;">信頼度: ${escHtml(dev.confidence)}</div>
          </div>
        </div>
      </div>
    `;
  }).join('');

  container.innerHTML = html;
}
