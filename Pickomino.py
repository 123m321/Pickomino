"""
The game of Pickomino, Regenwormen (NL) or Heckmeck (DE) is played with 8
dice and a lot of tiles.

"""
import random
import pandas as pd
import matplotlib.pyplot as plt

NR_OF_DICE = 8
FREE_SIDES = [1, 2, 3, 4, 5, 'W']
SCORE = 0
TILES = [x for x in range(21, 36)]
TILESoriginal = [x for x in range(21, 36)]
WORMS = [1]*4 + [2] * 4 + [3] * 4 + [4] * 4
TILES.append('X')
throw_number = 1
turn_number = 1
turncol = ['playerID', 'fail', 'W_found', 'SCORE', 'steal']
df = pd.DataFrame(columns=turncol)
playerID = 0
overallWinners = []
stay_in_turn = True
turndict = {}


class player:
    """
    This is my first class I ever used. It's made to create players,
    and currently there are 3 of them. Each with a slightly different 
    strategy.
    """
    def __init__(self, playername):
        self.name = playername
        self.human = False
        self.own_tiles = []
        self.tactic = 0

    def throw_dice(self, NR_OF_DICE):
        """
        Method to throw a number of dice. Only throw as many dice as
        you have left
        """
        self.thrown_dice = []
        for x in range(NR_OF_DICE):
            self.thrown_dice.append(random.randint(1, 6))
        return self.thrown_dice

    def orden_dices_in_dict(self, dicelist):
        """
        The dice thrown are ordered in a dictionary : hand
        """
        self.hand = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 'W': 0}
        for keys in self.hand:
            self.hand[keys] = dicelist.count(keys)
            self.hand['W'] = dicelist.count(6)
        return self.hand

    def calculate_SCORE(self, SCORE, points):
        """
        after throwing dice, and ordering in them, pick a value
        and calculate the new subtotal of thrown numbers : the score
        """
        self.SCORE = SCORE + points
        return self.SCORE

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
        print(f'{players[playerID].name} picks {possible_sides[mx_index]}\
 (score now {SCORE + mx})')
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
                if SCORE + pick == steal:
                    print('yes! steal possible')
                    mx = pick
                    mx_index = mx_pick.index(pick)
                    steal_opp = True
        if not found_the_W(FREE_SIDES):
            steal_opp = False
        if not steal_opp:
            pick_one = players[playerID].think_one_step_ahead(hand, possible_sides)
            return pick_one
        print(f'{players[playerID].name} picks {possible_sides[mx_index]},\
 score now {SCORE+mx}')
        return possible_sides[mx_index]

    def think_one_step_ahead(self, hand, possible_sides):
        mx_pick = []
        for pos_sides in possible_sides:
            mx_pick.append(hand[pos_sides] * pos_sides)
        if isinstance(mx_pick[-1], str):
            worms = mx_pick[-1].count('W')
            del mx_pick[-1]
            mx_pick.append(worms * 5)
        FREE_SIDES2 = FREE_SIDES[:]
        bothsteps = []
        for t in possible_sides:
            step1SCORE = mx_pick[possible_sides.index(t)] + SCORE
            FREE_SIDES2.remove(t)
            dice_left = new_nr_of_dice(hand, t)
            FREE_SIDES2_sum = FREE_SIDES_sum(FREE_SIDES2)
            step2SCORE = dice_left * (FREE_SIDES2_sum / 6)
            FREE_SIDES2.append(t)
            bothsteps.append(step1SCORE + step2SCORE)
        maxstep = max(bothsteps)
        print(f'{players[playerID].name} picks\
 {possible_sides[bothsteps.index(maxstep)]}\
 (score now {SCORE + mx_pick[bothsteps.index(maxstep)]})')
        return possible_sides[bothsteps.index(maxstep)]


def FREE_SIDES_sum(free):
    if 'W' in free:
        free.remove('W')
        free.append(5.01)
        sum_free = sum(free)
        del free[-1]
        free.append('W')
    else:
        sum_free = sum(free)
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


def possible_sides_to_pick(hand, FREE_SIDES):
    thrown_numbers = [key for key in hand if hand[key] > 0]
    return [x for x in thrown_numbers if x in FREE_SIDES]


def calculate_points(hand, pick_one):
    if pick_one != 'W':
        points = pick_one * hand[pick_one]
    elif pick_one == 'W':
        points = 5 * hand[pick_one]
    return points


