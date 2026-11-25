import json, glob
for d in sorted(glob.glob('runs/*t64alm_s0'))+sorted(glob.glob('runs/*t64pc_s0'))+['runs/pc_sigreg_T16_coupled_alm_s0','runs/pc_sigreg_T16_coupled_etafix_s0','runs/bp_sigreg_etafix_s0']:
    try: log = json.load(open(d+'/log.json'))
    except Exception: continue
    g = sorted(r['grad_norm_preclip'] for r in log if 'grad_norm_preclip' in r)
    n = len(g); frac = sum(1 for v in g if v > 1.0)/n
    print('%-40s median %.3g  p90 %.3g  clipped %.1f%% of steps' % (d.split('/')[1], g[n//2], g[int(.9*n)], 100*frac))
