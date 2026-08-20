
===== fn#0 '@/Users/jenkins/workspace/h18/publish/src/catchGame/loadingScene/BattleLoadingScene.lua' (125 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'common/scene_base'
g1 = g1(c2)
c2 = <G 'require'>
local c3 = 'lib/ds'
c2 = c2(c3)
c3 = <G 'require'>
local c4 = 'catchGame/box2d/RubeSceneReader'
c3 = c3(c4)
c4 = <G 'require'>
local c5 = 'catchGame/ClientEventManager'
c4 = c4(c5)
c5 = <G 'require'>
local c6 = 'catchGame/utils/battleDelayLog'
c5 = c5(c6)
c6 = <G 'require'>
local c7 = 'common/lua_event_manager'
c6 = c6(c7)
c7 = <G 'require'>
local c8 = 'catchGame/sdk/SdkPlatform'
c7 = c7(c8)
c8 = <G 'require'>
local c9 = 'catchGame/matchPlugins/MatchPluginRegistry'
c8 = c8(c9)
c9 = <G 'require'>
local c10 = 'lib/framework'
c9 = c9(c10)
c10 = <G 'class'>
local c11 = 'BattleLoadingScene'
local v12 = g1
c10 = c10(c11, v12)
c10['__CLASS_NAME__'] = 'BattleLoadingScene'
c10['__FILE_NAME__'] = 'BattleLoadingScene'
c11 = <imm0>
g1 = c5
g1 = c7
g1 = c8
c10['ctor'] = c11
c11 = <imm1>
c10['endHotfix'] = c11
c11 = <imm2>
c10['checkHotfix'] = c11
c11 = <imm3>
c10['checkUGCMapFile'] = c11
c11 = <imm4>
c10['endCheckUGCMapFile'] = c11
c11 = <imm5>
g1 = c9
c10['checkTextures'] = c11
c11 = <imm6>
g1 = c3
c10['initLoadingPros'] = c11
c11 = <imm7>
c10['initRoomRealName'] = c11
c11 = <imm8>
c10['pro_asyLoadTexture'] = c11
c11 = <imm9>
c10['pro_asyLoadSpine'] = c11
c11 = <imm10>
g1 = c3
c10['pro_loadResorece'] = c11
c11 = <imm11>
c10['_checkLoadingAnimFadein'] = c11
c11 = <imm12>
c10['pro_waitAnimFadein'] = c11
c11 = <imm13>
c10['pro_loadScene'] = c11
c11 = <imm14>
c10['pro_resLoadEnd'] = c11
c11 = <imm15>
c10['pro_endLoading'] = c11
c11 = <imm16>
c10['pro_showWatingOther'] = c11
c11 = <imm17>
c10['pro_checkFrameSpeed'] = c11
c11 = <imm18>
c10['onTick'] = c11
c11 = <imm19>
g1 = c4
c10['doEvent'] = c11
c11 = <imm20>
g1 = c4
c10['onCleanup'] = c11
c11 = <imm21>
c10['addTodoFunc'] = c11
c11 = <imm22>
c10['on_reconnect_rsp'] = c11
c11 = <imm23>
c10['on_load_begin'] = c11
c11 = <imm24>
c10['on_load_over'] = c11
c11 = <imm25>
c10['on_get_frame_list'] = c11
c11 = <imm26>
c10['on_settlement'] = c11
c11 = <imm27>
c10['on_watcher_game_finish'] = c11
c11 = <imm28>
c10['on_end_of_game_player'] = c11
c11 = <imm29>
c10['OnLoadingEnd'] = c11
c11 = <imm30>
c10['enterBattle'] = c11
c11 = <imm31>
c10['on_room_cancel'] = c11
c11 = <imm32>
c10['setLoading'] = c11
c11 = <imm33>
c10['isLoading'] = c11
c11 = <imm34>
c10['pause'] = c11
c11 = <imm35>
c10['resume'] = c11
c11 = <imm36>
g1 = c6
c10['WatchLoadingCloseSound'] = c11
c11 = <imm37>
g1 = c6
c10['WatchLoadingResumeSound'] = c11
c11 = <imm38>
c10['on_game_show_fashion'] = c11
c11 = <imm39>
c10['showShowTime'] = c11
return c10
return g1

