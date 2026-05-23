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
})();
