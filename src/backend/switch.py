import re


def seconds_to_hms(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{seconds:04.1f}"


def hms_to_seconds(time_str):
    hours, minutes, seconds = map(float, time_str.split(':'))
    return int(hours * 3600 + minutes * 60 + seconds)


def tuple2int(tuples):
    result_dict = {}

    for tup in tuples:
        result_dict[tup[0]] = tup[1]

    result_list = [result_dict[key] for key in range(max(result_dict) + 1)]

    return result_list


def process_ass_file(input_file_path, output_file_path, data_two):
    print("data_two:",data_two)
    print("data_two.length()",len(data_two))
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    dialogue_pattern = re.compile(r'^Dialogue: (.+)$')
    for i, line in enumerate(content):
        match = dialogue_pattern.match(line)
        if match:
            start_parts = match.group(1).split(',')

            # print("start_parts",start_parts)
            # print(i)
            # 更新 Start
            start_old = hms_to_seconds(start_parts[1])
            print(start_old)
            start_new = data_two[start_old]

            start_parts[1] = seconds_to_hms(start_new)

            # 更新 End
            new_end_seconds = start_new + 8.0
            new_end = seconds_to_hms(new_end_seconds)
            start_parts[2] = new_end

            # 重新组装该行
            content[i] = f"Dialogue: {','.join(start_parts)}\n"
            # print("after", content[i])

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.writelines(content)


def switch(input_ass_path: str, output_ass_path: str, map_tuple: list):
    # Example usage:

    # data_two = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    data_two = map_tuple
    data_two.append((data_two[-1][0] + 1, data_two[-1][1] + 1))  # 不加会后面段错误 out of range
    data_two = tuple2int(data_two)
    process_ass_file(input_ass_path, output_ass_path, data_two)
