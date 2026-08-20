
===== fn#0 '@src/catchGame/configReader/RecreationGameConfig.lua' (90 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'RecreationGameConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = {}
v4 = <G 'cg'>
v4 = v4['StringConfig']
v4 = v4:'getString'
local s5 = v4
local c6 = 'Monday'
v4 = v4(s5, c6)
c3[1.0] = v4
v4 = <G 'cg'>
v4 = v4['StringConfig']
v4 = v4:'getString'
s5 = v4
c6 = 'Tuesday'
v4 = v4(s5, c6)
c3[2.0] = v4
v4 = <G 'cg'>
v4 = v4['StringConfig']
v4 = v4:'getString'
s5 = v4
c6 = 'Wednesday'
v4 = v4(s5, c6)
c3[3.0] = v4
v4 = <G 'cg'>
v4 = v4['StringConfig']
v4 = v4:'getString'
s5 = v4
c6 = 'Thursday'
v4 = v4(s5, c6)
c3[4.0] = v4
v4 = <G 'cg'>
v4 = v4['StringConfig']
v4 = v4:'getString'
s5 = v4
c6 = 'Friday'
v4 = v4(s5, c6)
c3[5.0] = v4
v4 = <G 'cg'>
v4 = v4['StringConfig']
v4 = v4:'getString'
s5 = v4
c6 = 'Saturday'
v4 = v4(s5, c6)
c3[6.0] = v4
v4 = <G 'cg'>
v4 = v4['StringConfig']
v4 = v4:'getString'
s5 = v4
c6 = 'Sunday'
v4 = v4(s5, c6)
c3[7.0] = v4
v4 = <imm0>
c2['swapConfig'] = v4
v4 = <imm1>
g1 = c3
c2['dealDatas'] = v4
v4 = <imm2>
c2['getValidRecrationGameData'] = v4
v4 = <imm3>
c2['getAllTodayOpenRecreationGameData'] = v4
v4 = <imm4>
c2['getTodayShowInCustomRoomData'] = v4
v4 = <imm5>
c2['isOpenRecreationMode'] = v4
v4 = <imm6>
c2['getDataByMatchType'] = v4
v4 = <imm7>
c2['getDataByGameType'] = v4
v4 = <imm8>
c2['getGameNameByMatchType'] = v4
v4 = <imm9>
c2['getGameNameByGameType'] = v4
v4 = <imm10>
c2['getMapName'] = v4
v4 = <imm11>
c2['getRuleID'] = v4
v4 = <imm12>
g1 = c3
c2['getOpenState'] = v4
v4 = <imm13>
c2['getGradeLimit'] = v4
v4 = <imm14>
c2['checkModuleReady'] = v4
v4 = <imm15>
c2['isTodayOpenByGameType'] = v4
v4 = <imm16>
c2['isRecreationMode'] = v4
v4 = <imm17>
c2['isSpringFestivalGameType'] = v4
return c2
return g1

===== fn#0 '' (20 instr, depth 1) =====
R0['swapped'] = True
local g1 = <G 'pairs'>
local t2 = R0['datas']
g1 = g1(t2)
-- goto L0
-- L2:
local g3 = <G 'cg'>
g3 = g3['LevelLimitConfig']
g3 = g3:'getDataByName'
local s4 = g3
local t5 = R5['moduleName']
g3 = g3(s4, t5)
-- if not g3 goto L13
-- goto L1
-- goto L0
-- L1:
s4 = g3['level']
R5['openLevel'] = s4
s4 = g3['grade']
R5['openGrade'] = s4
-- L0:
-- op23 A=1 B=2 C=0
-- goto L2
return R0