import json

avatarList = [
    'Kate', 'Ayaka', 'Qin', 'PlayerBoy', 'Lisa', 'PlayerGirl', 'Barbara', 'Kaeya', 'Diluc', 'Razor', 'Ambor', 'Venti', 'Xiangling', 'Beidou', 'Xingqiu', 'Xiao', 'Ningguang', 'Klee', 'Zhongli', 'Fischl', 'Bennett', 'Tartaglia', 'Noel', 'Qiqi', 'Chongyun', 'Ganyu', 'Albedo', 'Diona', 'Mona', 'Keqing', 'Sucrose', 'Xinyan', 'Rosaria', 'Hutao', 'Kazuha', 'Feiyan', 'Yoimiya', 'Tohma', 'Eula', 'Shougun', 'Sayu', 'Kokomi', 'Gorou', 'Sara', 'Itto', 'Yae', 'Aloy', 'Shenhe', 'Yunjin', 'Ayato'
]

# 角色名称转id
def avatarName2id(avatarName):
    avatars = json.load(open('avatarNameId.json', 'r', encoding='utf-8'))
    l = list(filter(lambda x:x['name'] == avatarName, avatars))
    if(len(l) != 0):
        return l[0]['id']
    else:
        return list(filter(lambda x:x['nameCHS'] == avatarName, avatars))[0]['id']

# 角色名称或id转id
def avatar2id(avatar):
    avatarIndex = avatar if type(avatar) == int else avatarName2id(avatar)
    return avatarIndex

# 获取角色指定信息，输入为角色名称或id和信息名称
def getAvatarinfo(avatar='Ayaka', info='attackBase'):
    a = json.load(open('AvatarExcelConfigData.json', encoding='utf-8'))
    return list(filter(lambda x:x['id'] == avatar2id(avatar), a))[0][info]

# 获取角色突破类型，输入为角色名称或id
def getAvatarPromoteId(avatar='Ayaka'):
    return getAvatarinfo(avatar, 'avatarPromoteId')

# 获取指定类型和次数的突破属性
def getPromoteAddProps(id=2, times=1):
    a = json.load(open('AvatarPromoteExcelConfigData.json'))
    return list(filter(lambda x:x['avatarPromoteId'] == id, a))[times]['addProps']

# 获取指定角色和次数的突破所得攻击力
def getAvatarPromoteAttack(avatar='Ayaka', times=1):
    p = getPromoteAddProps(getAvatarPromoteId(avatar), times)
    return list(filter(lambda x:x['propType'] == 'FIGHT_PROP_BASE_ATTACK', p))[0]['value']

# 获取指定角色和次数的突破所得生命值
def getAvatarPromoteHP(avatar='Ayaka', times=1):
    p = getPromoteAddProps(getAvatarPromoteId(avatar), times)
    return list(filter(lambda x:x['propType'] == 'FIGHT_PROP_BASE_HP', p))[0]['value']

# 获取指定角色和次数的突破所得防御力
def getAvatarPromoteDefense(avatar='Ayaka', times=1):
    p = getPromoteAddProps(getAvatarPromoteId(avatar), times)
    return list(filter(lambda x:x['propType'] == 'FIGHT_PROP_BASE_DEFENSE', p))[0]['value']

# 获取基础攻击力，输入为角色名称或id
def getAvatarAttackBase(avatar='Ayaka'):
    return getAvatarinfo(avatar, 'attackBase')

# 获取基础生命值，输入为角色名称或id
def getAvatarHPBase(avatar='Ayaka'):
    return getAvatarinfo(avatar, 'hpBase')

# 获取基础防御力，输入为角色名称或id
def getAvatarDefenseBase(avatar='Ayaka'):
    return getAvatarinfo(avatar, 'defenseBase')

# 获取攻击力曲线类型，输入为角色名称或id
def getAvatarAttackCurve(avatar='Ayaka'):
    return getAvatarinfo(avatar, 'propGrowCurves')[1]['growCurve']

# 获取生命值曲线类型，输入为角色名称或id
def getAvatarHPCurve(avatar='Ayaka'):
    return getAvatarinfo(avatar, 'propGrowCurves')[0]['growCurve']

# 获取防御力曲线类型，输入为角色名称或id
def getAvatarDefenseCurve(avatar='Ayaka'):
    return getAvatarinfo(avatar, 'propGrowCurves')[2]['growCurve']

# 获取指定类型的乘数
def getAvatarCurveInfo(level=90, curveType='GROW_CURVE_ATTACK_S5'):
    c = json.load(open('AvatarCurveExcelConfigData.json'))
    infos = list(filter(lambda x: x['level'] == level, c))[0]['curveInfos']
    return list(filter(lambda x: x['type'] == curveType, infos))[0]['value']