def found_the_W(FREE_SIDES_of_dice):
    if 'W' not in FREE_SIDES_of_dice:
        return True
    return False


def stop_rolling_again_question():
    """This function asks if human user will throw again"""
    stop_or_not = input('Roll again? (y/n) .. ')
    if stop_or_not.upper() == "N":
        return False
    return True


def survival_rate(FREE_SIDES, dice_left):
    free = len(FREE_SIDES)
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


def pay_off_worms(FREE_SIDES, dice_left, SCORE):
    avg = int(dice_left) * int(sum(FREE_SIDES) / 6)
    top_of_stack = 0
    if players[playerID].own_tiles:
        top_of_stack = players[playerID].own_tiles[-1]
    print(f'now {players[playerID].name} would \
 win {worms_quantity(SCORE)} worms')
    extra_worms = worms_quantity(SCORE+avg) - worms_quantity(SCORE)
    print(f'if he throws again he expects to gain {extra_worms} extra worms')
    print(f'but if he loses, he loses {worms_quantity(top_of_stack)} worms')

    extra_worms_odds = (survival_rate(FREE_SIDES, dice_left) / 100) * extra_worms
    lose_worms_odds = worms_quantity(top_of_stack) * 0.01 * (1 - survival_rate(FREE_SIDES, dice_left))
    print(f'sum is {extra_worms_odds + lose_worms_odds}')
    return extra_worms_odds + lose_worms_odds


def new_nr_of_dice(hand, pick):
    return sum(hand.values()) - hand[pick]


def is_turn_over(NR_OF_DICE_left, FREE_SIDES_left):
    if NR_OF_DICE_left and FREE_SIDES_left:
        return False  # not dead, because dice left and sides left
    return True


def find_tile(tiles, lastSCORE):
    while True:
        if lastSCORE in tiles:
            break
        lastSCORE = lastSCORE - 1
    return lastSCORE


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
    NR_OF_DICE = 8
    FREE_SIDES = [1, 2, 3, 4, 5, 'W']
    SCORE = 0
    return NR_OF_DICE, FREE_SIDES, SCORE


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


def picked_sides(FREE_SIDES):
    taken = [1, 2, 3, 4, 5, 'W']
    picked = [e for e in taken if e not in FREE_SIDES]
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


def SCORE_high(SCORE, min_tiles):
    if SCORE >= min_tiles:
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


def steal_possible(SCORE, stealList):
    if SCORE in stealList:
        if stealList.index(SCORE) != playerID:
            return True
    return False


def strategy_thief():
    if steal_possible(SCORE, stealList):
        print('going to steal!')
        return False
    exp_result = pay_off_worms(FREE_SIDES, NR_OF_DICE, SCORE)
    if exp_result > 0:
        return True
    return False


