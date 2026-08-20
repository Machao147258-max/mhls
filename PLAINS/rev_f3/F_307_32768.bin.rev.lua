
===== fn#0 '@src/catchGame/configReader/LionDanceConfig.lua' (36 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'LionDanceConfig'
local v4 = g1
c2 = c2(c3, v4)
c2['configID'] = 1.0
c3 = <G 'cg'>
c3 = c3['systems']
c3 = c3['LionDanceSystem']
v4 = <imm0>
c2['getConfig'] = v4
v4 = <imm1>
c2['dealDatas'] = v4
v4 = <imm2>
c2['getQuestIDConfigByDataFile'] = v4
v4 = <imm3>
c2['getRewardDatas'] = v4
v4 = <imm4>
c2['getOpenDaysNow'] = v4
v4 = <imm5>
g1 = c3
c2['getNowLanternRewardCout'] = v4
v4 = <imm6>
g1 = c3
c2['getCampDatasByOpenDay'] = v4
v4 = <imm7>
g1 = c3
c2['gettCampDatas'] = v4
v4 = <imm8>
c2['getQuestDataByID'] = v4
v4 = <imm9>
c2['getQuestDataByIndex'] = v4
return c2
return g1

===== fn#0 '' (5 instr, depth 1) =====
local m1 = R0:'getDataById'
local s2 = R0
local t3 = R0['configID']
m1 = false
return m1
return R0