# 获取角色等级的攻击力乘数
def getAvatarLevelAttackMulti(avatar='Ayaka', level=90):
    return getAvatarCurveInfo(level, getAvatarAttackCurve(avatar))

# 获取角色等级的生命值乘数
def getAvatarLevelHPMulti(avatar='Ayaka', level=90):
    return getAvatarCurveInfo(level, getAvatarHPCurve(avatar))

# 获取角色等级的防御力乘数
def getAvatarLevelDefenseMulti(avatar='Ayaka', level=90):
    return getAvatarCurveInfo(level, getAvatarDefenseCurve(avatar))

# 获取指定角色等级的某项基础值
def getAvatarLevelBase(avatar='Ayaka', level=90, type='Attack'):
    f=[[getAvatarHPBase, getAvatarLevelHPMulti, getAvatarPromoteHP],[getAvatarAttackBase, getAvatarLevelAttackMulti, getAvatarPromoteAttack],[getAvatarDefenseBase, getAvatarLevelDefenseMulti, getAvatarPromoteDefense]][['HP', 'Attack', 'Defense'].index(type)]
    ab = f[0](avatar)
    am = 0
    ap = 0
    times = 0
    if str(level)[-1] != '+':
        level = int(level)
        am = f[1](avatar, level)
        if 20 < level <= 40:
            times = 1
        elif 40 < level <= 50:
            times = 2
        elif 50 < level <= 60:
            times = 3
        elif 60 < level <= 70:
            times = 4
        elif 70 < level <= 80:
            times = 5
        elif 80 < level <= 90:
            times = 6
        ap = f[2](avatar, times)
        return [ab * am + ap, ab, am, ap]
    else:
        am = f[1](avatar, int(level[:2]))
        ap = f[2](avatar, ['', '2', '4', '5', '6', '7', '8'].index(level[0]))
        return [ab * am + ap, ab, am, ap]

# 获取指定角色等级的基础攻击力
def getAvatarLevelAttackBase(avatar='Ayaka', level=90):
    return getAvatarLevelBase(avatar, level, 'Attack')[0]

# 获取指定角色等级的基础生命值
def getAvatarLevelHPBase(avatar='Ayaka', level=90):
    return getAvatarLevelBase(avatar, level, 'HP')[0]

# 获取指定角色等级的基础防御力
def getAvatarLevelDefenseBase(avatar='Ayaka', level=90):
    return getAvatarLevelBase(avatar, level, 'Defense')[0]

# 获取角色名称
def avatar2name(avatar='Ayaka'):
    avatars = json.load(open('avatarNameId.json', 'r', encoding='utf-8'))
    if isinstance(avatar, int):
        return list(filter(lambda x:str(x['id']).find(str(avatar)) > -1, avatars))[0]['name']
    elif isinstance(avatar, str):
        l = list(filter(lambda x:x['name'].find(avatar) > -1, avatars))
        if len(l) != 0:
            return l[0]['name']
        else:
            return list(filter(lambda x:x['nameCHS'].find(avatar) > -1, avatars))[0]['name']

# 获取角色技能倍率，只支持AEQ
def getAvatarSkill(avatar='Ayaka',skill=1,level=9):
    s = json.load(open('ProudSkillExcelConfigData.json', 'r'))
    avatar = avatar2name(avatar)
    if isinstance(skill, str): skill = {'A':1,'E':2,'Q':3}[skill]
    configStr = f'{avatar}_SkillUpgrade_{skill}'
    return list(filter(lambda x: x['openConfig'] == configStr, s))[level - 1]['paramList']

def test():
    testAvatar = 'Ayaka'
    testLevel = '90'
    # print(getAvatarAttackBase(testAvatar))
    # print(getAvatarHPBase(testAvatar))
    # print(getAvatarDefenseBase(testAvatar))
    # print(getAvatarAttackCurve(testAvatar))
    # print(getAvatarHPCurve(testAvatar))
    # print(getAvatarDefenseCurve(testAvatar))
    # print(getAvatarLevelAttackMulti(testAvatar, 90))
    # print(getAvatarLevelHPMulti(testAvatar, 90))
    # print(getAvatarLevelDefenseMulti(testAvatar, 90))
    # print(getAvatarPromoteAttack(testAvatar, 6))
    # a = json.load(open('AvatarCurveExcelConfigData.json'))
    # print(a[89])
    # print(getAvatarPromoteAttack(testAvatar, 6))
    a = getAvatarLevelAttackBase(testAvatar, testLevel)
    print(a, round(a, 0))
    h = getAvatarLevelHPBase(testAvatar, testLevel)
    print(h, round(h, 0))
    d = getAvatarLevelDefenseBase(testAvatar, testLevel)
    print(d, round(d, 0))

if __name__ == '__main__':
    test()
