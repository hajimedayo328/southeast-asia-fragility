/* Petri net page — visualize H-Petri Net simulation results.
 *
 * Reads docs/data/petri_comparison.json (output of `python -m h_petri.compare`)
 * and renders TrustHub / SystemicLoad rank curves for Bakong vs GCash.
 */

const RANK_LABELS = ['⊥', '⊤_priv', '⊤_bank', '⊤_pub'];

const PETRI_COLORS = {
  bakong: '#0891b2',  // cyan (central bank)
  gcash:  '#dc2626',  // red (private platform)
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

function makeRankChart(canvasId, bakongRanks, gcashRanks, opts = {}) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  const steps = bakongRanks.map((_, i) => i);
  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: steps,
      datasets: [
        {
          label: 'Bakong (中央銀行型, KH)',
          data: bakongRanks,
          borderColor: PETRI_COLORS.bakong,
          backgroundColor: PETRI_COLORS.bakong + '33',
          borderWidth: 2.5,
          pointRadius: 4,
          pointHoverRadius: 6,
          stepped: true,
          tension: 0,
        },
        {
          label: 'GCash (民間プラットフォーム型, PH)',
          data: gcashRanks,
          borderColor: PETRI_COLORS.gcash,
          backgroundColor: PETRI_COLORS.gcash + '33',
          borderWidth: 2.5,
          pointRadius: 4,
          pointHoverRadius: 6,
          stepped: true,
          tension: 0,
        },
      ],
    },
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

  const bakong = data.bakong;
  const gcash = data.gcash;

  // Trust curve
  makeRankChart('chart-petri-trust', bakong.trust_curve_ranks, gcash.trust_curve_ranks, {
    yLabel: 'TrustHub Heyting値の階数',
  });

  const trustStep = bakong.trust_reached_T_PUB_at_step;
  setText(
    'finding-petri-trust',
    `Bakong は step ${trustStep} で <strong>⊤_pub</strong> (rank 3) に到達し維持。
     GCash は何回送金しても <strong>⊤_priv</strong> (rank 1) で頭打ち。
     ${data.config.num_transactions} 回送金 (${bakong.steps} 遷移発火) で確認。
     最終値: Bakong=${bakong.final_invisible.TrustHub} / GCash=${gcash.final_invisible.TrustHub}。`
  );

  // Systemic load curve
  makeRankChart('chart-petri-load', bakong.systemic_load_curve_ranks, gcash.systemic_load_curve_ranks, {
    yLabel: 'SystemicLoad Heyting値の階数',
  });

  setText(
    'finding-petri-load',
    `Bakong は Reconciliation 遷移発火で <strong>⊤_bank</strong> (rank 2) まで上昇 — リアルタイム清算が銀行レベルの整合性を生む。
     GCash は <strong>⊤_priv</strong> (rank 1) 止まり — バッチ清算で民間レベルの整合性。
     最終値: Bakong=${bakong.final_invisible.SystemicLoad} / GCash=${gcash.final_invisible.SystemicLoad}。`
  );
})();
