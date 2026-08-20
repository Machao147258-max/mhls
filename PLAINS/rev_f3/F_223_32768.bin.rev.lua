
===== fn#0 '@src/catchGame/configReader/BeginerCeremonyConfig.lua' (15 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'require'>
local c3 = 'catchGame/configReader/ReaderFactory'
c2 = c2(c3)
c3 = <G 'class'>
local c4 = 'BeginerCeremonyConfig'
local v5 = g1
c3 = c3(c4, v5)
c4 = <imm0>
g1 = c2
c3['dealDatas'] = c4
return c3
return g1

===== fn#0 '' (35 instr, depth 1) =====
local g1 = <G 'ipairs'>
local t2 = R0['datas']
g1 = g1(t2)
-- goto L0
-- L3:
local g3 = <G 'string'>
g3 = g3['split']
local t4 = R5['generalactivityID']
local c5 = '.'
g3 = g3(t4, c5)
g3 = g3[1.0]
t4 = t4:'getConfigNameByDataName'
c5 = t4
local v6 = g3
t4 = t4(c5, v6)
g3 = t4
t4 = <G 'cg'>
g3 = t4[g3]
t4 = g3:'getDatas'
c5 = g3
t4 = t4(c5, v6)
c5 = {}
v6 = <G 'ipairs'>
local v7 = t4
v6 = v6(v7)
-- goto L1
-- L2:
local g8 = <G 'table'>
g8 = g8['insert']
local v9 = c5
local t10 = R13['questID']
g8 = g8(v9, t10)
-- L1:
-- op23 A=9 B=2 C=0
-- goto L2
R5['quests'] = c5
-- L0:
-- op23 A=1 B=2 C=0
-- goto L3
return R0