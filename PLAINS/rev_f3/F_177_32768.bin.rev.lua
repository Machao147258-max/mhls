
===== fn#0 '@src/catchGame/configReader/PrivilegeServiceConfig.lua' (17 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'PrivilegeServiceConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['getMembershipLevelByChatFrame'] = c3
c3 = <imm2>
c2['getPrivilegeConfigByCheckInCardID'] = c3
c3 = <imm3>
c2['getCheckinCardIDsByPrivilegeID'] = c3
return c2
return g1

===== fn#0 '' (17 instr, depth 1) =====
local g1 = <G 'pairs'>
local t2 = R0['datas']
g1 = g1(t2)
-- goto L0
-- L1:
local t3 = R5['privilege']
-- if not t3 goto L14
-- goto L0
t3 = <G 'string'>
t3 = t3['toArray']
local t4 = R5['privilege']
local c5 = ','
local n6 = nil
t3 = t3(t4, c5, n6)
R5['privileges'] = t3
-- L0:
-- op23 A=1 B=2 C=0
-- goto L1
return R0