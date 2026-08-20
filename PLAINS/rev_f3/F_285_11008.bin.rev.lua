
===== fn#0 '@src/catchGame/configReader/FunTravelPassportConfig.lua' (75 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'FunTravelPassportConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['_calcWeekTaskTotalRounds'] = c3
c3 = <imm2>
c2['getWeekTaskTotalRounds'] = c3
c3 = <imm3>
c2['getConfig'] = c3
c3 = <imm4>
c2['getActivityId'] = c3
c3 = <imm5>
c2['getEndTime'] = c3
c3 = <imm6>
c2['getStartTime'] = c3
c3 = <imm7>
c2['getStartTimeStamp'] = c3
c3 = <imm8>
c2['getEndTimeStamp'] = c3
c3 = <imm9>
c2['isInActivityTime'] = c3
c3 = <imm10>
c2['getMaxLevel'] = c3
c3 = <imm11>
c2['getActivityPerLevel'] = c3
c3 = <imm12>
c2['getGoldShelfGoodsId'] = c3
c3 = <imm13>
c2['getGoldShelfAdvancedGoodsId'] = c3
c3 = <imm14>
c2['getGoldShelfAdvancedUpdateLevel'] = c3
c3 = <imm15>
c2['getCoinIdTicket'] = c3
c3 = <imm16>
c2['getCoinIdActivity'] = c3
c3 = <imm17>
c2['getDesc'] = c3
c3 = <imm18>
c2['getDailyActivityId'] = c3
c3 = <imm19>
c2['getRefreshWeekday'] = c3
c3 = <imm20>
c2['getRefreshHour'] = c3
c3 = <imm21>
c2['getName'] = c3
c3 = <imm22>
c2['getGoldShelfValue'] = c3
c3 = <imm23>
c2['getPlusShelfValue'] = c3
c3 = <imm24>
c2['getFashionID'] = c3
c3 = <imm25>
c2['getGoldUnlockItem'] = c3
c3 = <imm26>
c2['getPlusUnlockItem'] = c3
c3 = <imm27>
c2['getEntranceImage'] = c3
c3 = <imm28>
c2['getEntranceRole100Image'] = c3
c3 = <imm29>
c2['getEntranceImageOpen'] = c3
c3 = <imm30>
c2['getEntranceRole100ImageOpen'] = c3
c3 = <imm31>
c2['getGoldShelfAdvancedBuyItems'] = c3
c3 = <imm32>
c2['getGoldShelfAdvancedTicketNum'] = c3
return c2
return g1

===== fn#0 '' (13 instr, depth 1) =====
R0['_config'] = None
local g1 = <G 'pairs'>
local t2 = R0['datas']
g1 = g1(t2)
-- goto L0
-- L2:
R0['_config'] = R5
-- goto L1
-- L0:
-- op23 A=1 B=2 C=0
-- goto L2
-- L1:
g1 = R0:'_calcWeekTaskTotalRounds'
t2 = R0
g1 = g1(t2)
R0['_weekTaskTotalRounds'] = g1
return R0