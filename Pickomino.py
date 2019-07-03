"""

Issue : make behaviour of players dependent on existing top of stack

Player tactic 1 means auto_thief function

"""
import random
import pandas as pd
import matplotlib.pyplot as plt

number_of_dice = 8
free_sides = [1, 2, 3, 4, 5, 'W']
score = 0
TILES = [x for x in range(21, 36)]
TILESoriginal = [x for x in range(21, 36)]
WORMS = [1]*4 + [2] * 4 + [3] * 4 + [4] * 4
TILES.append('X')
throw_number = 1
turn_number = 1
winning = []
turncol = ['playerID', 'fail', 'W_found', 'score', 'steal']
win_tiles = []
df = pd.DataFrame(columns=turncol)
playerID = 0
overallWinners = []
stay_in_turn = True

turndict = {}


class gameplay:
    def __init__(self):
        pass
    
    
        

class player:
    def __init__(self, playername):
        self.name = playername
        self.human = False
        self.own_tiles = []
        self.tactic = 0

    def throw_dice(self, number_of_dice):
        self.thrown_dice = []
        for x in range(number_of_dice):
            self.thrown_dice.append(random.randint(1, 6))
        return self.thrown_dice

    def orden_dices_in_dict(self, dicelist):
        self.hand = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 'W': 0}
        for keys in self.hand:
            self.hand[keys] = dicelist.count(keys)
            self.hand['W'] = dicelist.count(6)
        return self.hand

    def calculate_score(self, score, points):
        self.score = score + points
        return self.score

    def auto_mx_point(self, hand, possible_sides):
        mx_pick = []
        for pos_sides in possible_sides:
            mx_pick.append(hand[pos_sides] * pos_sides)
        if isinstance(mx_pick[-1], str):
            worms = mx_pick[-1].count('W')
            del mx_pick[-1]
            mx_pick.append(worms * 5)
        mx = max(mx_pick)
        mx_index = mx_pick.index(mx)
        print(f'{players[playerID].name} picks {possible_sides[mx_index]} (score now {score + mx})')
#        players[playerID].think_one_step_ahead(free_sides, score)
        return possible_sides[mx_index]

    def auto_thief(self, hand, possible_sides, stealList):
        mx_pick = []
        steal_opp = False
        steal_others = stealList[:]
        del steal_others[playerID]      
        for pos_sides in possible_sides:
            mx_pick.append(hand[pos_sides] * pos_sides)
        if isinstance(mx_pick[-1], str):
            worms = mx_pick[-1].count('W')
            del mx_pick[-1]
            mx_pick.append(worms * 5)
        for steal in steal_others:
            for pick in mx_pick:
                if score + pick == steal:
                    print('yes! steal possible')
                    mx = pick
                    mx_index = mx_pick.index(pick)
                    steal_opp = True
        if not found_the_W(free_sides):
            steal_opp = False
        if not steal_opp:
            pick_one = players[playerID].think_one_step_ahead(hand, possible_sides)
#            mx = max(mx_pick)
#            mx_index = mx_pick.index(mx)
            return pick_one
        print(f'{players[playerID].name} picks {possible_sides[mx_index]}, score now {score+mx}')
        return possible_sides[mx_index]

    def think_one_step_ahead(self, hand, possible_sides):
        current_worms = worms_quantity(score)
        mx_pick = []
        for pos_sides in possible_sides:
            mx_pick.append(hand[pos_sides] * pos_sides)
        if isinstance(mx_pick[-1], str):
            worms = mx_pick[-1].count('W')
            del mx_pick[-1]
            mx_pick.append(worms * 5)
        free_sides2 = free_sides[:]
        bothsteps = []
        for t in possible_sides:           
            step1score = mx_pick[possible_sides.index(t)] + score
            free_sides2.remove(t)
            dice_left = new_nr_of_dice(hand, t)
            free_sides2_sum = free_sides_sum(free_sides2)
            step2score = dice_left * (free_sides2_sum / 6)
            free_sides2.append(t)
#            print (f'Sum both steps = {step1score + step2score}')
            bothsteps.append(step1score + step2score)
        maxstep = max(bothsteps)
#        print(bothsteps)
#        print(f'Advice is {possible_sides[bothsteps.index(maxstep)]}')
        mx = max(mx_pick)
        mx_index = mx_pick.index(mx)
#        print(f'{players[playerID].name} picks {possible_sides[mx_index]} (score now {score + mx})')
        print(f'{players[playerID].name} picks {possible_sides[bothsteps.index(maxstep)]} (score now {score + mx})')
        if possible_sides[mx_index] != possible_sides[bothsteps.index(maxstep)]:
            print('alarm')
        return possible_sides[bothsteps.index(maxstep)]

