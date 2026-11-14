
===== fn#0 '@src/catchGame/systems/ExchangeSystem.lua' (50 instr, depth 0) =====
local g1 = <G 'tostring'>
local g2 = <G 'cg'>
local g3 = <G 'require'>
local c4 = 'catchGame/systems/BaseSystem'
g3 = g3(c4)
c4 = <G 'require'>
local c5 = 'catchGame/ClientEventManager'
c4 = c4(c5)
c5 = <G 'require'>
local c6 = 'catchGame/utils/Utils'
c5 = c5(c6)
c6 = <G 'require'>
local c7 = 'common/utils'
c6 = c6(c7)
c7 = <G 'require'>
local c8 = 'lib/scheduler'
c7 = c7(c8)
c8 = <G 'require'>
local c9 = 'cjson'
c8 = c8(c9)
c9 = <G 'class'>
local c10 = 'ExchangeSystem'
local v11 = g3
c9 = c9(c10, v11)
c10 = 200.0
v11 = <imm0>
g1 = g3
c9['ctor'] = v11
v11 = <imm1>
g1 = g3
c9['init'] = v11
v11 = <imm2>
g1 = g3
c9['reset'] = v11
v11 = <imm3>
c9['registEvent'] = v11
v11 = <imm4>
g1 = g1
c9['exchangeGift'] = v11
v11 = <imm5>
g1 = c10
g1 = g2
g1 = g1
g1 = c4
c9['onExchangeGift'] = v11
v11 = <imm6>
g1 = c4
c9['onExchangeGiftError'] = v11
return c9
return g1

===== fn#0 '' (5 instr, depth 1) =====
local t1 = R1['ctor']
local v2 = R0
t1 = t1(v2)
return R0