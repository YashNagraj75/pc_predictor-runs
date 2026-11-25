import json
for d in ("runs/bp_sigreg_pilot_s0", "runs/pc_sigreg_T16_coupled_pilot_s0"):
    log = json.load(open(d + "/log.json"))
    ev = [(r["step"], r["eval"]["embedding"]["knn"]) for r in log
          if isinstance(r.get("eval"), dict) and "knn" in r["eval"].get("embedding", {})]
    lf = [r["loss_ff"] for r in log]
    gn = sorted(r["grad_norm_preclip"] for r in log)
    best = max(k for _, k in ev)
    bstep = [s for s, k in ev if k == best][0]
    print(d.split("/")[1])
    print("   knn: " + "  ".join("s%d=%.4f" % (s, k) for s, k in ev))
    print("   first=%.4f best=%.4f(step %d) BEST-FIRST=%+.4f" % (ev[0][1], best, bstep, best - ev[0][1]))
    print("   loss_ff %.4f -> %.4f   |g| median %.3e" % (lf[0], lf[-1], gn[len(gn)//2]))
