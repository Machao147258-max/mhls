
===== fn#0 '@src/catchGame/utils/HttpHelper.lua' (15 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'cocos/json'
g1 = g1(c2)
g1 = {}
c2 = <imm0>
g1['encode'] = c2
c2 = <imm1>
g1['decode'] = c2
c2 = <imm2>
g1 = g1
g1['newHttpRequest'] = c2
c2 = <G 'cg'>
c2['HttpHelper'] = g1
return g1
return g1

===== fn#0 '' (26 instr, depth 1) =====
local c1 = ''
local g2 = <G 'pairs'>
local v3 = R0
g2 = g2(v3)
-- goto L0
-- L2:
-- if '' ~= c1 goto L10
-- goto L1
local v4 = c1
local c5 = '&'
c1 = v4 .. c5
-- L1:
v4 = c1
c5 = <G 'string'>
c5 = c5['format']
local c6 = '%s=%s'
local g7 = <G 'tostring'>
local v8 = R5
g7 = g7(v8)
v8 = <G 'tostring'>
local v9 = R6
v8 = v8(v9)
c5 = c5(c6, g7, v8)
c1 = v4 .. c5
-- L0:
-- op23 A=2 B=2 C=0
-- goto L2
return c1
return R0