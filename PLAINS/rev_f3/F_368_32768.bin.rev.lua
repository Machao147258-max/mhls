
===== fn#0 '@src/catchGame/configReader/AchievementScoreConfig.lua' (13 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'AchievementScoreConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['getSortedDatas'] = c3
return c2
return g1

===== fn#0 '' (19 instr, depth 1) =====
local t1 = {}
R0['sortedDatas'] = t1
t1 = <G 'pairs'>
local t2 = R0['datas']
t1 = t1(t2)
-- goto L0
-- L1:
local g3 = <G 'table'>
g3 = g3['insert']
local t4 = R0['sortedDatas']
local v5 = R5
g3 = g3(t4, v5)
-- L0:
-- op23 A=1 B=2 C=0
-- goto L1
t1 = <G 'table'>
t1 = t1['sort']
t2 = R0['sortedDatas']
local i6 = <imm0>
t1 = t1(t2, i6)
return R0

===== fn#0 '' (8 instr, depth 2) =====
local t1 = R0['id']
local t2 = R1['id']
-- if t2 < t1 goto L5
-- goto L0
t1 = nil
-- L0:
t1 = nil
return t1
return R0