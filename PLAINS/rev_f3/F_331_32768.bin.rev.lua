
===== fn#0 '@src/catchGame/configReader/MedalCollectionConfig.lua' (20 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'MedalCollectionConfig'
local v4 = g1
c2 = c2(c3, v4)
c2['MASTER'] = 7.0
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['getDataByMedalID'] = c3
c3 = <imm2>
c2['isMasterMedal'] = c3
c3 = <imm3>
c2['getDataByCount'] = c3
c3 = <imm4>
c2['getDataNextByCount'] = c3
return c2
return g1

===== fn#0 '' (55 instr, depth 1) =====
local c1 = 1.0
local t2 = R0['datas']
-- op29 A=2 B=0 C=2
local c3 = 1.0
-- op6 A=1 B=47 C=256
local t4 = {}
local c5 = 1.0
-- L1:
local t6 = R0['datas']
t6 = t6[R4]
local c7 = 'item'
local v8 = c5
local c9 = 'ID'
c7 = c7 .. c9
t6 = t6[c7]
-- if not t6 goto L47
-- goto L0
t6 = <G 'table'>
t6 = t6['insert']
c7 = t4
v8 = {}
c9 = R0['datas']
c9 = c9[R4]
local c10 = 'item'
local v11 = c5
local c12 = 'ID'
c10 = c10 .. c12
c9 = c9[c10]
v8['id'] = c9
c9 = R0['datas']
c9 = c9[R4]
c10 = 'item'
v11 = c5
c12 = 'Type'
c10 = c10 .. c12
c9 = c9[c10]
v8['type'] = c9
c9 = R0['datas']
c9 = c9[R4]
c10 = 'item'
v11 = c5
c12 = 'Num'
c10 = c10 .. c12
c9 = c9[c10]
v8['num'] = c9
t6 = t6(c7, v8)
-- op19 A=6 B=256 C=6
-- goto L1
-- L0:
-- op29 A=7 B=0 C=5
-- if t6 < 0.0 goto L53
-- goto L2
t6 = R0['datas']
t6 = t6[R4]
t6['items'] = t4
-- L2:
-- op8 A=1 B=462 C=255
return R0