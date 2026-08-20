
===== fn#0 '@src/catchGame/configReader/UpdateGuideConfig.lua' (13 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'PosterPopupConfiger'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['getUpdateVersion'] = c3
return c2
return g1

===== fn#0 '' (51 instr, depth 1) =====
local g1 = <G 'Globals'>
g1 = g1['IS_ANDROID']
-- if not g1 goto L6
-- goto L0
local c2 = 'ad'
-- goto L1
-- L0:
g1 = <G 'Globals'>
g1 = g1['IS_OHOS']
-- if not g1 goto L12
-- goto L2
c2 = 'ad'
-- goto L1
-- L2:
g1 = <G 'Globals'>
g1 = g1['IS_IOS']
-- if not g1 goto L17
-- goto L1
c2 = 'ios'
-- L1:
-- if not c2 goto L20
-- goto L3
return R0
-- L3:
g1 = nil
local g3 = <G '_PayPorts'>
g3 = g3['getPayChannel']
g3 = g3()
local g4 = <G 'pairs'>
local t5 = R0['datas']
g4 = g4(t5)
-- goto L4
-- L7:
local t6 = R8['platform']
-- if c2 == t6 goto L45
-- goto L4
t6 = R8['channel']
-- if not t6 goto L37
-- goto L5
t6 = R8['channel']
-- if '' == t6 goto L39
-- goto L6
-- L5:
g1 = R8['version']
-- goto L4
-- L6:
t6 = R8['channel']
-- if g3 == t6 goto L45
-- goto L4
t6 = R8['version']
R0['version'] = t6
return R0
-- L4:
-- op23 A=4 B=2 C=0
-- goto L7
-- if not g1 goto L50
-- goto L8
R0['version'] = g1
-- L8:
return R0