
===== fn#0 '@src/catchGame/systems/Logs/SquareTryOnLog.lua' (20 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/systems/Logs/logBase'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'SquareTryOnLog'
local v4 = g1
c2 = c2(c3, v4)
c3 = <G 'cg'>
c3 = c3['require']
v4 = 'DataHelper'
c3 = c3(v4)
v4 = <imm0>
c2['doEvent'] = v4
v4 = <imm1>
c2['_onTryOnStart'] = v4
v4 = <imm2>
g1 = c3
c2['_onTryOnEnd'] = v4
return c2
return g1

===== fn#0 '' (19 instr, depth 1) =====
local g1 = <G 'cg'>
g1 = g1['ClientEventManager']
g1 = g1['register']
local g2 = <G 'cg'>
g2 = g2['ClientEventManager']
g2 = g2['ON_SQUARE_TRY_ON_START']
local v3 = R0
local t4 = R0['_onTryOnStart']
g1 = g1(g2, v3)
g1 = <G 'cg'>
g1 = g1['ClientEventManager']
g1 = g1['register']
g2 = <G 'cg'>
g2 = g2['ClientEventManager']
g2 = g2['ON_SQUARE_TRY_ON_END']
v3 = R0
t4 = R0['_onTryOnEnd']
g1 = g1(g2, v3)
return R0