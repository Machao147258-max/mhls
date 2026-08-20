
===== fn#0 '@src/catchGame/configReader/ChristmasMainConfig.lua' (23 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'ChristmasMainConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['getLevelRanges'] = c3
c3 = <imm1>
c2['getLevelBox'] = c3
c3 = <imm2>
c2['getLevelLimit'] = c3
c3 = <imm3>
c2['getEndTime'] = c3
c3 = <imm4>
c2['getStartTime'] = c3
c3 = <imm5>
c2['isOpen'] = c3
c3 = <imm6>
c2['isValidOrnamentId'] = c3
return c2
return g1

===== fn#0 '' (19 instr, depth 1) =====
local t1 = {}
local t2 = R0['datas']
t2 = t2[1.0]
t2 = t2['level_1_range']
local t3 = R0['datas']
t3 = t3[1.0]
t3 = t3['level_2_range']
local t4 = R0['datas']
t4 = t4[1.0]
t4 = t4['level_3_range']
local t5 = R0['datas']
t5 = t5[1.0]
t5 = t5['level_4_range']
local t6 = R0['datas']
t6 = t6[1.0]
t6 = t6['level_5_range']
t1 = t5 .. t1
return t1
return R0