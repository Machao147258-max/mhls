
===== fn#0 '@src/catchGame/configReader/TutorialMenuConfig.lua' (65 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = {}
c2[1.0] = 2.0
local g3 = <G 'class'>
local c4 = 'TutorialMenuConfig'
local v5 = g1
g3 = g3(c4, v5)
g3['USE_BIN_DATA'] = True
c4 = <imm0>
g3['dealDatas'] = c4
c4 = <imm1>
g3['dealBinDatas'] = c4
c4 = <imm2>
g3['getTabBoxAwardState'] = c4
c4 = <imm3>
g3['getFirstGameID'] = c4
c4 = <imm4>
g3['getMouseGameID'] = c4
c4 = <imm5>
g3['getCatGameID'] = c4
c4 = <imm6>
g3['getTabNum'] = c4
c4 = <imm7>
g3['getTabList'] = c4
c4 = <imm8>
g3['getTutorialsNumByTab'] = c4
c4 = <imm9>
g3['getDebugTutorialsByTab'] = c4
c4 = <imm10>
g3['getTabInfo'] = c4
c4 = <imm11>
g3['getTutorialsByTab'] = c4
c4 = <imm12>
g3['isCompletedTotalTutorials'] = c4
c4 = <imm13>
g3['isCompletedBasicTutorials'] = c4
c4 = <imm14>
g3['isCompletedTutorialsByTab'] = c4
c4 = <imm15>
g3['completedTutorialsByTabNum'] = c4
c4 = {}
c4[1.0] = 'grade_stan'
c4[2.0] = 'grade_adv'
v5 = <imm16>
g1 = c4
g3['canFisrtOpenTutorialById'] = v5
v5 = <imm17>
g3['canFisrtOpenTutorialByTab'] = v5
v5 = <imm18>
g3['canFirstOpen'] = v5
v5 = <imm19>
g3['isCustomOperateTutorial'] = v5
v5 = <imm20>
g3['getTabAwardData'] = v5
v5 = <imm21>
g3['canShowSkinOfRocketAndRobotMouse'] = v5
v5 = <imm22>
g1 = c2
g3['getNextTutorialId'] = v5
v5 = <imm23>
g3['getRoleGradeData'] = v5
return g3
return g1

