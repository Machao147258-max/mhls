
===== fn#0 '@src/catchGame/configReader/RecreationOpenConfig.lua' (13 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'RecreationOpenConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['getGameplays'] = c3
return c2
return g1

===== fn#0 '' (17 instr, depth 1) =====
local g1 = <G 'pairs'>
local t2 = R0['datas']
g1 = g1(t2)
-- goto L0
-- L2:
local g3 = <G 'string'>
g3 = g3['toArray']
local t4 = R5['gameplay']
-- if not t4 goto L10
-- goto L1
t4 = ''
-- L1:
local c5 = ','
local n6 = nil
g3 = g3(t4, c5, n6)
R5['gameplays'] = g3
-- L0:
-- op23 A=1 B=2 C=0
-- goto L2
return R0