===== fn#0 '' (330 instr, depth 1) =====
local t1 = R0['super']
t1 = t1['ctor']
local v2 = R0
local t3 = {}
t3['autoRemoveRes'] = False
t3['resolutionShowAll'] = True
t1 = t1(v2, t3)
-- if not R5 goto L11
-- goto L0
t1 = {}
local v4 = t1
-- L0:
R0['game_dict'] = R1
R0['map_name'] = R2
t1 = <G 'cg'>
t1 = t1['systems']
t1 = t1['gmSystem']
t1 = t1:'startSingleRecord'
v2 = t1
t3 = R1
t1 = t1(v2, t3)
t1 = t1['setMapName']
v2 = R2
t1 = t1(v2, t3)
R0['tutorial_id'] = R3
R0['res_config'] = R4
R0['args'] = v4
t1 = R0['args']
v2 = R0['args']
v2 = v2['gradeType']
-- if not v2 goto L34
-- goto L1
v2 = <G 'NetGameEnum'>
v2 = v2['E_GRADE_TYPE']
v2 = v2['E_GRADE_TYPE_BASE']
-- L1:
t1['gradeType'] = v2
t1 = <G 'cg'>
-- if not t1 goto L50
-- goto L2
t1 = <G 'cg'>
t1 = t1['Utils']
-- if not t1 goto L50
-- goto L2
t1 = <G 'Globals'>
t1 = t1['lastSceneAutoRemoveRes']
-- if not t1 goto L50
-- goto L2
t1 = <G 'cg'>
t1 = t1['Utils']
t1 = t1['removeUnusedSpriteFrames']
t1 = t1(v2, t3)
-- L2:
t1 = {}
R0['_todoFuncs'] = t1
R0['_isEnterBattle'] = False
t1 = R1['reconnect']
-- if not t1 goto L57
-- goto L3
t1 = nil
-- L3:
R0['isReconnect'] = t1
t1 = R1['reconnect']
R0['_isReconnectAtBeg'] = t1
t1 = <G 'os'>
t1 = t1['time']
t1 = t1(v2, t3)
R0['_startTime'] = t1
t1 = R1['watchInfo']
-- if not t1 goto L71
-- goto L4
R0['isWatching'] = True
t1 = R1['watchInfo']
t1 = t1['isSpectator']
R0['isSpectator'] = t1
-- L4:
t1 = <G 'require'>
v2 = 'catchGame/BattleScene'
t1 = t1(v2, t3)
v2 = t1['new']
t3 = R0['game_dict']
local t5 = R0['map_name']
local t6 = R0['tutorial_id']
local t7 = R0['res_config']
local t8 = R0['args']
t8 = t8['mapLockedInfo']
local t9 = R0['args']
t9 = t9['gradeType']
local t10 = R0['args']
t10 = t10['forceMusic']
local t11 = R0['args']
t11 = t11['pauseMusic']
local t12 = R0['args']
t12 = t12['gameTutorialIDs']
local t13 = R0['args']
v2 = v2(t3, t5, t6)
R0['_scene'] = v2
v2 = R0['_scene']
v2 = v2:'retain'
t3 = v2
v2 = v2(t3, t5)
v2 = nil
t3 = R0['tutorial_id']
-- if not t3 goto L117
-- goto L5
t3 = <G 'cg'>
t3 = t3['Player']
t3 = t3:'isCompletedTutorialById'
t5 = t3
t6 = R0['tutorial_id']
t3 = t3(t5, t6, t7)
-- if not t3 goto L117
-- goto L5
t3 = <G 'cg'>
t3 = t3['TutorialMenuConfig']
t3 = t3:'getDataById'
t5 = t3
t6 = R0['tutorial_id']
t3 = t3(t5, t6, t7)
-- if not t3 goto L117
-- goto L5
t5 = t3['specLoading']
-- if not t5 goto L117
-- goto L5
v2 = nil
-- L5:
t3 = nil
-- if not v2 goto L127
-- goto L6
t5 = <G 'cg'>
t5 = t5['Game']
t5 = t5:'createLayer'
t6 = t5
t7 = 'TutorialLoadingLayer'
t5 = t5(t6, t7, t8)
t3 = t5
-- goto L7
-- L6:
t5 = R0['tutorial_id']
-- if not t5 goto L137
-- goto L8
t5 = <G 'cg'>
t5 = t5['Game']
t5 = t5:'createLayer'
t6 = t5
t7 = 'BattleLoading/LoadingTutorLayer2'
t5 = t5(t6, t7, t8)
t3 = t5
-- goto L7
-- L8:
t5 = t5:'getMemory'
t6 = t5
t5 = t5(t6, t7, t8)
R0['_physicalMemory'] = t5
t5 = <G 'cg'>
t5 = t5['systems']
t5 = t5['battleSystem']
t5 = t5:'getGameType'
t6 = t5
t5 = t5(t6, t7, t8)
t6 = t6:'getInstance'
t7 = t6
t6 = t6(t7, t8, t9)
t6 = t6:'getPluginByGameType'
t7 = t6
t8 = t5
t6 = t6(t7, t8, t9)
-- if not t6 goto L180
-- goto L9
t7 = t6['config']
t7 = t7['display']
-- if not t7 goto L161
-- goto L10
t7 = t6['config']
t7 = t7['display']
t7 = t7['loadingLayer']
-- L10:
-- if not t7 goto L180
-- goto L9
t8 = <G 'cg'>
t8 = t8['Game']
t8 = t8:'createLayer'
t9 = t8
t10 = t7
t11 = {}
t12 = R0['isReconnect']
t11['isReconnect'] = t12
t12 = R0['isWatching']
t11['isWatching'] = t12
t12 = R0['_physicalMemory']
-- if 1024.0 <= t12 goto L176
-- goto L11
t12 = nil
-- L11:
t12 = nil
t11['isSpecial'] = t12
t8 = t8(t9, t10, t11)
t3 = t8
-- L9:
-- if not t3 goto L270
-- goto L7
t7 = <G 'NetGameEnum'>
t7 = t7['E_GAME_TYPE']
t7 = t7['E_GAME_TYPE_NORMAL']
-- if t7 ~= t5 goto L197
-- goto L12
t7 = <G 'NetGameEnum'>
t7 = t7['E_GAME_TYPE']
t7 = t7['E_GAME_TYPE_HUMAN_MACHINE']
-- if t7 ~= t5 goto L197
-- goto L12
t7 = <G 'NetGameEnum'>
t7 = t7['E_GAME_TYPE']
t7 = t7['E_GAME_TYPE_LADDER']
-- if t7 == t5 goto L215
-- goto L13
-- L12:
t7 = <G 'cg'>
t7 = t7['Game']
t7 = t7:'createLayer'
t8 = t7
t9 = 'BattleLoading/Loading1v4Layer'
t10 = {}
t11 = R0['isReconnect']
t10['isReconnect'] = t11
t11 = R0['isWatching']
t10['isWatching'] = t11
t11 = R0['_physicalMemory']
-- if 1024.0 <= t11 goto L210
-- goto L14
t11 = nil
-- L14:
t11 = nil
t10['isSpecial'] = t11
t7 = t7(t8, t9, t10)
t3 = t7
-- goto L7
-- L13:
t7 = <G 'NetGameEnum'>
t7 = t7['E_GAME_TYPE']
t7 = t7['E_GAME_TYPE_5V5_CHEESE']
-- if t7 == t5 goto L238
-- goto L15
t7 = <G 'cg'>
t7 = t7['Game']
t7 = t7:'createLayer'
t8 = t7
t9 = 'BattleLoading/Loading5v5Layer'
t10 = {}
t11 = R0['isReconnect']
t10['isReconnect'] = t11
t11 = R0['isWatching']
t10['isWatching'] = t11
t11 = R0['_physicalMemory']
-- if 1024.0 <= t11 goto L233
-- goto L16
t11 = nil
-- L16:
t11 = nil
t10['isSpecial'] = t11
t7 = t7(t8, t9, t10)
t3 = t7
-- goto L7
-- L15:
t7 = <G 'NetGameEnum'>
t7 = t7['E_GAME_TYPE']
t7 = t7['E_GAME_TYPE_2V6']
-- if t7 == t5 goto L261
-- goto L17
t7 = <G 'cg'>
t7 = t7['Game']
t7 = t7:'createLayer'
t8 = t7
t9 = 'BattleLoading/Loading2v6Layer'
t10 = {}
t11 = R0['isReconnect']
t10['isReconnect'] = t11
t11 = R0['isWatching']
t10['isWatching'] = t11
t11 = R0['_physicalMemory']
-- if 1024.0 <= t11 goto L256
-- goto L18
t11 = nil
-- L18:
t11 = nil
t10['isSpecial'] = t11
t7 = t7(t8, t9, t10)
t3 = t7
-- goto L7
-- L17:
t7 = <G 'cg'>
t7 = t7['Game']
t7 = t7:'createLayer'
t8 = t7
t9 = 'LoadingLayer'
t10 = {}
t11 = R0['isWatching']
t10['isWatching'] = t11
t7 = t7(t8, t9, t10)
t3 = t7
-- L7:
t5 = t3:'setOnUpdate'
t6 = t3
t7 = <imm0>
local v14 = R0
t5 = t5(t6, t7)
t5 = v14:'addChild'
t6 = v14
t7 = t3
t5 = t5(t6, t7)
v14['_loadingUI'] = t3
t5 = <G 'cg'>
t5 = t5['ClientEventManager']
t5 = t5['fire']
t6 = <G 'cg'>
t6 = t6['ClientEventManager']
t6 = t6['ON_LOADING_UI_CREATE']
t7 = v14['_loadingUI']
t5 = t5(t6, t7)
t5 = <G 'require'>
t6 = 'launcher/LoadingManager'
t5 = t5(t6, t7, t8)
t5 = t5['new']
t5 = t5(t6, t7, t8)
v14['mgr'] = t5
t5 = v14['mgr']
t5 = t5:'setUserData'
t6 = t5
t7 = 'owner'
t8 = v14
t5 = t5(t6, t7)
t5 = v14:'doEvent'
t6 = v14
t5 = t5(t6, t7)
t5 = v4['movie']
-- if not t5 goto L323
-- goto L19
t5 = v4['movieCallback']
-- if not t5 goto L306
-- goto L20
t5 = <imm1>
-- L20:
t6 = v14:'addChild'
t7 = v14
t8 = <G 'cg'>
t8 = t8['Game']
t8 = t8:'createLayer'
t9 = t8
t10 = 'tutorial/TutorialMovieLayer'
t11 = {}
t12 = v4['movie']
t11['movie'] = t12
t12 = <imm2>
v14 = t5
v14 = v14
t11['endCallback'] = t12
t8 = t8(t9)
t6 = t6(t7, t8)
t6 = v14:'pause'
t7 = v14
t6 = t6(t7, t8)
-- op13 A=9 B=0 C=0
-- L19:
v14['_retryCount'] = 20.0
t5 = v14:'checkHotfix'
t6 = v14
t5 = t5(t6, t7)
t5 = <G 'logTrace'>
t6 = 'start loading======================'
t5 = t5(t6, t7)
return v14

===== fn#0 '' (4 instr, depth 2) =====
local m1 = R0:'onTick'
local s2 = R0
m1 = m1(s2)
return m1