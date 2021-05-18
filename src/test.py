from icecream import ic


# def neighbor(l, loc):
#     cur_row = loc[1]
#     cur_col = loc[0]
#     row_size = len(l)
#     col_size = len(l[0])
#     neighbors = list()

#     if cur_row != None and cur_col != None:
#         for r in range(cur_row - 1, cur_row + 2):
#             for c in range(cur_col - 1, cur_col + 2):
#                 if -1 < r < row_size and -1 < c < col_size and not (r == cur_row and c == cur_col):
#                     neighbors.append((c, r))

#     return neighbors


# l = list()

# for row in reversed(range(5)):
#     k = list()
#     for col in range(5):

#         k.append(str((col, row)))
#     l.append(k)

# ic('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in l]))
# # ic(l)

# ic(neighbor(l, (4, 2)))
# ic(neighbor(l, (1, 0)))


l = [[1, 2, 3], [4, 5, 6]]

for i in l:
    ic(i)
