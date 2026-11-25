import csv
rows = list(csv.DictReader(open("diag_inference_b256.csv")))
n = int(rows[0]["n_layers"])
print("%-9s %-9s %-9s %-6s %-6s  per-layer activity movement" % ("eta_h","F_final","L_final","mono","moved"))
for r in rows:
    per = " ".join("%.0e" % float(r["L%d_move" % i]) for i in range(n))
    print("%-9s %-9.4f %-9.4f %-6s %-6s  %s" % (
        r["eta_h"], float(r["F_final"]), float(r["L_final"]),
        r["L_monotone"][:1], r["n_layers_moved"]+"/"+r["n_layers"], per))
