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

  // ----- AI domain (§P5) -----
  await initAIDomain();
})();

// ---------------------------------------------------------------------------
// AI domain charts (§P5) — reads docs/data/ai_comparison.json
// ---------------------------------------------------------------------------

const AI_COLORS = {
  govai:   '#0891b2',  // cyan (公的) ≈ Bakong
  llama:   '#7c3aed',  // purple (分散) ≈ PayNow
  claude:  '#a16207',  // amber-dark (民間) ≈ KBZPay
  chatgpt: '#dc2626',  // red (民間) ≈ GCash
};

const AI_LABELS = {
  govai:   'GovAI (仮想・公的 ⊤_pub)',
  llama:   'Llama (Meta 開放配布 ⊤_bank)',
  claude:  'Claude (Anthropic 民間 ⊤_priv)',
  chatgpt: 'ChatGPT (OpenAI 民間 ⊤_priv)',
};

async function loadAI() {
  try {
    const r = await fetch('data/ai_comparison.json');
    if (!r.ok) return null;
    return await r.json();
  } catch (err) {
    console.warn('Failed to load ai_comparison.json', err);
    return null;
  }
}

function makeAIRankChart(canvasId, dataMap, yLabel) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  const firstKey = Object.keys(dataMap)[0];
  const steps = dataMap[firstKey].map((_, i) => i);

  const datasets = Object.entries(dataMap).map(([key, ranks]) => ({
    label: AI_LABELS[key] || key,
    data: ranks,
    borderColor: AI_COLORS[key] || '#6b7280',
    backgroundColor: (AI_COLORS[key] || '#6b7280') + '22',
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
          title: { display: true, text: '発火ステップ (LLM 質問サイクル)' },
          ticks: { stepSize: 1, autoSkip: false, maxRotation: 0 },
        },
        y: {
          title: { display: true, text: yLabel || 'Heyting値の階数' },
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

async function initAIDomain() {
  const ai = await loadAI();
  if (!ai) {
    setText(
      'finding-ai-trust',
      'data/ai_comparison.json が読み込めない。<code>python -m h_petri.compare_ai</code> を実行して生成してください。'
    );
    return;
  }

  const order = ['govai', 'llama', 'claude', 'chatgpt'].filter(k => ai.backbones[k]);

  // Trust curve
  const trustData = {};
  for (const k of order) trustData[k] = ai.backbones[k].trust_curve_ranks;
  makeAIRankChart('chart-ai-trust', trustData, 'TrustInLLM Heyting値の階数');

  const finals = order
    .map(k => `${k.toUpperCase()}=${ai.backbones[k].final_invisible.TrustInLLM}`)
    .join(' / ');
  setText(
    'finding-ai-trust',
    `4 LLM backbone を ${ai.config.num_queries} 質問サイクル動かした最終 TrustInLLM: ${finals}。
     金融 backbone と <strong>完全に同じ階数の半順序</strong> が再現する。
     これは「Heyting値階数は backbone タイプの本質的不変量」という主張の cross-domain 検証。`
  );

  // Cloudflare 2025-11 cascade
  if (ai.cloudflare_2025_11_cascade && ai.cloudflare_2025_11_cascade.curves) {
    const cascade = {};
    for (const k of order) cascade[k] = ai.cloudflare_2025_11_cascade.curves[k];
    makeAIRankChart('chart-ai-cascade', cascade, 'TrustInLLM (Cloudflare cascade injection)');
    setText(
      'finding-ai-cascade',
      `中点で <strong>民間 LLM (ChatGPT, Claude) だけ Trust が ⊥ に降下</strong>、Llama / GovAI は影響なし。
       2025-11-18 Cloudflare Workers KV 障害 (Downdetector 11,183 reports / 5.5h) を Petri net 上で再現。
       「単一 stalk の障害が全 dependent サービスを同時に落とす」という
       <strong>M-Pesa 2019 (Kenya 5h) と構造的に同型</strong>な事象 (notes/23 ペア2 / notes/25 sheaf)。`
    );
  }

  // Bottleneck reversal in AI
  if (ai.bottleneck_reversal_demo) {
    const br = ai.bottleneck_reversal_demo;
    // Append to trust finding
    const existing = document.getElementById('finding-ai-trust');
    if (existing) {
      existing.innerHTML +=
        `<br><br><strong>律速逆転 (AI 領域):</strong>
         ⊗ (ユーザーが最強 LLM を選ぶ): <strong>${br['monoidal_⊗_bound (max, user picks best LLM)']}</strong> /
         ▷ (multi-agent chain で全 LLM を直列に通す): <strong>${br['cospan_▷_bound  (meet, multi-agent chain)']}</strong>。
         Heyting階数差 <strong>${br.rank_gap}</strong> 段階。ReAct や多段パイプラインを組むと最弱の ChatGPT に律速される。`;
    }
  }
}
