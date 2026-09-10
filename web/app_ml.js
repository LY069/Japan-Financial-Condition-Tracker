/* =========================================================================
   Japan Monetary & Liquidity Conditions Tracker — dashboard logic
   Renders monetary conditions (MCI) and liquidity conditions (LCI) from
   window.ML_DATA (injected by data_ml.js); falls back to fetch('data_ml.json').
   Mirrors the helpers and conventions of app.js (Financial Conditions page).
   Requires Chart.js (loaded from CDN before this file).
   ========================================================================= */
(function () {
  "use strict";

  /* ----------------------------------------------------------------------
     Constants & shared palette (mirror styles.css / app.js)
     ---------------------------------------------------------------------- */
  var COLORS = {
    navy: "#1F3864", navySoft: "#2c4a7c", slate: "#4a5568", line: "#e2e6ee",
    green: "#1f8a55", amber: "#c98a16", red: "#c0392b",
    greenSoft: "rgba(31,138,85,.12)", redSoft: "rgba(192,57,43,.12)",
    navyFaint: "rgba(31,56,100,.06)"
  };

  // Score thresholds (positive = easier / more liquid). Identical to app.js.
  var POS = 0.15;   // >= POS  -> easy / liquid (green)
  var NEG = -0.15;  // <  NEG  -> tight / scarce (red); between -> neutral (amber)

  var MON_KEYS = ["mon_rates", "mon_money_credit", "mon_fx", "mon_balance_sheet"];
  var LIQ_KEYS = ["liq_cb", "liq_funding", "liq_market"];

  /* ----------------------------------------------------------------------
     Reusable helpers
     ---------------------------------------------------------------------- */
  function scoreClass(score) {
    if (score == null || isNaN(score)) return "neu";
    if (score >= POS) return "pos";
    if (score < NEG) return "neg";
    return "neu";
  }
  function colorByScore(score) {
    var c = scoreClass(score);
    return c === "pos" ? COLORS.green : c === "neg" ? COLORS.red : COLORS.amber;
  }
  function labelByScore(score) {
    var c = scoreClass(score);
    return c === "pos" ? "Accommodative" : c === "neg" ? "Restrictive" : "Broadly neutral";
  }

  // Number formatting helpers ------------------------------------------------
  // Typographic minus for readouts (e.g. "−30 bp").
  function num(v, dp) { return Number(v).toFixed(dp).replace("-", "−"); }
  function fmtSignedScore(v) {
    if (v == null || isNaN(v)) return "—";
    return (v >= 0 ? "+" : "") + num(v, 2);
  }
  function fmtPct(v, dp) {
    if (v == null || isNaN(v)) return "—";
    return num(v, dp == null ? 2 : dp) + "%";
  }
  // Unit-aware value formatting. "pp" is a display unit for spread series whose
  // stored unit is "percent" but whose name is tagged "(pp)".
  function fmtValue(v, unit) {
    if (v == null || isNaN(v)) return "—";
    switch (unit) {
      case "percent":
      case "percent_yoy":  return num(v, 2) + "%";
      case "pp":           return num(v, 2) + " pp";
      case "bp":           return num(v, 0) + " bp";
      case "di_points":    return (v > 0 ? "+" : "") + num(v, 0) + " pts";
      case "yen_per_usd":  return "¥" + num(v, 2);
      case "index":        return num(v, 1);
      default:             return num(v, 2);
    }
  }
  function unitLabel(unit) {
    return ({
      percent: "%", percent_yoy: "% y/y", di_points: "DI points", bp: "bp", pp: "pp",
      yen_per_usd: "¥ / USD", index: "index"
    })[unit] || unit || "";
  }
  // Display unit for a series object (spreads stored as percent are shown as pp).
  function seriesUnit(s) {
    if (!s) return "";
    if (s.unit === "percent" && /\bpp\)/.test(s.name || "")) return "pp";
    return s.unit;
  }

  // Apply a score class to a [data-role="chip"] element + set its text.
  function paintChip(el, score, text) {
    if (!el) return;
    el.classList.remove("pos", "neu", "neg");
    el.classList.add(scoreClass(score));
    el.textContent = text != null ? text : fmtSignedScore(score);
  }

  // Direction (momentum) chip: ▲ easing / ▼ tightening / → stable (as app.js).
  function dirChip(dir) {
    if (!dir || dir.label == null || dir.label === "n/a") return "";
    var map = { Easing: ["dir-pos", "▲"], Tightening: ["dir-neg", "▼"], Stable: ["dir-neu", "→"] };
    var m = map[dir.label] || ["dir-neu", "→"];
    var d = dir.delta == null ? "" : (dir.delta >= 0 ? "+" : "") + Number(dir.delta).toFixed(2);
    var since = dir.lag_date ? " since " + String(dir.lag_date).slice(0, 7) : "";
    return '<span class="dirchip ' + m[0] + '" title="6-month change in score: ' + d + since +
      '">' + m[1] + " " + dir.label + "</span>";
  }

  function dates(pairs) { return (pairs || []).map(function (p) { return p[0]; }); }
  function values(pairs) { return (pairs || []).map(function (p) { return p[1]; }); }

  // Map an observations array onto a given label (date) axis by date, so series
  // of different lengths/ranges never misalign by index. Missing -> null.
  function alignTo(labels, pairs) {
    var m = {};
    (pairs || []).forEach(function (p) { m[p[0]] = p[1]; });
    return labels.map(function (L) { return L in m ? m[L] : null; });
  }
  // Union of dates across several observation arrays, sorted.
  function unionDates() {
    var set = {};
    for (var i = 0; i < arguments.length; i++) {
      (arguments[i] || []).forEach(function (p) { set[p[0]] = 1; });
    }
    return Object.keys(set).sort();
  }

  /* ----------------------------------------------------------------------
     Chart.js shared defaults
     ---------------------------------------------------------------------- */
  function applyChartDefaults() {
    if (!window.Chart) return;
    Chart.defaults.font.family =
      '"Segoe UI","Helvetica Neue",Helvetica,Arial,system-ui,sans-serif';
    Chart.defaults.font.size = 12;
    Chart.defaults.color = COLORS.slate;
    Chart.defaults.plugins.legend.labels.boxWidth = 12;
    Chart.defaults.plugins.legend.labels.usePointStyle = true;
    Chart.defaults.plugins.tooltip.boxPadding = 6;
  }

  // Category (string-date) axis — no date adapter needed; ticks thinned.
  function timeScale(extra) {
    return Object.assign({
      type: "category",
      grid: { display: false },
      ticks: {
        autoSkip: true, maxTicksLimit: 8, maxRotation: 0,
        callback: function (val) {
          var lbl = this.getLabelForValue(val);
          return lbl ? String(lbl).slice(0, 7) : lbl; // YYYY-MM
        }
      }
    }, extra || {});
  }
  function yScale(extra) {
    return Object.assign({
      grid: { color: COLORS.line },
      border: { display: false }
    }, extra || {});
  }
  var baseLineOpts = {
    responsive: true, maintainAspectRatio: false,
    interaction: { mode: "index", intersect: false },
    elements: { point: { radius: 0, hoverRadius: 4 }, line: { borderWidth: 2 } }
  };
  function lineDS(label, data, color, width) {
    return {
      label: label, data: data, borderColor: color,
      backgroundColor: color, borderWidth: width || 2,
      pointRadius: 0, tension: .15, fill: false, spanGaps: true
    };
  }

  // Generic multi-series chart on a SHARED date axis. Every dataset is mapped
  // onto the union of all member dates by date (never by index), so series of
  // different start dates / frequencies (monthly vs quarterly) stay aligned.
  //   specs: [{ id, label, color, axis:'y'|'y2'|'y3', type:'line'|'bar', dash }]
  //   opts:  { yTitle, y2Title, y3Title, zero (bool), type ('line'|'bar' base) }
  // y2 and y3 are both right-hand axes (Chart.js stacks them side by side), so
  // series with very different magnitudes can share one panel legibly.
  function multiSeriesChart(canvasId, data, specs, opts) {
    var S = data.series; opts = opts || {};
    var live = specs.filter(function (sp) { return S[sp.id]; });
    if (!live.length) return null;
    var labels = unionDates.apply(null, live.map(function (sp) { return S[sp.id].observations; }));
    var hasY2 = false, hasY3 = false;
    var ds = live.map(function (sp) {
      var s = S[sp.id];
      var d = lineDS(sp.label || s.name, alignTo(labels, s.observations), sp.color, sp.width);
      d._unit = seriesUnit(s);
      if (sp.axis === "y2") { d.yAxisID = "y2"; hasY2 = true; }
      if (sp.axis === "y3") { d.yAxisID = "y3"; hasY3 = true; }
      if (sp.dash) d.borderDash = sp.dash;
      if (sp.type === "bar") {
        d.type = "bar"; d.backgroundColor = sp.color; d.borderWidth = 0;
        d.barPercentage = 0.9; d.categoryPercentage = 1.0;
      }
      return d;
    });
    var scales = { x: timeScale(), y: yScale({ title: { display: !!opts.yTitle, text: opts.yTitle || "" } }) };
    if (hasY2) scales.y2 = yScale({
      position: "right", grid: { drawOnChartArea: false },
      title: { display: !!opts.y2Title, text: opts.y2Title || "" }
    });
    if (hasY3) scales.y3 = yScale({
      position: "right", grid: { drawOnChartArea: false },
      title: { display: !!opts.y3Title, text: opts.y3Title || "" }
    });
    return new Chart(document.getElementById(canvasId), {
      type: opts.type || "line",
      data: { labels: labels, datasets: ds },
      options: Object.assign({}, baseLineOpts, {
        plugins: {
          legend: { position: "bottom" },
          annotationZero: !!opts.zero,
          tooltip: { callbacks: { label: function (c) {
            return c.dataset.label + ": " + fmtValue(c.parsed.y, c.dataset._unit); } } }
        },
        scales: scales
      })
    });
  }

  /* ----------------------------------------------------------------------
     Section renderers
     ---------------------------------------------------------------------- */

  // 1: Header ----------------------------------------------------------------
  function renderHeader(data) {
    var meta = data.meta, h = data.headline;
    setText("dash-title", meta.title);
    setText("framework-line", meta.framework);
    setText("asof-date", h.latest_date || meta.latest_date);
    setText("data-mode-badge", meta.data_mode);
    setText("source-note", meta.source_note);
    setText("score-window", meta.score_window);
    setText("gen-stamp", "Generated " + (meta.generated_utc || "").replace("T", " ").slice(0, 16) + " UTC");
  }

  // 2: Hero gauges + combined chip -------------------------------------------
  function drawGauge(canvasId, score) {
    // Semicircle gauge built on a doughnut. Scale −3 … +3 (as app.js).
    var lo = -3, hi = 3, span = hi - lo;
    var clamped = Math.max(lo, Math.min(hi, score == null ? 0 : score));
    var filled = ((clamped - lo) / span) * 100;
    new Chart(document.getElementById(canvasId), {
      type: "doughnut",
      data: { datasets: [{
        data: [filled, 100 - filled],
        backgroundColor: [colorByScore(score), "#edf0f6"], borderWidth: 0
      }] },
      options: {
        responsive: true, maintainAspectRatio: false,
        rotation: -90, circumference: 180, cutout: "72%",
        plugins: { legend: { display: false }, tooltip: { enabled: false } }
      }
    });
  }
  function renderGauges(data) {
    var h = data.headline;
    [
      { canvas: "mciGauge", score: h.mci_score, label: h.mci_label, dir: h.mci_direction, pre: "mci" },
      { canvas: "lciGauge", score: h.lci_score, label: h.lci_label, dir: h.lci_direction, pre: "lci" }
    ].forEach(function (g) {
      setText(g.pre + "-score", fmtSignedScore(g.score));
      var lblEl = document.getElementById(g.pre + "-label");
      if (lblEl) {
        lblEl.textContent = g.label || labelByScore(g.score);
        lblEl.style.color = colorByScore(g.score);
      }
      setHTML(g.pre + "-dir", dirChip(g.dir));
      drawGauge(g.canvas, g.score);
    });

    // Combined MLCI chip
    var sEl = document.getElementById("mlci-score");
    if (sEl) { sEl.textContent = fmtSignedScore(h.mlci_score); sEl.style.color = colorByScore(h.mlci_score); }
    paintChip(qChip("mlci-chip"), h.mlci_score, h.mlci_label || labelByScore(h.mlci_score));
    setHTML("mlci-dir", dirChip(h.mlci_direction));
  }

  function renderMetricCards(data) {
    var h = data.headline, S = data.series;
    var sc = function (id) { return S[id] ? scoreClass(S[id].score) : "neu"; };
    var cards = [
      { label: "Policy rate", value: fmtPct(h.policy_rate), sub: "overnight call rate target", cls: "neu" },
      { label: "Real policy rate (ex-post)", value: fmtPct(h.real_policy_rate_xp),
        sub: "policy − realized core CPI (" + fmtPct(h.core_cpi_yoy, 1) + " y/y)", cls: sc("real_policy_rate_xp") },
      { label: "M2 (y/y)", value: fmtPct(h.m2_yoy, 1), sub: "money stock", cls: sc("m2_yoy") },
      { label: "REER (2020=100)", value: fmtValue(h.reer, "index"), sub: "BIS broad; lower = weaker yen", cls: sc("reer") },
      { label: "BoJ assets (y/y)", value: fmtPct(h.boj_assets_yoy, 1), sub: "total balance sheet", cls: sc("boj_assets_yoy") },
      { label: "Monetary base (y/y)", value: fmtPct(h.monetary_base_yoy, 1), sub: "central-bank liquidity", cls: sc("monetary_base_yoy") },
      { label: "3m TIBOR–OIS", value: fmtValue(h.tibor_ois_3m, "pp"), sub: "bank funding premium", cls: sc("tibor_ois_3m") },
      { label: "USD/JPY basis (3m)", value: fmtValue(h.jpy_basis_3m, "bp"), sub: "cross-currency basis", cls: sc("jpy_basis_3m") },
      { label: "JGB market functioning DI", value: fmtValue(h.jgb_market_functioning_di, "di_points"),
        sub: "BoJ Bond Market Survey", cls: sc("jgb_market_functioning_di") },
      { label: "BoJ share of JGBs", value: fmtPct(h.boj_jgb_share, 1), sub: "of outstanding JGBs", cls: sc("boj_jgb_share") }
    ];
    document.getElementById("metric-cards").innerHTML = cards.map(function (c) {
      return '<div class="metric ' + c.cls + '">' +
        '<span class="metric-label">' + c.label + '</span>' +
        '<span class="metric-value sm">' + c.value + '</span>' +
        '<span class="metric-sub">' + c.sub + '</span></div>';
    }).join("");
    setText("assessment-text", h.assessment);
  }

  // 3/4: Stage chip + axis cards (shared by monetary & liquidity) -----------
  function renderStageChip(data, stageKey, prefix) {
    var s = data.stages[stageKey];
    if (!s) return;
    paintChip(qChip(prefix + "-score-chip"), s.score, fmtSignedScore(s.score));
    setText(prefix + "-label", s.label_text);
    setHTML(prefix + "-dir", dirChip(s.direction));
  }

  function renderAxisCards(data, containerId, keys) {
    var container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = "";
    var axisByKey = {};
    data.axes.forEach(function (a) { axisByKey[a.key] = a; });

    keys.forEach(function (key) {
      var axis = axisByKey[key];
      if (!axis) return;
      var cls = scoreClass(axis.score);

      var members = axis.members.map(function (id) {
        var s = data.series[id];
        if (!s) return "";
        var chip = s.score == null ? "" :
          '<span class="chip ' + scoreClass(s.score) + ' member-chip">' + fmtSignedScore(s.score) + '</span>';
        return '<li><span class="member-name">' + s.name + '</span>' +
          '<span class="member-val">' + fmtValue(s.latest_value, seriesUnit(s)) + '</span>' +
          chip + dirChip(s.direction) + '</li>';
      }).join("");

      var card = document.createElement("div");
      card.className = "card axis-card";
      card.innerHTML =
        '<div class="card-head"><h3>' + axis.label + '</h3>' +
          '<span class="chip ' + cls + '">' + fmtSignedScore(axis.score) + '</span></div>' +
        '<p class="note" style="margin-top:0;border:0;padding:0;color:var(--slate)">' +
          axis.label_text + dirChip(axis.direction) + '</p>' +
        '<p class="axis-desc">' + (axis.desc || "") + '</p>' +
        '<div class="axis-spark"><canvas></canvas></div>' +
        '<ul class="axis-members">' + members + '</ul>';
      container.appendChild(card);

      // sparkline of the axis indicator series
      var spark = data.indicator_series["axis::" + key] || [];
      new Chart(card.querySelector("canvas"), {
        type: "line",
        data: {
          labels: dates(spark),
          datasets: [{
            data: values(spark),
            borderColor: colorByScore(axis.score), borderWidth: 1.8,
            pointRadius: 0, tension: .25,
            fill: true, backgroundColor: cls === "neg" ? COLORS.redSoft : COLORS.greenSoft
          }]
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          plugins: { legend: { display: false }, tooltip: {
            callbacks: { title: function (t) { return t[0].label; },
              label: function (c) { return fmtSignedScore(c.parsed.y); } } } },
          scales: { x: { display: false }, y: { display: false } }
        }
      });
    });
  }

  // 4: Monetary conditions charts -------------------------------------------
  function renderMonetary(data) {
    renderStageChip(data, "ml_monetary", "mon");
    renderAxisCards(data, "mon-axis-cards", MON_KEYS);

    // (a) money & credit — three monthly series, shared date axis
    multiSeriesChart("moneyCreditChart", data, [
      { id: "m2_yoy", label: "M2", color: COLORS.navy },
      { id: "m3_yoy", label: "M3", color: COLORS.amber },
      { id: "bank_lending_yoy", label: "Bank lending", color: COLORS.green }
    ], { yTitle: "% y/y", zero: true });

    // (b) exchange rate — REER (left) vs USD/JPY (right); USD/JPY starts 2004
    multiSeriesChart("fxChart", data, [
      { id: "reer", label: "REER (2020=100)", color: COLORS.navy },
      { id: "usdjpy", label: "USD/JPY", color: COLORS.red, axis: "y2", dash: [4, 3] }
    ], { yTitle: "index", y2Title: "¥ / USD" });

    // (c) balance sheet — BoJ assets and monetary base
    multiSeriesChart("balanceSheetChart", data, [
      { id: "boj_assets_yoy", label: "BoJ total assets", color: COLORS.navy },
      { id: "monetary_base_yoy", label: "Monetary base", color: COLORS.amber }
    ], { yTitle: "% y/y", zero: true });

    // (d) real short-rate stance — 2004+ policy rate vs 1974+ 1Y, aligned by date
    multiSeriesChart("realRateChart", data, [
      { id: "real_policy_rate_xp", label: "Real policy rate", color: COLORS.navy, width: 2.5 },
      { id: "real_1y_xp", label: "Real 1Y rate", color: COLORS.green }
    ], { yTitle: "%", zero: true });
  }

  // 5: Liquidity conditions charts ------------------------------------------
  function renderLiquidity(data) {
    renderStageChip(data, "ml_liquidity", "liq");
    renderAxisCards(data, "liq-axis-cards", LIQ_KEYS);

    // (a) funding — spreads in pp (left) with USD/JPY basis in bp (right)
    multiSeriesChart("fundingChart", data, [
      { id: "tibor_ois_3m", label: "3m TIBOR–OIS", color: COLORS.navy },
      { id: "call_policy_spread", label: "Call rate − target", color: COLORS.amber },
      { id: "jpy_basis_3m", label: "USD/JPY 3m basis", color: COLORS.red, axis: "y2", dash: [4, 3] }
    ], { yTitle: "pp", y2Title: "bp", zero: true });

    // (b) market functioning — quarterly DI bars (2015+), quarterly BoJ share
    //     (2005+, right) and the monthly 10s30s slope (1999+, second right axis
    //     because ~1 pp would be invisible on the % share axis). All by date.
    multiSeriesChart("marketFunctioningChart", data, [
      { id: "jgb_market_functioning_di", label: "JGB functioning DI", color: COLORS.navySoft, type: "bar" },
      { id: "boj_jgb_share", label: "BoJ share of JGBs", color: COLORS.red, axis: "y2" },
      { id: "jgb_10s30s", label: "10s30s slope", color: COLORS.amber, axis: "y3", dash: [4, 3] }
    ], { type: "bar", yTitle: "DI points", y2Title: "% of JGBs", y3Title: "pp", zero: true });

    // (c) bid-ask (index, left) with Nikkei VI (%) and 10Y realized vol (bp) on
    //     the right — VI and vol are of comparable magnitude; vol starts 1987.
    multiSeriesChart("marketVolChart", data, [
      { id: "jgb_bid_ask", label: "10y JGB bid-ask", color: COLORS.navy },
      { id: "nikkei_vi", label: "Nikkei VI (%)", color: COLORS.amber, axis: "y2" },
      { id: "jgb_10y_vol", label: "10Y JGB realized vol (bp)", color: COLORS.red, axis: "y2", dash: [4, 3] }
    ], { yTitle: "normalized ticks", y2Title: "% / bp" });
  }

  // 6: Composite history ----------------------------------------------------
  function renderCompositeHistory(data) {
    var I = data.indicator_series;
    var labels = unionDates(I.mci, I.lci, I.mlci);
    var mlci = alignTo(labels, I.mlci);
    var posVals = mlci.map(function (v) { return v != null && v >= 0 ? v : null; });
    var negVals = mlci.map(function (v) { return v != null && v < 0 ? v : null; });

    new Chart(document.getElementById("compositeChart"), {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          { label: "MLCI (easy)", data: posVals, borderColor: COLORS.green, borderWidth: 0,
            pointRadius: 0, fill: "origin", backgroundColor: COLORS.greenSoft, spanGaps: false },
          { label: "MLCI (tight)", data: negVals, borderColor: COLORS.red, borderWidth: 0,
            pointRadius: 0, fill: "origin", backgroundColor: COLORS.redSoft, spanGaps: false },
          lineDS("MCI — monetary", alignTo(labels, I.mci), COLORS.amber, 1.6),
          lineDS("LCI — liquidity", alignTo(labels, I.lci), COLORS.navySoft, 1.6),
          lineDS("MLCI — combined", mlci, COLORS.navy, 2.5)
        ]
      },
      options: Object.assign({}, baseLineOpts, {
        plugins: {
          legend: { position: "bottom",
            labels: { filter: function (it) { return it.text.indexOf("MLCI (") !== 0; } } },
          tooltip: {
            filter: function (it) { return it.dataset.label.indexOf("MLCI (") !== 0; },
            callbacks: { label: function (c) { return c.dataset.label + ": " + fmtSignedScore(c.parsed.y); } }
          },
          annotationZero: true
        },
        scales: {
          x: timeScale(),
          y: yScale({ title: { display: true, text: "z-score (+ easier / more liquid)" },
            grid: { color: function (c) { return c.tick.value === 0 ? COLORS.slate : COLORS.line; } } })
        }
      })
    });
  }

  // 7: Axis comparison bar --------------------------------------------------
  function renderAxisBar(data) {
    var axisByKey = {};
    data.axes.forEach(function (a) { axisByKey[a.key] = a; });
    var order = (data.meta.axis_order && data.meta.axis_order.length) ? data.meta.axis_order
      : MON_KEYS.concat(LIQ_KEYS);
    var axes = order.map(function (k) { return axisByKey[k]; }).filter(Boolean);
    var stageShort = function (a) {
      return a.stage === "ml_monetary" ? "Monetary" : a.stage === "ml_liquidity" ? "Liquidity" : "";
    };
    new Chart(document.getElementById("axisBarChart"), {
      type: "bar",
      data: {
        labels: axes.map(function (a) { return [a.label, stageShort(a)]; }),
        datasets: [{
          data: axes.map(function (a) { return a.score; }),
          backgroundColor: axes.map(function (a) { return colorByScore(a.score); }),
          borderRadius: 4, barThickness: 22
        }]
      },
      options: {
        indexAxis: "y", responsive: true, maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: {
            title: function (t) { var a = axes[t[0].dataIndex]; return a.label + " · " + stageShort(a); },
            label: function (c) {
              var a = axes[c.dataIndex];
              return fmtSignedScore(c.parsed.x) + "  (" + (a.label_text || labelByScore(c.parsed.x)) + ")";
            } } }
        },
        scales: {
          x: yScale({ title: { display: true, text: "score (+ easier / more liquid)" },
            grid: { color: function (c) { return c.tick.value === 0 ? COLORS.slate : COLORS.line; } } }),
          y: { grid: { display: false }, ticks: { autoSkip: false } }
        }
      }
    });
  }

  // 9: Explore series -------------------------------------------------------
  function renderExplore(data) {
    var select = document.getElementById("series-select");
    var ids = Object.keys(data.series);

    // Group options: monetary axes, liquidity axes, then context.
    var groupOf = {};
    data.axes.forEach(function (a) {
      a.members.forEach(function (id) {
        groupOf[id] = a.stage === "ml_monetary" ? "Monetary conditions" : "Liquidity conditions";
      });
    });
    var groups = { "Monetary conditions": [], "Liquidity conditions": [], "Context": [] };
    ids.forEach(function (id) { groups[groupOf[id] || "Context"].push(id); });
    Object.keys(groups).forEach(function (g) {
      if (!groups[g].length) return;
      var og = document.createElement("optgroup");
      og.label = g;
      groups[g].forEach(function (id) {
        var opt = document.createElement("option");
        opt.value = id; opt.textContent = data.series[id].name;
        og.appendChild(opt);
      });
      select.appendChild(og);
    });

    var chart = null;
    function draw(id) {
      var s = data.series[id];
      if (!s) return;
      var u = seriesUnit(s);
      var meta = document.getElementById("explore-meta");
      var srcLink = s.source_url
        ? '<a href="' + s.source_url + '" target="_blank" rel="noopener">' + s.source + '</a>'
        : s.source;
      var scoreBit = s.score == null ? "" :
        '<span><b>Score:</b> <span class="chip ' + scoreClass(s.score) + '">' +
        fmtSignedScore(s.score) + " · " + (s.accommodation || labelByScore(s.score)) +
        "</span>" + dirChip(s.direction) + "</span>";
      meta.innerHTML =
        '<span class="em-name">' + s.name + '</span>' +
        '<span><b>Latest:</b> ' + fmtValue(s.latest_value, u) + " (" + (s.latest_date || "") + ")</span>" +
        '<span><b>Unit:</b> ' + unitLabel(u) + '</span>' +
        '<span><b>Frequency:</b> ' + (s.frequency || "—") + '</span>' +
        '<span><b>History from:</b> ' + (s.history_start || "—") + '</span>' +
        '<span><b>Source:</b> ' + srcLink + '</span>' + scoreBit;
      setText("explore-notes", s.notes || "");

      var color = s.score == null ? COLORS.navy : colorByScore(s.score);
      var cfg = {
        type: "line",
        data: {
          labels: dates(s.observations),
          datasets: [{
            label: s.name, data: values(s.observations),
            borderColor: color, borderWidth: 2, pointRadius: 0, tension: .15,
            fill: true, backgroundColor: COLORS.navyFaint
          }]
        },
        options: Object.assign({}, baseLineOpts, {
          plugins: { legend: { display: false }, tooltip: {
            callbacks: { label: function (c) { return fmtValue(c.parsed.y, u); } } } },
          scales: { x: timeScale(), y: yScale({ title: { display: true, text: unitLabel(u) } }) }
        })
      };
      if (chart) chart.destroy();
      chart = new Chart(document.getElementById("exploreChart"), cfg);
    }

    select.addEventListener("change", function () { draw(select.value); });
    var initial = ids.indexOf("m2_yoy") >= 0 ? "m2_yoy" : ids[0];
    select.value = initial;
    draw(initial);
  }

  // 10: Methodology table — weights (ml_weight) & assumptions ---------------
  function renderMethodology(data) {
    var el = document.getElementById("methodology-table");
    if (!el) return;
    var axisByKey = {};
    data.axes.forEach(function (a) { axisByKey[a.key] = a; });
    var stageLabel = function (a) {
      var st = data.stages[a.stage];
      return st && st.label ? st.label : a.stage;
    };

    var listed = {}, groups = [];
    (data.meta.axis_order || []).forEach(function (k) {
      var ax = axisByKey[k];
      if (!ax) return;
      var rows = ax.members.map(function (id) { listed[id] = 1; return data.series[id]; }).filter(Boolean);
      if (rows.length) groups.push({ title: stageLabel(ax) + " — " + ax.label, axis: ax.label, rows: rows });
    });
    var ctx = Object.keys(data.series).filter(function (id) { return !listed[id]; })
      .map(function (id) { return data.series[id]; });
    if (ctx.length) groups.push({ title: "Context — not scored", axis: "—", rows: ctx });

    function polText(s, scored) {
      if (!scored || s.polarity == null || s.polarity === 0) return "context only";
      return s.polarity > 0 ? "higher ⇒ easier" : "higher ⇒ tighter";
    }
    function wtText(w) {
      return (w && w > 0) ? String(Number(w).toFixed(2)).replace(/\.00$/, "").replace(/0$/, "") : "—";
    }

    el.innerHTML = groups.map(function (g) {
      var scored = g.axis !== "—";
      var body = g.rows.map(function (s) {
        return "<tr><td>" + s.name + "</td><td>" + g.axis + '</td><td class="num">' +
          wtText(s.ml_weight) + "</td><td>" + polText(s, scored) +
          '</td><td class="src">' + (s.source || "") + '</td><td class="assump">' + (s.notes || "") + "</td></tr>";
      }).join("");
      return '<table class="method-tbl"><caption>' + g.title + "</caption>" +
        '<thead><tr><th>Indicator</th><th>Axis</th><th class="num">Weight</th><th>Polarity</th>' +
        "<th>Source</th><th>Assumption / definition</th></tr></thead><tbody>" + body + "</tbody></table>";
    }).join("");
  }

  /* ----------------------------------------------------------------------
     Small DOM helpers
     ---------------------------------------------------------------------- */
  function setText(id, txt) {
    var el = document.getElementById(id);
    if (el) el.textContent = (txt == null ? "—" : txt);
  }
  function setHTML(id, html) {
    var el = document.getElementById(id);
    if (el) el.innerHTML = html || "";
  }
  function qChip(wrapId) {
    var w = document.getElementById(wrapId);
    return w ? w.querySelector('[data-role="chip"]') : null;
  }

  /* ----------------------------------------------------------------------
     Zero-line plugin (draws a baseline at y=0 when plugins.annotationZero)
     ---------------------------------------------------------------------- */
  var zeroLinePlugin = {
    id: "annotationZero",
    afterDraw: function (chart) {
      if (!chart.options.plugins || !chart.options.plugins.annotationZero) return;
      var y = chart.scales.y; if (!y) return;
      if (0 < y.min || 0 > y.max) return;
      var yp = y.getPixelForValue(0), area = chart.chartArea, ctx = chart.ctx;
      ctx.save();
      ctx.strokeStyle = COLORS.slate; ctx.lineWidth = 1; ctx.setLineDash([3, 3]);
      ctx.beginPath(); ctx.moveTo(area.left, yp); ctx.lineTo(area.right, yp); ctx.stroke();
      ctx.restore();
    }
  };

  /* ----------------------------------------------------------------------
     Boot
     ---------------------------------------------------------------------- */
  function boot(data) {
    try {
      applyChartDefaults();
      if (window.Chart) Chart.register(zeroLinePlugin);
      renderHeader(data);
      renderGauges(data);
      renderMetricCards(data);
      renderMonetary(data);
      renderLiquidity(data);
      renderCompositeHistory(data);
      renderAxisBar(data);
      renderExplore(data);
      renderMethodology(data);
    } catch (err) {
      console.error("Dashboard render error:", err);
    }
  }

  function init() {
    if (window.ML_DATA) {
      boot(window.ML_DATA);
    } else {
      fetch("data_ml.json")
        .then(function (r) { return r.json(); })
        .then(boot)
        .catch(function (e) {
          console.error("Failed to load data_ml.json:", e);
          document.body.insertAdjacentHTML("afterbegin",
            '<p style="padding:20px;color:#c0392b">Could not load data. ' +
            'Open this page with data_ml.js present, or via a local server.</p>');
        });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
