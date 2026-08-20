
===== fn#0 '@src/catchGame/uiExtend/ListViewAsync.lua' (87 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'common/utils'
g1 = g1(c2)
c2 = <G 'require'>
local c3 = 'lib/framework'
c2 = c2(c3)
c3 = <G 'class'>
local c4 = 'ListViewAsync'
local g5 = <G 'ccui'>
g5 = g5['ScrollView']
c3 = c3(c4, g5)
c4 = 100.0
g5 = <imm0>
g1 = c4
c3['ctor'] = g5
g5 = <imm1>
c3['getAllValidCells'] = g5
g5 = <imm2>
c3['getCell'] = g5
g5 = <imm3>
c3['getCellEx'] = g5
g5 = <imm4>
c3['scrollToCellIndex'] = g5
g5 = <imm5>
c3['scorllToCellIndex'] = g5
g5 = <imm6>
c3['scrollToTopCellIndex'] = g5
g5 = <imm7>
c3['scorllToCellIndexWitnAni'] = g5
g5 = <imm8>
c3['scorllToCellIndexAni2'] = g5
g5 = <imm9>
c3['scorllCellIndexToMiddleWitnAni'] = g5
g5 = <imm10>
c3['getCellPositionByIndex'] = g5
g5 = <imm11>
c3['getCellCache'] = g5
g5 = <imm12>
g1 = g1
c3['_resetCellButton'] = g5
g5 = <imm13>
c3['refreshItemCache'] = g5
g5 = <imm14>
c3['fireEvent'] = g5
g5 = <imm15>
c3['_getDataByCellIndex'] = g5
g5 = <imm16>
c3['_innerCreateCell'] = g5
g5 = <imm17>
g1 = c2
c3['updateRefresh'] = g5
g5 = <imm18>
g1 = c2
c3['refresh'] = g5
g5 = <imm19>
c3['updateItem'] = g5
g5 = <imm20>
c3['refreshAllItems'] = g5
g5 = <imm21>
c3['updateListTip'] = g5
g5 = <imm22>
c3['forceUpdate'] = g5
g5 = <imm23>
c3['setDatas'] = g5
g5 = <imm24>
c3['getDatas'] = g5
g5 = <imm25>
c3['getDataByIndex'] = g5
g5 = <imm26>
c3['updateDatas'] = g5
g5 = <imm27>
c3['updateData'] = g5
g5 = <imm28>
c3['getMidItemIndex'] = g5
g5 = <imm29>
c3['update'] = g5
g5 = <imm30>
g1 = c2
c3['onDestruction'] = g5
g5 = <imm31>
c3['getUsedContainerSize'] = g5
g5 = <imm32>
c3['setAlphaGradientPadding'] = g5
g5 = <imm33>
c3['updateAlphaGradientPadding'] = g5
return c3
return g1

===== fn#0 '' (125 instr, depth 1) =====
local m1 = R0:'setCascadeOpacityEnabled'
local s2 = R0
local n3 = nil
m1 = m1(s2, n3)
m1 = <G 'checktable'>
s2 = R1
m1 = m1(s2, n3)
local v4 = m1
R0['params'] = v4
m1 = v4['notUseCache']
-- op11 A=2 B=0 C=2
R0['useCache'] = m1
m1 = v4['useAsync']
R0['useAsync'] = m1
m1 = v4['columns']
-- if not m1 goto L17
-- goto L0
m1 = 1.0
-- L0:
R0['columns'] = m1
m1 = v4['itemSpacing']
-- if not m1 goto L22
-- goto L1
m1 = 5.0
-- L1:
R0['itemSpacing'] = m1
m1 = v4['cellSpacing']
R0['cellSpacing'] = m1
m1 = v4['limitCount']
-- if not m1 goto L29
-- goto L2
m1 = 15.0
-- L2:
R0['limitCount'] = m1
m1 = R0:'setDirection'
s2 = R0
n3 = v4['direction']
-- if not n3 goto L37
-- goto L3
n3 = <G 'ccui'>
n3 = n3['ScrollViewDir']
n3 = n3['vertical']
-- L3:
m1 = m1(s2, n3)
m1 = v4['createCell']
R0['createCell'] = m1
m1 = v4['updateCell']
R0['updateCell'] = m1
m1 = v4['autoMid']
R0['autoMid'] = m1
m1 = v4['alignCenter']
R0['alignCenter'] = m1
m1 = v4['updateInterval']
-- if not m1 goto L50
-- goto L4
m1 = 0.1
-- L4:
R0['updateInterval'] = m1
m1 = v4['datas']
R0['datas'] = m1
m1 = v4['updateFunc']
R0['updateFunc'] = m1
m1 = v4['getInnerContainerPosition']
-- if not m1 goto L65
-- goto L5
m1 = v4['getContentSize']
-- if not m1 goto L65
-- goto L5
m1 = v4['getInnerContainerPosition']
R0['getInnerContainerPosition'] = m1
m1 = v4['getContentSize']
R0['getContentSize'] = m1
-- L5:
m1 = v4['registerEvent']
R0['registerEvent'] = m1
m1 = v4['size']
-- if not m1 goto L73
-- goto L6
m1 = R0:'setSize'
s2 = R0
n3 = v4['size']
m1 = m1(s2, n3)
-- L6:
m1 = v4['listTip']
-- if not m1 goto L83
-- goto L7
m1 = v4['listTip']
R0['listTip'] = m1
m1 = v4['listTipVerticalPosY']
-- if not m1 goto L82
-- goto L8
m1 = 0.0
-- L8:
R0['listTipVerticalPosY'] = m1
-- L7:
m1 = R0:'registerScriptHandler'
s2 = R0
n3 = <imm0>
local v5 = R0
m1 = m1(s2, n3)
m1 = <G 'math'>
m1 = m1['ceil']
s2 = v5['limitCount']
-- op35 A=3 B=294 C=3
m1 = m1(s2, n3)
v5['midIndex'] = m1
m1 = <G 'cc'>
m1 = m1['p']
s2 = 0.0
n3 = 0.0
m1 = m1(s2, n3)
v5['lastInnerPos'] = m1
m1 = v4['getInnerContainerPosition']
-- if not m1 goto L105
-- goto L9
m1 = v5:'getInnerContainerPosition'
s2 = v5
m1 = m1(s2, n3)
v5['lastInnerPos'] = m1
-- L9:
m1 = {}
v5['cellCache'] = m1
m1 = v4['getCache']
-- if not m1 goto L113
-- goto L10
m1 = v4['getCache']
m1 = m1(s2, n3)
v5['cellCache'] = m1
-- L10:
m1 = {}
v5['items'] = m1
m1 = v4['alphaPadding']
v5['alphaPadding'] = m1
m1 = v4['smoothDistance']
-- if not m1 goto L121
-- goto L11
-- L11:
v5['smoothDistance'] = m1
m1 = v5:'updateAlphaGradientPadding'
s2 = v5
m1 = m1(s2, n3)
return v5

===== fn#0 '' (6 instr, depth 2) =====
-- if 'destruction' == R0 goto L5
-- goto L0
local m1 = R1:'onDestruction'
local s2 = R1
m1 = m1(s2)
-- L0:
return R0