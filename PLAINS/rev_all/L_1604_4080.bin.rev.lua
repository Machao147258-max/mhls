
===== fn#0 '@src/catchGame/sdk/AudioController.lua' (94 instr, depth 0) =====
local g1 = <G 'require'>
local c2 = 'catchGame/sdk/SdkPlatform'
g1 = g1(c2)
c2 = <G 'require'>
local c3 = 'cjson'
c2 = c2(c3)
c3 = {}
c3['get-speaking-list'] = True
c3['get-capture-energy'] = True
c3['show-all-json'] = True
local t4 = {}
local i5 = <imm0>
g1 = g1
t4['startAudio'] = i5
i5 = <imm1>
g1 = g1
t4['closeAudio'] = i5
i5 = <imm2>
g1 = g1
t4['setAudioFormat'] = i5
i5 = <imm3>
g1 = c3
g1 = c2
g1 = g1
t4['controlAudio'] = i5
i5 = <imm4>
t4['createSession'] = i5
i5 = <imm5>
t4['destroySession'] = i5
i5 = <imm6>
t4['loginSession'] = i5
i5 = <imm7>
t4['logoutSession'] = i5
i5 = <imm8>
t4['startCapture'] = i5
i5 = <imm9>
t4['stopCapture'] = i5
i5 = <imm10>
t4['muteCapture'] = i5
i5 = <imm11>
t4['mutePlayback'] = i5
i5 = <imm12>
t4['setPlaybackVol'] = i5
i5 = <imm13>
t4['setCaptureVol'] = i5
i5 = <imm14>
t4['ignoreVoice'] = i5
i5 = <imm15>
t4['testMic'] = i5
i5 = <imm16>
t4['extraStream'] = i5
i5 = <imm17>
t4['getSpeakingList'] = i5
i5 = <imm18>
t4['getCaptureEnergy'] = i5
i5 = <imm19>
t4['resetEngine'] = i5
i5 = <imm20>
t4['stopEngine'] = i5
i5 = <imm21>
t4['setMonoQuality'] = i5
i5 = <imm22>
t4['forceNoVad'] = i5
i5 = <imm23>
t4['autoDealHome'] = i5
i5 = <imm24>
t4['autoDealCategory'] = i5
i5 = <imm25>
t4['autoDealInterruption'] = i5
i5 = <imm26>
t4['notifyHome'] = i5
i5 = <imm27>
t4['showAllJson'] = i5
i5 = <imm28>
t4['eidRecordOpen'] = i5
i5 = <imm29>
t4['eidRecordClose'] = i5
i5 = <imm30>
t4['enableRecordLast'] = i5
i5 = <imm31>
t4['recordLastAudio'] = i5
i5 = <imm32>
t4['sendHeartbeat'] = i5
i5 = <imm33>
t4['enableAudioTransfer'] = i5
i5 = <imm34>
t4['enableHookCapture'] = i5
i5 = <imm35>
t4['disableHookCapture'] = i5
i5 = <imm36>
g1 = g1
t4['getJsonData'] = i5
return t4
return g1

===== fn#0 '' (31 instr, depth 1) =====
local g1 = <G 'cg'>
-- if not g1 goto L21
-- goto L0
g1 = <G 'cg'>
g1 = g1['elk']
-- if not g1 goto L21
-- goto L0
g1 = <G 'GAMEPARAM'>
-- if not g1 goto L21
-- goto L0
g1 = <G 'GAMEPARAM'>
g1 = g1['audioLog']
-- if not g1 goto L21
-- goto L0
g1 = <G 'cg'>
g1 = g1['elk']
g1 = g1:'upload'
local s2 = g1
local t3 = {}
t3['operation'] = 'audio'
t3['type'] = 'start-audio'
g1 = g1(s2, t3)
-- L0:
g1 = g1:'startAudio'
s2 = g1
t3 = R1
g1 = g1(s2, t3)
-- if 0.0 ~= s2 goto L28
-- goto L1
t3 = nil
-- L1:
t3 = nil
return t3
return R0