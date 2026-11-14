import io,re,os
d=r"C:\Users\20751\Desktop\猫和老鼠\REV_ALL2"
def fix(s):
    try:
        return s.encode('utf-8','surrogateescape').decode('gbk','replace')
    except Exception:
        return s
def rows(fn):
    raw=io.open(os.path.join(d,fn),encoding='utf-8',errors='replace').read()
    out=[]
    cur={}
    for ln in raw.splitlines():
        m=re.match(r"t_\d+\['?(.*?)'?\] = '(.*)'", ln.strip())
        if not m: 
            m2=re.match(r"t_\d+\[(\d+)\] = '(.*)'", ln.strip())
            if m2: cur.setdefault('_arr',[]).append(m2.group(2)); continue
            continue
        k,v=m.group(1),fix(m.group(2))
        cur[k]=v
        if k=='id':
            if cur: out.append(cur)
            cur={}
    if cur: out.append(cur)
    return out
for fn in ['src_catchGame_data_level_gameplay.lua.rev.lua']:
    print('=====',fn)
    for r in rows(fn):
        print(r.get('id'), '|', r.get('gameplay'), '| grade',r.get('grade'),'level',r.get('level'),'|', r.get('des'), '| show',r.get('isShowTip'))
