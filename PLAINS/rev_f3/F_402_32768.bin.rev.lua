
===== fn#0 '@src/catchGame/configReader/GiftPopularityConfig.lua' (26 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'GiftPopularityConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = {}
c3['S'] = 100.0
c3['A'] = 90.0
c3['B'] = 80.0
c3['C'] = 70.0
c3['D'] = 60.0
v4 = <imm0>
g1 = c3
c2['dealDatas'] = v4
v4 = <imm1>
c2['getQualityById'] = v4
v4 = <imm2>
c2['getAllSortedSADatas'] = v4
v4 = <imm3>
c2['getAllQualitySortedDatas'] = v4
v4 = <imm4>
c2['getDatasByQuality'] = v4
return c2
return g1

===== fn#0 '' (51 instr, depth 1) =====
local t1 = {}
R0['allSortedSADatas'] = t1
t1 = {}
R0['qualitySortedDatas'] = t1
t1 = <G 'pairs'>
local t2 = R0['datas']
t1 = t1(t2)
-- goto L0
-- L3:
local t3 = R5['quality']
local t4 = R0['qualitySortedDatas']
local t5 = R0['qualitySortedDatas']
t5 = t5[t3]
-- if not t5 goto L15
-- goto L1
t5 = {}
-- L1:
t4[t3] = t5
t4 = <G 'table'>
t4 = t4['insert']
t5 = R0['qualitySortedDatas']
t5 = t5[t3]
local v6 = R5
t4 = t4(t5, v6)
-- if 'S' ~= t3 goto L26
-- goto L2
-- if 'A' == t3 goto L31
-- goto L0
-- L2:
t4 = <G 'table'>
t4 = t4['insert']
t5 = R0['allSortedSADatas']
v6 = R5
t4 = t4(t5, v6)
-- L0:
-- op23 A=1 B=2 C=0
-- goto L3
t1 = <G 'table'>
t1 = t1['sort']
t2 = R0['allSortedSADatas']
local i7 = <imm0>
t1 = t1(t2, i7)
t1 = <G 'pairs'>
t2 = R0['qualitySortedDatas']
t1 = t1(t2, i7)
-- goto L4
-- L5:
t3 = <G 'table'>
t3 = t3['sort']
t4 = R5
t5 = <imm1>
t3 = t3(t4, t5)
-- L4:
-- op23 A=1 B=2 C=0
-- goto L5
return R0

===== fn#0 '' (28 instr, depth 2) =====
local t1 = R0['quality']
local t2 = R2[t1]
-- if not t2 goto L6
-- goto L0
t2 = 0.0
-- L0:
local t3 = R1['quality']
t1 = t1[t3]
-- if not t1 goto L12
-- goto L1
t1 = 0.0
-- L1:
-- if t1 == t2 goto L22
-- goto L2
t3 = R0['id']
local t4 = R1['id']
-- if t3 < t4 goto L19
-- goto L3
t3 = nil
-- L3:
t3 = nil
return t3
-- goto L4
-- L2:
-- if t2 < t1 goto L25
-- goto L5
t3 = nil
-- L5:
t3 = nil
return t3
-- L4:
return R0