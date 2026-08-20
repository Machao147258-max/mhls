
===== fn#0 '@src/catchGame/configReader/FashionCollectionConfig.lua' (20 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'require'>
local c3 = 'catchGame/GameConst'
c2 = c2(c3)
c3 = <G 'class'>
local c4 = 'FashionCollectionConfig'
local v5 = g1
c3 = c3(c4, v5)
c4 = c2['FASHION_COLLECTION_CLASS_NAME']
c3['className'] = c4
c4 = c2['FASHION_COLLECTION_STR_QUALITY']
c3['strQuality'] = c4
c4 = c2['FASHION_COLLECTION_SUB_CLASS_NAME']
c3['subClassName'] = c4
c4 = <imm0>
c3['dealDatas'] = c4
return c3
return g1

===== fn#0 '' (33 instr, depth 1) =====
local g1 = <G 'pairs'>
local t2 = R0['datas']
g1 = g1(t2)
-- goto L0
-- L3:
local c3 = ''
local t4 = R5['unlockFashionShow']
-- if not t4 goto L22
-- goto L1
t4 = R5['unlockFashionShow']
-- if 0.0 ~= t4 goto L22
-- goto L1
t4 = <G 'string'>
t4 = t4['format']
local g5 = <G 'cg'>
g5 = g5['StringConfig']
g5 = g5:'getString'
local s6 = g5
local c7 = 'CollectionFashionAwardShowNum'
g5 = g5(s6, c7)
s6 = R5['unlockFashionShow']
t4 = t4(g5, s6, c7)
c3 = t4
-- goto L2
-- L1:
t4 = <G 'cg'>
t4 = t4['Utils']
t4 = t4['getDetail']
g5 = R5['item1Type']
s6 = R5['item1ID']
t4 = t4(g5, s6, c7)
c3 = t4['name']
-- L2:
R5['name'] = c3
-- L0:
-- op23 A=1 B=2 C=0
-- goto L3
return R0