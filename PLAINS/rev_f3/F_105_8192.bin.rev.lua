
===== fn#0 '@src/catchGame/configReader/RankListConfig.lua' (11 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'RankListConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['dealDatas'] = c3
return c2
return g1

===== fn#0 '' (40 instr, depth 1) =====
local g1 = <G 'pairs'>
local t2 = R0['datas']
g1 = g1(t2)
-- goto L0
-- L7:
local t3 = R5['friendSwitch']
-- if 1.0 ~= t3 goto L8
-- goto L1
t3 = nil
-- L1:
t3 = nil
R5['friendSwitch'] = t3
t3 = R5['zoneSwitch']
-- if 1.0 ~= t3 goto L14
-- goto L2
t3 = nil
-- L2:
t3 = nil
R5['zoneSwitch'] = t3
t3 = R5['catMouseSwitch']
-- if 1.0 ~= t3 goto L20
-- goto L3
t3 = nil
-- L3:
t3 = nil
R5['catMouseSwitch'] = t3
t3 = R5['switch']
-- if 1.0 ~= t3 goto L26
-- goto L4
t3 = nil
-- L4:
t3 = nil
R5['switch'] = t3
t3 = R5['regionSelectSwitch']
-- if 0.0 ~= t3 goto L34
-- goto L5
t3 = R5['regionSelectSwitch']
-- if False == t3 goto L35
-- goto L6
-- L5:
t3 = nil
-- L6:
t3 = nil
R5['regionSelectSwitch'] = t3
-- L0:
-- op23 A=1 B=2 C=0
-- goto L7
return R0