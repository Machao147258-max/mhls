
===== fn#0 '@src/catchGame/configReader/EmojiConfig.lua' (16 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'BuffConfig'
local v4 = g1
c2 = c2(c3, v4)
c2['USE_BIN_DATA'] = True
c3 = <imm0>
c2['dealDatas'] = c3
c3 = <imm1>
c2['isFree'] = c3
c3 = <imm2>
c2['getTypeDatas'] = c3
return c2
return g1

===== fn#0 '' (27 instr, depth 1) =====
local t1 = {}
R0['typeDatas'] = t1
t1 = <G 'pairs'>
local t2 = R0['datas']
t1 = t1(t2)
-- goto L0
-- L2:
local t3 = R6['figure']
R6['icon'] = t3
t3 = R0['typeDatas']
local t4 = R6['role']
local t5 = R0['typeDatas']
local t6 = R6['role']
t5 = t5[t6]
-- if not t5 goto L16
-- goto L1
t5 = {}
-- L1:
t3[t4] = t5
t3 = <G 'table'>
t3 = t3['insert']
t4 = R0['typeDatas']
t5 = R6['role']
t4 = t4[t5]
t5 = R6
t3 = t3(t4, t5)
-- L0:
-- op23 A=2 B=2 C=0
-- goto L2
return R0