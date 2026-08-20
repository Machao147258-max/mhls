
===== fn#0 '@src/catchGame/configReader/CustomSwitchOptionConfig.lua' (27 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'CustomSwitchOptionConfig'
local v4 = g1
c2 = c2(c3, v4)
c2['USE_BIN_DATA'] = 'PUB'
c3 = <G 'userext'>
c3 = c3['CDict']
c3 = c3:'Create'
v4 = c3
local c5 = 2.0
local c6 = 1.0
c3 = c3(v4, c5, c6)
c2['FlagType'] = c3
c3 = c2['FlagType']
c3['Switch'] = 1.0
c3 = c2['FlagType']
c3['VisibleRange'] = 2.0
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['getDataByType'] = c3
c3 = <imm2>
c2['getParentTypes'] = c3
return c2
return g1

===== fn#0 '' (37 instr, depth 1) =====
local t1 = {}
R0['typeToParentType'] = t1
t1 = <G 'ipairs'>
local t2 = R0['datas']
t1 = t1(t2)
-- goto L0
-- L4:
local t3 = R5['subtypes']
local g4 = <G 'string'>
g4 = g4['toArray']
local v5 = t3
local c6 = ','
local n7 = nil
g4 = g4(v5, c6, n7)
t3 = g4
g4 = <G 'ipairs'>
v5 = t3
g4 = g4(v5, c6, n7)
-- goto L1
-- L3:
local t8 = R0['typeToParentType']
local t9 = R0['typeToParentType']
t9 = t9[R11]
-- if not t9 goto L24
-- goto L2
t9 = {}
-- L2:
t8[R11] = t9
t8 = <G 'table'>
t8 = t8['insert']
t9 = R0['typeToParentType']
t9 = t9[R11]
local t10 = R5['type']
t8 = t8(t9, t10)
-- L1:
-- op23 A=7 B=2 C=0
-- goto L3
R5['subTypeList'] = t3
-- L0:
-- op23 A=1 B=2 C=0
-- goto L4
return R0