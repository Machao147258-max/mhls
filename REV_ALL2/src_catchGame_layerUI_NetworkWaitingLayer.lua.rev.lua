-- [[ src/catchGame/layerUI/NetworkWaitingLayer.lua ]]  src=src/catchGame/layerUI/NetworkWaitingLayer.lua size=32768
-- top: code=79 consts=37 protos=21

local utils_1 = require('common/utils')
local LayerUtil_2 = require('catchGame/utils/LayerUtil')
local framework_3 = require('lib/framework')
local downloader_4 = require('lib/downloader')
local ViewBase_5 = require('catchGame/mvc/ViewBase')
local Cls_6 = class('NetworkWaitingLayer')
local t_7 = {}  -- NEWTABLE arr=1 hash=3
t_7['network_tip_3'] = 'res'
t_7[true] = 'isCatchGame'
Cls_6['class'] = 'RESOURCE_FILENAME'
Cls_6['res'] = 'onCreate'
Cls_6['res'] = 'onCleanup'
Cls_6['res'] = 'registerWaitMsg'
Cls_6['res'] = 'unRegisterWaitMsg'
Cls_6['res'] = 'registerClientEvent'
Cls_6['res'] = 'doEvent'
Cls_6['res'] = 'removeEvent'
Cls_6['res'] = 'doUI'
Cls_6['res'] = 'onClose'
Cls_6['res'] = 'initUI'
Cls_6['res'] = 'finishLaunching'
Cls_6['res'] = 'checkFinish'
Cls_6['res'] = 'update'
Cls_6['res'] = 'onRevMsg'
Cls_6['res'] = 'onRevClientEvent'
Cls_6['res'] = 'destroyUI'
Cls_6['res'] = '_createEvent'
Cls_6['res'] = 'startCheckNet'
Cls_6['res'] = 'showNotCheckServerTip'
Cls_6['res'] = 'showCheckServerTip'
Cls_6['res'] = 'addWaitingEvent'