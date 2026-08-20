
===== fn#0 '@src/catchGame/sdk/PushService.lua' (40 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/sdk/SdkPlatform'
g1 = g1(c2)
c2 = <G 'cc'>
c2 = c2['Application']
c2 = c2:'getInstance'
local s3 = c2
c2 = c2(s3)
c2 = c2:'getTargetPlatform'
s3 = c2
c2 = c2(s3)
s3 = <G 'cc'>
s3 = s3['PLATFORM_OS_IPHONE']
-- if s3 ~= c2 goto L18
-- goto L0
s3 = <G 'cc'>
s3 = s3['PLATFORM_OS_IPAD']
-- if s3 ~= c2 goto L18
-- goto L0
s3 = nil
-- L0:
s3 = nil
local g4 = <G 'cc'>
g4 = g4['PLATFORM_OS_ANDROID']
-- if g4 ~= c2 goto L24
-- goto L1
g4 = nil
-- L1:
g4 = nil
local g5 = <G 'cc'>
g5 = g5['PLAPLATFORM_OS_OHOS']
-- if g5 ~= c2 goto L30
-- goto L2
g5 = nil
-- L2:
g5 = nil
local t6 = {}
local i7 = <imm0>
g1 = s3
g1 = g1
g1 = g4
g1 = g5
t6['init'] = i7
return t6
return g1

===== fn#0 '' (105 instr, depth 1) =====
local g1 = <G 'userext'>
g1 = g1['SUPPORT_NEW_NGPUSH']
-- if 1.0 == g1 goto L31
-- goto L0
-- if not g1 goto L16
-- goto L1
g1 = g1:'bindPushAccount'
local s2 = g1
local g3 = <G 'cg'>
g3 = g3['Player']
g3 = g3['uid']
local n4 = nil
local n5 = nil
g1 = g1(s2, g3)
-- goto L2
-- L1:
-- if not g1 goto L22
-- goto L3
-- if not g1 goto L104
-- goto L2
-- L3:
g1 = g1:'bindPushAccount'
s2 = g1
g3 = <G 'cg'>
g3 = g3['Player']
g3 = g3['uid']
n4 = nil
n5 = nil
g1 = g1(s2, g3)
-- goto L2
-- L0:
-- if not g1 goto L77
-- goto L4
g1 = <G 'cc'>
g1 = g1['FileUtils']
g1 = g1:'getInstance'
s2 = g1
g1 = g1(s2, g3, n4)
g1 = g1:'getWritablePath'
s2 = g1
g1 = g1(s2, g3, n4)
s2 = 'devicetoken.data'
g1 = g1 .. s2
s2 = <G 'cc'>
s2 = s2['FileUtils']
s2 = s2:'getInstance'
g3 = s2
s2 = s2(g3, n4, n5)
s2 = s2:'getValueMapFromFile'
g3 = s2
n4 = g1
s2 = s2(g3, n4, n5)
-- if None ~= s2 goto L104
-- goto L2
g3 = s2['devicetoken']
n4 = 'com.netease.tomjerry'
n5 = <G 'logTrace'>
local c6 = 'register push service apns'
n5 = n5(c6)
-- if not g3 goto L104
-- goto L2
-- if '' ~= g3 goto L104
-- goto L2
n5 = g3
c6 = ',apns'
local c7 = ','
local v8 = n4
g3 = n5 .. v8
n5 = <G 'logTrace'>
c6 = 'register push service start :'
c7 = g3
c6 = c6 .. c7
n5 = n5(c6, c7)
n5 = <G 'cg'>
n5 = n5['systems']
n5 = n5['pushServiceSystem']
n5 = n5:'reqSubscribe'
c6 = n5
c7 = g3
n5 = n5(c6, c7)
-- goto L2
-- L4:
-- if not g1 goto L83
-- goto L5
-- if not g1 goto L104
-- goto L2
-- L5:
g1 = <G '_AppParam'>
g1 = g1['getRegid']
g1 = g1(s2, g3, n4)
s2 = <G 'logTrace'>
g3 = 'register push service niepush'
s2 = s2(g3, n4)
-- if not g1 goto L104
-- goto L2
-- if '' ~= g1 goto L104
-- goto L2
s2 = <G 'logTrace'>
g3 = 'register push service start:'
n4 = g1
g3 = g3 .. n4
s2 = s2(g3, n4)
s2 = <G 'cg'>
s2 = s2['systems']
s2 = s2['pushServiceSystem']
s2 = s2:'reqSubscribe'
g3 = s2
n4 = g1
s2 = s2(g3, n4)
-- L2:
return R0