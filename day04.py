from collections import Counter

def candidates(start_state, end_state):
    l = len(start_state)
    assert l == len(end_state), 'Digit sequences must be of same length.'
    state = next_candidate(parse_state(start_state))
    end_state = prev_candidate(parse_state(end_state))
    while state <= end_state:
        if len(set(state)) < l:
            yield ''.join(str(d) for d in state)
        for i in range(1, l + 1):
            if i == l or (state[-i] < state[-i - 1]):
                state[-i] += 1
                for j in range(-i + 1, 0):
                    state[j] = 0
                break


def parse_state(s):
    return [int(d) for d in s]

def next_candidate(state):
    l = len(state)
    s = state[:]
    for i in range(l - 1):
        if s[i] < s[i + 1]:
            s[i] += 1
            s[i + 1:] = (0 for _ in range(i + 1, l))
    return s

def prev_candidate(state):
    l = len(state)
    s = state[:]
    for i in range(l - 1):
        if s[i] < s[i + 1]:
            s[i + 1:] = (s[i] for _ in range(i + 1, l))
    return s


                         
def level1():
    count = 0
    for i in range(256310, 732736 + 1):
        s = list(str(i))
        count += ((len(set(s)) < len(s)) and sorted(s) == s)
    return count

def _level1():
    c 
    

def level2():
    count = 0
    for i in range(256310, 732736 + 1):
        s = list(str(i))
        reps = Counter(s).values()
        count += ((sorted(s) == s) and (2 in reps))
        
    return count


if __name__ == "__main__":
    # print(f"Solution 1: {level1()}")
    print(f"Solution 2: {level2()}")
