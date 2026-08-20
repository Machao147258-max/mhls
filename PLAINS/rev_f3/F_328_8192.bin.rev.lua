
===== fn#0 '@src/catchGame/configReader/CoinConfig.lua' (21 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'CoinConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['isShowInBag'] = c3
c3 = <imm1>
c2['getCoinIcon'] = c3
c3 = <imm2>
c2['getDataById'] = c3
c3 = <imm3>
c2['getShopChipPrice'] = c3
c3 = <imm4>
c2['getDiamondPriceByChipPrice'] = c3
c3 = <imm5>
c2['translateCoinData'] = c3
return c2
return g1

===== fn#0 '' (12 instr, depth 1) =====
local t1 = R0['datas']
t1 = t1[R1]
-- if not t1 goto L9
-- goto L0
local t2 = t1['isShow']
-- if not t2 goto L9
-- goto L0
t2 = nil
return t2
-- L0:
t2 = nil
return t2
return R0