===== fn#0 '' (236 instr, depth 1) =====
local t1 = {}
local t2 = {}
local t3 = {}
local t4 = {}
local t5 = {}
R0['_tabAwardDatas'] = t5
t5 = {}
R0['_roleGrades'] = t5
t5 = <G 'pairs'>
local t6 = R0['datas']
t5 = t5(t6)
-- goto L0
-- L16:
local t7 = R9['listId']
-- if not t7 goto L21
-- goto L1
t7 = R9['listRole']
-- if not t7 goto L21
-- goto L1
t7 = R0['_tabAwardDatas']
local t8 = R9['listId']
t7[t8] = R9
-- L1:
t7 = R9['listRole']
-- if not t7 goto L41
-- goto L2
t7 = R9['tutorialBelong']
-- if not t7 goto L41
-- goto L2
t7 = R0['_roleGrades']
t8 = R9['listRole']
t7 = t7[t8]
-- if not t7 goto L36
-- goto L3
t7 = R0['_roleGrades']
t8 = R9['listRole']
local t9 = {}
t7[t8] = t9
-- L3:
t7 = R0['_roleGrades']
t8 = R9['listRole']
t7 = t7[t8]
t8 = R9['tutorialBelong']
t7[t8] = R9
-- L2:
t7 = R9['isTab']
-- if 1.0 == t7 goto L52
-- goto L4
t7 = R9['tab']
t3[t7] = R9
t7 = <G 'table'>
t7 = t7['insert']
t8 = t4
t9 = R9
t7 = t7(t8, t9)
-- goto L0
-- L4:
t7 = {}
t8 = 1.0
-- L10:
t9 = 'role'
local v10 = t8
t9 = t9 .. v10
t9 = R9[t9]
-- if not t9 goto L144
-- goto L5
t9 = {}
v10 = 'role'
local v11 = t8
v10 = v10 .. v11
v10 = R9[v10]
t9['role'] = v10
v10 = 'char'
v11 = t8
v10 = v10 .. v11
v10 = R9[v10]
t9['char'] = v10
v10 = 'name'
v11 = t8
v10 = v10 .. v11
v10 = R9[v10]
t9['name'] = v10
v10 = 'ai'
v11 = t8
v10 = v10 .. v11
v10 = R9[v10]
t9['ai'] = v10
v10 = 'weapon'
v11 = t8
v10 = v10 .. v11
v10 = R9[v10]
t9['weapon'] = v10
v10 = {}
v11 = 'aiDeckId'
local v12 = t8
v11 = v11 .. v12
v11 = R9[v11]
-- if not v11 goto L99
-- goto L6
v11 = 'aiDeckId'
v12 = t8
v11 = v11 .. v12
v11 = R9[v11]
t9['aiDeckLevel'] = v11
-- goto L7
-- L6:
v11 = 1.0
-- L9:
v12 = 'commonSkill'
local v13 = t8
local c14 = '_'
local v15 = v11
v12 = v12 .. v15
v12 = R9[v12]
-- if not v12 goto L136
-- goto L7
v12 = 'commonSkill'
v13 = t8
c14 = '_'
v15 = v11
v12 = v12 .. v15
v12 = R9[v12]
v13 = 'commonSkillLv'
c14 = t8
v15 = '_'
local v16 = v11
v13 = v13 .. v16
v13 = R9[v13]
-- if not v13 goto L123
-- goto L8
v13 = 1.0
-- L8:
c14 = <G 'table'>
c14 = c14['insert']
v15 = v10
v16 = {}
v16['beforeLevel'] = 0.0
v16['bid'] = v12
v16['et'] = 0.0
v16['lastResolveTime'] = 0.0
v16['level'] = v13
v16['piece'] = 0.0
c14 = c14(v15, v16)
-- op19 A=14 B=264 C=14
-- goto L9
-- L7:
t9['commonSkills'] = v10
v11 = <G 'table'>
v11 = v11['insert']
v12 = t7
v13 = t9
v11 = v11(v12, v13)
-- op19 A=11 B=264 C=11
-- goto L10
-- L5:
R9['infos'] = t7
t9 = R9['lockItem']
-- if not t9 goto L154
-- goto L11
t9 = <G 'string'>
t9 = t9['toArray']
v10 = R9['lockItem']
v11 = ';'
t9 = t9(v10, v11, v12)
R9['lockItem'] = t9
-- L11:
t9 = R9['tab']
-- if not t9 goto L186
-- goto L12
t9 = R9['tab']
v10 = R9['tab']
v10 = t1[v10]
-- if not v10 goto L163
-- goto L13
v10 = {}
-- L13:
t1[t9] = v10
t9 = R9['tab']
v10 = R9['tab']
v10 = t2[v10]
-- if not v10 goto L170
-- goto L14
v10 = {}
-- L14:
t2[t9] = v10
t9 = <G 'table'>
t9 = t9['insert']
v10 = R9['tab']
v10 = t2[v10]
v11 = R9
t9 = t9(v10, v11)
t9 = R9['hide']
-- if not t9 goto L186
-- goto L12
t9 = <G 'table'>
t9 = t9['insert']
v10 = R9['tab']
v10 = t1[v10]
v11 = R9
t9 = t9(v10, v11)
-- L12:
t9 = R9['specLoading']
-- if 1.0 ~= t9 goto L190
-- goto L15
t9 = nil
-- L15:
t9 = nil
R9['specLoading'] = t9
t9 = R9['frame']
-- if 0.0 == t9 goto L196
-- goto L0
R9['frame'] = 78840000.0
-- L0:
-- op23 A=5 B=2 C=0
-- goto L16
t5 = <G 'pairs'>
t6 = t1
t5 = t5(t6)
-- goto L17
-- L20:
t7 = <G 'table'>
t7 = t7['sort']
t8 = R9
t9 = <imm0>
t7 = t7(t8, t9)
t7 = <G 'ipairs'>
t8 = R9
t7 = t7(t8, t9, v10, v11, v12)
-- goto L18
-- L19:
v11['index'] = v10
-- L18:
-- op23 A=10 B=2 C=0
-- goto L19
-- L17:
-- op23 A=5 B=2 C=0
-- goto L20
R0['_firstGameID'] = 1.0
R0['_mouseGameID'] = 2.0
R0['_catGameID'] = 4.0
t5 = <G 'table'>
t5 = t5['sort']
t6 = t4
local i17 = <imm1>
t5 = t5(t6, i17)
t5 = <G 'ipairs'>
t6 = t4
t5 = t5(t6, i17)
-- goto L21
-- L22:
R9['index'] = R8
-- L21:
-- op23 A=5 B=2 C=0
-- goto L22
R0['newDatas'] = t1
R0['tabs'] = t3
R0['tabList'] = t4
R0['debugData'] = t2
return R0

===== fn#0 '' (8 instr, depth 2) =====
local t1 = R0['id']
local t2 = R1['id']
-- if t2 < t1 goto L5
-- goto L0
t1 = nil
-- L0:
t1 = nil
return t1
return R0