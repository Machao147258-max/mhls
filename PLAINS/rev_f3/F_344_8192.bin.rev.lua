
===== fn#0 '@src/catchGame/configReader/MapDecorationTypeCollectionConfig.lua' (17 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'MapDecorationTypeCollectionConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['getDataByUnlockNeedType'] = c3
c3 = <imm2>
c2['getSortedDatas'] = c3
c3 = <imm3>
c2['getOwnedAndTotalValidCount'] = c3
return c2
return g1

===== fn#0 '' (26 instr, depth 1) =====
local t1 = {}
R0['sortedDatas'] = t1
t1 = <G 'cg'>
t1 = t1['Game']
t1 = t1:'newNowTime'
local s2 = t1
t1 = t1(s2)
s2 = <G 'pairs'>
local t3 = R0['datas']
s2 = s2(t3)
-- goto L0
-- L1:
local t4 = R6['isShow']
-- if not t4 goto L18
-- goto L0
t4 = <G 'table'>
t4 = t4['insert']
local t5 = R0['sortedDatas']
local v6 = R6
t4 = t4(t5, v6)
-- L0:
-- op23 A=2 B=2 C=0
-- goto L1
s2 = <G 'table'>
s2 = s2['sort']
t3 = R0['sortedDatas']
local i7 = <imm0>
s2 = s2(t3, i7)
return R0

===== fn#0 '' (20 instr, depth 2) =====
local t1 = R0['rankId']
local t2 = R1['rankId']
-- if t2 ~= t1 goto L12
-- goto L0
t1 = R0['rankId']
t2 = R1['rankId']
-- if t2 < t1 goto L9
-- goto L1
t1 = nil
-- L1:
t1 = nil
return t1
-- goto L2
-- L0:
t1 = R0['id']
t2 = R1['id']
-- if t2 < t1 goto L17
-- goto L3
t1 = nil
-- L3:
t1 = nil
return t1
-- L2:
return R0