-- [[ src/catchGame/systems/FriendSystemComponent.lua ]]  src=src/catchGame/systems/FriendSystemComponent.lua size=43335
-- top: code=490 consts=151 protos=60

local ClientEventManager_1 = require('catchGame/ClientEventManager')
local scheduler_2 = require('lib/scheduler')
local utils_3 = require('common/utils')
local cjson_4 = require('cjson')
local Cls_5 = class('PlayerSource')
local t_6 = {}  -- NEWTABLE arr=1 hash=9
t_6[300] = 'teacher'
t_6[256] = 'student'
t_6[128] = 'friend'
t_6[64] = 'classmate'
t_6[32] = 'recent'
t_6[16] = 'nearby'
t_6[8] = 'recommend'
t_6[-1] = 'none'
local t_7 = {}  -- NEWTABLE arr=1 hash=12
t_7[100] = 'couple'
t_7[95] = 'buddy'
t_7[90] = 'confidante'
t_7[85] = 'sidekick'
t_7[55] = 'teacher'
t_7[50] = 'student'
t_7[45] = 'classmate'
t_7[10] = 'mutualPraise'
t_7[9] = 'praise'
t_7[8] = 'praised'
t_7[-1] = 'none'
local t_8 = {}  -- NEWTABLE arr=1 hash=5
t_8[3] = 'mutualFollow'
t_8[2] = 'follow'
t_8[1] = 'fans'
t_8[-1] = 'none'
local t_9 = {}  -- NEWTABLE arr=1 hash=6
t_9['friend'] = 'E_INTIMATE_RELATION_NONE'['E_INTIMATE_RELATION'[<GLOBAL 'NetGameEnum'>]]
t_9['friend'] = 'E_INTIMATE_RELATION_COUPLE'['E_INTIMATE_RELATION'[<GLOBAL 'NetGameEnum'>]]
t_9['friend'] = 'E_INTIMATE_RELATION_BUDDY'['E_INTIMATE_RELATION'[<GLOBAL 'NetGameEnum'>]]
t_9['friend'] = 'E_INTIMATE_RELATION_SIDEKICK'['E_INTIMATE_RELATION'[<GLOBAL 'NetGameEnum'>]]
t_9['friend'] = 'E_INTIMATE_RELATION_CONFIDANTE'['E_INTIMATE_RELATION'[<GLOBAL 'NetGameEnum'>]]
Cls_5['PlayerSource'] = 'PLAYER_SOURCE'
Cls_5['teacher'] = 'RELATION_TYPE'
Cls_5[300] = 'FOLLOW_TYPE'
local t_10 = {}  -- NEWTABLE arr=5 hash=1
local t_11 = {}  -- NEWTABLE arr=1 hash=9
t_11[128] = 'source'
t_11[128] = 'relationType'
t_11[128] = 'followType'
t_11[0] = 'lastLogoutTime'
t_11[0] = 'status'
t_11[0] = 'extraStatusTags'
t_11[0] = 'gameType'
t_11[0] = 'gameStartTime'
local t_12 = {}  -- NEWTABLE arr=1 hash=7
t_12['classmate'] = 'teacher'[t_6]
t_12['classmate'] = 'student'[t_6]
t_12['classmate'] = 'classmate'[t_6]
t_12[32] = 'friend'[t_6]
t_12[64] = 'recent'[t_6]
t_12['recent'] = 'nearby'[t_6]
local t_13 = {}  -- NEWTABLE arr=1 hash=1
'pairs'(ClientEventManager_1, <R22>, <R23>)
'insert'[<GLOBAL 'table'>]()
'sort'[<GLOBAL 'table'>]()
local t_14 = {}  -- NEWTABLE arr=1 hash=12
t_14[100] = 'E_PLAYER_CURRENT_STATUS_HOME'['PLAYER_STATUS'['GameConst'[<GLOBAL 'cg'>]]]
t_14[95] = 'E_PLAYER_CURRENT_STATUS_ROOM'['PLAYER_STATUS'['GameConst'[<GLOBAL 'cg'>]]]
t_14[90] = 'E_PLAYER_CURRENT_STATUS_TEAM'['PLAYER_STATUS'['GameConst'[<GLOBAL 'cg'>]]]
t_14[0] = 'E_PLAYER_CURRENT_STATUS_NONE'['PLAYER_STATUS'['GameConst'[<GLOBAL 'cg'>]]]
t_14[80] = 'E_PLAYER_CURRENT_STATUS_GAME'['PLAYER_STATUS'['GameConst'[<GLOBAL 'cg'>]]]
t_14[70] = 'E_PLAYER_CURRENT_STATUS_MATCHING'['PLAYER_STATUS'['GameConst'[<GLOBAL 'cg'>]]]
t_14[75] = 'E_PLAYER_CURRENT_STATUS_PICK_CHARACTER'['PLAYER_STATUS'['GameConst'[<GLOBAL 'cg'>]]]
t_14[60] = 'E_PLAYER_CURRENT_STATUS_CONFIRM'['PLAYER_STATUS'['GameConst'[<GLOBAL 'cg'>]]]
t_14[40] = 'E_PLAYER_CURRENT_STATUS_WATCHING'['PLAYER_STATUS'['GameConst'[<GLOBAL 'cg'>]]]
t_14[50] = 'E_PLAYER_CURRENT_STATUS_TUTORIAL'['PLAYER_STATUS'['GameConst'[<GLOBAL 'cg'>]]]
t_14[85] = 'E_PLAYER_CURRENT_STATUS_SETTLEMENT'['PLAYER_STATUS'['GameConst'[<GLOBAL 'cg'>]]]
local t_15 = {}  -- NEWTABLE arr=1 hash=1
'pairs'(ClientEventManager_1, <R24>, 'insert'[<GLOBAL 'table'>])
'insert'[<GLOBAL 'table'>]()
'sort'[<GLOBAL 'table'>]()
Cls_5[-1] = 'ctor'
Cls_5[-1] = 'periodUpdate'
Cls_5[-1] = 'setRefreshData'
Cls_5[-1] = 'reqDataPeriod'
Cls_5[-1] = 'reset'
local t_16 = {}  -- NEWTABLE arr=8 hash=1
Cls_5['couple'] = 'recordAdditionInfo'
Cls_5['couple'] = 'getAdditionInfoByUID'
Cls_5['couple'] = 'resetAdditionInfo'
local t_17 = {}  -- NEWTABLE arr=1 hash=6
t_17['buddy'] = 'teacher'[t_6]
t_17['buddy'] = 'student'[t_6]
t_17['buddy'] = 'classmate'[t_6]
t_17['buddy'] = 'friend'[t_6]
t_17['buddy'] = 'recommend'[t_6]
local t_18 = {}  -- NEWTABLE arr=5 hash=1
Cls_5['buddy'] = 'getRelation'
Cls_5['buddy'] = 'init'
Cls_5['buddy'] = 'getBaseDataBySrcId'
Cls_5['buddy'] = 'getBaseDataByEvent'
Cls_5['buddy'] = 'getData'
Cls_5['buddy'] = '_getData'
Cls_5['buddy'] = 'registerEvent'
Cls_5['buddy'] = 'collegeUpdate'
Cls_5['buddy'] = 'friendUpdate'
Cls_5['buddy'] = 'recommendUpdate'
Cls_5['buddy'] = 'followUpdate'
Cls_5['buddy'] = 'reqGetFollowList'
Cls_5['buddy'] = 'getFollowList'
Cls_5['buddy'] = 'checkFollowType'
Cls_5['buddy'] = 'onGetFollowList'
Cls_5['buddy'] = 'reqGetPraiseList'
Cls_5['buddy'] = 'getPraiseList'
Cls_5['buddy'] = 'onGetPraiseList'
Cls_5['buddy'] = 'deregisterEvent'
Cls_5['buddy'] = 'onEvent'
Cls_5['buddy'] = 'reqAdditionInfo'
Cls_5['buddy'] = '_getAdditionInfo'
Cls_5['buddy'] = 'onRecAdditionInfo'
Cls_5['buddy'] = 'getOnlineRecommend'
Cls_5['buddy'] = 'reqOnlineRecommend'
Cls_5['buddy'] = 'onGetOnlineRecommend'
Cls_5['buddy'] = 'commonFire'
Cls_5['buddy'] = 'resetAllShowData'
local t_19 = {}  -- NEWTABLE arr=1 hash=1
local t_20 = {}  -- NEWTABLE arr=1 hash=1
Cls_5['mutualPraise'] = 'getAllShowData'
Cls_5['praise'] = 'getFilterFunc'
Cls_5['praise'] = 'debugShowAll'
local t_21 = {}  -- NEWTABLE arr=1 hash=8
local t_22 = {}  -- NEWTABLE arr=1 hash=3
t_22['bg_common_label_invite_2'] = 'icon'
t_22['CollegeEntr5'] = 'name'
t_21['praised'] = 'teacher'[t_6]
local t_23 = {}  -- NEWTABLE arr=1 hash=3
t_23['bg_common_label_invite_2'] = 'icon'
t_23['CollegeEntr5'] = 'name'
t_21['praised'] = 'student'[t_6]
local t_24 = {}  -- NEWTABLE arr=1 hash=3
t_24['bg_common_label_invite_3'] = 'icon'
t_24['FriendHomeLayerFriend'] = 'name'
t_21['praised'] = 'friend'[t_6]
local t_25 = {}  -- NEWTABLE arr=1 hash=3
t_25['bg_common_label_invite_2'] = 'icon'
t_25['CollegeEntr5'] = 'name'
t_21['praised'] = 'classmate'[t_6]
local t_26 = {}  -- NEWTABLE arr=1 hash=3
t_26['bg_common_label_invite_1'] = 'icon'
t_26['FriendHomeLayerPraise'] = 'name'
t_21['praised'] = 'recent'[t_6]
local t_27 = {}  -- NEWTABLE arr=1 hash=3
t_27['bg_common_label_invite_3'] = 'icon'
t_27['FriendHomeLayerNearBy'] = 'name'
t_21['praised'] = 'nearby'[t_6]
local t_28 = {}  -- NEWTABLE arr=1 hash=3
t_28['bg_common_label_invite_4'] = 'icon'
t_28['FriendAddLayerRecommend'] = 'name'
t_21['praised'] = 'recommend'[t_6]
local t_29 = {}  -- NEWTABLE arr=1 hash=11
local t_30 = {}  -- NEWTABLE arr=1 hash=3
t_30['bg_common_label_invite_1'] = 'icon'
t_30['CollegeTitle29'] = 'name'
t_29['mutualFollow'] = t_28
local t_31 = {}  -- NEWTABLE arr=1 hash=3
t_31['bg_common_label_invite_2'] = 'icon'
t_31['CollegeTitle27'] = 'name'
t_29['mutualFollow'] = t_28
local t_32 = {}  -- NEWTABLE arr=1 hash=3
t_32['bg_common_label_invite_3'] = 'icon'
t_32['CollegeTitle26'] = 'name'
t_29['mutualFollow'] = t_28
local t_33 = {}  -- NEWTABLE arr=1 hash=3
t_33['bg_common_label_invite_4'] = 'icon'
t_33['CollegeTitle28'] = 'name'
t_29['mutualFollow'] = t_28
local t_34 = {}  -- NEWTABLE arr=1 hash=3
t_34['bg_common_label_invite_1'] = 'icon'
t_34['CollegeTab7'] = 'name'
t_29['mutualFollow'] = t_28
local t_35 = {}  -- NEWTABLE arr=1 hash=3
t_35['bg_common_label_invite_4'] = 'icon'
t_35['CollegeTab8'] = 'name'
t_29['mutualFollow'] = t_28
local t_36 = {}  -- NEWTABLE arr=1 hash=3
t_36['bg_common_label_invite_3'] = 'icon'
t_36['CollegeTitle30'] = 'name'
t_29['mutualFollow'] = t_28
local t_37 = {}  -- NEWTABLE arr=1 hash=3
t_37['bg_common_label_invite_1'] = 'icon'
t_37['FriendLayerTag1'] = 'name'
t_29['mutualFollow'] = t_28
local t_38 = {}  -- NEWTABLE arr=1 hash=3
t_38['bg_common_label_invite_1'] = 'icon'
t_38['FriendLayerTag3'] = 'name'
t_29['mutualFollow'] = t_28
local t_39 = {}  -- NEWTABLE arr=1 hash=3
t_39['bg_common_label_invite_1'] = 'icon'
t_39['FriendLayerTag2'] = 'name'
t_29['mutualFollow'] = t_28
Cls_5['praised'] = 'getTagConfig'
local t_40 = {}  -- NEWTABLE arr=1 hash=3
t_40[3] = t_39
t_40[3] = t_39
Cls_5['mutualFollow'] = 'getStatusStrConfig'