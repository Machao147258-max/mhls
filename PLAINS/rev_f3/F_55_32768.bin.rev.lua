
===== fn#0 '@src/catchGame/configReader/LadderPeriodOpenConfig.lua' (13 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'LadderPeriodOpenConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['getDataByWeekDay'] = c3
return c2
return g1

===== fn#0 '' (19 instr, depth 1) =====
local g1 = <G 'pairs'>
local t2 = R0['datas']
g1 = g1(t2)
-- goto L0
-- L1:
local g3 = <G 'cg'>
g3 = g3['LadderLevelConfig']
g3 = g3:'getLevelBySortLevel'
local s4 = g3
local t5 = R5['minSortLevel']
g3 = g3(s4, t5)
R5['minLevel'] = g3
g3 = <G 'cg'>
g3 = g3['LadderLevelConfig']
g3 = g3:'getLevelBySortLevel'
s4 = g3
t5 = R5['maxSortLevel']
g3 = g3(s4, t5)
R5['maxLevel'] = g3
-- L0:
-- op23 A=1 B=2 C=0
-- goto L1
return R0