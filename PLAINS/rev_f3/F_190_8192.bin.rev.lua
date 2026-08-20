
===== fn#0 '@src/catchGame/configReader/BubbleCategoryConfig.lua' (15 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'BubbleCategoryConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['getCategoryByType'] = c3
c3 = <imm2>
c2['getCategoriesData'] = c3
return c2
return g1

===== fn#0 '' (12 instr, depth 1) =====
local t1 = {}
R0['category'] = t1
t1 = <G 'pairs'>
local t2 = R0['datas']
t1 = t1(t2)
-- goto L0
-- L1:
local t3 = R0['category']
local t4 = R5['type']
t3[t4] = R5
-- L0:
-- op23 A=1 B=2 C=0
-- goto L1
return R0