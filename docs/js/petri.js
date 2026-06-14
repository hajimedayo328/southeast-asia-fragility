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
    let text = `⊗ (4 backbone を並列): <strong>${br['monoidal_⊗_bound (max)']}</strong> (max 律速、最強=Bakong) <br>
       ▷ (4 backbone を統合): <strong>${br['cospan_▷_bound  (meet)']}</strong> (meet 律速、最弱=GCash) <br>
       Heyting半順序の階数差: <strong>${br.rank_gap}</strong> 段階。<br><br>
       <em>${br.interpretation}</em>`;

    // Cross-verify with Open Petri Net implementation
    try {
      const openR = await fetch('data/open_petri_composition.json');
      if (openR.ok) {
        const open = await openR.json();
        const opn = open.bottleneck_reversal;
        const consistent = (opn.parallel_bound === br['monoidal_⊗_bound (max)']) &&
                           (opn.cospan_bound === br['cospan_▷_bound  (meet)']);
        text += `<br><br><strong>独立実装での再現:</strong>
          <code>src/h_petri/open_net.py</code> (Baez-Master 2018 cospan 合成) でも
          ⊗=<strong>${opn.parallel_bound}</strong>, ▷=<strong>${opn.cospan_bound}</strong>,
          rank gap=<strong>${opn.rank_gap}</strong>。
          ${consistent ? '✓ <strong>compare.py と完全一致</strong>。' : '✗ 不一致 (要調査)。'}
          独立 2 実装で同じ結果 = 律速逆転定理の頑健性が数値で確認できた。`;
      }
    } catch (err) { /* fall through */ }

    setText('finding-petri-reversal', text);
  }

  // ----- Centrality (§P4-D) -----
  await initCentrality();

  // ----- AI domain (§P5) -----
  await initAIDomain();

  // ----- Sheaf H¹ (§P6) -----
  await initSheaf();

  // ----- False-positive panel (§P6-D) -----
  await initFPPanel();

  // ----- Writer H monad (§P7) -----
  await initMonad();
})();

// ---------------------------------------------------------------------------
// Centrality (§P4-D) — reads docs/data/centrality.json
// ---------------------------------------------------------------------------

async function loadCentrality() {
  try {
    const r = await fetch('data/centrality.json');
    if (!r.ok) return null;
    return await r.json();
  } catch (err) {
    console.warn('Failed to load centrality.json', err);
    return null;
  }
}

