
===== fn#0 '@src/catchGame/configReader/ContentCollectionConfig.lua' (11 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'ContentCollectionConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['getDataByType'] = c3
return c2
return g1

===== fn#0 '' (13 instr, depth 1) =====
local g1 = <G 'pairs'>
local t2 = R0['datas']
g1 = g1(t2)
-- goto L0
-- L1:
local t3 = R6['type']
-- if R1 == t3 goto L8
-- goto L0
return R6
-- L0:
-- op23 A=2 B=2 C=0
-- goto L1
g1 = {}
return g1
return R0