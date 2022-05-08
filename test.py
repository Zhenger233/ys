import Avatar
import Weapen
import json

avatarList = [
    'Kate', 'Ayaka', 'Qin', 'PlayerBoy', 'Lisa', 'PlayerGirl', 'Barbara', 'Kaeya', 'Diluc', 'Razor', 'Ambor', 'Venti', 'Xiangling', 'Beidou', 'Xingqiu', 'Xiao', 'Ningguang', 'Klee', 'Zhongli', 'Fischl', 'Bennett', 'Tartaglia', 'Noel', 'Qiqi', 'Chongyun', 'Ganyu', 'Albedo', 'Diona', 'Mona', 'Keqing', 'Sucrose', 'Xinyan', 'Rosaria', 'Hutao', 'Kazuha', 'Feiyan', 'Yoimiya', 'Tohma', 'Eula', 'Shougun', 'Sayu', 'Kokomi', 'Gorou', 'Sara', 'Itto', 'Yae', 'Aloy', 'Shenhe', 'Yunjin', 'Ayato'
]

# 获取角色白值
def testAvatarAttackBase():
    testAvatar = '神里绫华'
    testWeapen = '风鹰剑'
    a = Avatar.getAvatarLevelAttackBase(testAvatar, 90)
    w = Weapen.getWeapenLevelAttackBase(testWeapen, 90)
    print(f'角色白值:{a}, 武器白值:{w}, 实际白值:{a + w}, 显示白值:{a + w:.0f}')
    h = Avatar.getAvatarLevelHPBase(testAvatar, 90)
    d = Avatar.getAvatarLevelDefenseBase(testAvatar, 90)
    print(f'实际生命值白值:{h}, 显示生命值白值:{h:.0f}')
    print(f'实际防御力白值:{d}, 显示防御力白值:{d:.0f}')   

def testAvatarSkill():
    testAvatar = 'Ayaka'
    sa = Avatar.getAvatarSkill(testAvatar, 'A', 10)
    se = Avatar.getAvatarSkill(testAvatar, 'E', 10)
    sq = Avatar.getAvatarSkill(testAvatar, 'Q', 10)
    print(f'A技能倍率:{sa}\nE技能倍率:{se}\nQ技能倍率:{sq}')

if __name__ == "__main__":
    testAvatarAttackBase()
    testAvatarSkill()
