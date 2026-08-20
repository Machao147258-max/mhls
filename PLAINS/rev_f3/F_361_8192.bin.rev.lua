
===== fn#0 '@src/catchGame/configReader/PortraitFrameCollectionConfig.lua' (17 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'PortraitFrameCollectionConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <G 'cg'>
c3 = c3['Utils']
c3 = c3['convertDateStrToTimestamp']
v4 = <G 'cg'>
v4 = v4['PortraitFrameComConfig']
local i5 = <imm0>
g1 = c3
c2['dealDatas'] = i5
return c2
return g1

===== fn#0 '' (69 instr, depth 1) =====
local t1 = {}
local g2 = <G 'pairs'>
local t3 = R0['datas']
g2 = g2(t3)
-- goto L0
-- L5:
local t4 = R6['isShow']
-- if not t4 goto L60
-- goto L0
t4 = R6['isShow']
-- if 1.0 == t4 goto L60
-- goto L0
t4 = {}
local c5 = 1.0
-- L4:
local c6 = 'itemID'
local v7 = c5
c6 = c6 .. v7
c6 = R6[c6]
-- if not c6 goto L49
-- goto L1
c6 = <G 'cg'>
c6 = c6['PortraitFrameComConfig']
c6 = c6:'getDataById'
v7 = c6
local c8 = 'itemID'
local v9 = c5
c8 = c8 .. v9
c8 = R6[c8]
c6 = c6(v7, c8, v9)
v7 = c6['showTime']
-- if not v7 goto L39
-- goto L2
c8 = c6['showTime']
v7 = v7(c8, v9)
c8 = <G 'cg'>
c8 = c8['Game']
c8 = c8:'newNowTime'
v9 = c8
c8 = c8(v9)
-- if c8 <= v7 goto L47
-- goto L3
-- L2:
v7 = <G 'table'>
v7 = v7['insert']
c8 = t4
v9 = 'itemID'
local v10 = c5
v9 = v9 .. v10
v9 = R6[v9]
v7 = v7(c8, v9)
-- L3:
-- op19 A=8 B=259 C=8
-- goto L4
-- L1:
R6['items'] = t4
c6 = <G 'table'>
c6 = c6['array2keymap']
v7 = t4
c6 = c6(v7, c8, v9)
R6['itemMap'] = c6
c6 = <G 'table'>
c6 = c6['insert']
v7 = t1
c8 = R6
c6 = c6(v7, c8)
-- L0:
-- op23 A=2 B=2 C=0
-- goto L5
g2 = <G 'table'>
g2 = g2['sort']
t3 = t1
local i11 = <imm0>
g2 = g2(t3, i11)
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