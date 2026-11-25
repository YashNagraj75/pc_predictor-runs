import csv
rows = list(csv.DictReader(open("diag_alm_T64.csv")))
g = [r for r in rows if r.get("mean_layer_cos")]
print("%-8s %-7s %-11s %-8s %-10s %-10s" % ("eta_h","alpha","mean/layer","front","global","|g|/|g_bp|"))
for r in g:
    print("%-8s %-7s %-11.5f %-8s %-10.5f %-10.4g" % (
        r["eta_h"], r["alpha"], float(r["mean_layer_cos"]),
        r["front_0p9"]+"/10", float(r["cos"]), float(r["norm_ratio"])))
tt = [r for r in rows if r.get("cos_alpha0")]
if tt:
    print()
    print("cos vs T (global):  " + "   ".join(
        "T=%s: a0=%.3f a_sel=%.3f" % (r["T"], float(r["cos_alpha0"]), float(r["cos_alpha_sel"])) for r in tt))
pl = [r for r in rows if r.get("L0_cos") and not r.get("mean_layer_cos")]
for r in pl:
    print("per-layer alpha=%-5s " % r["alpha"] + " ".join("%6.3f" % float(r["L%d_cos"%i]) for i in range(10)))
