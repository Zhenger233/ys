import json

# 武器名称转id，id是WeaponExcelConfigData的id
def weapenName2id(weapenName):
    wi = json.load(open('weapenid.json', encoding='utf-8'))
    return wi[weapenName]

# 武器名称转id
def weapen2id(weapen):
    weapenId = weapen if isinstance(weapen, int) else weapenName2id(weapen)
    return weapenId

# 获取武器指定信息，输入为武器名称或id和信息名称
def getWeapenInfo(weapen=11501, info='weaponProp'):
    id = weapen2id(weapen)
    w = json.load(open('WeaponExcelConfigData.json'))
    return list(filter(lambda x:x['id'] == id, w))[0][info]

# 获取武器初始攻击力
def getWeapenAttackBase(weapen=11501):
    wp = getWeapenInfo(weapen, 'weaponProp')
    return list(filter(lambda x:x['propType'] == 'FIGHT_PROP_BASE_ATTACK', wp))[0]['initValue']

# 获取武器基础攻击力曲线类型
def getWeapenCurveType(weapen=11501):
    wp = getWeapenInfo(weapen, 'weaponProp')
    return list(filter(lambda x:x['propType'] == 'FIGHT_PROP_BASE_ATTACK', wp))[0]['type']

# 获取指定类型的乘数
def getWeapenCurveInfo(level=90, curveType='GROW_CURVE_ATTACK_302'):
    c = json.load(open('WeaponCurveExcelConfigData.json'))
    infos = list(filter(lambda x: x['level'] == level, c))[0]['curveInfos']
    return list(filter(lambda x: x['type'] == curveType, infos))[0]['value']

# 获取武器等级基础攻击力乘数
def getWeapenLevelAttackBaseMulti(weapen=11501, level=90):
    return getWeapenCurveInfo(level, getWeapenCurveType(weapen))

# 获取武器突破类型
def getWeapenPromoteId(weapen=11501):
    return getWeapenInfo(weapen, 'weaponPromoteId')

# 获取指定类型和次数的突破属性
def getPromoteAddProps(id=2, times=1):
    a = json.load(open('WeaponPromoteExcelConfigData.json'))
    return list(filter(lambda x:x['weaponPromoteId'] == id, a))[times]['addProps']

# 获取指定武器和次数的突破所得攻击力
def getWeapenPromoteAttack(weapen=11501, times=1):
    p = getPromoteAddProps(getWeapenPromoteId(weapen), times)
    return list(filter(lambda x:x['propType'] == 'FIGHT_PROP_BASE_ATTACK', p))[0]['value']

# 获取指定武器等级的基础攻击力
def getWeapenLevelAttackBase(weapen=11501, level=90):
    ab = getWeapenAttackBase(weapen)
    am = 0
    ap = 0
    times = 0
    if str(level)[-1] != '+':
        level = int(level)
        am = getWeapenLevelAttackBaseMulti(weapen, level)
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
        ap = getWeapenPromoteAttack(weapen, times)
        return ab * am + ap
    else:
        am = getWeapenLevelAttackBaseMulti(weapen, int(level[:2]))
        ap = getWeapenPromoteAttack(weapen, ['', '2', '4', '5', '6', '7', '8'].index(level[0]))
        return ab * am + ap

def test():
    testWeapen = 11501
    # print(weapen2id(testWeapen))
    # print(getWeapenInfo(testWeapen))
    # print(getWeapenAttackBase(testWeapen))
    # print(getWeapenCurveType(testWeapen))
    # print(getWeapenCurveInfo(90))
    # print(getWeapenLevelAttackBaseMulti(testWeapen, 90))
    # print(getWeapenPromoteId(testWeapen))
    # print(getPromoteAddProps(11501,6))
    # print(getWeapenPromoteAttack(testWeapen, 6))
    a = getWeapenLevelAttackBase(testWeapen, '80+')
    print(a, round(a, 0))
if __name__ == '__main__':
    test()