def free_sides_sum(free):
    if 'W' in free:
        free.remove('W')
        free.append(5.01)
        sum_free = sum(free)
        del free[-1]
        free.append('W')
    else:
        sum_free= sum(free)
    return sum_free



def add_human():
    add_human = input('A human player joining? (y/n)  ')
    if add_human.upper() == 'Y':
        while True:
            who = input(f'Play with Albert, Boris or Chris? (a/b/c) ')
            if who.upper() == 'A':
                albert.human = True
                break
            if who.upper() == 'B':
                boris.human = True
                break
            if who.upper() == 'C':
                chris.human = True
                break
            print("I don't understand. A, B or C")


def create_stealList(players):
    stealList = []
    for play in players:
        stealList.append(0)
    return stealList


def update_stealList(players, stealList):
    nr_of_players_min1 = (len(players))
    for x in range(0, nr_of_players_min1):
        if players[x].own_tiles:
            stealList[x] = players[x].own_tiles[-1]
        else:
            stealList[x] = 0
    return stealList


def work_with_int_and_string(decided):
    # humans only
    if decided.upper() != 'W':
        decided = int(decided)
    else:
        decided = decided.upper()
    return decided


def print_flathand(hand, playerID):
    flat = []
    for key in hand:
        flat.append(str(key) * hand[key],)
    flat = ''.join(str(e) for e in flat)
    print(f'{players[playerID].name} throws ' + flat)


def possible_sides_to_pick(hand, free_sides):
    thrown_numbers = [key for key in hand if hand[key] > 0]
    return [x for x in thrown_numbers if x in free_sides]


def calculate_points(hand, pick_one):
    if pick_one != 'W':
        points = pick_one * hand[pick_one]
    elif pick_one == 'W':
        points = 5 * hand[pick_one]
    return points


def found_the_W(free_sides_of_dice):
    if 'W' not in free_sides_of_dice:
        return True
    return False


def stop_rolling_again_question():
    """This function asks if human user will throw again"""
    stop_or_not = input('Roll again? (y/n) .. ')
    if stop_or_not.upper() == "N":
        return False
    return True


def survival_rate(free_sides, dice_left):
    free = len(free_sides)
    notfree = 6 - free
    notfreepower = notfree ** dice_left
    allsixsides = 6 ** dice_left
    deadrate = notfreepower / allsixsides
    return int(100 * (1 - deadrate))


def worms_quantity(nr):
    if nr < 21:
        return 0
    if 25 > nr > 20:
        return 1
    if 29 > nr > 24:
        return 2
    if 33 > nr > 28:
        return 3
    if nr > 32:
        return 4


def pay_off_worms(free_sides, dice_left, score):
    avg = int(dice_left) * int(sum(free_sides) / 6)
    top_of_stack = 0
    if players[playerID].own_tiles:
        top_of_stack = players[playerID].own_tiles[-1]
    print(f'now {players[playerID].name} would win {worms_quantity(score)} worms')
    extra_worms = worms_quantity(score+avg) - worms_quantity(score)
    print(f'if he throws again he expects to gain {extra_worms} extra worms')
    print(f'but if he loses, he loses {worms_quantity(top_of_stack)} worms')

    extra_worms_odds = (survival_rate(free_sides, dice_left) / 100) * extra_worms
    lose_worms_odds = worms_quantity(top_of_stack) * 0.01 * (1 - survival_rate(free_sides, dice_left)) 
    print(f'sum is {extra_worms_odds + lose_worms_odds}')
    return (extra_worms_odds + lose_worms_odds)


def new_nr_of_dice(hand, pick):
    return sum(hand.values()) - hand[pick]


def is_turn_over(number_of_dice_left, free_sides_left):
    if number_of_dice_left and free_sides_left:
        return False  # not dead, because dice left and sides left
    return True


def find_tile(tiles, lastscore):
    while True:
        if lastscore in tiles:
            break
        lastscore = lastscore - 1
    return lastscore


def remove_last_tile(tiles):
    last_tiles = -1
    while True:
        if isinstance(tiles[last_tiles], int):
            tiles[last_tiles] = 'X'
            break
        else:
            last_tiles -= 1
    return tiles


def reset_vars():
    number_of_dice = 8
    free_sides = [1, 2, 3, 4, 5, 'W']
    score = 0
    return number_of_dice, free_sides, score


