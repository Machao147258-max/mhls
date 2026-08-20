
===== fn#0 '@src/catchGame/configReader/BubbleConfig.lua' (36 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'BubbleConfig'
local v4 = g1
c2 = c2(c3, v4)
c2['USE_BIN_DATA'] = True
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['dealBinDatas'] = c3
c3 = <imm2>
c2['dealEmojis'] = c3
c3 = <imm3>
c2['dealWords'] = c3
c3 = <imm4>
c2['getItemInfo'] = c3
c3 = <imm5>
c2['getEmojis'] = c3
c3 = <imm6>
c2['getWords'] = c3
c3 = <imm7>
c2['getMyWords'] = c3
c3 = <imm8>
c2['returnWordsDatas'] = c3
c3 = <imm9>
c2['getDatasByEventId'] = c3
c3 = <imm10>
c2['getDataByAutoId'] = c3
c3 = <imm11>
c2['getMouseDefaultShowTeamWords'] = c3
c3 = <imm12>
c2['getMouseDefaultTeamWords'] = c3
return c2
return g1

===== fn#0 '' (72 instr, depth 1) =====
local t1 = {}
R0['catEmojis'] = t1
t1 = {}
R0['mouseEmojis'] = t1
t1 = {}
R0['roleWordsList'] = t1
t1 = {}
R0['catDefaultGlobalWords'] = t1
t1 = {}
R0['mouseDefaultGlobalWords'] = t1
t1 = {}
R0['mouseDefaultTeamWords'] = t1
t1 = {}
R0['autoIdMap'] = t1
t1 = {}
local g2 = <G 'pairs'>
local g3 = <G 'cg'>
g3 = g3['GameConst']
g3 = g3['BUBBLE_CATEGORY']
g2 = g2(g3)
-- goto L0
-- L1:
local c4 = 'category'
local g5 = <G 'tostring'>
local v6 = R6
g5 = g5(v6)
c4 = c4 .. g5
t1[R6] = c4
-- L0:
-- op23 A=2 B=2 C=0
-- goto L1
g2 = <G 'pairs'>
g3 = R0['datas']
g2 = g2(g3)
-- goto L2
-- L9:
c4 = R6['priority']
-- if not c4 goto L37
-- goto L3
c4 = 0.0
-- L3:
R6['priority'] = c4
c4 = {}
R6['category'] = c4
c4 = <G 'pairs'>
g5 = t1
c4 = c4(g5, v6)
-- goto L4
-- L6:
local t7 = R6['category']
local t8 = R6[R11]
-- if 0.0 == t8 goto L49
-- goto L5
t8 = nil
-- L5:
t8 = nil
t7[R10] = t8
-- L4:
-- op23 A=7 B=2 C=0
-- goto L6
c4 = R6['itemType']
-- if 0.0 == c4 goto L60
-- goto L7
c4 = R0:'dealEmojis'
g5 = R0
v6 = R6
c4 = c4(g5, v6)
-- goto L8
-- L7:
c4 = R0:'dealWords'
g5 = R0
v6 = R6
c4 = c4(g5, v6)
-- L8:
c4 = R6['autoId']
-- if not c4 goto L69
-- goto L2
c4 = R0['autoIdMap']
g5 = R6['autoId']
c4[g5] = R6
-- L2:
-- op23 A=2 B=2 C=0
-- goto L9
return R0