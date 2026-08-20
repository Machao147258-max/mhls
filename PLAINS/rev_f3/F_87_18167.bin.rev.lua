
===== fn#0 '@src/catchGame/configReader/TutorialListConfig.lua' (64 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/configReader/BaseReader'
g1 = g1(c2)
c2 = <G 'require'>
local c3 = 'catchGame/sdk/SdkPlatform'
c2 = c2(c3)
c3 = <G 'class'>
local c4 = 'TutorialMenuConfig'
local v5 = g1
c3 = c3(c4, v5)
c3['CHECK_ENTER_LIMIT_TIME'] = 604800.0
c4 = <imm0>
c3['ctor'] = c4
c4 = <imm1>
c3['checkReloadOnLogin'] = c4
c4 = <imm2>
c3['dealDatas'] = c4
c4 = <imm3>
c3['getTabDatas'] = c4
c4 = <imm4>
c3['getTabMouseTitle'] = c4
c4 = <imm5>
c3['getTabCatTitle'] = c4
c4 = <imm6>
c3['getTabSubDataByTabId'] = c4
c4 = <imm7>
c3['getAIData'] = c4
c4 = <imm8>
c3['getAITutorialId'] = c4
c4 = <imm9>
c3['isTabUnlock'] = c4
c4 = <imm10>
c3['isTutorialCollectionComplete'] = c4
c4 = <imm11>
c3['isExamTutorialUnlock'] = c4
c4 = <imm12>
c3['getExamTutorialRelys'] = c4
c4 = <imm13>
c3['isTabRedDot'] = c4
c4 = <imm14>
c3['isHomeRedDot'] = c4
c4 = <imm15>
g1 = c2
g1 = c3
c3['checkEnterTutorTime'] = c4
c4 = <imm16>
g1 = c2
c3['setEnterTutorTime'] = c4
c4 = <imm17>
c3['getDataCurrAwardInfo'] = c4
c4 = <imm18>
c3['getCompleteExamTutorialData'] = c4
c4 = <imm19>
c3['getUpdateRoleGradeInfo'] = c4
c4 = <imm20>
c3['_getLeftNotCompleteTutorId'] = c4
c4 = <imm21>
c3['isExamByTutorialId'] = c4
c4 = <imm22>
c3['getDataByTutorialId'] = c4
c4 = <imm23>
c3['checkNotExistNoCompleteReply'] = c4
return c3
return g1

===== fn#0 '' (18 instr, depth 1) =====
R0['_baseDataName'] = R1
local g1 = <G 'cg'>
g1 = g1['systems']
g1 = g1['tutorialSystem']
g1 = g1:'getVersionType'
local s2 = g1
g1 = g1(s2)
s2 = <G 'NetGameEnum'>
s2 = s2['E_TUTORIAL_VERSION_TYPE']
s2 = s2['E_TUTORIAL_VERSION_TYPE_B']
-- if s2 == g1 goto L14
-- goto L0
g1 = R1
s2 = '_b'
local s3 = g1 .. s2
-- L0:
R0['dataName'] = s3
g1 = R0:'reload'
s2 = R0
g1 = g1(s2)
return R0