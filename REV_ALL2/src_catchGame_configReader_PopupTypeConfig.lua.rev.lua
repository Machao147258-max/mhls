-- [[ src/catchGame/configReader/PopupTypeConfig.lua ]]  src=src/catchGame/configReader/PopupTypeConfig.lua size=32768
-- top: code=27 consts=19 protos=7

local BaseReader_1 = require('catchGame/configReader/BaseReader')
local Cls_2 = class('PopupTypeConfig')
Cls_2[3] = 'COUST_MAX'
Cls_2[1] = 'QUEUE_MAX'
Cls_2[-99999] = 'FORCE_WEIGHT'
Cls_2[-9999] = 'QUEUE_WEIGHT'
Cls_2['class'] = 'getCountMax'
Cls_2['class'] = 'getQueueMax'
Cls_2['class'] = 'getRankWithForceByID'
Cls_2['class'] = 'getQueueWeightByID'
Cls_2['class'] = 'setQueueTimeByID'
Cls_2['class'] = 'getIdByRank'
Cls_2['class'] = 'getRankWithForceAndQueueByID'