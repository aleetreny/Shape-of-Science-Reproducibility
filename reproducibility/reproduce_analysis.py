"""Recompute statistical results from frozen measurements, without embeddings."""
import argparse, csv, hashlib, json, math, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

def read(path):
    with path.open(newline='') as f:return list(csv.DictReader(f))

def compare_csv(actual, expected):
    a,b=read(actual),read(expected)
    assert len(a)==len(b),(actual.name,len(a),len(b))
    cells=0
    for x,y in zip(a,b):
        assert set(x)==set(y),(actual.name,'columns')
        for k in x:
            if x[k]==y[k]:continue
            try:u,v=float(x[k]),float(y[k])
            except ValueError:raise AssertionError((actual.name,k,x[k],y[k])) from None
            assert math.isclose(u,v,rel_tol=1e-10,abs_tol=1e-10),(actual.name,k,u,v)
            cells+=1
    return {'rows':len(a),'numerically_equal_nonidentical_cells':cells}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'reproduced')
    parser.add_argument('--skip-integrity',action='store_true',help='Skip hashing every supplied data file.')
    args=parser.parse_args()
    out=args.output.resolve()
    assert out!=ROOT and not out.is_relative_to(ROOT/'data') and not out.is_relative_to(ROOT/'reports'),'Use a separate output folder.'
    out.mkdir(parents=True,exist_ok=True)
    if not args.skip_integrity:
        selection=json.loads((ROOT/'SELECTION.json').read_text())
        for record in selection['included']:
            p=ROOT/record['path']
            h=hashlib.sha256()
            with p.open('rb') as f:
                for block in iter(lambda:f.read(4*1024**2),b''):h.update(block)
            assert h.hexdigest()==record['sha256'],record['path']
        print('All supplied data checksums verified.',flush=True)
    import numpy as np
    from sos_closure import summarize
    summarize.REPORT=out/'closure'
    summarize.REPORT.mkdir(exist_ok=True)
    results={}
    for name in ['centres','headline','morphology','quality']:
        results[name]=getattr(summarize,name)()
        print('Recomputed:',name,flush=True)
    checked={}
    for p in sorted(summarize.REPORT.glob('*.csv')):
        checked[p.name]=compare_csv(p,ROOT/'reports/robustness_closure_v1'/p.name)
    local=[];checks=0
    for p in sorted((ROOT/'data/analysis_v1/neighbors/overlap/local').glob('*/summary.json')):
        data=json.loads(p.read_text());counts=np.load(p.with_name('shared_counts.npy'))
        assert counts.shape[1:]==(45,3)
        for score in data['scores']:
            pi=data['pairs'].index([score['model_a'],score['model_b']]);ki=data['ks'].index(score['k'])
            actual=float(counts[:,pi,ki].mean()/score['k'])
            assert math.isclose(actual,score['mean_overlap'],abs_tol=1e-12,rel_tol=0)
            checks+=1
        local.append(float(counts[:,:,1].mean()/25))
    assert len(local)==130
    global_counts=np.load(ROOT/'data/analysis_v1/neighbors/overlap/global/anchors/shared_counts.npy')
    assert global_counts.shape==(13000,45,3)
    local_k25=float(np.mean(local)); global_k25=float(global_counts[:,:,1].mean()/25)
    expected=read(ROOT/'reports/analysis_v1/final/tables/neighbors_local.csv')
    expected_local=np.mean([float(r['mean_overlap']) for r in expected if r['k']=='25'])
    assert math.isclose(local_k25,float(expected_local),abs_tol=1e-12,rel_tol=0)
    expected=read(ROOT/'reports/analysis_v1/final/tables/neighbors_global.csv')
    assert math.isclose(global_k25,float(np.mean([float(r['mean_overlap']) for r in expected if r['k']=='25'])),abs_tol=1e-12,rel_tol=0)
    subprocess.run([sys.executable,'-I','-S',str(ROOT/'reproducibility/reproduce_summaries.py')],check=True,stdout=subprocess.DEVNULL)
    report={'all_checks_passed':True,'closure_tables':checked,'closure_csv_rows':sum(r['rows'] for r in checked.values()),'local_neighbor_score_checks':checks,'neighbor_agreement_k25':{'local_equal_cell_weight':local_k25,'global_balanced_queries':global_k25},'four_figure_quickcheck':True,'boundary':'Recomputes statistical analyses from frozen model-derived measurements. Does not regenerate embeddings or reconstruct nearest-neighbor lists from texts.'}
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
