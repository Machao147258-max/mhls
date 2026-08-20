
===== fn#0 '@src/catchGame/configReader/SkillTemporaryFreeConfig.lua' (15 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'SkillTemporaryFreeConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['getInPeriodRow'] = c3
c3 = <imm1>
c2['isInPeriod'] = c3
c3 = <imm2>
c2['getEndTimeStamp'] = c3
return c2
return g1

===== fn#0 '' (36 instr, depth 1) =====
local g1 = <G 'cg'>
g1 = g1['SystemSwitchConfig']
g1 = g1:'getSwitch'
local s2 = g1
local g3 = <G 'NetGameEnum'>
g3 = g3['E_SYSTEM_SWITCH_TYPE']
g3 = g3['E_SYSTEM_SWITCH_TYPE_SKILL_TEMPORARY_FREE']
g1 = g1(s2, g3)
-- if not g1 goto L10
-- goto L0
return R0
-- L0:
g1 = <G 'cg'>
g1 = g1['Game']
g1 = g1:'nowTime'
s2 = g1
g1 = g1(s2, g3)
s2 = <G 'pairs'>
g3 = R0['datas']
s2 = s2(g3)
-- goto L1
-- L2:
local t4 = R6['startTimeStamp']
-- if not t4 goto L31
-- goto L1
t4 = R6['endTimeStamp']
-- if not t4 goto L31
-- goto L1
t4 = R6['startTimeStamp']
-- if g1 <= t4 goto L31
-- goto L1
t4 = R6['endTimeStamp']
-- if t4 < g1 goto L31
-- goto L1
return R6
-- L1:
-- op23 A=2 B=2 C=0
-- goto L2
s2 = nil
return s2
return R0