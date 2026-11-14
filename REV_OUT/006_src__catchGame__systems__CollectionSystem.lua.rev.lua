// 文件: 006_src__catchGame__systems__CollectionSystem.lua.luac
// 顶层原型: code=342 consts=132 protos=0

local BaseSystem_1 = require('catchGame/systems/BaseSystem')
local ClientEventManager_2 = require('catchGame/ClientEventManager')
local Utils_3 = require('catchGame/utils/Utils')
local utils_4 = require('common/utils')
local scheduler_5 = require('lib/scheduler')
local GameConst_6 = require('catchGame/GameConst')
local ShallowDataClone_7 = require('lib/ds/ShallowDataClone')
local ReaderFactory_8 = require('catchGame/configReader/ReaderFactory')
local CollectionUtils_9 = require('catchGame/layerUI/Collection/CollectionUtils')
local Cls_10 = class('CollectionSystem')
local t_11 = {}  -- NEWTABLE arr=7 hash=1
local t_12 = {}  -- NEWTABLE arr=1 hash=2
t_12['type'] = 'type'
local t_13 = {}  -- NEWTABLE arr=1 hash=4
t_13['cg'] = 'type'
t_13[nil] = nil
t_13[nil] = nil
local t_14 = {}  -- NEWTABLE arr=1 hash=5
t_14['GameC'] = 'type'
t_14[nil] = nil
t_14[nil] = nil
t_14[nil] = nil
local t_15 = {}  -- NEWTABLE arr=1 hash=5
t_15[nil] = 'type'
t_15[nil] = nil
t_15[nil] = nil
t_15[nil] = nil
local t_16 = {}  -- NEWTABLE arr=1 hash=5
t_16[nil] = 'type'
t_16[nil] = nil
t_16[nil] = nil
t_16[nil] = nil
local t_17 = {}  -- NEWTABLE arr=1 hash=5
t_17[nil] = 'type'
t_17[nil] = nil
t_17[nil] = nil
t_17[nil] = nil
local t_18 = {}  -- NEWTABLE arr=5 hash=1
local t_19 = {}  -- NEWTABLE arr=1 hash=5
t_19[nil] = nil
t_19[nil] = nil
t_19[nil] = nil
t_19[nil] = nil
local t_20 = {}  -- NEWTABLE arr=1 hash=5
local t_21 = {}  -- NEWTABLE arr=1 hash=2
local t_22 = {}  -- NEWTABLE arr=4 hash=1
t_21[nil] = nil
t_20[nil] = nil[t_16]
local t_23 = {}  -- NEWTABLE arr=1 hash=2
local t_24 = {}  -- NEWTABLE arr=4 hash=1
t_23[nil] = nil
t_20[nil] = nil[t_16]
local t_25 = {}  -- NEWTABLE arr=1 hash=7
local t_26 = {}  -- NEWTABLE arr=3 hash=1
t_25[nil] = t_24
local t_27 = {}  -- NEWTABLE arr=3 hash=1
t_25[nil] = t_24
local t_28 = {}  -- NEWTABLE arr=3 hash=1
t_25[nil] = t_24
local t_29 = {}  -- NEWTABLE arr=3 hash=1
t_25[nil] = t_24
local t_30 = {}  -- NEWTABLE arr=2 hash=1
t_25[nil] = t_24
local t_31 = {}  -- NEWTABLE arr=2 hash=1
t_25[nil] = t_24
t_20[nil] = nil[t_16]
local t_32 = {}  -- NEWTABLE arr=1 hash=5
local t_33 = {}  -- NEWTABLE arr=3 hash=1
t_32[nil] = t_24
local t_34 = {}  -- NEWTABLE arr=3 hash=1
t_32[nil] = t_24
local t_35 = {}  -- NEWTABLE arr=2 hash=1
t_32[nil] = t_24
local t_36 = {}  -- NEWTABLE arr=2 hash=1
t_32[nil] = t_24
t_20[nil] = nil[t_16]
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
Cls_10[nil] = nil
