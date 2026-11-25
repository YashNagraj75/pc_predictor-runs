import json, glob
for d in sorted(glob.glob("runs/*_alm_s*")) + ["runs/pc_sigreg_T16_coupled_etafix_s0",
                                                "runs/bp_sigreg_etafix_s0"]:
    try: log = json.load(open(d + "/log.json"))
    except Exception: continue
    ev = [(r["step"], r["eval"]["embedding"]["knn"]) for r in log
          if isinstance(r.get("eval"), dict) and "knn" in r["eval"].get("embedding", {})]
    if not ev: continue
    lf = [r["loss_ff"] for r in log]
    dn = [r["dual_norm"] for r in log if "dual_norm" in r]
    best = max(k for _, k in ev); bstep = [s for s, k in ev if k == best][0]
    print("%-38s first=%.4f best=%.4f@%-6d last=%.4f BEST-FIRST=%+.4f  loss_ff %.4f->%.4f%s" % (
        d.split("/")[1], ev[0][1], best, bstep, ev[-1][1], best-ev[0][1], lf[0], lf[-1],
        ("  dual %.1f->%.1f" % (dn[0], dn[-1])) if dn else ""))
