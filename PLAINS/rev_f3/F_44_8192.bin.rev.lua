
===== fn#0 '@src/catchGame/configReader/LadderSeasonConfig.lua' (16 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'require'>
local c3 = 'cjson'
c2 = c2(c3)
c3 = <G 'class'>
local c4 = 'LadderSeasonConfig'
local v5 = g1
c3 = c3(c4, v5)
c4 = <imm0>
c3['dealDatas'] = c4
c4 = <imm1>
c3['getDataById'] = c4
return c3
return g1

===== fn#0 '' (14 instr, depth 1) =====
R0['maxSeason'] = 1.0
local g1 = <G 'pairs'>
local t2 = R0['datas']
g1 = g1(t2)
-- goto L0
-- L1:
local t3 = R5['id']
local t4 = R0['maxSeason']
-- if t3 < t4 goto L11
-- goto L0
t3 = R5['id']
R0['maxSeason'] = t3
-- L0:
-- op23 A=1 B=2 C=0
-- goto L1
return R0