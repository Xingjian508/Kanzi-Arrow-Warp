# 如何使用：
# Input: 将'0xC1'这种格式的16进制字符串，放在raw.txt里面。点击raw_sample.txt看例子。
# 不要修改coordinates.txt。确定了有507个坐标。不要修改shifts.txt，这个文件应该为空。
# 跑这个程序。shifts.txt将会记录每个点的变化。
# Output: 绘制出一个results.png，根据坐标移动来画图。点击result_sample.png看例子。

import matplotlib.pyplot as plt

def read_coordinates(file_path):
    """Reads all the coordinates from a cleaned file, returning a list of coordinate tuples."""

    with open(file_path, 'r') as file:
        lines = file.readlines()
    given_coordinates = []
    for line in lines:
        x, y = map(float, line.strip('()\n').split(','))
        given_coordinates.append((x, y))
    return given_coordinates

def read_shifts(file_path):
    """Reads all the shifts from a cleaned file, returning a list of shifting tuples."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    given_shifts = []
    for line in lines:
        x, y = map(float, line.strip('()\n').split(','))
        given_shifts.append((x, y))
    return given_shifts

def convert_base16_to_coordinates(file_path):
    """Cleans and converts base 16 numbers to base 10, returning a list of shifting tuples."""
    with open(file_path) as f:
        nums = _clean(f.read().split())
    return [_conversion_helper(*([e[2:] for e in nums[n:n+2]])) for n in range(0, len(nums), 2)]

def _clean(nums: list):
    """Helper method to clean up the base 16 numbers, returning a cleaned list."""
    cleaned_nums = []
    i = 0
    while i < len(nums):
        if len(nums[i]) == 4:
            cleaned_nums.append(nums[i])
        elif len(nums[i]) in {1, 2, 3}:
            if len(nums[i]) + len(nums[i+1]) == 4:
                cleaned_nums.append(nums[i]+nums[i+1])
                i += 1
            else:
                raise Exception("WTF!")
        elif len(nums[i]) in {4, 5, 6, 7}:
            if len(nums[i]) + len(nums[i+1]) == 8:
                cleaned_nums.append((nums[i]+nums[i+1])[:4])
                cleaned_nums.append((nums[i]+nums[i+1])[4:])
                i += 1
            else:
                raise Exception("WTF!")
        elif len(nums[i]) == 8:
            cleaned_nums.append(nums[i][:4])
            cleaned_nums.append(nums[i][4:])
        i += 1
    return cleaned_nums

def _conversion_helper(x: str, y: str):
    """Helper method to convert a tuple of base 16 to base 10, returning a base 10 tuple."""
    return float(_base16_to_base10(x))/4, float(_base16_to_base10(y))/4

def _base16_to_base10(s: str):
    """Helper method to convert base 16 to base 10, returning a base 10 number."""
    base_10 = int(s, 16)

    msb = 1 << (len(s) * 4 - 1)
    if base_10 & msb:
        base_10 -= 1 << (len(s) * 4)

    return base_10

def write_coordinates(content: list, file_path):
    """Writes content's coordinates to the given file path."""
    with open(file_path, 'w') as f:
        for element in content:
            f.write(str(element)+'\n')
        f.close()

def plot_coordinates(given_coordinates, given_shifts, output, with_numbers, original):
    """Plots the coordinates and saves the png."""
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)

    for i, (x, y) in enumerate(given_coordinates):
        if original:
            ax.plot(x, y, 'bo', markersize=MARKER_SIZE)
            ax.text(x, y, _include_numbers(i+1, with_numbers),
                                        color='black', ha='center', va='center', fontsize=FONT_SIZE)

        if i < len(given_shifts):
            shift_x, shift_y = given_coordinates[i]
            shift_x += given_shifts[i][0]
            shift_y += given_shifts[i][1]
            ax.plot(shift_x, shift_y, 'ro', markersize=MARKER_SIZE)
            ax.text(shift_x, shift_y, _include_numbers(i+1, with_numbers),
                                    color='black', ha='center', va='center', fontsize=FONT_SIZE)

    plt.xlim(-ADJUSTMENT, 2*HALF_VAL)
    plt.ylim(-ADJUSTMENT, 2*HALF_VAL)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.gca().invert_yaxis()
    plt.title('Coordinates with Shifts')
    plt.savefig(output)

def rotated_plot_coordinates(given_coordinates, given_shifts, output, with_numbers, original):
    """Plots the coordinates in a rotated manner and saves the png."""
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)

    for i, (x, y) in enumerate(given_coordinates):
        rotated_x, rotated_y = y, -x
        rotated_y += HALF_VAL

        if original:
            ax.plot(rotated_x, rotated_y, 'bo', markersize=MARKER_SIZE)
            ax.text(rotated_x, rotated_y, _include_numbers(i+1, with_numbers),
                                        color='black', ha='center', va='center', fontsize=FONT_SIZE)

        if i < len(given_shifts):
            shift_x, shift_y = given_coordinates[i]
            shift_x += given_shifts[i][0]
            shift_y += given_shifts[i][1]

            rotated_shift_x, rotated_shift_y = shift_y, -shift_x
            rotated_shift_y += HALF_VAL

            ax.plot(rotated_shift_x, rotated_shift_y, 'ro', markersize=MARKER_SIZE)
            ax.text(rotated_shift_x, rotated_shift_y, _include_numbers(i+1, with_numbers),
                                    color='black', ha='center', va='center', fontsize=FONT_SIZE)

    plt.xlim(-ADJUSTMENT, 2*HALF_VAL)
    plt.ylim(-ADJUSTMENT, 2*HALF_VAL)
    plt.gca().invert_yaxis()
    plt.title('Coordinates with Shifts')
    plt.savefig(output)

def _include_numbers(i: int, with_numbers: bool):
    if with_numbers:
        return str(i)
    else:
        return ''

def direct_plot(coordinates_file, shifts_file, output, original, with_numbers=False):
    """Plots the coordinates of base 10."""
    coordinates = read_coordinates(coordinates_file)
    shifts = read_shifts(shifts_file)

    plot_coordinates(coordinates, shifts, output, with_numbers, original)

def base_16_plot(raw_file, coordinates_file, shifts_file, output, original, with_numbers=False):
    """Plots the coordinates of base 16."""
    write_coordinates(convert_base16_to_coordinates(raw_file), shifts_file)

    coordinates = read_coordinates(coordinates_file)
    shifts = read_shifts(shifts_file)

    plot_coordinates(coordinates, shifts, output, with_numbers, original)

# 以下是执行。修改最后两个变量可以达到对应的效果。
if __name__ == "__main__":

    # 编辑以下的参数
    HALF_VAL = 540
    COORDINATES = 'shifts/coordinates.txt'
    SHIFTS = 'shifts/shifts.txt'
    RAW_PATH = 'shifts/raw.txt'
    OUTPUT = 'shifts/result.png'
    ADJUSTMENT = 200
    FIGURE_SIZE = (40, 24)
    MARKER_SIZE = 15
    FONT_SIZE = 6

    base_16_plot(RAW_PATH, COORDINATES, SHIFTS, OUTPUT, original=False, with_numbers=True)
