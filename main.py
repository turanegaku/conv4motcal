#!/usr/bin/env python3
# set fenc=utf-8

import re
import sys
import json
import subprocess
from base64 import b64encode

def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))

def pprint(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python main.py deck.json')
        sys.exit(0)

    deckname = sys.argv[1]


    with open(deckname, 'r') as f:
        data = json.load(f)
    with open('resource/jobs.json', 'r') as f:
        jobs = json.load(f)
    with open('resource/skilltypes.json', 'r') as f:
        skilltypes = json.load(f)
    with open('resource/template.json', 'r') as f:
        kare = json.load(f)
    armType = ['none', 'sword', 'dagger', 'spear', 'axe', 'wand', 'gun', 'fist', 'bow', 'music', 'katana']
    elementType = ['non', 'fire', 'water', 'earth', 'wind', 'light', 'dark']
    re_skill = re.compile(r'skill_(\w+?)(_[am])?_(\d)(_\d)?')


    # search job from data
    job = [job for job in jobs if jobs[job]['name'] == data['deck']['pc']['job']['master']['name']][0]
    ele = elementType[int(data['deck']['pc']['weapons']['1']['master']['attribute'])] or elementType[1]

    profile = kare['storedData']['data']['profile']

    profile['masterBonus'] = data['deck']['pc']['job']['bonue']['master_bonus']['0']['param']
    profile['masterBonusHP'] = data['deck']['pc']['job']['bonue']['master_bonus']['4']['param']
    profile['element'] = ele
    profile['enemyElement'] = 'light'
    profile['DA'] = jobs[job]['DaBonus']
    profile['TA'] = jobs[job]['TaBonus']
    profile['job'] = job

    armlist = kare['storedData']['data']['armlist']
    armlist.clear()

    def existSameWeapon(armlist, weapon):
        return [i for i, arm in enumerate(armlist) if
                arm['name'] == weapon['master']['name'] and
                arm['attack'] == weapon['param']['attack'] and
                arm['hp'] == weapon['param']['hp']]

    for weapon in sorted(list(data['deck']['pc']['weapons'].values()), key=lambda x:x['master']['name']):
        i = existSameWeapon(armlist, weapon)
        if i:
            armlist[i[0]]['considerNumberMax'] += 1
            continue

        arm = {
            'name'              : '%s %s' % (weapon['master']['name'], weapon['param']['level']),
            'attack'            : weapon['param']['attack'],
            'hp'                : weapon['param']['hp'],
            'armType'           : armType[int(weapon['master']['kind'])],
            'skill1'            : 'non',
            'skill2'            : 'non',
            'slv'               : weapon['param']['skill_level'],
            'considerNumberMin' : 0,
            'considerNumberMax' : 1,
            'element'          : elementType[int(weapon['master']['attribute'])],
            'element1'          : elementType[int(weapon['master']['attribute'])],
            'element2'          : elementType[int(weapon['master']['attribute'])],
            }
        for i in range(1, 3):
            s, e = 'skill%d' % i, 'element%d' % i
            if weapon[s]:
                if weapon[s]['attribute']:
                    arm[e] = elementType[int(weapon[s]['attribute'])]

                m = re_skill.match(weapon[s]['image'])
                if m:
                    m = m.groups()
                    if m[2]:
                        arm[e] = elementType[int(m[2])]
                    if not m[1]:
                        if m[0] == 'baha':
                            # バハ
                            arm[s] = skilltypes[int(weapon[s]['id']) - 320]
                        if m[0] == 'atk':
                            # 通常攻刃
                            arm[s] = skilltypes[int(m[3][1]) + 1]
                        if m[0] == 'backwater':
                            # 通常背水
                            arm[s] = skilltypes[int(m[3][1]) + 6]
                    elif m[1] == '_m':
                        if m[0] == 'atk':
                            # マグナ攻刃
                            arm[s] = skilltypes[int(m[3][1]) + 16]
                        if m[0] == 'backwater':
                            # マグナ背水
                            arm[s] = skilltypes[int(m[3][1]) + 19]
                    elif m[1] == '_a':
                        if m[0] == 'atk':
                            # EX攻刃
                            arm[s] = skilltypes[int(m[3][1]) + 31]
                        if m[0] == 'backwater':
                            # EX背水
                            arm[s] = skilltypes[int(m[3][1]) + 29]

        armlist.append(arm)

    for summon in kare['storedData']['data']['summon']:
        summon['hp'] = data['deck']['pc']['summons_hp']
        summon['attack'] = data['deck']['pc']['summons_attack']
        summon['selfElement'] = ele
        summon['friendElement'] = ele

    kare['storedData']['data']['armNum'] = len(armlist)

    print('localStorage.setItem("data", "%s")' % b64encode(json.dumps(kare['storedData']).encode('utf-8')).decode('utf-8'))
    # write_to_clipboard('localStorage.setItem("data", "%s")' % b64encode(json.dumps(kare['storedData']).encode('utf-8')).decode('utf-8'))
