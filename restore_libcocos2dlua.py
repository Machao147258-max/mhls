import shutil, os
BAK = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so.orig'
F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
if os.path.exists(BAK):
    shutil.copy2(BAK, F)
    print("restored")
else:
    print("no backup")
