# print("\033[31mRed\033[0m")     # preset fg colors
# print("\033[44mBlue\033[0m")    # preset bg colors
# print("\033[38;5;82m Hello \033[38;5;198m World ")              # 256 fg colors
# print("\033[40;38;5;82m Hello \033[30;48;5;82m World \033[0m")  # 256 bg colors

for i in range(256):
    print(f"\033[38;5;{i}m {i} \033[0m")      # 256 fg colors
# for i in range(256):
#     print(f"\033[40;38;5;{i}m {i} \033[0m")   # 256 fg colors with black bg
# for i in range(256):
    # print(f"\033[48;5;{i}m {i} \033[0m")      # 256 bg colors
