
===== fn#0 '@src/catchGame/configReader/Spring2026Config.lua' (19 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'Spring2026Config'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['getValidRoadMapConfigs'] = c3
c3 = <imm1>
c2['checkValid'] = c3
c3 = <imm2>
c2['checkHaveFreeGoodsStar'] = c3
c3 = <imm3>
c2['getNeedShowBubbleGeneralMallID'] = c3
c3 = <imm4>
c2['getValidEntries'] = c3
return c2
return g1

===== fn#0 '' (48 instr, depth 1) =====
local m1 = R0:'getDataById'
local s2 = R0
local v3 = R1
m1 = m1(s2, v3)
s2 = <G 'cg'>
s2 = s2['Game']
s2 = s2:'newNowTime'
v3 = s2
s2 = s2(v3)
v3 = {}
local i4 = <imm0>
local v5 = s2
local v6 = i4
local t7 = m1['roadMapID']
v6 = v6(t7)
-- if not v6 goto L24
-- goto L0
t7 = <G 'table'>
t7 = t7['insert']
local v8 = v3
local t9 = {}
t9['isMain'] = True
local t10 = m1['roadMapID']
t9['roadMapID'] = t10
t9['roadMapConfig'] = v6
t7 = t7(v8, t9)
-- L0:
t7 = <G 'ipairs'>
v8 = m1['roadMapBranchIDs']
-- if not v8 goto L29
-- goto L1
v8 = {}
-- L1:
t7 = t7(v8, t9, t10)
-- goto L2
-- L3:
local v11 = i4
local v12 = R11
v11 = v11(v12)
-- if not v11 goto L44
-- goto L2
v12 = <G 'table'>
v12 = v12['insert']
local v13 = v3
local t14 = {}
t14['isMain'] = False
t14['roadMapID'] = R11
t14['roadMapConfig'] = v11
v12 = v12(v13, t14)
-- L2:
-- op23 A=7 B=2 C=0
-- goto L3
return v3
return v5

===== fn#0 '' (17 instr, depth 2) =====
local g1 = <G 'cg'>
g1 = g1['ActivityRoadMapConfig']
g1 = g1:'getDataById'
local s2 = g1
local v3 = R0
g1 = g1(s2, v3)
s2 = g1['startTimeStamp']
-- if v3 <= s2 goto L14
-- goto L0
v3 = g1['endTimeStamp']
-- if v3 <= s2 goto L14
-- goto L0
return g1
-- L0:
s2 = nil
return s2
return R0