
===== fn#0 '@src/catchGame/systems/Rank/ClanRank.lua' (55 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/systems/Rank/RankBase'
g1 = g1(c2)
c2 = <G 'class'>
local c3 = 'ClanRank'
local v4 = g1
c2 = c2(c3, v4)
c3 = {}
c3['rankId'] = 'rankType'
c3['clanRankRange'] = '_rangeRange'
v4 = <imm0>
c2['onCreate'] = v4
v4 = <imm1>
c2['clearCacheData'] = v4
v4 = <imm2>
c2['registEvent'] = v4
v4 = <imm3>
g1 = c3
c2['getInfoBySelects'] = v4
v4 = <imm4>
c2['getIndexByInfo'] = v4
v4 = <imm5>
c2['getRankConfig'] = v4
v4 = <imm6>
c2['getRankIndex'] = v4
v4 = <imm7>
c2['getRankData'] = v4
v4 = <imm8>
c2['tryGetRankData'] = v4
v4 = <imm9>
c2['getRankSelf'] = v4
v4 = <imm10>
c2['tryGetRankSelf'] = v4
v4 = <imm11>
c2['reqRank'] = v4
v4 = <imm12>
c2['reqClanRankList'] = v4
v4 = <imm13>
c2['rspClanRankList'] = v4
v4 = <imm14>
local i5 = <imm15>
local t6 = {}
local g7 = <G 'NetGameEnum'>
g7 = g7['E_CLAN_RANK']
g7 = g7['E_CLAN_RANK_SCORE']
t6[g7] = v4
g7 = <G 'NetGameEnum'>
g7 = g7['E_CLAN_RANK']
g7 = g7['E_CLAN_RANK_LIVENESS']
t6[g7] = i5
g7 = <imm16>
g1 = t6
c2['reqClanMemberRank'] = g7
return c2
return g1

===== fn#0 '' (3 instr, depth 1) =====
local m1 = R0:'clearCacheData'
local s2 = R0
m1 = m1()
return R0