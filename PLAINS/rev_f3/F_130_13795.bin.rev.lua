
===== fn#0 '@src/catchGame/configReader/ActivityListConfig.lua' (70 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'NetGameEnum'>
c2 = c2['E_ACTIVITY_TYPE']
c2 = c2['E_ACTIVITY_GENERAL_QUEST']
local g3 = <G 'NetGameEnum'>
g3 = g3['E_ACTIVITY_TYPE']
g3 = g3['E_ACTIVITY_GENERAL_MALL']
local g4 = <G 'NetGameEnum'>
g4 = g4['E_ACTIVITY_TYPE']
g4 = g4['E_ACTIVITY_AD_FACE']
local g5 = <G 'class'>
local c6 = 'ActivityListConfig'
local v7 = g1
g5 = g5(c6, v7)
c6 = <imm0>
g5['getDataByType'] = c6
c6 = <imm1>
g5['getLocalTypeActivity'] = c6
c6 = <imm2>
g1 = g4
g1 = c2
g5['dealDatas'] = c6
c6 = <imm3>
g5['isExistQuestTypeConfig'] = c6
c6 = <imm4>
g1 = c2
g5['getAllGeneralQuestActivity'] = c6
c6 = <imm5>
g1 = g3
g5['getAllGeneralMallActivity'] = c6
c6 = <imm6>
g1 = c2
g5['getDataByQuestType'] = c6
c6 = <imm7>
g5['isLoginActivity'] = c6
c6 = <imm8>
g5['isDailyBattle'] = c6
c6 = <imm9>
g5['isGeneralTask'] = c6
c6 = <imm10>
g5['getAllActivityByType'] = c6
c6 = <imm11>
g5['getActivityBySubtype'] = c6
c6 = <imm12>
g5['getAllActivityIDByType'] = c6
c6 = <imm13>
g5['isAcccumRecharge'] = c6
c6 = <imm14>
g5['isSpringRedPacket'] = c6
c6 = <imm15>
g5['isSevenDayChallenge'] = c6
c6 = <imm16>
g5['isNationalBox'] = c6
c6 = <imm17>
g5['isUiType'] = c6
c6 = <imm18>
g5['isMonthRecharge'] = c6
c6 = <imm19>
g5['isDailyMeal'] = c6
c6 = <imm20>
g1 = g4
g5['isActivitySignUp'] = c6
c6 = <imm21>
g5['checkUIName'] = c6
c6 = <imm22>
g5['getActivityByTab'] = c6
return g5
return g1

===== fn#0 '' (18 instr, depth 1) =====
local g1 = <G 'pairs'>
local t2 = R0['datas']
g1 = g1(t2)
-- goto L0
-- L1:
local t3 = R6['type']
-- if R1 == t3 goto L8
-- goto L0
return R6
-- L0:
-- op23 A=2 B=2 C=0
-- goto L1
g1 = <G 'logDebug'>
t2 = 'Not Find ActivityList Data, activType --- '
local g4 = <G 'tostring'>
local v5 = R1
g4 = g4(v5)
t2 = t2 .. g4
g1 = g1(t2, g4)
return R0