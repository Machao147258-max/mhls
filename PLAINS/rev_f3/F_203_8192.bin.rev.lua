
===== fn#0 '@src/catchGame/configReader/PopupTypeConfig.lua' (27 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'PopupTypeConfig'
local v4 = g1
c2 = c2(c3, v4)
c2['COUST_MAX'] = 3.0
c2['QUEUE_MAX'] = 1.0
c2['FORCE_WEIGHT'] = -99999.0
c2['QUEUE_WEIGHT'] = -9999.0
c3 = <imm0>
c2['getCountMax'] = c3
c3 = <imm1>
c2['getQueueMax'] = c3
c3 = <imm2>
c2['getRankWithForceByID'] = c3
c3 = <imm3>
c2['getQueueWeightByID'] = c3
c3 = <imm4>
c2['setQueueTimeByID'] = c3
c3 = <imm5>
c2['getIdByRank'] = c3
c3 = <imm6>
c2['getRankWithForceAndQueueByID'] = c3
return c2
return g1

===== fn#0 '' (15 instr, depth 1) =====
local t1 = R0['datas']
-- if not t1 goto L14
-- goto L0
t1 = R0['datas']
t1 = t1[1.0]
-- if not t1 goto L14
-- goto L0
t1 = R0['datas']
t1 = t1[1.0]
t1 = t1['daily_max_popup']
-- if not t1 goto L13
-- goto L1
t1 = R0['COUST_MAX']
-- L1:
return t1
-- L0:
return R0