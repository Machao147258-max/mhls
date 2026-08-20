
===== fn#0 '@src/catchGame/configReader/PresentConfig.lua' (137 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'PresentConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = {}
c3['Normal'] = 0.0
c3['Letter'] = 1.0
c3['Ring'] = 2.0
c3['Letter2'] = 3.0
c2['Type'] = c3
v4 = 3.0
local c5 = 4.0
local c6 = 100.0
local c7 = 101.0
local c8 = 114.0
local c9 = 117.0
local c10 = 119.0
local c11 = 125.0
c2['DragonPalaceDiceId'] = 120.0
c2['FuCharacterMin'] = c8
c2['FuCharacterMax'] = c9
local t12 = {}
t12[v4] = 1.0
t12[c5] = 2.0
t12[c6] = 3.0
t12[c7] = 3.0
t12[c10] = 1.0
local t13 = {}
local t14 = {}
local c15 = 'chooseFriendAndConfirm'
local c16 = 'reqSendPresent'
t14 = c3 .. c2
t13['default'] = t14
t14 = c3['Letter']
c15 = {}
c16 = 'chooseFriend'
local c17 = 'writeMsg'
local c18 = 'reqSendPresent'
c15 = v4 .. c2
t13[t14] = c15
t14 = c3['Ring']
c15 = {}
c16 = 'buildCP'
c15 = c2 .. c2
t13[t14] = c15
t14 = c3['Letter2']
c15 = {}
c16 = 'chooseFriend'
c17 = 'writeMsg2'
c18 = 'reqSendPresent'
c15 = v4 .. c2
t13[t14] = c15
t14 = {}
t14['default'] = 'GiftCardLayer'
c15 = c3['Letter']
t14[c15] = 'LetterDetailLayer'
c15 = c3['Letter2']
t14[c15] = 'LetterMsg2'
c15 = {}
c16 = {}
c16['boxEffect'] = 'loveLetter'
c15[v4] = c16
c16 = {}
c16['boxEffect'] = 'anonymityLetter'
c15[c5] = c16
c16 = {}
c16['boxEffect'] = 'greetingLetter'
c15[c6] = c16
c16 = {}
c16['boxEffect'] = 'greetingLetter'
c15[c7] = c16
c16 = {}
c16['boxEffect'] = 'greetingLetter'
c15[c10] = c16
c16 = {}
c17 = {}
c17['boxEffect'] = 'box'
c17['isShowAward'] = False
c17['isShowDetail'] = True
c16['default'] = c17
c17 = c3['Letter2']
c18 = {}
c18['layer'] = 'LetterMsg2'
c16[c17] = c18
c17 = <imm0>
c2['dealDatas'] = c17
c17 = <imm1>
g1 = t13
g1 = c3
c2['getSendSteps'] = c17
c17 = <imm2>
g1 = c16
g1 = c15
c2['getRecieveAnis'] = c17
c17 = <imm3>
g1 = t14
c2['getDetailUIName'] = c17
c17 = <imm4>
c2['calcMaxSendNum'] = c17
c17 = <imm5>
g1 = c5
c2['isAnonymity'] = c17
c17 = <imm6>
g1 = c3
c2['isCPPresent'] = c17
c17 = <imm7>
g1 = c3
c2['getCPPresent'] = c17
c17 = <imm8>
c2['isShowNotice'] = c17
c17 = <imm9>
c2['isTargetByCfg'] = c17
c17 = <imm10>
c2['getBagSearchBids'] = c17
c17 = <imm11>
g1 = c11
c2['isBugsBunnyLetter'] = c17
c17 = <imm12>
g1 = c6
g1 = c7
c2['isRedPacketLetter'] = c17
c17 = <imm13>
g1 = c8
g1 = c9
c2['isFuCharacter'] = c17
c17 = <imm14>
g1 = t12
c2['getLetterStyle'] = c17
c17 = <imm15>
c2['checkHaveEnclosure'] = c17
c17 = <imm16>
c2['isTypeById'] = c17
return c2
return g1

===== fn#0 '' (18 instr, depth 1) =====
local g1 = <G 'pairs'>
local t2 = R0['datas']
g1 = g1(t2)
-- goto L0
-- L3:
local t3 = R5['closeGiftIcon']
-- if 0.0 ~= t3 goto L10
-- goto L1
t3 = R5['closeGiftIcon']
-- if '' == t3 goto L11
-- goto L2
-- L1:
R5['closeGiftIcon'] = None
-- L2:
t3 = R5['ifActivtiyGift']
-- if 1.0 == t3 goto L15
-- goto L0
R5['isActivtiyGift'] = True
-- L0:
-- op23 A=1 B=2 C=0
-- goto L3
return R0