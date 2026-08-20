
===== fn#0 '@src/catchGame/configReader/LevelLimitConfig.lua' (31 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'LevelLimitConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = {}
c3['LEVEL'] = 1.0
c3['GRADE'] = 2.0
c2['LVLUP_TYPE'] = c3
c3 = 'catchGame/data/'
v4 = <imm0>
g1 = c3
c2['switchConfig'] = v4
v4 = <imm1>
c2['isLimit'] = v4
v4 = <imm2>
c2['getDataByName'] = v4
v4 = <imm3>
c2['isLimitWithGrade'] = v4
v4 = <imm4>
c2['isShowLvlupTip'] = v4
v4 = <imm5>
c2['getGradeLimit'] = v4
v4 = <imm6>
c2['getUnlockDataByLevel'] = v4
v4 = <imm7>
c2['getTipData'] = v4
return c2
return g1

===== fn#0 '' (27 instr, depth 1) =====
-- if 'level_gameplay' == R1 goto L3
-- goto L0
return R0
-- L0:
local v1 = R1
local s2 = R2 .. v1
R0['dataName'] = s2
v1 = R0:'reload'
local s3 = R0
v1 = v1(s3)
v1 = <G 'pairs'>
s3 = R0['datas']
v1 = v1(s3)
-- goto L1
-- L2:
local t4 = R7['grade']
-- if not t4 goto L17
-- goto L1
R7['grade'] = 0.0
-- L1:
-- op23 A=3 B=2 C=0
-- goto L2
v1 = <G 'cg'>
v1 = v1['RecreationGameConfig']
-- if not v1 goto L26
-- goto L3
v1 = <G 'cg'>
v1 = v1['RecreationGameConfig']
v1['swapped'] = False
-- L3:
return R0