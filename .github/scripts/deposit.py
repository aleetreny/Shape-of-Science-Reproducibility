"""Copy verified v1.1.0 assets to its exact Zenodo draft; never publish/delete."""
import hashlib, http.client, json, os, ssl, sys, time
from pathlib import Path
from urllib.parse import urlsplit, quote
RECORD=22876602
ROOT=Path(__file__).resolve().parents[2]
FILES=ROOT/'downloads'
TOKEN=os.environ['ZENODO_TOKEN']
CONTEXT=ssl.create_default_context()
API=f'/api/deposit/depositions/{RECORD}'

def request(method,path,body=None):
    assert method in {'GET','PUT'}
    assert (method=='GET' and path==API) or (method=='PUT' and path.startswith('/api/files/'))
    conn=http.client.HTTPSConnection('zenodo.org',timeout=300,context=CONTEXT)
    try:
        headers={'Authorization':'Bearer '+TOKEN,'Accept':'application/json'}
        if body is not None:headers['Content-Type']='application/octet-stream'
        conn.request(method,path,body=body,headers=headers)
        response=conn.getresponse()
        if not 200<=response.status<300:raise RuntimeError(f'Zenodo HTTP {response.status}')
        return json.loads(response.read())
    finally:conn.close()

def draft():
    d=request('GET',API)
    assert d['id']==RECORD and d['submitted'] is False and d['state']=='unsubmitted','Unexpected draft state'
    return d

def matches(remote,local):
    return int(remote.get('filesize',remote.get('size',-1)))==local['bytes'] and str(remote['checksum']).removeprefix('md5:')==local['md5']

manifest_bytes=(ROOT/'release-manifest.json').read_bytes()
assert (FILES/'release-manifest.json').read_bytes()==manifest_bytes
entries=json.loads(manifest_bytes)['files']
entries=entries+[{'name':'release-manifest.json','bytes':len(manifest_bytes),'sha256':hashlib.sha256(manifest_bytes).hexdigest()}]
for e in entries:
    assert Path(e['name']).name==e['name']
    b=(FILES/e['name']).read_bytes()
    assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],e['name']
    e['md5']=hashlib.md5(b).hexdigest()
assert {p.name for p in FILES.iterdir()}=={e['name'] for e in entries}
for e in sorted(entries,key=lambda e:e['bytes']):
    for attempt in range(5):
        d=draft();remote={f['filename']:f for f in d['files']}
        assert set(remote)<={e['name'] for e in entries},'Unexpected remote files'
        if e['name'] in remote:
            assert matches(remote[e['name']],e),e['name']
            print('Already verified:',e['name'],flush=True);break
        url=urlsplit(d['links']['bucket'])
        assert url.scheme=='https' and url.netloc=='zenodo.org' and url.path.startswith('/api/files/') and not url.query
        try:
            print('Uploading:',e['name'],e['bytes'],'bytes; attempt',attempt+1,flush=True)
            result=request('PUT',url.path+'/'+quote(e['name'],safe=''),(FILES/e['name']).read_bytes())
            assert matches(result,e),e['name']
            print('Verified:',e['name'],flush=True);break
        except (OSError,http.client.HTTPException,RuntimeError) as exc:
            # Never print arbitrary exception/request bodies containing credentials.
            print('Temporary transfer failure:',type(exc).__name__,flush=True)
            if attempt==4:raise SystemExit('Upload failed after five attempts; no publication performed.')
            time.sleep(min(2**(attempt+1),30))
    else:raise SystemExit('Upload incomplete')
d=draft();remote={f['filename']:f for f in d['files']}
assert set(remote)=={e['name'] for e in entries}
assert all(matches(remote[e['name']],e) for e in entries)
print(json.dumps({'record':RECORD,'files_verified':len(entries),'bytes':sum(e['bytes'] for e in entries),'published':False}),flush=True)
