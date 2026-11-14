
===== fn#0 '@src/catchGame/systems/SurrenderSystem.lua' (299 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/systems/BaseSystem'
g1 = g1(c2)
c2 = <G 'require'>
local c3 = 'catchGame/ClientEventManager'
c2 = c2(c3)
c3 = <G 'require'>
local c4 = 'common/utils'
c3 = c3(c4)
c4 = <G 'require'>
local c5 = 'catchGame/utils/Utils'
c4 = c4(c5)
c5 = 1.0
local c6 = 60.0
local g7 = <G 'class'>
local c8 = 'SurrenderInstance'
g7 = g7(c8)
c8 = <imm0>
g1 = c2
g7['ctor'] = c8
c8 = <imm1>
g7['getInitiatorUid'] = c8
c8 = <imm2>
g7['getInitiatorName'] = c8
c8 = <imm3>
g7['getStartTime'] = c8
c8 = <imm4>
g7['getDurationTime'] = c8
c8 = <imm5>
g7['isMyTeamSurrenderInstance'] = c8
c8 = <imm6>
g7['getVoteNum'] = c8
c8 = <imm7>
g7['getLeftTime'] = c8
c8 = <imm8>
g7['canLocalPlayerVote'] = c8
c8 = <imm9>
g7['canLocalPlayerDoVote'] = c8
c8 = <imm10>
g7['getAgreeNum'] = c8
c8 = <imm11>
g7['getRejectNum'] = c8
c8 = <imm12>
g7['isSurrenderSuccess'] = c8
c8 = <imm13>
g7['checkSurrenderCamp'] = c8
c8 = <imm14>
g1 = c2
g1 = c3
g1 = c5
g7['startSurrender'] = c8
c8 = <imm15>
g1 = c2
g7['_checkEnd'] = c8
c8 = <imm16>
g7['setSendEndStr'] = c8
c8 = <imm17>
g7['isSendEndStr'] = c8
c8 = <imm18>
g1 = c2
g1 = c3
g7['updateSurrenderInfo'] = c8
c8 = <imm19>
g1 = c3
g7['onDestroy'] = c8
c8 = {}
local i9 = <imm20>
g1 = c8
local i10 = <imm21>
g1 = c8
local g11 = <G 'class'>
local c12 = 'BaseCondition'
g11 = g11(c12)
c12 = <imm22>
g11['ctor'] = c12
c12 = <imm23>
g11['init'] = c12
c12 = <imm24>
g11['setPermanentSatisfied'] = c12
c12 = <imm25>
g11['isSatisfied'] = c12
c12 = <imm26>
g11['clear'] = c12
c12 = <imm27>
g11['tryPopCondition'] = c12
c12 = <G 'class'>
local c13 = 'Cond_DualMoment'
local v14 = g11
c12 = c12(c13, v14)
c13 = <imm28>
c12['isSatisfied'] = c13
c13 = i9
v14 = 'Cond_DualMoment'
local v15 = c12
c13 = c13(v14, v15)
c13 = <G 'class'>
v14 = 'Cond_GameTime'
v15 = g11
c13 = c13(v14, v15)
v14 = <imm29>
c13['init'] = v14
v14 = <imm30>
c13['isSatisfied'] = v14
v14 = i9
v15 = 'Cond_GameTime'
local v16 = c13
v14 = v14(v15, v16)
v14 = <G 'class'>
v15 = 'Cond_GoldenHoleOpen'
v16 = g11
v14 = v14(v15, v16)
v15 = <imm31>
g1 = c2
v14['init'] = v15
v15 = <imm32>
v14['_onOpenGoldHole'] = v15
v15 = <imm33>
g1 = c2
v14['clear'] = v15
v15 = i9
v16 = 'Cond_GoldenHoleOpen'
local v17 = v14
v15 = v15(v16, v17)
v15 = <G 'class'>
v16 = 'Cond_SmallGoldenOpen'
v17 = g11
v15 = v15(v16, v17)
v16 = <imm34>
g1 = c2
v15['init'] = v16
v16 = <imm35>
v15['_onTaskStateChanged'] = v16
v16 = i9
v17 = 'Cond_SmallGoldenOpen'
local v18 = v15
v16 = v16(v17, v18)
v16 = <G 'class'>
v17 = 'Cond_LiveMiceLostControl'
v18 = g11
v16 = v16(v17, v18)
v17 = <imm36>
g1 = c2
v16['init'] = v17
v17 = <imm37>
v16['_checkPopCondition'] = v17
v17 = <imm38>
g1 = c2
v16['clear'] = v17
v17 = <imm39>
v16['isSatisfied'] = v17
v17 = i9
v18 = 'Cond_LiveMiceLostControl'
local v19 = v16
v17 = v17(v18, v19)
v17 = {}
v18 = <imm40>
g1 = v17
v19 = <imm41>
g1 = v17
g1 = v19
local g20 = <G 'class'>
local c21 = 'BaseCampType'
g20 = g20(c21)
c21 = <imm42>
g20['ctor'] = c21
c21 = <imm43>
g20['init'] = c21
c21 = <imm44>
g20['getCondiTip'] = c21
c21 = <imm45>
g20['canStartSurrender'] = c21
c21 = <imm46>
g1 = i10
g20['createConditions'] = c21
c21 = <imm47>
g20['clear'] = c21
c21 = <imm48>
g20['popSurrenderCondition'] = c21
c21 = <imm49>
g20['getVoteNum'] = c21
c21 = <imm50>
g20['onPreSurrenderAgree'] = c21
c21 = <imm51>
g20['onPreSurrenderReject'] = c21
c21 = v18
local c22 = 'BaseCampType'
local v23 = g20
c21 = c21(c22, v23)
c21 = <G 'class'>
c22 = 'CampType_1'
v23 = g20
c21 = c21(c22, v23)
c22 = <imm52>
c21['init'] = c22
c22 = <imm53>
c21['getVoteNum'] = c22
c22 = <imm54>
g1 = c4
c21['onPreSurrenderAgree'] = c22
c22 = <imm55>
c21['onPreSurrenderReject'] = c22
c22 = v18
v23 = 'CampType_1'
local v24 = c21
c22 = c22(v23, v24)
c22 = <G 'class'>
v23 = 'SurrenderSystem'
v24 = g1
c22 = c22(v23, v24)
v23 = <imm56>
g1 = g1
c22['ctor'] = v23
v23 = <imm57>
g1 = g1
c22['init'] = v23
v23 = <imm58>
g1 = c2
c22['tryStartSystem'] = v23
v23 = <imm59>
c22['_resetData'] = v23
v23 = <imm60>
c22['_initLocalPlayerInfo'] = v23
v23 = <imm61>
g1 = v19
c22['_dealConfigData'] = v23
v23 = <imm62>
g1 = c2
c22['closeSystem'] = v23
v23 = <imm63>
c22['canShowSurrenderBtn'] = v23
v23 = <imm64>
g1 = c4
c22['tryStartSurrender'] = v23
v23 = <imm65>
c22['voteSurrender'] = v23
v23 = <imm66>
c22['reqStartVoteCd'] = v23
v23 = <imm67>
c22['canVoteSurrender'] = v23
v23 = <imm68>
g1 = g7
c22['_onRecvSurrenderInfo'] = v23
v23 = <imm69>
g1 = c2
c22['_onRecvSurrenderCD'] = v23
v23 = <imm70>
g1 = c2
c22['_onSurrenderErr'] = v23
v23 = <imm71>
c22['getLpRoleType'] = v23
v23 = <imm72>
c22['isMyInSurrenderProcess'] = v23
v23 = <imm73>
c22['getMySurrenderVoteNum'] = v23
v23 = <imm74>
c22['getMySurrenderInitiatorName'] = v23
v23 = <imm75>
c22['getMySurrenderLeftTime'] = v23
v23 = <imm76>
c22['canLocalPlayerVote'] = v23
v23 = <imm77>
c22['getMySurrendeAgreeNum'] = v23
v23 = <imm78>
c22['getMySurrendeRejectNum'] = v23
v23 = <imm79>
c22['getVoteInfo'] = v23
v23 = <imm80>
c22['getWaitInfo'] = v23
v23 = <imm81>
c22['getSurrendCD'] = v23
v23 = <imm82>
c22['getSurrendStartCD'] = v23
v23 = <imm83>
g1 = c6
c22['setSurrenderInCD'] = v23
v23 = <imm84>
g1 = c6
g1 = c2
c22['destroySurrenderInstance'] = v23
v23 = <imm85>
g1 = c2
c22['_onFrameSurrender'] = v23
v23 = <imm86>
c22['isMySurrenderSuccess'] = v23
v23 = <imm87>
c22['isOpSurrenderSuccess'] = v23
v23 = <imm88>
c22['isSurrenderSuccess'] = v23
v23 = <imm89>
g1 = c2
c22['tryPopSurrenderCondition'] = v23
v23 = <imm90>
c22['getPreSurrenderVoteNum'] = v23
v23 = <imm91>
c22['onPreSurrenderAgree'] = v23
v23 = <imm92>
c22['onPreSurrenderReject'] = v23
return c22
return g1

