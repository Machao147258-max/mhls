
===== fn#0 '@src/catchGame/configReader/ChipShopConfig.lua' (13 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'ChipShopConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['isFashionBannedByRank'] = c3
return c2
return g1

===== fn#0 '' (60 instr, depth 1) =====
local g1 = <G 'pairs'>
local t2 = R0['datas']
g1 = g1(t2)
-- goto L0
-- L6:
local t3 = {}
R5['additionGoodsIDList'] = t3
t3 = R5['additionGoodsIDs']
-- if not t3 goto L26
-- goto L1
t3 = <G 'string'>
t3 = t3['toArray']
local t4 = R5['additionGoodsIDs']
local c5 = ','
local n6 = nil
t3 = t3(t4, c5, n6)
t4 = <G 'ipairs'>
c5 = t3
t4 = t4(c5, n6)
-- goto L2
-- L3:
local g7 = <G 'table'>
g7 = g7['insert']
local t8 = R5['additionGoodsIDList']
local v9 = R11
g7 = g7(t8, v9)
-- L2:
-- op23 A=7 B=2 C=0
-- goto L3
-- L1:
t3 = R5['excludeGoodsIDs']
-- if not t3 goto L36
-- goto L4
t3 = <G 'string'>
t3 = t3['toArray']
t4 = R5['excludeGoodsIDs']
c5 = ','
n6 = nil
t3 = t3(t4, c5, n6)
R5['excludeGoodsIDs'] = t3
-- L4:
t3 = R5['exclude_skin_rank']
-- if not t3 goto L45
-- goto L5
t3 = <G 'string'>
t3 = t3['toArray']
t4 = R5['exclude_skin_rank']
c5 = ','
t3 = t3(t4, c5, n6)
R5['excludeSkinRanks'] = t3
-- L5:
t3 = <G 'cg'>
t3 = t3['Utils']
t3 = t3['convertTime']
t4 = R5['startTime']
t3 = t3(t4, c5, n6)
R5['startTimeStamp'] = t3
t3 = <G 'cg'>
t3 = t3['Utils']
t3 = t3['convertTime']
t4 = R5['endTime']
t3 = t3(t4, c5, n6)
R5['endTimeStamp'] = t3
-- L0:
-- op23 A=1 B=2 C=0
-- goto L6
return R0