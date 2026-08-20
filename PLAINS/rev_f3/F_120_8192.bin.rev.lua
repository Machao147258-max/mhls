
===== fn#0 '@src/catchGame/configReader/RecreationLobbyConfig.lua' (15 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'RecreationLobbyConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['convertTimeFormat'] = c3
c3 = <imm2>
c2['getOpenDayArrayByGameType'] = c3
return c2
return g1

===== fn#0 '' (77 instr, depth 1) =====
local g1 = <G 'checknumber'>
local g2 = <G 'os'>
g2 = g2['date']
local c3 = '%W'
local g4 = <G 'cg'>
g4 = g4['Game']
g4 = g4:'nowTime'
local s5 = g4
g4 = g4(s5)
g2 = g2(c3)
g1 = g1(g2, c3, g4)
R0['currWeek'] = g1
g2 = {}
R0['currWeekData'] = g2
g2 = {}
c3 = <G 'pairs'>
g4 = R0['datas']
c3 = c3(g4, s5)
-- goto L0
-- L4:
local m6 = R0:'convertTimeFormat'
local s7 = R0
local t8 = R7['date']
m6 = m6(s7, t8)
R7['weekInYear'] = m6
R7['dayInWeek'] = s7
-- if g1 ~= m6 goto L33
-- goto L1
-- if 0.0 == m6 goto L29
-- goto L2
-- if 52.0 ~= g1 goto L33
-- goto L1
-- L2:
-- if 52.0 == m6 goto L52
-- goto L0
-- if 0.0 == g1 goto L52
-- goto L0
-- L1:
t8 = <G 'string'>
t8 = t8['toArray']
local t9 = R7['gameplay']
local c10 = ','
local n11 = nil
t8 = t8(t9, c10, n11)
R7['gamePlayTab'] = t8
t9 = <G 'table'>
t9 = t9['insert']
c10 = R0['currWeekData']
n11 = <G 'clone'>
local v12 = R7
n11 = n11(v12)
t9 = t9(c10, n11)
-- if 0.0 == s7 goto L51
-- goto L3
g2[7.0] = True
-- goto L0
-- L3:
g2[s7] = True
-- L0:
-- op23 A=3 B=2 C=0
-- goto L4
c3 = 1.0
g4 = 7.0
s5 = 1.0
-- op6 A=3 B=16 C=256
local t13 = g2[R6]
-- if not t13 goto L75
-- goto L5
t13 = {}
t13['weekInYear'] = g1
t13['dayInWeek'] = R6
m6 = <G 'cg'>
m6 = m6['RecreationOpenConfig']
m6 = m6:'getGameplays'
s7 = m6
t8 = R6
m6 = m6(s7, t8, t9)
t13['gamePlayTab'] = m6
m6 = <G 'table'>
m6 = m6['insert']
s7 = R0['currWeekData']
t8 = t13
m6 = m6(s7, t8)
-- L5:
-- op8 A=3 B=493 C=255
return R0