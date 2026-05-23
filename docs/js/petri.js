/* Petri net page — visualize H-Petri Net simulation results.
 *
 * Reads docs/data/petri_comparison.json (output of `python -m h_petri.compare`)
 * and renders TrustHub / SystemicLoad rank curves for Bakong vs GCash.
 */

const RANK_LABELS = ['⊥', '⊤_priv', '⊤_bank', '⊤_pub'];

const PETRI_COLORS = {
  bakong: '#0891b2',  // cyan (central bank)
  paynow: '#7c3aed',  // purple (bank consortium)
  kbzpay: '#a16207',  // amber-dark (bank single)
  gcash:  '#dc2626',  // red (private platform)
};

const PETRI_LABELS = {
  bakong: 'Bakong (中央銀行型, KH)',
  paynow: 'PayNow (銀行コンソーシアム型, SG)',
  kbzpay: 'KBZPay (銀行単独型, MM)',
  gcash:  'GCash (民間プラットフォーム型, PH)',
};

function rankTickLabel(value) {
  return RANK_LABELS[value] ?? '';
}

async function loadPetri() {
  try {
    const r = await fetch('data/petri_comparison.json');
    if (!r.ok) return null;
    return await r.json();
  } catch (err) {
    console.warn('Failed to load petri_comparison.json', err);
    return null;
  }
}

function makeRankChart(canvasId, backboneData, opts = {}) {
  // backboneData: { backboneKey: ranksArray, ... }
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  const firstKey = Object.keys(backboneData)[0];
  const steps = backboneData[firstKey].map((_, i) => i);

  const datasets = Object.entries(backboneData).map(([key, ranks]) => ({
    label: PETRI_LABELS[key] || key,
    data: ranks,
    borderColor: PETRI_COLORS[key] || '#6b7280',
    backgroundColor: (PETRI_COLORS[key] || '#6b7280') + '22',
    borderWidth: 2.5,
    pointRadius: 4,
    pointHoverRadius: 6,
    stepped: true,
    tension: 0,
  }));

  return new Chart(ctx, {
    type: 'line',
    data: { labels: steps, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top', align: 'end' },
        tooltip: {
          callbacks: {
            label: (c) =>
              `${c.dataset.label}: ${rankTickLabel(c.parsed.y)} (rank ${c.parsed.y})`,
          },
        },
      },
      scales: {
        x: {
          title: { display: true, text: '発火ステップ (Firing Step)' },
          ticks: { stepSize: 1, autoSkip: false, maxRotation: 0 },
        },
        y: {
          title: { display: true, text: opts.yLabel || 'Heyting 値の階数' },
          min: 0,
          max: 3,
          ticks: {
            stepSize: 1,
            callback: (v) => `${v}: ${rankTickLabel(v)}`,
          },
        },
      },
    },
  });
}

function setText(id, html) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = html;
}

(async function init() {
  const data = await loadPetri();
  if (!data) {
    setText(
      'finding-petri-trust',
      'data/petri_comparison.json が読み込めない。<code>python -m h_petri.compare</code> を実行して生成してください。'
    );
    return;
  }

  const backbones = data.backbones || { bakong: data.bakong, gcash: data.gcash };
  const order = ['bakong', 'paynow', 'kbzpay', 'gcash'].filter(k => backbones[k]);

  const trustData = {};
  const loadData = {};
  for (const k of order) {
    trustData[k] = backbones[k].trust_curve_ranks;
    loadData[k] = backbones[k].systemic_load_curve_ranks;
  }

  // Trust curve
  makeRankChart('chart-petri-trust', trustData, { yLabel: 'TrustHub Heyting値の階数' });

  const finals = order.map(k => `${k.toUpperCase()}=${backbones[k].final_invisible.TrustHub}`).join(' / ');
  setText(
    'finding-petri-trust',
    `Bakong → <strong>⊤_pub</strong>、PayNow & KBZPay → <strong>⊤_bank</strong>、GCash → <strong>⊤_priv</strong> で永久に頭打ち。
     ${data.config.num_transactions} 回送金 (${backbones[order[0]].steps} 遷移発火)。
     最終値: ${finals}。
     <strong>Heyting半順序の3段階差</strong>が同じ構造の Petri net で実現してる。`
  );

  // Systemic load curve
  makeRankChart('chart-petri-load', loadData, { yLabel: 'SystemicLoad Heyting値の階数' });

  const loadFinals = order.map(k => `${k.toUpperCase()}=${backbones[k].final_invisible.SystemicLoad}`).join(' / ');
  setText(
    'finding-petri-load',
    `SystemicLoad も backbone タイプで上限が違う。最終値: ${loadFinals}。
     リアルタイム清算 (中銀・銀行) は ⊤_bank に到達、バッチ清算 (民間) は ⊤_priv 止まり。`
  );

  // Bottleneck reversal demo (notes/15)
  if (data.bottleneck_reversal_demo) {
    const br = data.bottleneck_reversal_demo;
    setText(
      'finding-petri-reversal',
      `⊗ (4 backbone を並列): <strong>${br['monoidal_⊗_bound (max)']}</strong> (max 律速、最強=Bakong) <br>
       ▷ (4 backbone を統合): <strong>${br['cospan_▷_bound  (meet)']}</strong> (meet 律速、最弱=GCash) <br>
       Heyting半順序の階数差: <strong>${br.rank_gap}</strong> 段階。<br><br>
       <em>${br.interpretation}</em>`
    );
  }
})();
