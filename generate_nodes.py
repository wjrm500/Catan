import numpy as np

def find_nearest_square_above(n):
    while n > 0:
        n_sqrt = np.sqrt(n)
        if n_sqrt == int(n_sqrt):
            return n
        n += 1

def is_hexagonal_num(n):
    hexagonal_num, hexagonal_nums = 1, []
    for i in range(10):
        hexagonal_num += i * 6
        hexagonal_nums.append(hexagonal_num)
    return n in hexagonal_nums

a = input('How many hexes would you like, including the desert hex? (Hexagonal numbers only)\n')
a = int(a)

if not is_hexagonal_num(a):
    print('Input is not a hexagonal number')
    exit()
sqr_above = find_nearest_square_above(a)
hex_limit_1d = int(np.sqrt(sqr_above))
num_horizonts = hex_limit_1d * 2 + 1
generated_horizonts = []
external_offset, internal_offset = 0.5, 1
for _ in range(num_horizonts):
    x_pos = external_offset
    generated_horizont = [x_pos]
    for _ in range(hex_limit_1d):
        x_pos += internal_offset
        generated_horizont.append(x_pos)
        internal_offset = 1 if internal_offset == 2 else 2
    external_offset = 0.5 if external_offset == 0 else 0
    generated_horizonts.append(generated_horizont)

updated_generated_horizonts = []
for idx, generated_horizont in enumerate(generated_horizonts):
    dist_from_end = min(idx + 1, num_horizonts - idx)
    # print(dist_from_end)
    updated_generated_horizont = generated_horizont
    num_nodes_kept = dist_from_end * 2
    while len(generated_horizont) > num_nodes_kept:
        updated_generated_horizont = updated_generated_horizont[1:-1]
    updated_generated_horizonts.append(updated_generated_horizont)

# print(generated_horizonts)
print(updated_generated_horizonts)

### Two different approaches
### Allow only hexagonal numbers - try first
### Grow organically from central hex - better but more difficult