
===== fn#0 '@src/catchGame/configReader/ErrorCodeConfig.lua' (13 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'ErrorCodeConfig'
local v4 = g1
c2 = c2(c3, v4)
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['showErrorCode'] = c3
return c2
return g1

===== fn#0 '' (24 instr, depth 1) =====
local t1 = {}
R0['_codes'] = t1
t1 = <G 'pairs'>
local t2 = R0['datas']
t1 = t1(t2)
-- goto L0
-- L3:
local t3 = R5['code']
local t4 = R5['msgid']
-- if not t4 goto L11
-- goto L1
t4 = 0.0
-- L1:
local t5 = R0['_codes']
t5 = t5[t3]
-- if not t5 goto L18
-- goto L2
t5 = R0['_codes']
local t6 = {}
t5[t3] = t6
-- L2:
t5 = R0['_codes']
t5 = t5[t3]
t5[t4] = R5
-- L0:
-- op23 A=1 B=2 C=0
-- goto L3
return R0