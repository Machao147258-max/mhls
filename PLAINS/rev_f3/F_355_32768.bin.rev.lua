
===== fn#0 '@src/catchGame/configReader/PortraitConfig.lua' (36 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'PortraitConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = {}
c3['Normal'] = 0.0
c3['Share'] = 1.0
c3['BetaTest'] = 2.0
c3['Questionnaire'] = 3.0
c2['Type'] = c3
c2['USE_BIN_DATA'] = True
c3 = <imm0>
c2['getAllCongfig'] = c3
c3 = <imm1>
c2['dealDatas'] = c3
c3 = <imm2>
c2['getMyOrder'] = c3
c3 = <imm3>
c2['getConfig'] = c3
c3 = <imm4>
g1 = c2
c2['getTip'] = c3
c3 = <imm5>
g1 = c2
c2['getDes'] = c3
c3 = <imm6>
g1 = c2
c2['getRandomPortrait'] = c3
c3 = <imm7>
g1 = c2
c2['getNormalPortraits'] = c3
return c2
return g1

===== fn#0 '' (3 instr, depth 1) =====
local t1 = R0['datas']
return t1
return R0