
===== fn#0 '@src/catchGame/configReader/PosterPopupConfiger.lua' (35 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'require'>
local c3 = 'svn_version'
c2 = c2(c3)
c3 = <G 'require'>
local c4 = 'common/utils'
c3 = c3(c4)
c4 = <G 'require'>
local c5 = 'catchGame/sdk/SdkPlatform'
c4 = c4(c5)
c5 = <G 'class'>
local c6 = 'PosterPopupConfiger'
local v7 = g1
c5 = c5(c6, v7)
c6 = <imm0>
c5['dealDatas'] = c6
c6 = <imm1>
c5['isAlternatePoster'] = c6
c6 = <imm2>
g1 = c2
c5['getAllValidPoster'] = c6
c6 = <imm3>
g1 = c4
c5['getCurrentASTCType'] = c6
c6 = <imm4>
c5['isPosterResourceValid'] = c6
c6 = <imm5>
c5['isOutOfShowTime'] = c6
c6 = <imm6>
g1 = c3
c5['checkConditionNotShow'] = c6
return c5
return g1

===== fn#0 '' (73 instr, depth 1) =====
local g1 = <G 'pairs'>
local t2 = R0['datas']
g1 = g1(t2)
-- goto L0
-- L4:
local g3 = <G 'cg'>
g3 = g3['Utils']
g3 = g3['convertDateStrToTimestamp']
local t4 = R5['startTime']
g3 = g3(t4)
t4 = <G 'cg'>
t4 = t4['Utils']
t4 = t4['convertDateStrToTimestamp']
local t5 = R5['endTime']
t4 = t4(t5)
R5['startTime'] = g3
R5['endTime'] = t4
t5 = R5['jumpUi']
-- if 30.0 == t5 goto L23
-- goto L1
t5 = {}
local t6 = R5['param']
t5['url'] = t6
R5['param'] = t5
-- L1:
t5 = R5['jumpExtraData']
-- if not t5 goto L43
-- goto L2
t5 = <G 'string'>
t5 = t5['tomap']
t6 = R5['jumpExtraData']
local c7 = ';'
local c8 = '='
t5 = t5(t6, c7, c8)
R5['jumpExtraData'] = t5
t5 = <G 'type'>
t6 = R5['param']
t5 = t5(t6, c7, c8)
-- if 'table' == t5 goto L43
-- goto L2
t5 = <G 'table'>
t5 = t5['merge']
t6 = R5['param']
c7 = R5['jumpExtraData']
t5 = t5(t6, c7)
-- L2:
t5 = R5['jumpUi2']
-- if 30.0 == t5 goto L50
-- goto L3
t5 = {}
t6 = R5['param2']
t5['url'] = t6
R5['param2'] = t5
-- L3:
t5 = R5['jumpExtraData2']
-- if not t5 goto L70
-- goto L0
t5 = <G 'string'>
t5 = t5['tomap']
t6 = R5['jumpExtraData2']
c7 = ';'
c8 = '='
t5 = t5(t6, c7, c8)
R5['jumpExtraData2'] = t5
t5 = <G 'type'>
t6 = R5['param2']
t5 = t5(t6, c7, c8)
-- if 'table' == t5 goto L70
-- goto L0
t5 = <G 'table'>
t5 = t5['merge']
t6 = R5['param2']
c7 = R5['jumpExtraData2']
t5 = t5(t6, c7)
-- L0:
-- op23 A=1 B=2 C=0
-- goto L4
return R0