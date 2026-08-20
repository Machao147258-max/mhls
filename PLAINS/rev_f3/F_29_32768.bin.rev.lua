
===== fn#0 '@src/catchGame/configReader/PartnerFashionConfig.lua' (19 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'PartnerFashionConfig'
local v4 = g1
c2 = c2(c3, v4)
c2['DefaultFashion'] = 0.0
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['getAllDatasByPartner'] = c3
c3 = <imm2>
g1 = c2
c2['getDefaultFashion'] = c3
c3 = <imm3>
c2['getSeriesFashion'] = c3
return c2
return g1

===== fn#0 '' (25 instr, depth 1) =====
local t1 = {}
R0['_fashionDatas'] = t1
t1 = <G 'pairs'>
local t2 = R0['datas']
t1 = t1(t2)
-- goto L0
-- L2:
local t3 = R0['_fashionDatas']
local t4 = R5['partnerId']
t3 = t3[t4]
-- if not t3 goto L15
-- goto L1
t3 = R0['_fashionDatas']
t4 = R5['partnerId']
local t5 = {}
t3[t4] = t5
-- L1:
t3 = <G 'table'>
t3 = t3['insert']
t4 = R0['_fashionDatas']
t5 = R5['partnerId']
t4 = t4[t5]
t5 = R5
t3 = t3(t4, t5)
-- L0:
-- op23 A=1 B=2 C=0
-- goto L2
return R0