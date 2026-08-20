
===== fn#0 '@src/catchGame/configReader/ReputationLevelConfig.lua' (15 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'ReputationConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['getLevelByExp'] = c3
c3 = <imm2>
c2['getMaxLevel'] = c3
return c2
return g1

===== fn#0 '' (38 instr, depth 1) =====
local g1 = <G 'pairs'>
local t2 = R0['datas']
g1 = g1(t2)
-- goto L0
-- L2:
local t3 = {}
R5['items'] = t3
t3 = 1.0
local c4 = 10.0
local c5 = 1.0
-- op6 A=6 B=23 C=256
local c6 = 'item'
local v7 = R9
local c8 = 'Type'
c6 = c6 .. c8
c6 = R5[c6]
-- if not c6 goto L34
-- goto L1
c6 = 'item'
v7 = R9
c8 = 'Type'
c6 = c6 .. c8
c6 = R5[c6]
v7 = 'item'
c8 = R9
local c9 = 'ID'
v7 = v7 .. c9
v7 = R5[v7]
c8 = <G 'table'>
c8 = c8['insert']
c9 = R5['items']
local t10 = {}
t10['type'] = c6
t10['id'] = v7
c8 = c8(c9, t10)
-- L1:
-- op8 A=6 B=486 C=255
-- L0:
-- op23 A=1 B=2 C=0
-- goto L2
return R0