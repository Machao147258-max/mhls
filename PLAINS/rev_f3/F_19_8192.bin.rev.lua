
===== fn#0 '@src/catchGame/dataBinding/dataModel/LocalUserData.lua' (33 instr, depth 0) =====
local g1 = <G 'class'>
local c2 = 'LocalUserData'
g1 = g1(c2)
c2 = <G 'require'>
local c3 = 'cjson'
c2 = c2(c3)
c3 = <G 'cc'>
c3 = c3['FileUtils']
c3 = c3:'getInstance'
local s4 = c3
c3 = c3(s4)
c3 = c3:'getWritablePath'
s4 = c3
c3 = c3(s4)
s4 = c3
local c5 = 'localData'
s4 = s4 .. c5
c5 = <imm0>
g1['ctor'] = c5
c5 = <imm1>
g1 = s4
g1 = c2
g1['loadData'] = c5
c5 = <imm2>
g1 = c2
g1 = s4
g1['saveData'] = c5
c5 = <imm3>
g1['_getUserData'] = c5
c5 = <imm4>
g1['getCurUserData'] = c5
c5 = <imm5>
g1['setCurUserData'] = c5
return g1
return g1

===== fn#0 '' (5 instr, depth 1) =====
local t1 = {}
R0['userData'] = t1
t1 = R0:'loadData'
local s2 = R0
t1 = t1(s2)
return R0