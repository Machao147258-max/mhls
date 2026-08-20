
===== fn#0 '@src/catchGame/configReader/BattlePassAwardConfig.lua' (44 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'require'>
local c3 = 'lib/framework'
c2 = c2(c3)
c3 = <G 'class'>
local c4 = 'BattlePassAwardConfig'
local v5 = g1
c3 = c3(c4, v5)
c4 = <imm0>
c3['dealDatas'] = c4
c4 = <imm1>
c3['_getSeasonConfig'] = c4
c4 = <imm2>
c3['_findSeasonById'] = c4
c4 = <imm3>
c3['_getSeasonData'] = c4
c4 = <imm4>
c3['_loadSeasonData'] = c4
c4 = <imm5>
c3['_dealSeasonDatas'] = c4
c4 = <imm6>
c3['getDatasBySeason'] = c4
c4 = <imm7>
c3['getLevelDatasBySeason'] = c4
c4 = <imm8>
c3['getNormalLevelDatasBySeason'] = c4
c4 = <imm9>
c3['getAllLevelDatasBySeason'] = c4
c4 = <imm10>
c3['getLevelToNextDatasBySeason'] = c4
c4 = <imm11>
c3['getDefaultAwardBySeason'] = c4
c4 = <imm12>
c3['getSpecialAwardBySeason'] = c4
c4 = <imm13>
c3['getChallengeDatasBySeasion'] = c4
c4 = <imm14>
c3['getDataById'] = c4
c4 = <imm15>
c3['fixSeasonData'] = c4
return c3
return g1

===== fn#0 '' (5 instr, depth 1) =====
local t1 = {}
R0['realDatas'] = t1
t1 = {}
R0['seasonDatas'] = t1
return R0