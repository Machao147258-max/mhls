
===== fn#0 '@src/catchGame/configReader/PosterSignUpConfig.lua' (38 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'require'>
local c3 = 'svn_version'
c2 = c2(c3)
c3 = <G 'class'>
local c4 = 'PosterSignUpConfig'
local v5 = g1
c3 = c3(c4, v5)
c4 = <G 'NetGameEnum'>
c4 = c4['E_ACTIVITY_TYPE']
c4 = c4['E_ACTIVITY_AD_FACE']
v5 = <G 'NetGameEnum'>
v5 = v5['E_ACTIVITY_TYPE']
v5 = v5['E_ACTIVITY_GENERAL_QUEST']
local t6 = {}
t6['FREE'] = 1.0
t6['UNPAID'] = 2.0
t6['PAID'] = 3.0
c3['LAYER_STATE'] = t6
t6 = <imm0>
c3['dealDatas'] = t6
t6 = <imm1>
g1 = c4
c3['checkShowPosterSignUp'] = t6
t6 = <imm2>
c3['canPopup'] = t6
t6 = <imm3>
g1 = c2
c3['unpaidPop'] = t6
t6 = <imm4>
c3['getState'] = t6
t6 = <imm5>
g1 = v5
c3['isValidGeneralActivtiy'] = t6
return c3
return g1

===== fn#0 '' (56 instr, depth 1) =====
local g1 = <G 'pairs'>
local t2 = R0['datas']
g1 = g1(t2)
-- goto L0
-- L9:
local t3 = R5['questShowID']
-- if not t3 goto L15
-- goto L1
t3 = <G 'string'>
t3 = t3['toArray']
local t4 = R5['questShowID']
local c5 = ','
local n6 = nil
t3 = t3(t4, c5, n6)
R5['showQuestList'] = t3
-- goto L2
-- L1:
t3 = {}
R5['showQuestList'] = t3
-- L2:
t3 = R5['showStartTime']
-- if not t3 goto L27
-- goto L3
t3 = <G 'cg'>
t3 = t3['Utils']
t3 = t3['convertTime']
t4 = R5['showStartTime']
t3 = t3(t4, c5, n6)
-- if not t3 goto L28
-- goto L4
-- L3:
t3 = 0.0
-- L4:
R5['showStartTimeStamp'] = t3
t3 = R5['startTime']
-- if not t3 goto L39
-- goto L5
t3 = <G 'cg'>
t3 = t3['Utils']
t3 = t3['convertTime']
t4 = R5['startTime']
t3 = t3(t4, c5, n6)
-- if not t3 goto L40
-- goto L6
-- L5:
t3 = 0.0
-- L6:
R5['startTimeStamp'] = t3
t3 = R5['endTime']
-- if not t3 goto L51
-- goto L7
t3 = <G 'cg'>
t3 = t3['Utils']
t3 = t3['convertTime']
t4 = R5['endTime']
t3 = t3(t4, c5, n6)
-- if not t3 goto L52
-- goto L8
-- L7:
t3 = 0.0
-- L8:
R5['endTimeStamp'] = t3
-- L0:
-- op23 A=1 B=2 C=0
-- goto L9
return R0