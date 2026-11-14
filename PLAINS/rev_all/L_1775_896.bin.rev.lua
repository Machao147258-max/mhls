
===== fn#0 '@src/catchGame/systems/Logs/fpsLog.lua' (23 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/systems/Logs/logBase'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'fpsLog'
local v4 = g1
c2 = c2(c3, v4)
c3 = 0.1
v4 = <imm0>
c2['onCreate'] = v4
v4 = <imm1>
g1 = c3
c2['update'] = v4
v4 = <imm2>
c2['addLatencyDealy'] = v4
v4 = <imm3>
c2['record'] = v4
v4 = <imm4>
c2['clearRecord'] = v4
v4 = <imm5>
c2['calcAvg'] = v4
return c2
return g1

===== fn#0 '' (20 instr, depth 1) =====
R0['tmpFrame'] = 0.0
R0['accumDt'] = 0.0
R0['fps'] = 0.0
local t1 = {}
R0['lastFpsList'] = t1
t1 = {}
R0['lastPingList'] = t1
t1 = {}
R0['lastLatencyList'] = t1
R0['_totalLatency'] = 0.0
R0['_latencyCount'] = 0.0
t1 = R0['_system']
t1 = t1:'addTimer'
local s2 = t1
local c3 = 0.0
local g4 = <G 'handler'>
local v5 = R0
local t6 = R0['update']
g4 = g4(v5)
t1 = t1(s2, c3)
return R0