if __name__ == "__main__":
    albert = player('Albert')
    boris = player('Boris')
    chris = player('Chris')
    albert.tactic = 1
    boris.tactic = 2
    print('Rules. Try to win most worms. Tiles on table have worms,\
  21 - 24 have 1 worm')
    print('25-28 2 worms, 29 - 32 : 3 worms and higher 4 worms.\n')
    print('Start with 8 dice, you need to pick a side to keep it apart.\
  \nYou need a worm too (worth 5 points) - the Worm replaced the 6 on the die')
    print('you can steal from other players, or grab from table. If you die,\
  you lose top of your stack')
    print('Check \
  https://frozenfractal.com/blog/2015/5/3/how-to-win-at-pickomino/ for\
  more details')
    players = [albert, boris, chris]
    stealList = create_stealList(players)
    number_of_games = int(input(f'Number of games? (For AI analysis) : '))
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
                thrown = players[playerID].throw_dice(NR_OF_DICE)
                hand = players[playerID].orden_dices_in_dict(thrown)
                print_flathand(hand, playerID)
                # next step, pick a number if possible
                possible_sides = possible_sides_to_pick(hand, FREE_SIDES)
                if possible_sides:
                    # dice are thrown, and able to pick a number (or R)
                    if not players[playerID].human:
                        if players[playerID].tactic == 1:
                            pick_one = players[playerID].auto_thief(hand, possible_sides, stealList)
                        elif players[playerID].tactic == 2:
                            pick_one = players[playerID].think_one_step_ahead(hand, possible_sides)
                        else:
                            pick_one = players[playerID].auto_mx_point(hand, possible_sides)  # max pick
                        FREE_SIDES.remove(pick_one)
                        NR_OF_DICE = new_nr_of_dice(hand, pick_one)
                        points = calculate_points(hand, pick_one)
                    else:
                        while True:
                            # routine for human question of picking a side
                            print(f'Possible choices : {possible_sides}')
                            pick_one = input(f'Which one will you pick? :')
                            pick_one = work_with_int_and_string(pick_one)
                            if pick_one in possible_sides_to_pick(hand, FREE_SIDES):  # valid choice
                                FREE_SIDES.remove(pick_one)
                                NR_OF_DICE = new_nr_of_dice(hand, pick_one)
                                points = calculate_points(hand, pick_one)
                                print(f'Points is {points}')
                                break
                            else:
                                print("Sorry, that isn't possible \n")
                else:
                    fail = True
                    break
    #  after throwing, and picking a side - calculate SCORE etc
                SCORE = players[playerID].calculate_SCORE(SCORE, points)
                if players[playerID].human:
                    print(f'SCORE is {SCORE}, dice left = {NR_OF_DICE},\
 picked sides = {picked_sides(FREE_SIDES)} ')
                if is_turn_over(NR_OF_DICE, FREE_SIDES):  # no dice/sides
                    # check here if SCORE is high enough
                    if found_the_W(FREE_SIDES):
                        if SCORE_high(SCORE, min_tiles_calc(TILES)[0]):
                            fail = False
                        elif steal_possible(SCORE, stealList):
                            fail = False
                        else:
                            fail = True
                        break
                    print('no W found')
                    fail = True
                    break
                rfound = found_the_W(FREE_SIDES)
                if rfound:
                    NR_OF_DICE = new_nr_of_dice(hand, pick_one)
                    min_tiles_list = min_tiles_calc(TILES)
                    if SCORE_high(SCORE, min_tiles_list[0]) \
                        or steal_possible(SCORE, stealList):
                        if not players[playerID].human:
                            stay_in_turn = strategy_thief()
                        else:
                            # keep rolling or stop for humans
                            stay_in_turn = stop_rolling_again_question()
                    if stay_in_turn:
                        continue
                    else:
                        break
                continue

    # here doing the stuff after finishing the turn
            steal = False
            if not fail:
                if steal_possible(SCORE, stealList):
                    print(f'succesful steal {SCORE} from\
 {players[stealList.index(SCORE)].name}\n')
                    steal = True
                    players[stealList.index(SCORE)].own_tiles.remove(SCORE)
                    players[playerID].own_tiles.append(SCORE)
                else:
                    tilenr = find_tile(TILES, SCORE)
                    TILES.remove(tilenr)
                    players[playerID].own_tiles.append(tilenr)
                    update_stealList(players, stealList)
                    print(f'{players[playerID].name} added {tilenr}\
 on top of his stack\n')

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
            if players[playerID].human:
                waiting_a_moment = input('<press any key>')
            stealList = update_stealList(players, stealList)
#            Fill turn df
            if fail:
                SCORE = 0
            turndict = {turncol[0]: players[playerID].name, turncol[1]: fail,
                        turncol[2]: rfound, turncol[3]: worms_quantity(SCORE),
                        turncol[4]: steal}
            df = df.append(turndict, ignore_index=True)
            playerID = next_player(players, playerID)
            print(f'Next player will be {players[playerID].name} and his tiles\
 are {players[playerID].own_tiles}')
            NR_OF_DICE, FREE_SIDES, SCORE = reset_vars()

        overallWinners.append(most_worms(players))
        TILES, players[playerID].own_tiles, throw_number, turn_number,\
            winnaar = reset_tiles(playerID)
        winner_count(overallWinners, players)
        print('\n')
        bool_col = ['W_found', 'fail', 'steal']
        for bc in bool_col:
            df[bc] = df[bc].astype(bool)
        df.SCORE = df.SCORE.astype(int)
    df2 = df.groupby('playerID').mean()
    print(df2)
    fig, ax = plt.subplots(3, 1)
    ax[0].bar(df2.index, df2.steal)
    ax[0].set_ylabel('steal')
    ax[1].bar(df2.index, df2.fail)
    ax[1].set_ylabel('fail')
    ax[2].bar(df2.index, df2.SCORE)
    ax[2].set_ylabel('SCORE')
    ax[2].set_xlabel('player')
    plt.show()
