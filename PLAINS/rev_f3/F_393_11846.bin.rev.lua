
===== fn#0 '@src/catchGame/configReader/SPGachaConfig.lua' (61 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'SPGachaConfig'
local v4 = g1
c2 = c2(c3, v4)
c2['configID'] = 1.0
c3 = 86400.0
v4 = 'SPGachaTimeStampClear'
local g5 = <G 'tostring'>
local g6 = <G 'cg'>
g6 = g6['Player']
g6 = g6['uid']
g5 = g5(g6)
v4 = v4 .. g5
g5 = 'SPGachaNewFashionCheck'
g6 = <G 'tostring'>
local g7 = <G 'cg'>
g7 = g7['Player']
g7 = g7['uid']
g6 = g6(g7)
g5 = g5 .. g6
g6 = <imm0>
c2['dealDatas'] = g6
g6 = <imm1>
c2['getConfig'] = g6
g6 = <imm2>
c2['initPools'] = g6
g6 = <imm3>
c2['sortPools'] = g6
g6 = <imm4>
c2['initLabels'] = g6
g6 = <imm5>
c2['getLabels'] = g6
g6 = <imm6>
c2['getLabelByCount'] = g6
g6 = <imm7>
c2['getLabelDesc'] = g6
g6 = <imm8>
c2['getNewFashions'] = g6
g6 = <imm9>
g1 = c3
g1 = v4
c2['checkClearRedDot'] = g6
g6 = <imm10>
g1 = c3
g1 = v4
c2['setClearRedDot'] = g6
g6 = <imm11>
g1 = g5
c2['checkNewFashionRedDot'] = g6
g6 = <imm12>
g1 = g5
c2['setNewFashionRedDot'] = g6
g6 = <imm13>
c2['initSkinPoolsAndItemPools'] = g6
g6 = <imm14>
c2['getskinBySkinPools'] = g6
return c2
return g1

===== fn#0 '' (23 instr, depth 1) =====
local g1 = <G 'pairs'>
local t2 = R0['datas']
g1 = g1(t2)
-- goto L0
-- L1:
local t3 = {}
R5['sellSlots'] = t3
t3 = R5['privilegemallSellSlotIDs']
-- if not t3 goto L16
-- goto L0
t3 = <G 'string'>
t3 = t3['toArray']
local t4 = R5['privilegemallSellSlotIDs']
local c5 = ','
local n6 = nil
t3 = t3(t4, c5, n6)
R5['sellSlots'] = t3
-- L0:
-- op23 A=1 B=2 C=0
-- goto L1
g1 = R0:'initPools'
t2 = R0
g1 = g1(t2)
g1 = R0:'initLabels'
t2 = R0
g1 = g1(t2)
return R0