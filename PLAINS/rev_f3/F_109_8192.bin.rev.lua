
===== fn#0 '@src/catchGame/configReader/DiamondCostConfig.lua' (15 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'DiamondCostConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = {}
v4 = <imm0>
g1 = c3
c2['dealDatas'] = v4
v4 = <imm1>
c2['getRewardDataByID'] = v4
return c2
return g1

===== fn#0 '' (64 instr, depth 1) =====
local t1 = {}
R0['idRewards'] = t1
t1 = <G 'ipairs'>
local t2 = R0['datas']
t1 = t1(t2)
-- goto L0
-- L7:
local t3 = R5['rewardConfig']
-- if not t3 goto L61
-- goto L0
local t4 = R5['rewardConfig']
t3 = t3[t4]
-- if not t3 goto L24
-- goto L1
t4 = R5['rewardConfig']
local g5 = <G 'require'>
local g6 = <G 'string'>
g6 = g6['format']
local c7 = 'catchGame/data/%s'
local t8 = R5['rewardConfig']
g6 = g6(c7)
g5 = g5(g6, c7, t8)
t3[t4] = g5
-- L1:
t4 = R5['rewardConfig']
t3 = t3[t4]
-- if not t3 goto L61
-- goto L0
t4 = <G 'clone'>
g5 = t3
t4 = t4(g5, g6, c7)
t3 = t4
t4 = <G 'ipairs'>
g5 = t3
t4 = t4(g5, g6, c7, t8)
-- goto L2
-- L6:
local t9 = t8['show1Type']
-- if not t9 goto L41
-- goto L3
t9 = t8['item1Type']
-- L3:
t8['show1Type'] = t9
t9 = t8['show1ID']
-- if not t9 goto L46
-- goto L4
t9 = t8['item1ID']
-- L4:
t8['show1ID'] = t9
t9 = t8['show1Num']
-- if not t9 goto L51
-- goto L5
t9 = t8['item1Num']
-- L5:
t8['show1Num'] = t9
-- L2:
-- op23 A=7 B=2 C=0
-- goto L6
t4 = <G 'table'>
t4 = t4['sort']
g5 = t3
g6 = <imm0>
t4 = t4(g5, g6)
t4 = R0['idRewards']
t4[R4] = t3
-- L0:
-- op23 A=1 B=2 C=0
-- goto L7
return R0

===== fn#0 '' (8 instr, depth 2) =====
local t1 = R0['needNum']
local t2 = R1['needNum']
-- if t2 < t1 goto L5
-- goto L0
t1 = nil
-- L0:
t1 = nil
return t1
return R0