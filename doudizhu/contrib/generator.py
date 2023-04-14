# encoding=utf8

# 1) Leaflet: from 3 (minimum) to King (maximum);
# 2) Pair: two cards of the same rank, from 3 (smallest) to 2 (largest);
# 3) Three of a Kind: Three cards of the same size;
# 4) Three with one: three and any card, such as 6-6-6-8, compared according to the size of the three, for example, 9-9-9-3 covers 8-8-8-A ;
# 5) Three cards with a pair: three cards and a pair, similar to the side road (Full House) in poker, compared according to the size of the three cards, for example, Q-Q-Q-6-6 overshadows 10-10-10-K-K;
# 6) Straight: at least 5 cards of consecutive sizes (from 3 to A, 2 and King cannot be used), such as 8-9-10-J-Q;
# 7) Connected pairs: at least 3 pairs of consecutive sizes (from 3 to A, 2 and king cannot be used), such as 10-10-J-J-Q-Q-K-K;
# 8) Three-of-a-kind straight: at least two consecutive three-of-a-kind (from 3 to A), e.g. 4-4-4-5-5-5;
# 9) Three-of-a-kind straight: Each three carries an extra single, such as 7-7-7-8-8-8-3-6, although three 2s cannot be used, but can be brought leaflet 2 and king;
# 10) Three-of-a-kind straight: Each triple brings an extra pair, such as 8-8-8-9-9-9-4-4-J-J, although three of 2 cannot be used, but can bring On a pair of 2, singles and a pair on three cards cannot be mixed, for example, 3-3-3-4-4-4-6-7-7 is illegal;
# 11) Bomb: four cards of the same size, the bomb can cover other card types except the rocket, and the big bomb can cover the small bomb;
# 12) Rocket: A pair of kings, this is the biggest combination, which can cover any card type including bombs;
# 13) Four-card routine (four with two): There are two types of cards, a four with two singles, such as 6-6-6-6-8-9, or a four with two pairs, such as J-J-J-J- 9-9-Q-Q, four cards with two cards and four cards with two pairs belong to different card types and cannot overwrite each other;

# ♠ ♡ ♢ ♣
CARDS = '34567890JQKA2'
RULE = {}


def generate_seq(num, seq_db):
    seq = []
    for idx, s in enumerate(seq_db):
        if idx + num > 12:
            break
        seq.append(''.join(seq_db[idx:idx + num]))
    return seq


def generate_seqs(allow_seq, seq_db):
    ret = []
    for size in allow_seq:
        seq = generate_seq(size, seq_db)
        if seq:
            ret.append(seq)
    return ret


def combination(seq, k):
    if k == 0:
        print('error: ', 0)
        return []
    if len(seq) < k:
        print('error: ', seq, k)
        return []
    if k == 1:
        return [[s] for s in seq]
    if len(seq) == k:
        return [seq]
    no_first = combination(seq[1:], k)
    has_first = map(lambda sub: [seq[0]] + sub, combination(seq[1:], k - 1))
    return no_first + list(has_first)


def permutation(seq):
    if len(seq) == 1:
        return [seq]
    perms = []
    for idx, s in enumerate(seq):
        # for m in permutation(seq[0:idx]+seq[idx+1:]):
        #    all.append([s] + m)
        m = map(lambda sub: [s] + sub, permutation(seq[0:idx] + seq[idx + 1:]))
        perms.extend(list(m))
    return perms


def sort_cards(cards):
    c = sorted(cards, key=lambda card: '34567890JQKA2Ww'.find(card))
    return ''.join(c)


def generate():
    RULE['single'] = []
    RULE['pair'] = []
    RULE['trio'] = []
    RULE['bomb'] = []
    for c in CARDS:
        RULE['single'].append(c)
        RULE['pair'].append(c + c)
        RULE['trio'].append(c + c + c)
        RULE['bomb'].append(c + c + c + c)

    # rule['seq_single'] = generateSeq([5, 6, 7, 8, 9, 10, 11, 12], rule['single'])
    # rule['seq_pair'] = generateSeq([3, 4, 5, 6, 7, 8, 9, 10], rule['pair'])
    # rule['seq_trio'] = generateSeq([2, 3, 4, 5, 6], rule['trio'])
    # rule['seq_bomb'] = generateSeq([2, 3, 4, 5], rule['bomb'])

    for num in [5, 6, 7, 8, 9, 10, 11, 12]:
        RULE['seq_single' + str(num)] = generate_seq(num, RULE['single'])
    for num in [3, 4, 5, 6, 7, 8, 9, 10]:
        RULE['seq_pair' + str(num)] = generate_seq(num, RULE['pair'])
    for num in [2, 3, 4, 5, 6]:
        RULE['seq_trio' + str(num)] = generate_seq(num, RULE['trio'])

    RULE['single'].append('w')
    RULE['single'].append('W')
    RULE['rocket'] = ['Ww']

    RULE['trio_single'] = []
    RULE['trio_pair'] = []
    for t in RULE['trio']:
        for s in RULE['single']:
            if s != t[0]:
                RULE['trio_single'].append(sort_cards(t + s))
        for p in RULE['pair']:
            if p[0] != t[0]:
                RULE['trio_pair'].append(sort_cards(t + p))

    # rule['seq_trio_single'] = []
    # rule['seq_trio_pair'] = []
    for num in [2, 3, 4, 5]:
        seq_trio_single = []
        seq_trio_pair = []
        for seq_trio in RULE['seq_trio' + str(num)]:
            seq = RULE['single'].copy()
            for i in range(0, len(seq_trio), 3):
                seq.remove(seq_trio[i])
            for single in combination(seq, len(seq_trio) / 3):
                single = ''.join(single)
                seq_trio_single.append(sort_cards(seq_trio + single))
                if 'w' not in single and 'W' not in single:
                    pair = ''.join([s + s for s in single])
                    seq_trio_pair.append(sort_cards(seq_trio + pair))
        RULE['seq_trio_single' + str(num)] = seq_trio_single
        RULE['seq_trio_pair' + str(num)] = seq_trio_pair

    RULE['bomb_single'] = []
    RULE['bomb_pair'] = []
    for b in RULE['bomb']:
        seq = RULE['single'].copy()
        seq.remove(b[0])
        for comb in combination(seq, 2):
            comb = ''.join(comb)
            RULE['bomb_single'].append(sort_cards(b + comb))
            if 'w' not in comb and 'W' not in comb:
                RULE['bomb_pair'].append(sort_cards(b + comb[0] + comb[0] + comb[1] + comb[1]))

    count = 0
    keys = []
    for name, cards in RULE.items():
        keys.append(name)
        count += len(cards)
        if not isinstance(cards[0], str):
            print(cards)
    keys.sort()
    print(len(keys), keys)
    print(count)


if __name__ == '__main__':
    generate()
    import json

    with open('rule.json', 'w') as out:
        # json.dump(RULE, out, sort_keys=True, indent=4)
        json.dump(RULE, out)
