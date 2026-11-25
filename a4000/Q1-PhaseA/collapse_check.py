"""Are the pilot sparse codes / embeddings input-dependent?  (job 629aa534 pilots)"""
import sys, os, json; sys.path.insert(0, ".")
import jax.numpy as jnp, numpy as np, data as D, sparse as SP
from run_probes import load_run
out = []
X0 = None
for r in ("pc_sigreg_T16_coupled_spBpilot_s0", "bp_sigreg_spBpilot_s0",
          "pc_sigreg_T16_coupled_spCpilot_s0", "bp_sigreg_spCpilot_s0"):
    cfg, p = load_run("runs/" + r)
    if X0 is None:
        Xte, yte = D.load_dataset(cfg.data)[2:4]
        X0, y0 = Xte[:1000], np.asarray(yte[:1000])
    acts, ex = SP.deploy(p, D.eval_batch(jnp.asarray(X0), cfg.data), cfg)
    s = cfg.sparse.layer
    v = np.asarray(acts[s] if cfg.sparse.case == "B" else ex["a"])
    z, f = np.asarray(acts[-1]), np.asarray(ex["f_s"])
    on = v != 0
    fm = f.mean(0)
    cosm = (f @ fm) / (np.linalg.norm(f, axis=1) * np.linalg.norm(fm) + 1e-12)
    top = np.bincount(np.argmax(np.abs(v), 1), minlength=v.shape[1])
    row = {"run": r, "width": int(v.shape[1]), "units_ever_active": int(on.any(0).sum()),
           "mean_active_per_sample": float(on.sum(1).mean()),
           "distinct_supports": len({tuple(np.where(q)[0]) for q in on}),
           "top_unit_share": float(top.max() / len(v)),
           "embed_std_over_inputs": float(z.std(0).mean()),
           "embed_norm_mean": float(np.linalg.norm(z, axis=1).mean()),
           "f_s_cos_to_mean_median": float(np.median(cosm)),
           "majority_class_rate": float(np.bincount(y0).max() / len(y0))}
    out.append(row); print(json.dumps(row), flush=True)
json.dump(out, open(os.path.join(os.environ["JOBDIR"], "collapse_check.json"), "w"), indent=1)
