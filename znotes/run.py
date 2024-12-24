from main import *

# app()

# ((neovim + vim) - nvim-tree) * (bash + cli + zsh + edit)


# a - b + c * d + e
# a - b + cd + e
# a - bcd + e
# a - bcde


operators = [')','-', '+', '*', '(']

def get_op_order(op):
    return operators.index(op) if op in operators else -1

def apply_op(sb, sa, op):
    match op:
        case '*': return sa & sb
        case '+': return sa | sb
        case '-': return sa - sb
    raise Exception(f"Unknown operator '{op}'") 

def tokenize(expstr):
    ret = expstr.split(' ')
    return ret

def next_token(tokens):
    if len(tokens) <= 0:
        return None, 0
    t = tokens.pop(0)
    o = get_op_order(t)
    return t, o

def process_expr(expr, val_table):
    highest_op_order = len(operators)-1
    ops = []
    vals = []
    tokens = tokenize(expr)
    last_op_order = 0
    curr_token = tokens.pop(0)
    curr_op_order = get_op_order(curr_token)
    running = True

    while running:
        if len(tokens) + len(ops) <= 0:
            running = False
            continue
        if curr_op_order < 0:
            vals.append(val_table[curr_token])
            curr_token, curr_op_order = next_token(tokens)
            continue
        if curr_op_order >= last_op_order:
            ops.append(curr_token)
            last_op_order = 0 if curr_op_order == highest_op_order else curr_op_order
            curr_token, curr_op_order = next_token(tokens)
            continue
        if curr_op_order < last_op_order:
            if last_op_order < highest_op_order:
                sr = apply_op(vals.pop(), vals.pop(), ops.pop())
                vals.append(sr)
            else:
                ops.pop()
                curr_token, curr_op_order = next_token(tokens)
            last_op_order = get_op_order(ops[-1]) if len(ops) > 0 else 0
            continue

    return vals.pop()


values = {"sa":{"a", "b", "c"}, "sb":{"a", "i"}, "sc":{"e", "f", "g", "c"}}


strexp = "sa * sb + sc - sa"
result = process_expr(strexp, values)
print(f"Result: {result}")
assert result == {'e', 'f', 'g'}

strexp = "sa * sb - sc + sa"
result = process_expr(strexp, values)
print(f"Result: {result}")
assert result == set()

strexp = "sa + sb * sc - sa"
result = process_expr(strexp, values)
print(f"Result: {result}")
assert result == set()

strexp = "sa + sb - sc * sa"
result = process_expr(strexp, values)
print(f"Result: {result}")
assert result == {'a', 'b', 'i'}

strexp = "sa - sa * ( sb + sc )"
result = process_expr(strexp, values)
print(f"Result: {result}")
assert result == {'b'}

strexp = "sc + sa * ( sb + sc * ( sb + sc ) - sa )"
result = process_expr(strexp, values)
print(f"Result: {result}")
# assert result == {'b'}

x = values['sb'] | values['sc']
print(f"sb + sc = {x}")
x = values['sc'] & x
print(f"sc * (sb + sc) = {x}")
x = values['sb'] | x
print(f"(sb + sc * (sb + sc)) = {x}")
x = x - values['sa']
print(f"(sb + sc * (sb + sc) - sa) = {x}")
x = values['sa'] & x
print(f"sa * (sb + sc * (sb + sc) - sa) = {x}")
x = values['sc'] | x
print(f"sc + sa * (sb + sc * (sb + sc) - sa) = {x}")

