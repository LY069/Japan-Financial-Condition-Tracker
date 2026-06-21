/* =========================================================================
   Japan Financial Conditions Tracker — dashboard logic
   Renders the BoJ two-stage assessment (Review 2026-E-4) from window.FCI_DATA.
   Loads data from the global injected by data.js; falls back to fetch().
   Requires Chart.js (loaded from CDN before this file).
   ========================================================================= */
(function () {
  "use strict";

  /* ----------------------------------------------------------------------
     Constants & shared palette (mirror styles.css)
     ---------------------------------------------------------------------- */
  var COLORS = {
    navy: "#1F3864", navySoft: "#2c4a7c", slate: "#4a5568", line: "#e2e6ee",
    green: "#1f8a55", amber: "#c98a16", red: "#c0392b",
    greenSoft: "rgba(31,138,85,.12)", redSoft: "rgba(192,57,43,.12)"
  };

  // Accommodation thresholds (positive = more accommodative).
  var POS = 0.15;   // >= POS  -> accommodative (green)
  var NEG = -0.15;  // <  NEG  -> restrictive  (red); between -> neutral (amber)

  /* ----------------------------------------------------------------------
     Reusable helpers
     ---------------------------------------------------------------------- */

  // Bucket a score into 'pos' | 'neu' | 'neg'.
  function scoreClass(score) {
    if (score == null || isNaN(score)) return "neu";
    if (score >= POS) return "pos";
    if (score < NEG) return "neg";
    return "neu";
  }
  // Hex color for a score, by convention.
  function colorByScore(score) {
    var c = scoreClass(score);
    return c === "pos" ? COLORS.green : c === "neg" ? COLORS.red : COLORS.amber;
  }
  // Human label for a score.
  function labelByScore(score) {
    var c = scoreClass(score);
    return c === "pos" ? "Accommodative" : c === "neg" ? "Restrictive" : "Broadly neutral";
  }

  // Number formatting helpers ------------------------------------------------
  function fmtSignedScore(v) {
    if (v == null || isNaN(v)) return "—";
    return (v >= 0 ? "+" : "") + v.toFixed(2);
  }
  function fmtPct(v, dp) {
    if (v == null || isNaN(v)) return "—";
    return v.toFixed(dp == null ? 2 : dp) + "%";
  }
  // Unit-aware value formatting for member / explore readouts.
  function fmtValue(v, unit) {
    if (v == null || isNaN(v)) return "—";
    switch (unit) {
      case "percent":
      case "percent_yoy":  return v.toFixed(2) + "%";
      case "di_points":    return (v >= 0 ? "+" : "") + v.toFixed(1) + " pts";
      case "yen_per_usd":  return "¥" + v.toFixed(2);
      case "index":        return v.toLocaleString(undefined, { maximumFractionDigits: 0 });
      default:             return v.toFixed(2);
    }
  }
  function unitLabel(unit) {
    return ({
      percent: "%", percent_yoy: "% y/y", di_points: "DI points",
      yen_per_usd: "¥ / USD", index: "index"
    })[unit] || unit || "";
  }

  // Apply a score class to a [data-role="chip"] element + set its text.
  function paintChip(el, score, text) {
    if (!el) return;
    el.classList.remove("pos", "neu", "neg");
    el.classList.add(scoreClass(score));
    el.textContent = text != null ? text : fmtSignedScore(score);
  }

  // Direction (momentum) chip: ▲ easing / ▼ tightening / → stable.
  function dirChip(dir) {
    if (!dir || dir.label == null || dir.label === "n/a") return "";
    var map = { Easing: ["dir-pos", "▲"], Tightening: ["dir-neg", "▼"], Stable: ["dir-neu", "→"] };
    var m = map[dir.label] || ["dir-neu", "→"];
    var d = dir.delta == null ? "" : (dir.delta >= 0 ? "+" : "") + Number(dir.delta).toFixed(2);
    var since = dir.lag_date ? " since " + String(dir.lag_date).slice(0, 7) : "";
    return '<span class="dirchip ' + m[0] + '" title="6-month change in score: ' + d + since +
      '">' + m[1] + " " + dir.label + "</span>";
  }
  // One gap readout for the natural-rate second read (negative = below = accommodative).
  function gapItem(label, v) {
    if (v == null || isNaN(v)) return "";
    var cls = v < 0 ? "pos" : v > 0 ? "neg" : "neu";
    return '<div class="nr-gap"><span class="nr-gap-val ' + cls + '">' +
      (v >= 0 ? "+" : "") + v.toFixed(2) + 'pp</span><span class="nr-gap-lbl">' + label + "</span></div>";
  }

  // Convert [[date,val],...] pairs into Chart.js {x,y} points (date kept as label).
  function toXY(pairs) {
    return (pairs || []).map(function (p) { return { x: p[0], y: p[1] }; });
  }
  function dates(pairs) { return (pairs || []).map(function (p) { return p[0]; }); }
  function values(pairs) { return (pairs || []).map(function (p) { return p[1]; }); }

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

  // A time-ish category axis. We use category scale (string dates) so no
  // date adapter is needed; ticks are thinned for readability.
  function timeScale(extra) {
    return Object.assign({
      type: "category",
      grid: { display: false },
      ticks: {
        autoSkip: true, maxTicksLimit: 8, maxRotation: 0,
        callback: function (val, idx) {
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

  /* ----------------------------------------------------------------------
     Section renderers
     ---------------------------------------------------------------------- */

  // 1 + 2: Header & hero -----------------------------------------------------
  function renderHeader(data) {
    var meta = data.meta, h = data.headline;
    setText("dash-title", meta.title);
    setText("framework-line", meta.framework);
    setText("asof-date", h.latest_date || meta.latest_date);
    setText("data-mode-badge", meta.data_mode);
    setText("source-note", meta.source_note);
    setText("gen-stamp", "Generated " + (meta.generated_utc || "").replace("T", " ").slice(0, 16) + " UTC");
  }

  function renderGauge(data) {
    var score = data.headline.fci_score;
    setText("gauge-score", fmtSignedScore(score));
    var lblEl = document.getElementById("gauge-label");
    lblEl.textContent = data.headline.fci_label || labelByScore(score);
    lblEl.style.color = colorByScore(score);
    var dEl = document.getElementById("gauge-dir");
    if (dEl) dEl.innerHTML = dirChip(data.headline.fci_direction);

    // Custom semicircle gauge built on a doughnut. Scale −3 … +3.
    var lo = -3, hi = 3, span = hi - lo;
    var clamped = Math.max(lo, Math.min(hi, score));
    var frac = (clamped - lo) / span;             // 0..1 across the arc
    var filled = frac * 100;

    new Chart(document.getElementById("fciGauge"), {
      type: "doughnut",
      data: {
        datasets: [{
          // value arc up to the needle, then a faint remainder
          data: [filled, 100 - filled],
          backgroundColor: [colorByScore(score), "#edf0f6"],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        rotation: -90, circumference: 180, cutout: "72%",
        plugins: { legend: { display: false }, tooltip: { enabled: false } }
      }
    });
  }

  function renderMetricCards(data) {
    var h = data.headline;
    var cards = [
      { label: "Policy rate", value: fmtPct(h.policy_rate), sub: "Overnight call rate", cls: "neu" },
      { label: "Real policy rate", value: fmtPct(h.real_policy_rate),
        sub: "policy − 1y exp. inflation", cls: scoreClass(-h.real_policy_rate) },
      { label: "Rate gap vs natural", value: fmtPct(h.rate_gap),
        sub: "real rate − midpoint (−0.15%)", cls: scoreClass(-h.rate_gap), band: true },
      { label: "Core CPI (y/y)", value: fmtPct(h.core_cpi_yoy), sub: "ex-fresh food", cls: "neu" },
      { label: "10Y JGB yield", value: fmtPct(h.jgb_10y), sub: "benchmark long rate", cls: "neu" }
    ];

    var html = cards.map(function (c) {
      var band = c.band ? bandViz(h) : "";
      return '<div class="metric ' + c.cls + '">' +
        '<span class="metric-label">' + c.label + '</span>' +
        '<span class="metric-value">' + c.value + '</span>' +
        '<span class="metric-sub">' + c.sub + '</span>' + band +
        '</div>';
    }).join("");
    document.getElementById("metric-cards").innerHTML = html;

    setText("assessment-text", h.assessment);
  }

  // Mini natural-rate band visualization (low..high, midpoint, current real rate).
  function bandViz(h) {
    var lo = h.natural_rate_low, mid = h.natural_rate_mid, hi = h.natural_rate_high;
    var now = h.real_policy_rate;
    // map a value within a padded [vmin, vmax] window to 0..100%
    var pad = 0.4;
    var vmin = Math.min(lo, now) - pad, vmax = Math.max(hi, now) + pad;
    var pos = function (v) {
      return Math.max(0, Math.min(100, ((v - vmin) / (vmax - vmin)) * 100));
    };
    var rangeL = pos(lo), rangeR = pos(hi);
    return '<div class="band-viz" title="Natural-rate band −0.85% … +0.55%, midpoint −0.15%">' +
      '<div class="band-track">' +
        '<span class="band-range" style="left:' + rangeL + '%;width:' + (rangeR - rangeL) + '%"></span>' +
        '<span class="band-mid" style="left:' + pos(mid) + '%"></span>' +
        '<span class="band-now" style="left:' + pos(now) + '%"></span>' +
      '</div>' +
      '<div class="band-legend"><span>band ' + lo.toFixed(2) + '</span>' +
      '<span>now ' + now.toFixed(2) + '</span><span>' + hi.toFixed(2) + '</span></div>' +
    '</div>';
  }

  // 3: Stage 1 ---------------------------------------------------------------
  function renderStage1(data) {
    var s = data.stages.stage1;
    paintChip(qChip("stage1-score-chip"), s.score, fmtSignedScore(s.score));
    setText("stage1-label", s.label_text);
    setHTML("stage1-dir", dirChip(s.direction));

    var S = data.series;
    // Real rates by maturity
    new Chart(document.getElementById("realRatesChart"), Object.assign({}, baseLineOpts, {
      type: "line",
      data: {
        labels: dates(S.real_1y.observations),
        datasets: [
          lineDS("Real 1Y", values(S.real_1y.observations), COLORS.green),
          lineDS("Real 3Y", values(S.real_3y.observations), COLORS.amber),
          lineDS("Real 10Y", values(S.real_10y.observations), COLORS.navy)
        ]
      },
      options: Object.assign({}, baseLineOpts, {
        plugins: { legend: { position: "bottom" }, annotationZero: true },
        scales: { x: timeScale(), y: yScale({ title: { display: true, text: "%" } }) }
      })
    }));

    // Policy rate + 10Y JGB
    new Chart(document.getElementById("policyChart"), Object.assign({}, baseLineOpts, {
      type: "line",
      data: {
        labels: dates(S.policy_rate.observations),
        datasets: [
          lineDS("Policy rate", values(S.policy_rate.observations), COLORS.navy),
          lineDS("10Y JGB", values(S.jgb_10y.observations), COLORS.red)
        ]
      },
      options: Object.assign({}, baseLineOpts, {
        plugins: { legend: { position: "bottom" } },
        scales: { x: timeScale(), y: yScale({ title: { display: true, text: "%" } }) }
      })
    }));
  }

  // 4: Natural rate ----------------------------------------------------------
  function renderNaturalRate(data) {
    var h = data.headline, S = data.series;
    paintChip(qChip("rate-gap-chip"), -h.rate_gap, fmtPct(h.rate_gap));

    // Second read (level-based): where the real policy rate sits in the band.
    var b = h.rstar_band, rd = document.getElementById("natrate-read");
    if (b && rd) {
      rd.innerHTML =
        '<div class="nr-read-main">' +
          '<span class="chip ' + scoreClass(b.band_score) + ' big">' + fmtSignedScore(b.band_score) + "</span>" +
          '<div><div class="nr-stance">' + b.stance + dirChip(b.direction) + "</div>" +
            '<div class="nr-sub">Real policy rate <strong>' + fmtPct(b.real_policy_rate) +
              "</strong> vs band " + fmtPct(b.low) + " … " + fmtPct(b.high) +
              " (midpoint " + fmtPct(b.mid) + ")</div></div>" +
        "</div>" +
        '<div class="nr-gaps">' +
          gapItem("vs lower bound", b.gap_to_low) +
          gapItem("vs midpoint", b.gap_to_mid) +
          gapItem("vs upper bound", b.gap_to_high) +
        "</div>";
    }

    var labels = dates(S.real_policy_rate.observations);
    new Chart(document.getElementById("natRateChart"), Object.assign({}, baseLineOpts, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          // band drawn as two stacked-style area lines (high w/ fill down to low)
          {
            label: "Natural-rate band (high)",
            data: values(S.natural_rate_high.observations),
            borderColor: "rgba(31,56,100,.35)", borderWidth: 1,
            borderDash: [4, 3], pointRadius: 0, fill: "+1",
            backgroundColor: "rgba(31,56,100,.08)"
          },
          {
            label: "Natural-rate band (low)",
            data: values(S.natural_rate_low.observations),
            borderColor: "rgba(31,56,100,.35)", borderWidth: 1,
            borderDash: [4, 3], pointRadius: 0, fill: false
          },
          {
            label: "Natural rate (midpoint)",
            data: values(S.natural_rate_mid.observations),
            borderColor: COLORS.slate, borderWidth: 1.5, pointRadius: 0,
            borderDash: [2, 2]
          },
          lineDS("Real policy rate", values(S.real_policy_rate.observations), COLORS.navy, 2.5)
        ]
      },
      options: Object.assign({}, baseLineOpts, {
        plugins: {
          legend: {
            position: "bottom",
            labels: { filter: function (it) { return it.text.indexOf("(low)") === -1; } }
          }
        },
        scales: { x: timeScale(), y: yScale({ title: { display: true, text: "%" } }) }
      })
    }));
  }

  // 5: Stage 2 axis cards ----------------------------------------------------
  function renderStage2(data) {
    var s = data.stages.stage2;
    paintChip(qChip("stage2-score-chip"), s.score, fmtSignedScore(s.score));
    setText("stage2-label", s.label_text);
    setHTML("stage2-dir", dirChip(s.direction));

    var container = document.getElementById("axis-cards");
    container.innerHTML = "";

    // Only the four Stage-2 axes (exclude real_rate which belongs to Stage 1).
    var stage2Keys = ["funding_costs", "availability", "asset_prices", "funding_volumes"];
    var axisByKey = {};
    data.axes.forEach(function (a) { axisByKey[a.key] = a; });

    stage2Keys.forEach(function (key) {
      var axis = axisByKey[key];
      if (!axis) return;
      var cls = scoreClass(axis.score);

      var members = axis.members.map(function (id) {
        var s = data.series[id];
        if (!s) return "";
        var mcls = scoreClass(s.score);
        var chip = s.score == null ? "" :
          '<span class="chip ' + mcls + ' member-chip">' + fmtSignedScore(s.score) + '</span>';
        return '<li><span class="member-name">' + s.name + '</span>' +
          '<span class="member-val">' + fmtValue(s.latest_value, s.unit) + '</span>' +
          chip + dirChip(s.direction) + '</li>';
      }).join("");

      var card = document.createElement("div");
      card.className = "card axis-card";
      card.innerHTML =
        '<div class="card-head"><h3>' + axis.label + '</h3>' +
          '<span class="chip ' + cls + '">' + fmtSignedScore(axis.score) + '</span></div>' +
        '<p class="note" style="margin-top:0;border:0;padding:0;color:var(--slate)">' +
          axis.label_text + dirChip(axis.direction) + '</p>' +
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

  // 6: Composite FCI history -------------------------------------------------
  function renderFciHistory(data) {
    var fci = data.indicator_series.fci || [];
    var vals = values(fci);
    // Color the fill above/below zero by splitting into pos/neg masked series.
    var posVals = vals.map(function (v) { return v >= 0 ? v : null; });
    var negVals = vals.map(function (v) { return v < 0 ? v : null; });

    new Chart(document.getElementById("fciHistoryChart"), {
      type: "line",
      data: {
        labels: dates(fci),
        datasets: [
          {
            label: "FCI (accommodative)", data: posVals,
            borderColor: COLORS.green, borderWidth: 0,
            pointRadius: 0, fill: "origin", backgroundColor: COLORS.greenSoft, spanGaps: false
          },
          {
            label: "FCI (restrictive)", data: negVals,
            borderColor: COLORS.red, borderWidth: 0,
            pointRadius: 0, fill: "origin", backgroundColor: COLORS.redSoft, spanGaps: false
          },
          {
            label: "Composite FCI", data: vals,
            borderColor: COLORS.navy, borderWidth: 2,
            pointRadius: 0, fill: false
          }
        ]
      },
      options: Object.assign({}, baseLineOpts, {
        plugins: {
          legend: { position: "bottom",
            labels: { filter: function (it) { return it.text === "Composite FCI"; } } },
          tooltip: { filter: function (it) { return it.dataset.label === "Composite FCI"; } }
        },
        scales: {
          x: timeScale(),
          y: yScale({ title: { display: true, text: "z-score" },
            grid: { color: function (c) { return c.tick.value === 0 ? COLORS.slate : COLORS.line; } } })
        }
      })
    });
  }

  // 7: Axis comparison bar ---------------------------------------------------
  function renderAxisBar(data) {
    var axes = data.axes;
    new Chart(document.getElementById("axisBarChart"), {
      type: "bar",
      data: {
        labels: axes.map(function (a) { return a.label; }),
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
          tooltip: { callbacks: { label: function (c) {
            return fmtSignedScore(c.parsed.x) + "  (" + labelByScore(c.parsed.x) + ")"; } } }
        },
        scales: {
          x: yScale({ title: { display: true, text: "accommodation score" },
            grid: { color: function (c) { return c.tick.value === 0 ? COLORS.slate : COLORS.line; } } }),
          y: { grid: { display: false } }
        }
      }
    });
  }

  // 8: Explore series --------------------------------------------------------
  function renderExplore(data) {
    var select = document.getElementById("series-select");
    var ids = Object.keys(data.series);

    // Group options by stage for usability.
    ids.forEach(function (id) {
      var s = data.series[id];
      var opt = document.createElement("option");
      opt.value = id;
      opt.textContent = s.name;
      select.appendChild(opt);
    });

    var chart = null;
    function draw(id) {
      var s = data.series[id];
      if (!s) return;

      // meta block
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
        '<span><b>Latest:</b> ' + fmtValue(s.latest_value, s.unit) +
          " (" + (s.latest_date || "") + ")</span>" +
        '<span><b>Unit:</b> ' + unitLabel(s.unit) + '</span>' +
        '<span><b>Frequency:</b> ' + (s.frequency || "—") + '</span>' +
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
            fill: true, backgroundColor: "rgba(31,56,100,.06)"
          }]
        },
        options: Object.assign({}, baseLineOpts, {
          plugins: { legend: { display: false }, tooltip: {
            callbacks: { label: function (c) { return fmtValue(c.parsed.y, s.unit); } } } },
          scales: {
            x: timeScale(),
            y: yScale({ title: { display: true, text: unitLabel(s.unit) } })
          }
        })
      };
      if (chart) chart.destroy();
      chart = new Chart(document.getElementById("exploreChart"), cfg);
    }

    select.addEventListener("change", function () { draw(select.value); });
    // default to the composite-relevant policy rate
    var initial = ids.indexOf("policy_rate") >= 0 ? "policy_rate" : ids[0];
    select.value = initial;
    draw(initial);
  }

  // 3b: Real-rate horizon ladder --------------------------------------------
  function renderHorizons(data) {
    var rows = data.real_rate_horizons || [];
    var el = document.getElementById("horizon-table");
    if (!el || !rows.length) return;
    setText("horizon-note", (data.meta && data.meta.score_window) || "");
    var body = rows.map(function (r) {
      var cls = scoreClass(r.score);
      var head = r.window.indexOf("headline") >= 0 ? ' class="hz-head"' : "";
      return "<tr" + head + "><td>" + r.window + '</td><td class="src">' + r.basis +
        '</td><td class="num"><span class="chip ' + cls + '">' + fmtSignedScore(r.score) +
        "</span></td><td>" + r.label + "</td></tr>";
    }).join("");
    el.innerHTML = '<table class="hz-tbl"><thead><tr><th>Baseline window</th>' +
      "<th>Real-rate basis</th><th class=\"num\">Score</th><th>Assessment</th></tr></thead>" +
      "<tbody>" + body + "</tbody></table>";
  }

  // 9: Methodology table — weights & assumptions for every indicator ---------
  function renderMethodology(data) {
    var el = document.getElementById("methodology-table");
    if (!el) return;
    var axisByKey = {};
    data.axes.forEach(function (a) { axisByKey[a.key] = a; });

    var listed = {}, groups = [];
    (data.meta.axis_order || []).forEach(function (k) {
      var ax = axisByKey[k];
      if (!ax) return;
      var rows = ax.members.map(function (id) { listed[id] = 1; return data.series[id]; })
        .filter(Boolean);
      if (rows.length) groups.push({ title: ax.label, rows: rows });
    });
    var ctx = Object.keys(data.series).filter(function (id) { return !listed[id]; })
      .map(function (id) { return data.series[id]; });
    if (ctx.length) groups.push({ title: "Context — not scored", rows: ctx });

    function polText(p) {
      return p > 0 ? "higher ⇒ easier" : p < 0 ? "higher ⇒ tighter" : "context only";
    }
    function wtText(w) {
      return (w && w > 0) ? String(Number(w).toFixed(2)).replace(/\.00$/, "").replace(/0$/, "") : "—";
    }

    el.innerHTML = groups.map(function (g) {
      var body = g.rows.map(function (s) {
        return "<tr><td>" + s.name + '</td><td class="num">' + wtText(s.weight) +
          "</td><td>" + polText(s.polarity) + '</td><td class="src">' + (s.source || "") +
          '</td><td class="assump">' + (s.notes || "") + "</td></tr>";
      }).join("");
      return '<table class="method-tbl"><caption>' + g.title + "</caption>" +
        '<thead><tr><th>Indicator</th><th class="num">Weight</th><th>Polarity</th>' +
        "<th>Source</th><th>Assumption / definition</th></tr></thead><tbody>" +
        body + "</tbody></table>";
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
  function lineDS(label, data, color, width) {
    return {
      label: label, data: data, borderColor: color,
      backgroundColor: color, borderWidth: width || 2,
      pointRadius: 0, tension: .15, fill: false
    };
  }

  /* ----------------------------------------------------------------------
     Zero-line plugin (draws a baseline at y=0 on relevant line charts)
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
      renderGauge(data);
      renderMetricCards(data);
      renderStage1(data);
      renderHorizons(data);
      renderNaturalRate(data);
      renderStage2(data);
      renderFciHistory(data);
      renderAxisBar(data);
      renderExplore(data);
      renderMethodology(data);
    } catch (err) {
      console.error("Dashboard render error:", err);
    }
  }

  function init() {
    if (window.FCI_DATA) {
      boot(window.FCI_DATA);
    } else {
      // file:// fallback when data.js is unavailable
      fetch("data.json")
        .then(function (r) { return r.json(); })
        .then(boot)
        .catch(function (e) {
          console.error("Failed to load data.json:", e);
          document.body.insertAdjacentHTML("afterbegin",
            '<p style="padding:20px;color:#c0392b">Could not load data. ' +
            'Open this page with data.js present, or via a local server.</p>');
        });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
