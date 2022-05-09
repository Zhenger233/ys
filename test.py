import Avatar
import Weapen
import json
import itertools
import csv
import pandas as pd

avatarList = [
    'Kate', 'Ayaka', 'Qin', 'PlayerBoy', 'Lisa', 'PlayerGirl', 'Barbara', 'Kaeya', 'Diluc', 'Razor', 'Ambor', 'Venti', 'Xiangling', 'Beidou', 'Xingqiu', 'Xiao', 'Ningguang', 'Klee', 'Zhongli', 'Fischl', 'Bennett', 'Tartaglia', 'Noel', 'Qiqi', 'Chongyun', 'Ganyu', 'Albedo', 'Diona', 'Mona', 'Keqing', 'Sucrose', 'Xinyan', 'Rosaria', 'Hutao', 'Kazuha', 'Feiyan', 'Yoimiya', 'Tohma', 'Eula', 'Shougun', 'Sayu', 'Kokomi', 'Gorou', 'Sara', 'Itto', 'Yae', 'Aloy', 'Shenhe', 'Yunjin', 'Ayato'
]

propList = ['生命值','防御力','攻击力','生命值百分比','防御力百分比','攻击力百分比','暴击率','暴击伤害','元素精通','元素充能效率']

# 用装饰器输出函数参数
def func_show(function):
    from functools import wraps
    @wraps(function)
    def function_timer(*args, **kvargs):
        print(f"[Function: {function.__name__} start with args: {list(map(lambda x:{'type':type(x),'value':x},args))}, kwargs: {list(map(lambda x:{'type':type(x),'value':x},kvargs))}]")
        result = function(*args, **kvargs)
        return result
    return function_timer

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

# 获取圣遗物词条名字
def getReliqPropName(prop:str):
    if prop.startswith('FIGHT_PROP_'):
        return prop
    else:
        pMap = json.load(open('ReliquaryPropsName.json', 'r', encoding='utf-8'))
        return pMap[prop]

# 获取指定星级等级圣遗物的某个主属性
def getReliqMainProp(rank:int = 5, level:int = 20, prop:str = 'FIGHT_PROP_HP'):
    a = json.load(open('ReliquaryLevelExcelConfigData.json', 'r', encoding='utf-8'))
    props = list(filter(lambda x: x.get('rank', '') == rank and x.get('level', '') == level + 1, a))[0]['addProps']
    prop = getReliqPropName(prop)
    return list(filter(lambda x: x.get('propType', '') == prop, props))[0]['value']

# 获取指定星级圣遗物的某个副属性列表
def getReliqAffixProps(rank:int = 5, prop:str = 'FIGHT_PROP_HP'):
    a = json.load(open('ReliquaryAffixExcelConfigData.json', 'r', encoding='utf-8'))
    prop = getReliqPropName(prop)
    props = list(filter(lambda x: str(x.get('id', ''))[0] == str(rank) and x.get('propType', '') == prop, a))
    return list(map(lambda x: x.get('propValue', 0), props))

# 获取指定圣遗物词条和准确数值的显示值
def getReliqShowProp(name:str = '生命值', value:float = 0) -> str:
    return format(value, '.0f') if name in ['攻击力', '防御力', '生命值', '元素精通'] else format(value, '.3f')

# 获取指定星级属性显示值对应的真实值列表
def getReliqAffixPromotions(rank:int = 5, name:str = '生命值', value:float = 0):
    rap = pd.read_csv('ReliquaryAffixPromotions.csv', encoding='utf-8')
    l = len(rap)
    ans = set()
    for i in range(l):
        if rap['rank'][i] == rank and rap['name'][i] == name and rap['show'][i] == float(value):
            ans.add(rap['value'][i])
        # list(map(lambda x:float(x), rap['list'][i][1:-2].split(', ')))
    return list(ans)

# 生成指定星级和词条的强化列表 name,prop,rank,num,show,value,list
def genReliqAffixPromotions(rank:int = 1, name:str = '生命值'):
    prop = getReliqPropName(name)
    p = getReliqAffixProps(rank, prop)
    maxNum = [1,2,2,4,5,6][rank]
    with open('ReliquaryAffixPromotions.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator = '\n')
        for num in range(maxNum + 1):
            for i in itertools.combinations_with_replacement(p, num):
                s = sum(i)
                shows = getReliqShowProp(name, s)
                """词条中文名，词条英文名，星级，词条数量，显示值，真实值，原始词条列表"""
                l = [name, prop, rank, num, str(shows), s, list(i)]
                writer.writerow(l)

# 用装饰器实现函数计时
def func_timer(function):
    from functools import wraps
    import time
    @wraps(function)
    def function_timer(*args, **kwargs):
        print(f'[Function: {function.__name__} start...]')
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print(f'[Function: {function.__name__} finished, spent time: {t1 - t0:.2f}s]')
        return result
    return function_timer

# 生成所有星级和词条的强化列表
def genReliqAffixPromotionsAll():
    propList = ['生命值','防御力','攻击力','生命值百分比','防御力百分比','攻击力百分比','暴击率','暴击伤害','元素精通','元素充能效率']
    for prop in propList:
        for i in range(1, 6):
            genReliqAffixPromotions(i, prop)    

@func_timer
def test():
    print(getReliqAffixPromotions(5, '暴击伤害', 0.225))
    print(getReliqAffixPromotions(5, '攻击力百分比', 0.105))
    print(getReliqAffixPromotions(5, '防御力百分比', 0.058))
    print(getReliqAffixPromotions(5, '防御力', 37))



if __name__ == "__main__":
    test()