===== fn#0 '' (90 instr, depth 1) =====
R0['_isRunning'] = False
R0['_surrenderInfo'] = R1
R0['_localCamp'] = R2
R0['_system'] = R3
local t1 = R1['acceptUID']
-- op29 A=4 B=0 C=4
R0['_agreeNum'] = t1
t1 = R1['refuseUID']
-- op29 A=4 B=0 C=4
R0['_rejectNum'] = t1
t1 = R1['totalUID']
-- op29 A=4 B=0 C=4
R0['_voteNum'] = t1
R0['_realVoteNum'] = 0.0
t1 = <G 'ipairs'>
local t2 = R0['_surrenderInfo']
t2 = t2['totalUID']
t1 = t1(t2)
-- goto L0
-- L1:
-- if R8 < 0.0 goto L24
-- goto L0
local t3 = R0['_realVoteNum']
-- op19 A=9 B=270 C=9
R0['_realVoteNum'] = t3
-- L0:
-- op23 A=4 B=2 C=0
-- goto L1
t1 = <G 'cg'>
t1 = t1['systems']
t1 = t1['battleSystem']
t1 = t1:'getPlayerInfoById'
t2 = t1
local t4 = R0['_surrenderInfo']
t4 = t4['initiator']
t1 = t1(t2, t4)
-- if not t1 goto L38
-- goto L2
t2 = t1['name']
R0['_initiatorName'] = t2
-- goto L3
-- L2:
R0['_initiatorName'] = ''
-- L3:
t2 = R0:'isMyTeamSurrenderInstance'
t4 = R0
t2 = t2(t4)
-- if not t2 goto L57
-- goto L4
t2 = <G 'ipairs'>
t4 = R0['_surrenderInfo']
t4 = t4['totalUID']
t2 = t2(t4)
-- goto L5
-- L6:
local g5 = <G 'cg'>
g5 = g5['Player']
g5 = g5['uid']
-- if g5 == t3 goto L55
-- goto L5
R0['_isLocalPlayerVoter'] = True
-- goto L4
-- L5:
-- op23 A=5 B=2 C=0
-- goto L6
-- L4:
t2 = R0['_agreeNum']
t4 = R0['_voteNum']
-- if t2 <= t4 goto L89
-- goto L7
t2 = nil
t4 = R0:'isMyTeamSurrenderInstance'
local s6 = R0
t4 = t4(s6)
-- if not t4 goto L74
-- goto L8
t4 = <G 'cg'>
t4 = t4['StringConfig']
t4 = t4:'getString'
s6 = t4
local c7 = 'SurrenderSuccessMy'
t3 = R0['_initiatorName']
t4 = t4(s6, c7, t3)
t2 = t4
-- goto L9
-- L8:
t4 = <G 'cg'>
t4 = t4['StringConfig']
t4 = t4:'getString'
s6 = t4
c7 = 'SurrenderSuccessOp'
t4 = t4(s6, c7, t3)
t2 = t4
-- L9:
t4 = R0:'setSendEndStr'
s6 = R0
c7 = nil
t4 = t4(s6, c7)
t4 = t4['fire']
s6 = s6['ON_GAME_BUBBLE_HISTORY_STR']
c7 = t2
t4 = t4(s6, c7)
-- L7:
return R0