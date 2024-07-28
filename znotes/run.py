from main import *

# app()

# ((neovim + vim) - nvim-tree) * (bash + cli + zsh + edit)


# a - b + c * d + e
# a - b + cd + e
# a - bcd + e
# a - bcde


ops = ['-', '+', '*']

def get_op_order(op):
    return ops.index(op)+1 if op in ops else -1

def apply_op(sb, sa, op):
    match op:
        case '*': return sa & sb
        case '+': return sa | sb
        case '-': return sa - sb
    raise Exception(f"Unknown operator '{op}'") 

def tokenize(expstr):
    ret = expstr.split(' ')
    return ret


def process_expr(expr, val_table):
    ops = []
    vals = []
    last_op_order = 0

    tokens = tokenize(expr)
    for t in tokens:
        op_order = get_op_order(t)
        # print(f"processing token: {t} with order: {op_order}")
        if op_order > 0:
            if op_order > last_op_order:
                ops.append(t)
                last_op_order = op_order
            else:
                while op_order <= last_op_order:
                    sr = apply_op(vals.pop(), vals.pop(), ops.pop())
                    vals.append(sr)
                    last_op_order = get_op_order(ops[-1]) if len(ops) > 0 else 0
                ops.append(t)
        elif t in val_table:
            vals.append(val_table[t])
        else:
            raise Exception(f"Unkown token '{t}'")
        print(ops)
        print(vals)

    while len(ops) > 0:
        sr = apply_op(vals.pop(), vals.pop(), ops.pop())
        vals.append(sr)

    return vals.pop()


values = {"sa":{"a", "b", "c"}, "sb":{"a", "i"}, "sc":{"e", "f", "g", "c"}}

# print(((values["sa"] & values["sb"]) | values["sc"]) - values["sa"])

strexp = "sa * sb + sc - sa"
result = process_expr(strexp, values)
print(f"{result}")
assert result == {'e', 'f', 'g'}

# strexp = "sa * sb - sc + sa"
# result = process_expr(strexp, values)
# assert result == {'a', 'b', 'c'}
# print(f"{result}")
#
# strexp = "sa + sb * sc - sa"
# result = process_expr(strexp, values)
# assert result == {'a', 'b', 'i'}
# print(f"{result}")
#
# strexp = "sa + sb - sc * sa"
# result = process_expr(strexp, values)
# assert result == {'a', 'b', 'i'}
# print(f"{result}")