def reset_tiles(playerID):
    TILES = [x for x in range(21, 36)]
    TILES.append('X')
    players[playerID].own_tiles = []
    throw_number = 1
    turn_number = 1
    winnaar = ""
    return TILES, players[playerID].own_tiles,\
        throw_number, turn_number, winnaar


def check_first_tiles_int(first_tile):
    if len(first_tile) < 1:
        print('tiles empty!')
        return True
    return isinstance(first_tile[0], int)


def give_back_tile(number, TILES):
    TILES.insert(0, number)
    TILES = [n for n in TILES if isinstance(n, int)]
    TILES.sort()
    TILES.append('X')
    return TILES


def picked_sides(free_sides):
    taken = [1, 2, 3, 4, 5, 'W']
    picked = [e for e in taken if e not in free_sides]
    picked = ''.join(str(e) for e in picked)
    return picked


def string_not_list(lst):
    return ''.join(str(e) for e in lst)


def min_tiles_calc(TILES):
    lowest_tile = []
    lowest_tile.append(min(n for n in TILES if isinstance(n, int)))
    return lowest_tile


def max_tiles_calc(TILES):
    max_tile = []
    max_tile.append(max(n for n in TILES if isinstance(n, int)))
    return max(max_tile)


def score_high(score, min_tiles):
    if score >= min_tiles:
        return True
    return False


def next_player(players, playerID):
    playerID += 1
    if playerID == len(players):
        playerID = 0
    return playerID


def most_worms(players):
    # calculate most worms
    total_worms = []
    for playerID in players:
        ownWorms = []
        for tile in playerID.own_tiles:
            spot = worms_quantity(tile)
            ownWorms.append(spot)
        print(f'Worms {playerID.name} = {sum(ownWorms)}')
        total_worms.append(sum(ownWorms))
    winner = (total_worms.index(max(total_worms)))
# check draw
    if total_worms.count(max(total_worms)) > 1:
        print('draw in worms')
        draw = []
        for play1 in players:
            draw.append(sum(play1.own_tiles))
        winner = draw.index(max(draw))
    print(f'{players[winner].name} is the winner')
    return players[winner].name


def winner_count(list, players):
    for play in players:
        print(f'{play.name} won {list.count(play.name)} times')


def steal_possible(score, stealList):
    if score in stealList:
        if stealList.index(score) != playerID:
            return True
    return False


def strategy_thief():
    if steal_possible(score, stealList):
        print ('going to steal!')
        return False
    else:
        exp_result = pay_off_worms(free_sides, number_of_dice, score)
        if exp_result > 0:
            return True
        return False


if __name__ == "__main__":
    albert = player('Albert')
    boris = player('Boris')
    chris = player('Chris')
    albert.tactic = 1
    boris.tactic = 2
    print('Rules. Try to win most worms. Tiles on table have worms, 21 - 24 have 1 worm')
    print('25-28 2 worms, 29 - 32 : 3 worms and higher 4 worms.\n')
    print('Start with 8 dice, you need to pick a side to keep it apart.\nYou need a worm too (worth 5 points)')
    print('you can steal from other players, or grab from table. If you die, you lose top of your stack')
    print('Check https://frozenfractal.com/blog/2015/5/3/how-to-win-at-pickomino/ for more details')
    players = [albert, boris, chris]
    stealList = create_stealList(players)
    number_of_games = int(input(f'Number of games? (For auto players analysis) '))
    add_human()
