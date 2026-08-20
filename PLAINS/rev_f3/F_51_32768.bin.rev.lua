
===== fn#0 '@src/catchGame/configReader/LadderOpenConfig.lua' (11 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'LadderOpenConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['getDataByWeekDay'] = c3
return c2
return g1

===== fn#0 '' (20 instr, depth 1) =====
local t1 = {}
local g2 = <G 'pairs'>
local t3 = R0['datas']
g2 = g2(t3)
-- goto L0
-- L1:
local t4 = R7['weekday']
local g5 = <G 'tonumber'>
local v6 = R1
g5 = g5(v6)
-- if g5 == t4 goto L16
-- goto L0
t4 = <G 'table'>
t4 = t4['insert']
g5 = t1
v6 = R7
t4 = t4(g5, v6)
-- L0:
-- op23 A=3 B=2 C=0
-- goto L1
return t1
return R0