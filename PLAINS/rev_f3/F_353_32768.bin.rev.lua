
===== fn#0 '@src/catchGame/configReader/PortraitCollectionConfig.lua' (16 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'PortraitCollectionConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <G 'cg'>
c3 = c3['Utils']
c3 = c3['convertDateStrToTimestamp']
v4 = <G 'cg'>
v4 = v4['PortraitConfig']
local i5 = <imm0>
c2['dealDatas'] = i5
return c2
return g1

===== fn#0 '' (67 instr, depth 1) =====
local t1 = {}
local g2 = <G 'cg'>
g2 = g2['Game']
g2 = g2:'newNowTime'
local s3 = g2
g2 = g2(s3)
s3 = <G 'pairs'>
local t4 = R0['datas']
s3 = s3(t4)
-- goto L0
-- L5:
local t5 = R7['isShow']
-- if not t5 goto L58
-- goto L0
t5 = R7['isShow']
-- if 1.0 == t5 goto L58
-- goto L0
t5 = {}
local c6 = 1.0
-- L4:
local c7 = 'itemID'
local v8 = c6
c7 = c7 .. v8
c7 = R7[c7]
-- if not c7 goto L47
-- goto L1
c7 = <G 'cg'>
c7 = c7['PortraitConfig']
c7 = c7:'getDataById'
v8 = c7
local c9 = 'itemID'
local v10 = c6
c9 = c9 .. v10
c9 = R7[c9]
c7 = c7(v8, c9, v10)
v8 = c7['showTimeStamp']
-- if not v8 goto L37
-- goto L2
v8 = c7['showTimeStamp']
-- if g2 <= v8 goto L45
-- goto L3
-- L2:
v8 = <G 'table'>
v8 = v8['insert']
c9 = t5
v10 = 'itemID'
local v11 = c6
v10 = v10 .. v11
v10 = R7[v10]
v8 = v8(c9, v10)
-- L3:
-- op19 A=9 B=262 C=9
-- goto L4
-- L1:
R7['items'] = t5
c7 = <G 'table'>
c7 = c7['array2keymap']
v8 = t5
c7 = c7(v8, c9, v10)
R7['itemMap'] = c7
c7 = <G 'table'>
c7 = c7['insert']
v8 = t1
c9 = R7
c7 = c7(v8, c9)
-- L0:
-- op23 A=3 B=2 C=0
-- goto L5
s3 = <G 'table'>
s3 = s3['sort']
t4 = t1
local i12 = <imm0>
s3 = s3(t4, i12)
R0['datas'] = t1
return R0

===== fn#0 '' (8 instr, depth 2) =====
local t1 = R0['rankId']
local t2 = R1['rankId']
-- if t2 < t1 goto L5
-- goto L0
t1 = nil
-- L0:
t1 = nil
return t1
return R0