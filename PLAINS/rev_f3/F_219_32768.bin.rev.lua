
===== fn#0 '@src/catchGame/configReader/ChargeGuideConfig.lua' (15 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'ChargeGuideConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['dealRewardDatas'] = c3
c3 = <imm2>
c2['dealShowDatas'] = c3
return c2
return g1

===== fn#0 '' (15 instr, depth 1) =====
local g1 = <G 'pairs'>
local t2 = R0['datas']
g1 = g1(t2)
-- goto L0
-- L1:
local m3 = R0:'dealShowDatas'
local s4 = R0
local t5 = R5['showId']
m3 = m3(s4, t5)
R5['showItem'] = m3
m3 = R0:'dealRewardDatas'
s4 = R0
t5 = R5['reward']
m3 = m3(s4, t5)
R5['rewardItem'] = m3
-- L0:
-- op23 A=1 B=2 C=0
-- goto L1
return R0