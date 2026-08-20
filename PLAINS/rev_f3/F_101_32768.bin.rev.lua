
===== fn#0 '@src/catchGame/configReader/RankTitleConfig.lua' (25 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'RankTitleConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = {}
c3['CONTROY'] = 1.0
c3['PROVINCE'] = 2.0
c3['CITY'] = 3.0
c3['DISTRICT'] = 4.0
c2['RANK_LEVEL'] = c3
c3 = <imm0>
c2['getRankTitleData'] = c3
c3 = <imm1>
c2['getRankLevel'] = c3
c3 = <imm2>
c2['getSpecialTitleData'] = c3
c3 = <imm3>
c2['getBattlePassTitle'] = c3
c3 = <imm4>
c2['getRankTitleDataByTitle'] = c3
return c2
return g1

===== fn#0 '' (108 instr, depth 1) =====
local t1 = {}
local g2 = <G 'pairs'>
local t3 = R0['datas']
g2 = g2(t3)
-- goto L0
-- L2:
local t4 = R12['type']
local g5 = <G 'NetGameEnum'>
g5 = g5['E_TITLE_TYPE']
g5 = g5['E_TITLE_SHOW_TYPE_RANK']
-- if g5 == t4 goto L22
-- goto L0
t4 = R12['rank_level']
-- if R1 == t4 goto L22
-- goto L0
t4 = R12['rank_max']
-- if t4 <= R2 goto L22
-- goto L0
t4 = R12['rank_min']
-- if R2 <= t4 goto L22
-- goto L0
t1 = R12
-- goto L1
-- L0:
-- op23 A=8 B=2 C=0
-- goto L2
-- L1:
-- if not R3 goto L106
-- goto L3
g2 = <G 'NetGameEnum'>
g2 = g2['E_RANK_LIST_DETAIL_TYPE']
g2 = g2['E_RANK_LIST_DETAIL_ROLEWIN']
-- if g2 == R3 goto L57
-- goto L4
g2 = <G 'cg'>
g2 = g2['RoleConfig']
g2 = g2:'getDataById'
t3 = g2
local v6 = R5
g2 = g2(t3, v6)
-- if not g2 goto L40
-- goto L5
t3 = {}
return t3
-- L5:
t3 = <G 'cg'>
t3 = t3['StringConfig']
t3 = t3:'getString'
v6 = t3
local c7 = 'ZoneRoleWinTitle'
t3 = t3(v6, c7)
v6 = R6
c7 = t3
local t8 = g2['name']
t4 = <G 'cg'>
t4 = t4['StringConfig']
t4 = t4:'getString'
g5 = t4
local c9 = 'Ranking'
local v10 = R2
t4 = t4(g5, c9, v10)
v6 = v6 .. t4
t1['describe'] = v6
return t1
-- L4:
g2 = <G 'cg'>
g2 = g2['RankListConfig']
g2 = g2:'getDataById'
t3 = g2
v6 = R3
g2 = g2(t3, v6, c7)
-- if not g2 goto L106
-- goto L3
-- if not R6 goto L67
-- goto L6
local c11 = ''
-- L6:
t3 = g2['catMouseSwitch']
-- if False == t3 goto L81
-- goto L7
t3 = c11
v6 = g2['name']
c7 = <G 'cg'>
c7 = c7['StringConfig']
c7 = c7:'getString'
t8 = c7
t4 = 'Ranking'
g5 = R2
c7 = c7(t8, t4, g5)
t3 = t3 .. c7
t1['describe'] = t3
-- goto L3
-- L7:
-- if 0.0 == R4 goto L90
-- goto L8
t3 = <G 'cg'>
t3 = t3['StringConfig']
t3 = t3:'getString'
v6 = t3
c7 = 'MouseRank'
t3 = t3(v6, c7, t8)
-- if not t3 goto L95
-- goto L9
-- L8:
t3 = <G 'cg'>
t3 = t3['StringConfig']
t3 = t3:'getString'
v6 = t3
c7 = 'CatRank'
t3 = t3(v6, c7, t8)
-- L9:
v6 = c11
c7 = g2['name']
t8 = t3
t4 = <G 'cg'>
t4 = t4['StringConfig']
t4 = t4:'getString'
g5 = t4
c9 = 'Ranking'
v10 = R2
t4 = t4(g5, c9, v10)
v6 = v6 .. t4
t1['describe'] = v6
-- L3:
return t1
return R0