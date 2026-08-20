
===== fn#0 '@src/catchGame/configReader/BingoChessActivityConfig.lua' (16 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'BingoChessActivityConfig'
local v4 = g1
c2 = c2(c3, v4)
c2['configID'] = 1.0
c3 = <imm0>
c2['getConfig'] = c3
c3 = <imm1>
c2['dealDatas'] = c3
c3 = <imm2>
c2['initDiscount'] = c3
return c2
return g1

===== fn#0 '' (5 instr, depth 1) =====
local m1 = R0:'getDataById'
local s2 = R0
local t3 = R0['configID']
m1 = false
return m1
return R0