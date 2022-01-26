import re
from collections import defaultdict, Counter

def filter_words(words, include, exclude, fixed):
    matching = []
    for word in words:
        include_fail = False
        for let in include:
            if let not in word:
                include_fail = True
                break
            else:
                for i in include[let]:
                    if word[i] == let:
                        include_fail = True
                        break
        if include_fail:
            continue
        exclude_fail = False
        for let in exclude:
            if let in word:
                exclude_fail = True
                continue
        if exclude_fail:
            continue
        fixed_fail = False
        for i, let in enumerate(fixed):
            if not re.match(r'[A-Z]',let.upper()):
                continue
            else:
                if word[i] != let:
                    fixed_fail = True
                    break
        if fixed_fail:
            continue
        matching.append(word)
    return matching

def get_words():
    words = []
    with open('/usr/share/dict/words') as f:
        for l in f:
            word = l.strip()
            word = word.upper()
            if len(word) != 5:
                continue
            if not re.match(r'[A-Z]*$', word):
                continue
            words.append(word)
    return words

def letter_frequency(words):
    freq = defaultdict(lambda: 0)
    counts = Counter()
    for word in words:
        counts.update(word)
    total = counts.total()
    for let in counts:
        freq[let] = counts[let]/total
    return freq

def rank_words(words, let_freq):
    scored = []
    for word in words:
        score = sum([let_freq[let] for let in word])
        scored.append((score, word))
    scored.sort(reverse=True)
    return [_[1] for _ in scored]
    

if __name__ == '__main__':
    import re
    from argparse import ArgumentParser
    
    parser = ArgumentParser()
    parser.add_argument('-i','--include',
        default='',
        help='Letters to include, and positions they are not in. Format A24,B0',
    )
    parser.add_argument('-e','--exclude',
        default='',
        help='letters to exclude',
    )
    parser.add_argument('-f','--fixed',
        default='',
        help='letters with fixed positions. Must be 5 letters long. Use _ for unknown letters',
    )
    args = parser.parse_args()

    words = get_words()
    let_freq = letter_frequency(words)

    include = {}
    if args.include:
        for tok in args.include.split(','):
            let = tok[0].upper()
            positions = {int(_) for _ in tok[1:]}
            include[let] = positions        
    
    
    match_words = filter_words(words, include, args.exclude.upper(), args.fixed.upper())
    print('\n'.join(match_words))
    #ranked_words = rank_words(match_words, let_freq)
    #print('\n'.join(ranked_words))
    
