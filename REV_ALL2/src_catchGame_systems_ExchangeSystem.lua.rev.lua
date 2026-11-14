-- [[ src/catchGame/systems/ExchangeSystem.lua ]]  src=src/catchGame/systems/ExchangeSystem.lua size=4080
-- top: code=50 consts=19 protos=7

local BaseSystem_1 = require('catchGame/systems/BaseSystem')
local ClientEventManager_2 = require('catchGame/ClientEventManager')
local Utils_3 = require('catchGame/utils/Utils')
local utils_4 = require('common/utils')
local scheduler_5 = require('lib/scheduler')
local cjson_6 = require('cjson')
local Cls_7 = class('ExchangeSystem')
Cls_7['ExchangeSystem'] = 'ctor'
Cls_7['ExchangeSystem'] = 'init'
Cls_7['ExchangeSystem'] = 'reset'
Cls_7['ExchangeSystem'] = 'registEvent'
Cls_7['ExchangeSystem'] = 'exchangeGift'
Cls_7['ExchangeSystem'] = 'onExchangeGift'
Cls_7['ExchangeSystem'] = 'onExchangeGiftError'