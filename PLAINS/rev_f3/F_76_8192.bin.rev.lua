
===== fn#0 '@src/catchGame/configReader/AdvancedFashionConfig.lua' (18 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'AdvancedFashionConfig'
local v4 = g1
c2 = c2(c3, v4)
c2['USE_BIN_DATA'] = True
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['getDataByFashionId'] = c3
c3 = <imm2>
c2['getRoleIds'] = c3
c3 = <imm3>
c2['getDatasByRoleId'] = c3
return c2
return g1

===== fn#0 '' (27 instr, depth 1) =====
local g1 = <G 'pairs'>
local t2 = R0['datas']
g1 = g1(t2)
-- goto L0
-- L2:
local t3 = R5['roleid']
-- if not t3 goto L14
-- goto L1
t3 = <G 'string'>
t3 = t3['toArray']
local t4 = R5['roleid']
local c5 = ';'
local n6 = nil
t3 = t3(t4, c5, n6)
R5['roleid'] = t3
-- L1:
t3 = R5['particle']
-- if not t3 goto L24
-- goto L0
t3 = <G 'string'>
t3 = t3['toArray']
t4 = R5['particle']
c5 = ';'
n6 = nil
t3 = t3(t4, c5, n6)
R5['particle'] = t3
-- L0:
-- op23 A=1 B=2 C=0
-- goto L2
return R0