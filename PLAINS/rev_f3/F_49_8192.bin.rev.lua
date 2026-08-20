
===== fn#0 '@src/catchGame/configReader/BattlePassSeasonConfig.lua' (20 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'require'>
local c3 = 'lib/framework'
c2 = c2(c3)
c3 = <G 'class'>
local c4 = 'BattlePassSeasonConfig'
local v5 = g1
c3 = c3(c4, v5)
c4 = <imm0>
c3['dealDatas'] = c4
c4 = <imm1>
c3['getBattlePassSeasonBySeason'] = c4
c4 = <imm2>
c3['_parseIntroduceFromString'] = c4
c4 = <imm3>
c3['getValidSeasons'] = c4
return c3
return g1

===== fn#0 '' (23 instr, depth 1) =====
local g1 = <G 'pairs'>
local t2 = R0['datas']
g1 = g1(t2)
-- goto L0
-- L4:
local t3 = R5['goldShelfExchangeDiscount']
-- if not t3 goto L8
-- goto L1
t3 = 0.0
-- L1:
-- op35 A=6 B=261 C=6
R5['goldShelfCrystalDiscount'] = t3
t3 = R5['skillPointBuyLimit']
-- if not t3 goto L14
-- goto L2
t3 = 0.0
-- L2:
R5['skillPointBuyLimit'] = t3
t3 = R5['skillPointNeedNum']
-- if not t3 goto L19
-- goto L3
t3 = 1.0
-- L3:
R5['skillPointNeedNum'] = t3
-- L0:
-- op23 A=1 B=2 C=0
-- goto L4
return R0