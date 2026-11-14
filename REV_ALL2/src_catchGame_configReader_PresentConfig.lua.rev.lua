-- [[ src/catchGame/configReader/PresentConfig.lua ]]  src=src/catchGame/configReader/PresentConfig.lua size=32768
-- top: code=137 consts=61 protos=17

local BaseReader_1 = require('catchGame/configReader/BaseReader')
local Cls_2 = class('PresentConfig')
local t_3 = {}  -- NEWTABLE arr=1 hash=5
t_3[0] = 'Normal'
t_3[1] = 'Letter'
t_3[2] = 'Ring'
t_3[3] = 'Letter2'
Cls_2['class'] = 'Type'
Cls_2[120] = 'DragonPalaceDiceId'
Cls_2[1] = 'FuCharacterMin'
Cls_2['Ring'] = 'FuCharacterMax'
local t_4 = {}  -- NEWTABLE arr=1 hash=6
t_4[1] = 3
t_4[2] = 4
t_4[3] = 100
t_4[3] = 101
t_4[1] = 119
local t_5 = {}  -- NEWTABLE arr=1 hash=5
local t_6 = {}  -- NEWTABLE arr=3 hash=1
t_5[4] = 'default'
local t_7 = {}  -- NEWTABLE arr=4 hash=1
t_5[100] = t_6
local t_8 = {}  -- NEWTABLE arr=2 hash=1
t_5[100] = t_6
local t_9 = {}  -- NEWTABLE arr=4 hash=1
t_5[100] = t_6
local t_10 = {}  -- NEWTABLE arr=1 hash=4
t_10['GiftCardLayer'] = 'default'
t_10['LetterDetailLayer'] = t_9
t_10['LetterMsg2'] = t_9
local t_11 = {}  -- NEWTABLE arr=1 hash=6
local t_12 = {}  -- NEWTABLE arr=1 hash=2
t_12['loveLetter'] = 'boxEffect'
t_11[101] = 3
local t_13 = {}  -- NEWTABLE arr=1 hash=2
t_13['anonymityLetter'] = 'boxEffect'
t_11[101] = 4
local t_14 = {}  -- NEWTABLE arr=1 hash=2
t_14['greetingLetter'] = 'boxEffect'
t_11[101] = 100
local t_15 = {}  -- NEWTABLE arr=1 hash=2
t_15['greetingLetter'] = 'boxEffect'
t_11[101] = 101
local t_16 = {}  -- NEWTABLE arr=1 hash=2
t_16['greetingLetter'] = 'boxEffect'
t_11[101] = 119
local t_17 = {}  -- NEWTABLE arr=1 hash=3
local t_18 = {}  -- NEWTABLE arr=1 hash=4
t_18['box'] = 'boxEffect'
t_18[false] = 'isShowAward'
t_18[true] = 'isShowDetail'
t_17[114] = 'default'
local t_19 = {}  -- NEWTABLE arr=1 hash=2
t_19['LetterMsg2'] = 'layer'
t_17[117] = t_18
Cls_2[114] = 'dealDatas'
Cls_2[114] = 'getSendSteps'
Cls_2[114] = 'getRecieveAnis'
Cls_2[114] = 'getDetailUIName'
Cls_2[114] = 'calcMaxSendNum'
Cls_2[114] = 'isAnonymity'
Cls_2[114] = 'isCPPresent'
Cls_2[114] = 'getCPPresent'
Cls_2[114] = 'isShowNotice'
Cls_2[114] = 'isTargetByCfg'
Cls_2[114] = 'getBagSearchBids'
Cls_2[114] = 'isBugsBunnyLetter'
Cls_2[114] = 'isRedPacketLetter'
Cls_2[114] = 'isFuCharacter'
Cls_2[114] = 'getLetterStyle'
Cls_2[114] = 'checkHaveEnclosure'
Cls_2[114] = 'isTypeById'