#    number_of_games = 100
    for i in range(0, number_of_games):
        playerID = random.randint(0, 2)  # random start of player
        i += 1
        for singleplayers in players:
            singleplayers.own_tiles = []
        stealList = create_stealList(players)  # rest stealList
        while check_first_tiles_int(TILES):  # the main loop of the game    
            while True:  # the loop of throwing dice and picking numbers
                fail = False  # at start of throwing, there is no fail yet

                #  dice are thrown here for first time
                thrown = players[playerID].throw_dice(number_of_dice)
                hand = players[playerID].orden_dices_in_dict(thrown)
                print_flathand(hand, playerID)
                # next step, pick a number if possible
                possible_sides = possible_sides_to_pick(hand, free_sides)
                if possible_sides:
                    # dice are thrown, and able to pick a number (or R)
                    if not players[playerID].human:
                        if players[playerID].tactic == 1:
                            pick_one = players[playerID].auto_thief(hand, possible_sides, stealList)
                        elif players[playerID].tactic == 2:
                            pick_one = players[playerID].think_one_step_ahead(hand, possible_sides)
                        else:   
                            pick_one = players[playerID].auto_mx_point(hand, possible_sides)  # max pick
                        free_sides.remove(pick_one)
                        number_of_dice = new_nr_of_dice(hand, pick_one)
                        points = calculate_points(hand, pick_one)
                    else:
                        while True:
                            # routine for human question of picking a side
                            print(f'Possible choices : {possible_sides}')
                            pick_one = input(f'Which one will you pick? :')
                            pick_one = work_with_int_and_string(pick_one)
                            if pick_one in possible_sides_to_pick(hand, free_sides):  # valid choice
                                free_sides.remove(pick_one)
                                number_of_dice = new_nr_of_dice(hand, pick_one)
                                points = calculate_points(hand, pick_one)
                                print(f'Points is {points}')
                                break
                            else:
                                print("Sorry, that isn't possible \n")
                else:
                    fail = True
                    break    
    #  after throwing, and picking a side - calculate score etc
                score = players[playerID].calculate_score(score, points)
                if players[playerID].human:
                    print(f'Score is {score}, dice left = {number_of_dice}, picked sides = {picked_sides(free_sides)} ')
                if is_turn_over(number_of_dice, free_sides): # out of dice or sides
                    # check here if score is high enough
                    if found_the_W(free_sides):
                        if score_high(score, min_tiles_calc(TILES)[0]):
                            fail = False
                        elif steal_possible(score, stealList):
                            fail = False
                        else:
                            fail = True
                        break
                    print('no W found')
                    fail = True
                    break
                rfound = found_the_W(free_sides)
                if rfound:
                    number_of_dice = new_nr_of_dice(hand, pick_one)
                    min_tiles_list = min_tiles_calc(TILES)
                    if score_high(score, min_tiles_list[0]) or steal_possible(score, stealList):
                        if not players[playerID].human:
                            stay_in_turn = strategy_thief()    
                        else:
                            # keep rolling or stop for humans
                            stay_in_turn = stop_rolling_again_question()
    
                    if stay_in_turn:
                        #print('survival prob : ' + str(survival_rate(free_sides, number_of_dice)) + '%')
                        continue
                    else:
                        break
                continue
    
    # here doing the stuff after finishing the turn
            steal = False
            if not fail:
                if steal_possible(score, stealList):
                    print(f'succesful steal {score} from {players[stealList.index(score)].name}\n')
                    steal = True
                    players[stealList.index(score)].own_tiles.remove(score)
                    players[playerID].own_tiles.append(score)   
                else:
                    tilenr = find_tile(TILES, score)
                    TILES.remove(tilenr)
                    players[playerID].own_tiles.append(tilenr)
                    update_stealList(players, stealList)
                    print(f'{players[playerID].name} added {tilenr} on top of his stack\n')
                    
            else:
                print(f'{players[playerID].name} died.\n')
                TILES = remove_last_tile(TILES)
                if players[playerID].own_tiles:
                    tileback = players[playerID].own_tiles.pop(-1)
                    TILES = give_back_tile(tileback, TILES)
                    update_stealList(players, stealList)
    

            print(f'Tiles on the table : {TILES}')
            for each_player in players:
                print(f'{each_player.name} : {each_player.own_tiles}')
            stay_in_turn = True
#            print('\n')
            if players[playerID].human:
                waiting_a_moment = input('<press any key>')
            stealList = update_stealList(players, stealList)
#            Fill turn df
            if fail:
                score = 0
            turndict = {turncol[0] : players[playerID].name, turncol[1] : fail, turncol[2] : rfound,
                        turncol[3] : worms_quantity(score), turncol[4] : steal}
            df = df.append(turndict, ignore_index = True)
            playerID = next_player(players, playerID)
            print(f'Next player will be {players[playerID].name} and his tiles \
are {players[playerID].own_tiles}')
            number_of_dice, free_sides, score = reset_vars()
                        
        overallWinners.append(most_worms(players))    
        TILES, players[playerID].own_tiles, throw_number, turn_number, winnaar = reset_tiles(playerID)
        winner_count(overallWinners, players)
        print('\n\n')
        bool_col =  ['W_found', 'fail', 'steal']
        for bc in bool_col:
            df[bc] = df[bc].astype(bool)
        df.score = df.score.astype(int)
    df2 = df.groupby('playerID').mean()
    print(df2)
    fig, ax = plt.subplots(3,1)
    #ax.plot(df2.index, df2['score'])
    ax[0].bar(df2.index, df2.steal)
    ax[0].set_ylabel('steal')
    ax[1].bar(df2.index, df2.fail)
    ax[1].set_ylabel('fail')
    ax[2].bar(df2.index, df2.score)
    ax[2].set_ylabel('score')
    
    
    ax[2].set_xlabel('player')

    plt.show()