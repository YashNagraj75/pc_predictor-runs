import json, glob
for d in sorted(glob.glob("runs/*etafix_s*")):
    log = json.load(open(d + "/log.json"))
    ev = [(r["step"], r["eval"]["embedding"]["knn"]) for r in log
          if isinstance(r.get("eval"), dict) and "knn" in r["eval"].get("embedding", {})]
    lf = [r["loss_ff"] for r in log]
    best = max(k for _, k in ev); bstep = [s for s, k in ev if k == best][0]
    print("%-38s first=%.4f best=%.4f@%-6d last=%.4f  BEST-FIRST=%+.4f  loss_ff %.4f->%.4f" % (
        d.split("/")[1], ev[0][1], best, bstep, ev[-1][1], best - ev[0][1], lf[0], lf[-1]))
