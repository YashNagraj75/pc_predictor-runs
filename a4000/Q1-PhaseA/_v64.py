import json, glob
for d in sorted(glob.glob('runs/*t64alm_s0')) + sorted(glob.glob('runs/*t64pc_s0')):
    r = json.load(open(d + '/probes.json')); cl = r['scene']['classification']
    print('%-40s lin %.4f mlp %.4f knn %.4f ssim %.4f' % (d.split('/')[1], cl['linear']['accuracy'],
          cl['mlp']['accuracy'], r['knn']['accuracy'], r['decode']['ssim']))
