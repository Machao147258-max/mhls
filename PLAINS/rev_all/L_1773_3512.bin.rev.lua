
===== fn#0 '@src/catchGame/systems/RuyuMovieSystem.lua' (66 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/systems/BaseSystem'
g1 = g1(c2)
c2 = <G 'require'>
local c3 = 'catchGame/ClientEventManager'
c2 = c2(c3)
c3 = <G 'require'>
local c4 = 'catchGame/utils/Utils'
c3 = c3(c4)
c4 = <G 'require'>
local c5 = 'lib/bit_op'
c4 = c4(c5)
c5 = <G 'class'>
local c6 = 'RuyuMovieSystem'
local v7 = g1
c5 = c5(c6, v7)
c6 = <imm0>
g1 = g1
c5['ctor'] = c6
c6 = <imm1>
c5['registEvent'] = c6
c6 = <imm2>
g1 = c2
c5['removeEvent'] = c6
c6 = <imm3>
c5['reqGetRuyuInfo'] = c6
c6 = <imm4>
g1 = c2
c5['onRspGetRuyuInfo'] = c6
c6 = <imm5>
c5['reqGetRuyuReward'] = c6
c6 = <imm6>
g1 = c3
g1 = c4
g1 = c2
c5['onRspGetRuyuReward'] = c6
c6 = <imm7>
c5['reqRuyuClean'] = c6
c6 = <imm8>
c5['onRspRuyuClean'] = c6
c6 = <imm9>
g1 = c2
c5['NtfRuyuProgressChange'] = c6
c6 = <imm10>
c5['onRuyuActivityError'] = c6
c6 = <imm11>
c5['getActivityRewardProcess'] = c6
c6 = <imm12>
g1 = c4
c5['getActivityRewardisFinish'] = c6
c6 = <imm13>
c5['initConfig'] = c6
c6 = <imm14>
c5['resetData'] = c6
c6 = <imm15>
c5['saveProcess'] = c6
c6 = <imm16>
c5['getProcess'] = c6
c6 = <imm17>
c5['getNowConfigData'] = c6
c6 = <imm18>
c5['checkRuyuActivityGuide'] = c6
c6 = <imm19>
c5['setRuyuActivityGuide'] = c6
return c5
return g1

===== fn#0 '' (5 instr, depth 1) =====
local t1 = R1['ctor']
local v2 = R0
t1 = t1(v2)
return R0