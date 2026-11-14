
===== fn#0 '@src/catchGame/systems/RechargeSumSystem.lua' (70 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/systems/BaseSystem'
g1 = g1(c2)
c2 = <G 'require'>
local c3 = 'catchGame/ClientEventManager'
c2 = c2(c3)
c3 = <G 'require'>
local c4 = 'catchGame/utils/Utils'
c3 = c3(c4)
c4 = <G 'require'>
local c5 = 'common/utils'
c4 = c4(c5)
c5 = <G 'require'>
local c6 = 'cjson'
c5 = c5(c6)
c6 = <G 'class'>
local c7 = 'RechargeSumSystem'
local v8 = g1
c6 = c6(c7, v8)
c6['DIAMOND_GIFT'] = 1.0
c6['POINT_ITEM_ID'] = 1000809.0
c7 = <imm0>
g1 = g1
c6['ctor'] = c7
c7 = <imm1>
g1 = g1
c6['init'] = c7
c7 = <imm2>
g1 = g1
c6['reset'] = c7
c7 = <imm3>
g1 = c2
c6['registEvent'] = c7
c7 = <imm4>
c6['onConsumeInfoNtf'] = c7
c7 = <imm5>
c6['onConsumeRewardInfoNtf'] = c7
c7 = <imm6>
c6['reqConsumeRewardGet'] = c7
c7 = <imm7>
g1 = c3
c6['onConsumeRewardGetSuccess'] = c7
c7 = <imm8>
c6['onConsumeRewardGetError'] = c7
c7 = <imm9>
c6['getAllRewardInfo'] = c7
c7 = <imm10>
c6['getCurrentStageInfo'] = c7
c7 = <imm11>
c6['getCanGetRewardStageInfos'] = c7
c7 = <imm12>
c6['checkRedDot'] = c7
c7 = <imm13>
c6['_calcStageIndex'] = c7
c7 = <imm14>
c6['getNextStageInfo'] = c7
c7 = <imm15>
c6['getStageIndex'] = c7
c7 = <imm16>
c6['_formatRechargeSumData'] = c7
c7 = <imm17>
c6['updateConfigPoint'] = c7
c7 = <imm18>
c6['_updateConsumeInfo'] = c7
c7 = <imm19>
c6['_updateRewardStageInfo'] = c7
c7 = <imm20>
c6['_updateSystemLockInfo'] = c7
return c6
return g1

===== fn#0 '' (5 instr, depth 1) =====
local t1 = R1['ctor']
local v2 = R0
t1 = t1(v2)
return R0