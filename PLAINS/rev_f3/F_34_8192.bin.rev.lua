
===== fn#0 '@src/catchGame/configReader/PartnerSkillUnlockConfig.lua' (15 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'PartnerPropertyConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['getCostById'] = c3
c3 = <imm2>
c2['getDefaultSkills'] = c3
return c2
return g1

===== fn#0 '' (54 instr, depth 1) =====
local t1 = {}
R0['skillDatas'] = t1
t1 = {}
R0['defaultSkills'] = t1
t1 = <G 'pairs'>
local t2 = R0['datas']
t1 = t1(t2)
-- goto L0
-- L2:
local t3 = R0['skillDatas']
t3[R4] = R5
t3 = {}
local c4 = 1.0
local c5 = 10.0
local c6 = 1.0
-- op6 A=7 B=23 C=256
local c7 = 'costCoin'
local v8 = R10
local c9 = 'Id'
c7 = c7 .. c9
c7 = R5[c7]
-- if not c7 goto L39
-- goto L1
c7 = <G 'table'>
c7 = c7['insert']
v8 = t3
c9 = {}
local c10 = 'costCoin'
local v11 = R10
local c12 = 'Id'
c10 = c10 .. c12
c10 = R5[c10]
c9['id'] = c10
c10 = 'costCoin'
v11 = R10
c12 = 'Num'
c10 = c10 .. c12
c10 = R5[c10]
c9['num'] = c10
c7 = c7(v8, c9)
-- L1:
-- op8 A=7 B=486 C=255
c4 = R0['skillDatas']
c4 = c4[R4]
c4['cost'] = t3
-- op29 A=7 B=0 C=6
-- if 0.0 == c4 goto L51
-- goto L0
c4 = <G 'table'>
c4 = c4['insert']
c5 = R0['defaultSkills']
c6 = R4
c4 = c4(c5, c6)
-- L0:
-- op23 A=1 B=2 C=0
-- goto L2
return R0