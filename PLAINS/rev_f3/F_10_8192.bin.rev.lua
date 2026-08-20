
===== fn#0 '@src/catchGame/layerUI/CommonToastLayer.lua' (48 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/mvc/ViewBase'
g1 = g1(c2)
c2 = <G 'require'>
local c3 = 'catchGame/utils/Utils'
c2 = c2(c3)
c3 = <G 'require'>
local c4 = 'common/utils'
c3 = c3(c4)
c4 = <G 'require'>
local c5 = 'catchGame/GameConst'
c4 = c4(c5)
c5 = <G 'class'>
local c6 = 'CommonToastLayer'
local v7 = g1
c5 = c5(c6, v7)
c6 = {}
c6['res'] = 'common_toast'
c6['isCatchGame'] = True
c5['RESOURCE_FILENAME'] = c6
c6 = 0.8
v7 = 2.4
local i8 = <imm0>
g1 = c4
c5['showInfoToScene'] = i8
i8 = <imm1>
g1 = c4
c5['showInfo'] = i8
i8 = <imm2>
g1 = c6
c5['showInfoList'] = i8
i8 = <imm3>
c5['onCreate'] = i8
i8 = <imm4>
g1 = c3
c5['doUI'] = i8
i8 = <imm5>
g1 = c3
g1 = c2
g1 = c5
g1 = v7
c5['addInfo'] = i8
i8 = <imm6>
c5['updateTipList'] = i8
i8 = <imm7>
c5['removePan'] = i8
return c5
return g1

===== fn#0 '' (32 instr, depth 1) =====
-- if not R3 goto L3
-- goto L0
return R0
-- L0:
local t1 = R3['__currentTip']
-- if not t1 goto L11
-- goto L1
local m2 = t1:'addInfo'
local s3 = t1
local v4 = R1
local v5 = R2
m2 = m2(s3, v4)
-- goto L2
-- L1:
m2 = <G 'cg'>
m2 = m2['Game']
m2 = m2:'createLayer'
s3 = m2
v4 = 'CommonToastLayer'
v5 = {}
v5['info'] = R1
m2 = m2(s3, v4, v5)
t1 = m2
m2 = R3:'addChild'
s3 = R3
v4 = t1
v5 = v5['LARGE_LAYER_ZORDER']
m2 = m2(s3, v4)
R3['__currentTip'] = t1
m2 = {}
t1['panToastList'] = m2
m2 = t1:'addInfo'
s3 = t1
v4 = R1
v5 = R2
m2 = m2(s3, v4)
-- L2:
return R0