import json, glob
pats = ["runs/*t64almpilot*", "runs/*t64pcpilot*",
        "runs/pc_sigreg_T16_coupled_almpilot_s0", "runs/bp_sigreg_pilot_s0",
        "runs/pc_sigreg_T16_coupled_pilot_s0"]
for p in pats:
    for d in sorted(glob.glob(p)):
        try: log = json.load(open(d + "/log.json"))
        except Exception: continue
        ev = [(r["step"], r["eval"]["embedding"]["knn"]) for r in log
              if isinstance(r.get("eval"), dict) and "knn" in r["eval"].get("embedding", {})]
        if not ev: continue
        lf = [r["loss_ff"] for r in log]
        dn = [r["dual_norm"] for r in log if "dual_norm" in r]
        b = max(k for _, k in ev)
        print("%-48s knn %.4f -> best %.4f (+%.4f)  loss_ff %.4f -> %.4f%s" % (
            d.split("/")[1], ev[0][1], b, b-ev[0][1], lf[0], lf[-1],
            ("  dual %.1f" % dn[-1]) if dn else ""))
