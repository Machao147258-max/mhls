
===== fn#0 '@src/catchGame/configReader/LadderQualifierConfig.lua' (15 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'LadderQualifierConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['getQualifierConfigByRole'] = c3
c3 = <imm2>
c2['getQualifierConfigByRoleAndElapsed'] = c3
return c2
return g1

===== fn#0 '' (40 instr, depth 1) =====
local t1 = {}
R0['roleToData'] = t1
t1 = {}
R0['roleToDataList'] = t1
t1 = <G 'ipairs'>
local t2 = R0['datas']
t1 = t1(t2)
-- goto L0
-- L2:
local t3 = R0['roleToDataList']
local t4 = R5['role']
t3 = t3[t4]
-- if not t3 goto L18
-- goto L1
t4 = {}
t3 = t4
t4 = R0['roleToDataList']
local t5 = R5['role']
t4[t5] = t3
-- L1:
t4 = <G 'table'>
t4 = t4['insert']
t5 = t3
local v6 = R5
t4 = t4(t5, v6)
-- L0:
-- op23 A=1 B=2 C=0
-- goto L2
t1 = <G 'pairs'>
t2 = R0['roleToDataList']
t1 = t1(t2)
-- goto L3
-- L4:
t3 = <G 'table'>
t3 = t3['sort']
t4 = R5
t5 = <imm0>
t3 = t3(t4, t5)
t3 = R0['roleToData']
t4 = R5[1.0]
t3[R4] = t4
-- L3:
-- op23 A=1 B=2 C=0
-- goto L4
return R0

===== fn#0 '' (14 instr, depth 2) =====
local t1 = R0['startTime']
-- if not t1 goto L4
-- goto L0
t1 = 0.0
-- L0:
local t2 = R1['startTime']
-- if not t2 goto L8
-- goto L1
t2 = 0.0
-- L1:
-- if t2 < t1 goto L11
-- goto L2
t1 = nil
-- L2:
t1 = nil
return t1
return R0