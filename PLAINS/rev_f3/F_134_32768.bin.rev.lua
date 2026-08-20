
===== fn#0 '@src/catchGame/configReader/ADConfig.lua' (17 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'ADConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['getUpActivityTab'] = c3
c3 = <imm2>
c2['getValidDataById'] = c3
c3 = <imm3>
c2['dealShareQuest'] = c3
return c2
return g1

===== fn#0 '' (199 instr, depth 1) =====
local c1 = 0.0
local g2 = <G 'cg'>
-- if not g2 goto L19
-- goto L0
g2 = <G 'cg'>
g2 = g2['Player']
-- if not g2 goto L19
-- goto L0
g2 = <G 'cg'>
g2 = g2['Player']
g2 = g2['createTime']
-- if not g2 goto L19
-- goto L0
g2 = <G 'checknumber'>
local g3 = <G 'cg'>
g3 = g3['Player']
g3 = g3['createTime']
g2 = g2(g3)
c1 = g2
-- L0:
g2 = {}
R0['upActivityTab'] = g2
g2 = <G 'pairs'>
g3 = R0['datas']
g2 = g2(g3)
-- goto L1
-- L21:
local t4 = R6['type']
-- if not t4 goto L29
-- goto L2
t4 = 5.0
-- L2:
R6['type'] = t4
t4 = R6['uiType']
-- if not t4 goto L40
-- goto L3
t4 = R6['template_id']
-- if not t4 goto L39
-- goto L4
t4 = 2.0
-- if not t4 goto L40
-- goto L3
-- L4:
t4 = 1.0
-- L3:
R6['uiType'] = t4
t4 = R6['isUp']
-- if not t4 goto L52
-- goto L5
t4 = R6['isUp']
-- if 1.0 == t4 goto L52
-- goto L5
t4 = <G 'table'>
t4 = t4['insert']
local t5 = R0['upActivityTab']
local v6 = R6
t4 = t4(t5, v6)
-- L5:
t4 = R6['channelID']
-- if not t4 goto L61
-- goto L6
t4 = <G 'string'>
t4 = t4['split']
t5 = R6['channelID']
v6 = ';'
t4 = t4(t5, v6)
R6['channelTab'] = t4
-- L6:
t4 = R6['showChannel']
-- if not t4 goto L70
-- goto L7
t4 = <G 'string'>
t4 = t4['split']
t5 = R6['showChannel']
v6 = ';'
t4 = t4(t5, v6)
R6['showChannelTab'] = t4
-- L7:
t4 = R6['generalactivityID']
-- if not t4 goto L77
-- goto L8
t4 = R0:'dealShareQuest'
t5 = R0
v6 = R6['generalactivityID']
t4 = t4(t5, v6)
R6['shareQuest'] = t4
-- L8:
t4 = R6['tab']
-- if not t4 goto L81
-- goto L9
R6['tab'] = 1.0
-- L9:
t4 = R6['startTime']
-- if not t4 goto L91
-- goto L10
t4 = <G 'cg'>
t4 = t4['Utils']
t4 = t4['convertTime']
t5 = R6['startTime']
t4 = t4(t5, v6)
-- if not t4 goto L92
-- goto L11
-- L10:
t4 = 0.0
-- L11:
R6['startTimeStamp'] = t4
t4 = R6['endTime']
-- if not t4 goto L103
-- goto L12
t4 = <G 'cg'>
t4 = t4['Utils']
t4 = t4['convertTime']
t5 = R6['endTime']
t4 = t4(t5, v6)
-- if not t4 goto L104
-- goto L13
-- L12:
t4 = 0.0
-- L13:
R6['endTimeStamp'] = t4
t4 = R6['durationDays']
-- if not t4 goto L124
-- goto L14
t4 = <G 'math'>
t4 = t4['max']
t5 = R6['startTimeStamp']
v6 = c1
t4 = t4(t5, v6)
R6['startTimeStamp'] = t4
t4 = <G 'math'>
t4 = t4['min']
t5 = R6['endTimeStamp']
v6 = R6['durationDays']
-- op25 A=9 B=294 C=9
-- op25 A=9 B=295 C=9
-- op25 A=9 B=295 C=9
-- op19 A=9 B=9 C=1
t4 = t4(t5, v6)
R6['endTimeStamp'] = t4
-- L14:
t4 = R6['jumpui']
-- if 30.0 == t4 goto L131
-- goto L15
t4 = {}
t5 = R6['param']
t4['url'] = t5
R6['param'] = t4
-- L15:
t4 = R6['jumpExtraData']
-- if not t4 goto L151
-- goto L16
t4 = <G 'string'>
t4 = t4['tomap']
t5 = R6['jumpExtraData']
v6 = ';'
local c7 = '='
t4 = t4(t5, v6, c7)
R6['jumpExtraData'] = t4
t4 = <G 'type'>
t5 = R6['param']
t4 = t4(t5, v6, c7)
-- if 'table' == t4 goto L151
-- goto L16
t4 = <G 'table'>
t4 = t4['merge']
t5 = R6['param']
v6 = R6['jumpExtraData']
t4 = t4(t5, v6)
-- L16:
t4 = R6['jumpui2']
-- if 30.0 == t4 goto L158
-- goto L17
t4 = {}
t5 = R6['param2']
t4['url'] = t5
R6['param2'] = t4
-- L17:
t4 = R6['jumpExtraData2']
-- if not t4 goto L178
-- goto L18
t4 = <G 'string'>
t4 = t4['tomap']
t5 = R6['jumpExtraData2']
v6 = ';'
c7 = '='
t4 = t4(t5, v6, c7)
R6['jumpExtraData2'] = t4
t4 = <G 'type'>
t5 = R6['param2']
t4 = t4(t5, v6, c7)
-- if 'table' == t4 goto L178
-- goto L18
t4 = <G 'table'>
t4 = t4['merge']
t5 = R6['param2']
v6 = R6['jumpExtraData2']
t4 = t4(t5, v6)
-- L18:
t4 = 1.0
-- L20:
t5 = 'jumpui_'
v6 = t4
t5 = t5 .. v6
v6 = 'param_'
c7 = t4
v6 = v6 .. c7
c7 = R6[t5]
-- if not c7 goto L196
-- goto L1
c7 = {}
local t8 = R6[v6]
c7['url'] = t8
R6[v6] = c7
-- goto L19
-- goto L1
-- L19:
-- op19 A=7 B=269 C=7
-- goto L20
-- L1:
-- op23 A=2 B=2 C=0
-- goto L21
return R0