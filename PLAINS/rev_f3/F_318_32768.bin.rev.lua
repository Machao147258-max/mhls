
===== fn#0 '@src/catchGame/configReader/LuckyWheelShopConfig.lua' (21 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'LuckyWheelShopConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['getCostsByConfigAndGoodsId'] = c3
c3 = <imm2>
c2['getDataByConfigAndGoodsId'] = c3
c3 = <imm3>
c2['getTypeByConfigAndGoodsId'] = c3
c3 = <imm4>
c2['getIdByConfigAndGoodsId'] = c3
c3 = <imm5>
c2['_extractSubConfig'] = c3
return c2
return g1

===== fn#0 '' (14 instr, depth 1) =====
local t1 = {}
R0['goodsData'] = t1
t1 = <G 'pairs'>
local t2 = R0['datas']
t1 = t1(t2)
-- goto L0
-- L1:
local m3 = R0:'_extractSubConfig'
local s4 = R0
local v5 = R5
local c6 = 'sellGoods_config'
local t7 = R0['goodsData']
m3 = m3(s4, v5)
-- L0:
-- op23 A=1 B=2 C=0
-- goto L1
return R0