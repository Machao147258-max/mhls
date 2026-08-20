
===== fn#0 '@src/catchGame/data/beginerActivityConfig.lua' (38 instr, depth 0) =====
local t1 = {}
local t2 = {}
t2['id'] = 1.0
t2['name'] = 'ifPopup'
t2['desc'] = '是否自动弹出(每天弹1次）'
t2['value'] = 1.0
t1[1.0] = t2
t2 = {}
t2['id'] = 2.0
t2['name'] = 'rewardText'
t2['desc'] = '有奖励可领时文案'
t2['value'] = '有奖励可以领取哟~'
t1[2.0] = t2
t2 = {}
t2['id'] = 3.0
t2['name'] = 'bubbleTime'
t2['desc'] = '气泡持续存在最大时间，单位为秒。'
t1[3.0] = t2
t2 = {}
t2['id'] = 4.0
t2['name'] = 'bubblePublicCD'
t2['desc'] = '气泡公共cd'
t2['value'] = 120.0
t1[4.0] = t2
t2 = {}
t2['id'] = 5.0
t2['name'] = 'bubblePrivateCD'
t2['desc'] = '气泡私有cd'
t2['value'] = 240.0
t1[5.0] = t2
t2 = {}
t2['id'] = 6.0
t2['name'] = 'saturdayPopup'
t2['desc'] = '累计弹出X次后改为每周弹出一次，重置弹出时间为周六0点'
t2['value'] = 15.0
t1[6.0] = t2
return t1
return t1