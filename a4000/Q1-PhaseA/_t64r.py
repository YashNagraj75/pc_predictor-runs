import json, glob
rows = [("runs/pc_sigreg_T64_coupled_t64alm_s0", "PC-ALM T=64 a=2"),
        ("runs/pc_sigreg_T16_coupled_alm_s0",    "PC-ALM T=16 a=1"),
        ("runs/pc_sigreg_T16_coupled_etafix_s0", "plain PC T=16"),
        ("runs/bp_sigreg_etafix_s0",             "backprop")]
for d, lab in rows:
    try: log = json.load(open(d + "/log.json"))
    except Exception: continue
    ev = [(r["step"], r["eval"]["embedding"]["knn"]) for r in log
          if isinstance(r.get("eval"), dict) and "knn" in r["eval"].get("embedding", {})]
    if not ev: continue
    lf = [r["loss_ff"] for r in log]
    dn = [r["dual_norm"] for r in log if "dual_norm" in r]
    b = max(k for _, k in ev); bs = [s for s, k in ev if k == b][0]
    print("%-18s first=%.4f best=%.4f@%-6d last=%.4f  BEST-FIRST=%+.4f  loss_ff %.4f->%.4f%s" % (
        lab, ev[0][1], b, bs, ev[-1][1], b-ev[0][1], lf[0], lf[-1],
        ("  dual %.1f->%.1f" % (dn[0], dn[-1])) if dn else ""))
    print("%-18s traj: %s" % ("", " ".join("%d:%.4f" % (s, k) for s, k in ev)))