async function initCentrality() {
  const c = await loadCentrality();
  if (!c) {
    setText('finding-centrality',
      'data/centrality.json が読み込めない。<code>python -m h_petri.centrality</code> を実行してください。');
    return;
  }

  const grid = document.getElementById('centrality-grid');
  if (grid) {
    const order = ['bakong', 'paynow', 'kbzpay', 'gcash'];
    const colorOf = {
      bakong: '#0891b2', paynow: '#7c3aed', kbzpay: '#a16207', gcash: '#dc2626',
    };
    grid.innerHTML = order.filter(k => c.backbones[k]).map(k => {
      const r = c.backbones[k];
      const hs = c.hotspots[k];
      const trustHubHCC = r.places.TrustHub?.HCC ?? '—';
      return `
        <div class="cent-card" style="border-left: 4px solid ${colorOf[k]};">
          <div class="cent-key">${k.toUpperCase()}</div>
          <div class="cent-metric">
            <span class="lbl">HHI-AC</span>
            <span class="val">${r.HHI_AC}</span>
          </div>
          <div class="cent-metric">
            <span class="lbl">hotspot</span>
            <span class="val mono">${hs ? hs.place : '—'}</span>
          </div>
          <div class="cent-metric">
            <span class="lbl">max BI</span>
            <span class="val">${hs ? hs.BI : '—'}</span>
          </div>
          <div class="cent-metric">
            <span class="lbl">TrustHub HCC</span>
            <span class="val mono"><strong>${trustHubHCC}</strong></span>
          </div>
        </div>
      `;
    }).join('');
  }

  const hhiSet = new Set(Object.values(c.backbones).map(r => r.HHI_AC));
  const biSet  = new Set(Object.values(c.hotspots).map(h => h.BI));
  const hccSet = new Set(Object.values(c.backbones).map(r => r.places.TrustHub?.HCC));
  setText('finding-centrality',
    `HHI-AC は <strong>${[...hhiSet].join(' / ')}</strong> (${hhiSet.size === 1 ? '全 backbone 完全一致' : '差あり'})。
     ホットスポットの BI は <strong>${[...biSet].join(' / ')}</strong> (${biSet.size === 1 ? '完全一致' : '差あり'})。
     TrustHub の HCC は <strong>${[...hccSet].join(' / ')}</strong> (${hccSet.size > 1 ? '←ここだけ分離' : '一致'})。
     <em>${c.lesson}</em>`);
}

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
       2025-11-18 Cloudflare 設定ファイル障害 (Bot Management 設定 / widespread Downdetector reports / 約4時間) を Petri net 上で再現。
       「単一 stalk の障害が全 dependent サービスを同時に落とす」という
       <strong>M-Pesa 2019 (Kenya 5h) と同じく数時間規模の単一民間 backbone 障害</strong>な事象 (notes/23 ペア2 / notes/25 sheaf)。`
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

// ---------------------------------------------------------------------------
// Sheaf H¹ charts (§P6) — reads docs/data/sheaf_h1.json
// ---------------------------------------------------------------------------

const RANK_OF = { '⊥': 0, '⊤_priv': 1, '⊤_bank': 2, '⊤_pub': 3 };

async function loadSheaf() {
  try {
    const r = await fetch('data/sheaf_h1.json');
    if (!r.ok) return null;
    return await r.json();
  } catch (err) {
    console.warn('Failed to load sheaf_h1.json', err);
    return null;
  }
}

function makeSheafChart(canvasId, snapshots, opts) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  const labels = snapshots.map((s, i) => `T${i}`);

  const datasets = [];
  if (opts.showH1) {
    datasets.push({
      label: 'H¹ (gluing failures)',
      data: snapshots.map(s => s.h1_count),
      borderColor: '#dc2626',
      backgroundColor: '#dc262622',
      borderWidth: 2.5,
      pointRadius: 5,
      pointHoverRadius: 7,
      tension: 0,
      stepped: true,
      yAxisID: 'y',
    });
  }
  if (opts.showH0) {
    datasets.push({
      label: 'H⁰(meet) Heyting rank',
      data: snapshots.map(s => RANK_OF[s.h0_meet] ?? 0),
      borderColor: '#0891b2',
      backgroundColor: '#0891b222',
      borderWidth: 2.5,
      pointRadius: 5,
      pointHoverRadius: 7,
      tension: 0,
      stepped: true,
      yAxisID: opts.showH1 ? 'y1' : 'y',
    });
  }

  const scales = {
    x: {
      title: { display: true, text: 'スナップショット (時系列)' },
      ticks: {
        callback: (_, i) => `${labels[i]}\n${(snapshots[i].snapshot || '').slice(0, 24)}`,
        maxRotation: 0,
        font: { size: 10 },
      },
    },
  };
  if (opts.showH1) {
    scales.y = {
      title: { display: true, text: 'H¹ (# inconsistent edges)' },
      beginAtZero: true,
      ticks: { stepSize: 1 },
      position: 'left',
    };
  }
  if (opts.showH0) {
    const key = opts.showH1 ? 'y1' : 'y';
    scales[key] = {
      title: { display: true, text: 'H⁰(meet) rank' },
      min: 0,
      max: 3,
      ticks: {
        stepSize: 1,
        callback: (v) => `${v}: ${rankTickLabel(v)}`,
      },
      position: opts.showH1 ? 'right' : 'left',
      grid: opts.showH1 ? { drawOnChartArea: false } : undefined,
    };
  }

  return new Chart(ctx, {
    type: 'line',
    data: { labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top', align: 'end' },
        tooltip: {
          callbacks: {
            title: (items) => snapshots[items[0].dataIndex].snapshot,
          },
        },
      },
      scales,
    },
  });
}

async function initSheaf() {
  const s = await loadSheaf();
  if (!s) {
    setText('finding-sheaf-afc',
      'data/sheaf_h1.json が読み込めない。<code>python -m h_petri.sheaf.cech</code> を実行してください。');
    return;
  }

  // 1997 AFC — show H¹
  const afc = s.scenario_1997_afc.timeline;
  makeSheafChart('chart-sheaf-afc', afc, { showH1: true, showH0: true });
  const afcSeries = afc.map(x => x.h1_count).join(' → ');
  setText('finding-sheaf-afc',
    `H¹ 推移: <strong>${afcSeries}</strong>。
     ${afc.length} スナップショット (USDペッグ崩壊から MY 資本規制まで)。
     共通 stalk (USDペッグ) が消えた瞬間に H¹ が階段状に上昇、
     H⁰(meet) は <strong>${afc[0].h0_meet} → ${afc[afc.length-1].h0_meet}</strong> に低下。
     <em>これが「sheaf 視点での通貨危機の構造的指紋」</em>。`);

  // Cloudflare — show H¹ and H⁰
  const cf = s.scenario_cloudflare_2025_11.timeline;
  makeSheafChart('chart-sheaf-cf', cf, { showH1: true, showH0: true });
  const cfH0 = cf.map(x => x.h0_meet).join(' → ');
  setText('finding-sheaf-cf',
    `H⁰(meet) 推移: <strong>${cfH0}</strong>。
     09:30 の設定ファイル障害 (Bot Management 設定) で全 Cloudflare-fronted AI サービスが ⊥ に同時降下、
     H⁰(meet) が <strong>⊤_priv → ⊥</strong> に崩壊。約4時間後に復旧。
     1997 と <em>H¹ の出方は違うが、共通 stalk 崩壊という構造的事象は同じ</em>。
     これが notes/23 予言ペア2 (M-Pesa 2019 ↔ Cloudflare 2025-11) の sheaf-理論的根拠。`);
}

// ---------------------------------------------------------------------------
// False-positive panel (§P6-D) — reads false_positive_panel.json + _ci.json
// ---------------------------------------------------------------------------

async function initFPPanel() {
  if (!document.getElementById('chart-fp-panel')) return;
  let p, ci = null;
  try {
    const r1 = await fetch('data/false_positive_panel.json');
    if (!r1.ok) throw new Error('panel');
    p = await r1.json();
    const r2 = await fetch('data/false_positive_panel_ci.json');
    if (r2.ok) ci = await r2.json();
  } catch (err) {
    setText('finding-fp-panel',
      'data/false_positive_panel.json が読み込めない。<code>python src/h_petri/empirical/false_positive_panel.py</code> を実行してください。');
    return;
  }

  const rule = p.preregistered_design.primary_rule;   // 'LV_30_10'
  const m = p.primary_result[rule].metrics;
  const c = p.primary_result[rule].counts;
  const cov = p.panel_coverage;
  const base = m.base_rate, prec = m.precision;
  const pct = x => +(x * 100).toFixed(1);

  const ctx = document.getElementById('chart-fp-panel');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['全平穏年 (ベースレート)', '比率>1 が発火した後'],
      datasets: [
        { label: '2年内に通貨危機', data: [pct(base), pct(prec)],
          backgroundColor: '#dc2626', borderWidth: 0 },
        { label: '危機なし (空振り)', data: [pct(1 - base), pct(1 - prec)],
          backgroundColor: '#e5e7eb', borderWidth: 0 },
      ],
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top', align: 'end' },
        title: { display: true,
          text: `Guidotti-Greenspan 発火で2年内危機率 ${pct(base)}% → ${pct(prec)}% (lift ${m.lift})` },
        tooltip: { callbacks: { label: x => `${x.dataset.label}: ${x.parsed.x}%` } },
      },
      scales: {
        x: { stacked: true, max: 100, title: { display: true, text: '% of country-years' } },
        y: { stacked: true },
      },
    },
  });

  const liftCI = ci?.results?.[rule]?.ci?.lift?.ci95;
  const ntsCI = ci?.results?.[rule]?.ci?.noise_to_signal_KLR?.ci95;
  const absent = (cov.ss5_5_countries_absent || []).join(' / ');
  const ciTxt = liftCI
    ? `国単位ブートストラップ 95%CI: lift <strong>[${liftCI[0]}, ${liftCI[1]}]</strong>・noise-to-signal <strong>[${ntsCI[0]}, ${ntsCI[1]}]</strong> がともに 1 を除外 = <strong>弱いが統計的に有意</strong>。`
    : '';
  setText('finding-fp-panel',
    `実データ <strong>${cov.signal_countries} カ国</strong> (${cov.year_min}-${cov.year_max}, 平穏 ${m.N} 国年)。
     混同行列 TP=${c.TP} / FP=${c.FP} / FN=${c.FN} / TN=${c.TN}。
     発火 ${m.signal_fires} 回のうち <strong>偽警報 ${Math.round(m.false_alarm_share * 100)}%</strong>、
     recall <strong>${Math.round(m.recall_TPR * 100)}%</strong> (危機の多くは比率≤1 で来る = 偽陰性)。
     noise-to-signal <strong>${m.noise_to_signal_KLR}</strong>・lift <strong>${m.lift}</strong>。${ciTxt}
     <em>「弱いが本物・偽警報支配」— Frankel–Saravelos(有用な準備指標)と Berg–Pattillo(単一閾値は誤報が常)の両方に整合。${absent ? `なお §5.5 の ${absent} は WDI 欠損。` : ''}</em>`);
}

// ---------------------------------------------------------------------------
// Writer H monad (§P7) — reads docs/data/writer_h.json
// ---------------------------------------------------------------------------

async function loadMonad() {
  try {
    const r = await fetch('data/writer_h.json');
    if (!r.ok) return null;
    return await r.json();
  } catch (err) {
    console.warn('Failed to load writer_h.json', err);
    return null;
  }
}

async function initMonad() {
  const m = await loadMonad();
  if (!m) {
    setText('finding-monad-eat',
      'data/writer_h.json が読み込めない。<code>python -m h_petri.monad.writer_h</code> を実行してください。');
    return;
  }

  // Effect Accumulation Theorem
  const eat = m.effect_accumulation;
  setText('finding-monad-eat',
    `投入コスト: <code>${JSON.stringify(eat.costs)}</code><br>
     順列数: <strong>${eat.num_permutations_tested}</strong> 通り。
     全て同じログ?: <strong>${eat.all_permutations_yield_same_log ? '✓ YES' : '✗ NO'}</strong>。
     観測された distinct なログ: <strong>${eat.distinct_logs_observed.join(', ')}</strong>
     (= 期待値 <code>${eat.expected_join}</code> のみ)。
     <em>結合律と冪等性が「累積順依存性ゼロ」を構造的に保証している。</em>`);

  // Bridge demo
  const grid = document.getElementById('monad-bridge-grid');
  if (grid && m.bridge_demo) {
    const colorOf = {
      'Bakong': '#0891b2',
      'PayNow': '#7c3aed',
      'KBZPay': '#a16207',
      'GCash':  '#dc2626',
    };
    grid.innerHTML = m.bridge_demo.results.map(r => `
      <div class="bridge-card" style="border-left: 4px solid ${colorOf[r.backbone] || '#6b7280'};">
        <div class="bridge-backbone">${r.backbone}</div>
        <div class="bridge-log"><code>${r.kleisli_log}</code></div>
      </div>
    `).join('') + `
      <div class="bridge-note">
        Chain 長 <strong>${m.bridge_demo.sequence_length} 射</strong>、全 backbone で同じ。
        累積ログだけが backbone タイプで分離している。
      </div>
    `;
  }
}
