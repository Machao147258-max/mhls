
===== fn#0 '@src/catchGame/configReader/GradeSwitchConfig.lua' (13 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'GradeSwitchConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['getConfigName'] = c3
return c2
return g1

===== fn#0 '' (29 instr, depth 1) =====
local t1 = {}
R0['timeList'] = t1
R0['defaultFileName'] = None
t1 = <G 'pairs'>
local t2 = R0['datas']
t1 = t1(t2)
-- goto L0
-- L2:
local t3 = R5['createTime']
-- if not t3 goto L24
-- goto L1
t3 = <G 'table'>
t3 = t3['insert']
local t4 = R0['timeList']
local t5 = {}
local g6 = <G 'cg'>
g6 = g6['Utils']
g6 = g6['convertTime']
local t7 = R5['createTime']
g6 = g6(t7)
t5['timeStamp'] = g6
g6 = R5['gameplayFile']
t5['filename'] = g6
t3 = t3(t4, t5)
-- goto L0
-- L1:
t3 = R5['gameplayFile']
R0['defaultFileName'] = t3
-- L0:
-- op23 A=1 B=2 C=0
-- goto L2
return R0