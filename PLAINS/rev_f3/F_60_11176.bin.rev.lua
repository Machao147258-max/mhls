
===== fn#0 '@src/catchGame/layerUI/CommonSceneFloatTip.lua' (57 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/mvc/ViewBase'
g1 = g1(c2)
c2 = <G 'require'>
local c3 = 'common/utils'
c2 = c2(c3)
c3 = <G 'require'>
local c4 = 'catchGame/utils/LayerUtil'
c3 = c3(c4)
c4 = <G 'require'>
local c5 = 'lib/framework'
c4 = c4(c5)
c5 = <G 'require'>
local c6 = 'lib/ds'
c5 = c5(c6)
c6 = <G 'class'>
local c7 = 'CommonSceneFloatTip'
local v8 = g1
c6 = c6(c7, v8)
c7 = {}
c7['res'] = 'common_scene_float_tip'
c7['isCatchGame'] = True
c6['RESOURCE_FILENAME'] = c7
c7 = 5.0
v8 = 180.0
local i9 = <imm0>
g1 = c5
c6['onCreate'] = i9
i9 = <imm1>
g1 = c2
g1 = c7
c6['doUI'] = i9
i9 = <imm2>
g1 = c4
c6['onExit'] = i9
i9 = <imm3>
c6['setData'] = i9
i9 = <imm4>
g1 = v8
c6['updateData'] = i9
i9 = <imm5>
c6['dealContentData'] = i9
i9 = <imm6>
c6['getTimestampParam'] = i9
i9 = <imm7>
c6['dealTemplateParams'] = i9
i9 = <imm8>
g1 = c4
c6['play'] = i9
i9 = <imm9>
c6['_setContent'] = i9
i9 = <imm10>
c6['_playEffect'] = i9
i9 = <imm11>
c6['close'] = i9
return c6
return g1

===== fn#0 '' (7 instr, depth 1) =====
R0['_isClosing'] = False
local t1 = R2['queue']
t1 = t1['new']
t1 = t1()
R0['_marquee'] = t1
return R0