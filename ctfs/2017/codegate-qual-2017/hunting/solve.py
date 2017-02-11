from zio import *
import os, time

rand_arr = os.popen('./leak 0').read().split()

io = zio("./hunting2", print_read = COLORED(RAW, 'red'), print_write = COLORED(RAW, 'yellow'), timeout = 10000)

# global
rand_count = 1
level = 0
switch = False
skill = 0
ICEBALL = 3
ICESWARD = 7
FIREBALL = 2

def show_hp(s):
    if 'hp is' in s:
        print 'hp : %s' % hex(int(s[(s.find('Boss\'s hp is') + 13):].splitlines()[0]))

def upgrade_level(s):
    global level, switch
    if 'You Win! Boss is upgrading..' in s:
        level += 1
        print '[+] level %d' % level
        if level == 3:
            switch = True
            return True
    return False

def switch_skill(i):
    global skill
    io.read_until('6. Exit')
    io.writeline('3')
    io.read_until('choice')
    io.writeline(str(i))
    skill = i
    print '[+] switch to skill %d' % i

def use_skill():
    global rand_count, skill

    s = io.read_until('6. Exit')
    if upgrade_level(s):
        io.writeline('3')
        io.read_until('choice')
        io.writeline(str(FIREBALL))
        skill = FIREBALL

    io.writeline('2')

    if skill == ICEBALL:
        rand_count += 1
    elif skill == ICESWARD:
        rand_count += 3
    elif skill == FIREBALL:
        rand_count += 1

    show_hp(s)

def defend():
    global rand_count, switch, level

    s = io.read_until('3. windshield')
    if upgrade_level(s):
        switch_skill(FIREBALL)
    upgrade_level(s)
    show_hp(s)

    val = int(rand_arr[rand_count]) % 4
    if val == 1:
        io.writeline(str(3))
    elif val == 2:
        io.writeline(str(2))
    elif val == 0:
        io.writeline(str(1))
    else:
        io.writeline(str(2))

    rand_count += 1

if __name__ == '__main__':

    switch_skill(ICEBALL)

    while True:
        use_skill()
        defend()
        if switch == True:
            break

    # come to level3

    # add 1 hp
    use_skill()
    defend()

    switch_skill(ICESWARD)
    use_skill()
    defend()
    time.sleep(2)

    # add 1 hp
    switch_skill(FIREBALL)
    use_skill()
    defend()

    switch_skill(ICESWARD)
    use_skill()
    defend()
    time.sleep(2)

    # finish
    io.interact()
