
===== fn#0 '@src/catchGame/configReader/ItemConfig2.lua' (39 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'require'>
local c3 = 'lib/ds/ShallowDataClone'
c2 = c2(c3)
c3 = <G 'class'>
local c4 = 'ItemConfig2'
local v5 = g1
c3 = c3(c4, v5)
c4 = {}
c4['low'] = 1001611.0
c4['med'] = 1001612.0
c4['high'] = 1001613.0
c3['BOOSTER'] = c4
c3['USE_BIN_DATA'] = True
c4 = <imm0>
c3['dealDatas'] = c4
c4 = <imm1>
c3['getItems'] = c4
c4 = <imm2>
c3['getGiftDataName'] = c4
c4 = <imm3>
c3['getGiftDataNameById'] = c4
c4 = <imm4>
c3['getItemByType'] = c4
c4 = <imm5>
g1 = c2
c3['getItemByByTypeAndId'] = c4
c4 = <imm6>
c3['getItemByByTypeAndIdNoClone'] = c4
c4 = <imm7>
c3['getComExprienceType'] = c4
c4 = <imm8>
c3['isDye'] = c4
c4 = <imm9>
c3['getItemsByItem1TypeAndItem1ID'] = c4
return c3
return g1

===== fn#0 '' (149 instr, depth 1) =====
local t1 = {}
R0['types'] = t1
t1 = {}
R0['item1List'] = t1
t1 = <G 'pairs'>
local t2 = R0['datas']
t1 = t1(t2)
-- goto L0
-- L14:
local t3 = {}
R5['items'] = t3
t3 = 1.0
-- L3:
local c4 = 'item'
local v5 = t3
local c6 = 'Type'
c4 = c4 .. c6
c4 = R5[c4]
-- if not c4 goto L52
-- goto L1
c4 = 'item'
v5 = t3
c6 = 'Type'
c4 = c4 .. c6
c4 = R5[c4]
v5 = 'item'
c6 = t3
local c7 = 'ID'
v5 = v5 .. c7
v5 = R5[v5]
c6 = 'item'
c7 = t3
local c8 = 'Num'
c6 = c6 .. c8
c6 = R5[c6]
c7 = 'item'
c8 = t3
local c9 = 'Time'
c7 = c7 .. c9
c7 = R5[c7]
-- if not c7 goto L41
-- goto L2
c7 = 0.0
-- L2:
c8 = <G 'table'>
c8 = c8['insert']
c9 = R5['items']
local t10 = {}
t10['type'] = c4
t10['id'] = v5
t10['num'] = c6
t10['time'] = c7
c8 = c8(c9, t10)
-- op19 A=6 B=261 C=6
-- goto L3
-- L1:
c4 = {}
R5['showItems'] = c4
t3 = 1.0
-- L5:
c4 = 'show'
v5 = t3
c6 = 'Type'
c4 = c4 .. c6
c4 = R5[c4]
-- if not c4 goto L87
-- goto L4
c4 = 'show'
v5 = t3
c6 = 'Type'
c4 = c4 .. c6
c4 = R5[c4]
v5 = 'show'
c6 = t3
c7 = 'ID'
v5 = v5 .. c7
v5 = R5[v5]
c6 = 'show'
c7 = t3
c8 = 'Num'
c6 = c6 .. c8
c6 = R5[c6]
c7 = <G 'table'>
c7 = c7['insert']
c8 = R5['showItems']
c9 = {}
c9['type'] = c4
c9['id'] = v5
c9['showNum'] = c6
c7 = c7(c8, c9)
-- op19 A=6 B=261 C=6
-- goto L5
-- L4:
c4 = R5['expireDay']
-- if not c4 goto L104
-- goto L6
c4 = R5['expireDay']
-- if 0.0 ~= c4 goto L104
-- goto L6
c4 = R5['name']
v5 = '('
c6 = R5['expireDay']
c7 = <G 'cg'>
c7 = c7['StringConfig']
c7 = c7:'getString'
c8 = c7
c9 = 'Day'
c7 = c7(c8, c9, t10)
c8 = ')'
c4 = c4 .. c8
R5['expireName'] = c4
-- L6:
c4 = R5['type']
-- if not c4 goto L108
-- goto L7
c4 = 0.0
-- L7:
v5 = R0['types']
v5 = v5[c4]
-- if not v5 goto L116
-- goto L8
c6 = {}
v5 = c6
c6 = R0['types']
c6[c4] = v5
-- L8:
c6 = R5['item1ID']
-- if not c6 goto L120
-- goto L9
c6 = 0.0
-- L9:
c7 = v5[c6]
-- if not c7 goto L126
-- goto L10
c8 = {}
c7 = c8
v5[c6] = c7
-- L10:
c7[R4] = R5
c8 = R5['item1Type']
-- if not c8 goto L131
-- goto L11
c8 = 0.0
-- L11:
c9 = R0['item1List']
c9 = c9[c8]
-- if not c9 goto L139
-- goto L12
t10 = {}
c9 = t10
t10 = R0['item1List']
t10[c8] = c9
-- L12:
t10 = c9[c6]
-- if not t10 goto L145
-- goto L13
local t11 = {}
t10 = t11
c9[c6] = t10
-- L13:
t10[R4] = R5
-- L0:
-- op23 A=1 B=2 C=0
-- goto L14
return R0