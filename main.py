import sys
from data_check import *

txt_file = sys.argv[1]
# txt_file = 'test_3.txt'
with open(txt_file, 'r') as file:
    data = file.read()
    if syntax_correct(data):
        lines = create_line_dict(data)
        for line in lines.values():
            if not line.check_data():
                print(f'There is no start or end stop for the line: {line.line_nr}.')
                break
        else:
            stops = create_stop_dict(data)
            get_statistics(stops)
        try:
            arrival_time_test(data)
        except TypeError:
            pass
        else:
            get_invalid_stops(create_stop_dict(data))
    else:
        exit(0)
