
===== fn#0 '@src/catchGame/configReader/BeginerMallConfig.lua' (15 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'BeginerMallConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = 1.0
v4 = 2.0
local i5 = <imm0>
g1 = c3
g1 = v4
c2['dealDatas'] = i5
return c2
return g1

===== fn#0 '' (64 instr, depth 1) =====
local g1 = <G 'ipairs'>
local t2 = R0['datas']
g1 = g1(t2)
-- goto L0
-- L6:
local g3 = <G 'type'>
local t4 = R5['goodsID']
g3 = g3(t4)
-- if 'nil' ~= g3 goto L10
-- goto L1
g3 = nil
-- L1:
g3 = nil
R5['buyLocal'] = g3
g3 = R5['buyLocal']
-- if not g3 goto L18
-- goto L2
-- if not g3 goto L19
-- goto L3
-- L2:
-- L3:
R5['buyWay'] = g3
g3 = R5['getReward']
-- if not g3 goto L61
-- goto L0
g3 = {}
t4 = <G 'ipairs'>
local g5 = <G 'string'>
g5 = g5['split']
local t6 = R5['getReward']
local c7 = ';'
g5 = g5(t6)
t4 = t4(g5, t6, c7)
-- goto L4
-- L5:
local g8 = <G 'string'>
g8 = g8['split']
local v9 = R11
local c10 = ','
g8 = g8(v9, c10)
v9 = 1.0
-- op29 A=14 B=0 C=12
local c11 = 1.0
-- op6 A=13 B=3 C=256
local g12 = <G 'tonumber'>
local t13 = g8[R16]
g12 = g12(t13)
g8[R16] = g12
-- op8 A=13 B=506 C=255
v9 = {}
c10 = g8[1.0]
v9['type'] = c10
c10 = g8[2.0]
v9['id'] = c10
c10 = g8[3.0]
v9['num'] = c10
c10 = <G 'table'>
c10 = c10['insert']
c11 = g3
local v14 = v9
c10 = c10(c11, v14)
-- L4:
-- op23 A=7 B=2 C=0
-- goto L5
R5['items'] = g3
-- L0:
-- op23 A=1 B=2 C=0
-- goto L6
return R0