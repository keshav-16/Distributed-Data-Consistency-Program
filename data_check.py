import re
import json
from datetime import datetime
from typing import Dict, List


class TimetableUnit:
    def __init__(self, info: dict):
        self.bus_id: bool = type(info["bus_id"]) is int
        self.stop_id: bool = type(info["stop_id"]) is int
        self.stop_name = (
            lambda s: True if re.match(r'^[A-Z][A-Za-z ]+ (Road|Town|Nagar|Street)$', s) is not None else False)(
            info["stop_name"])
        self.next_stop: bool = type(info["next_stop"]) is int and info["next_stop"] is not None
        self.stop_type = (lambda s: True if re.match(r'^[SOF]$|^$', s) is not None else False)(info["stop_type"])
        self.a_time = (lambda s: True if re.match(r'^(0[1-9]|1[0-9]|2[0-3]):[0-5][0-9]$', s) is not None else False)(
            info["a_time"])


def sum_errors(string):
    table_of_errors = {"stop_name": 0,
                       "stop_type": 0,
                       "a_time": 0}
    for unit in json.loads(string):
        new_part = TimetableUnit(unit)
        for key, value in new_part.__dict__.items():
            if value is False:
                try:
                    table_of_errors[key] += 1
                except KeyError:
                    table_of_errors[key] = 1
    return table_of_errors


def syntax_correct(string) -> bool:
    sum_of_errors = sum(sum_errors(string).values())
    print(f'Format validation: {sum_of_errors} errors')
    for key, value in sum_errors(string).items():
        print(f'{key}: {value}')
    return sum_of_errors == 0


class BusStop:
    def __init__(self, info: dict):
        self.lines = []
        self.lines.append(info["bus_id"])
        self.stop_id = info["stop_id"]
        self.stop_name = info["stop_name"]
        self.is_start = info["stop_type"] == 'S'
        self.is_finnish = info["stop_type"] == 'F'
        self.is_on_demand = info["stop_type"] == 'O'

    def update(self, other):
        self.lines += other.lines
        self.is_start = self.is_start or other.is_start
        self.is_finnish = self.is_finnish or other.is_finnish
        self.is_on_demand = self.is_on_demand or other.is_on_demand


class Stop:
    def __init__(self, id, name, time, next_stop):
        self.id = id
        self.name = name
        self.time = time
        self.next_stop = next_stop


class BusLine:
    def __init__(self, info: dict):
        self.line_nr = info["bus_id"]
        self.start = info["stop_id"] if info["stop_type"] == 'S' else ''
        self.finnish = info["stop_id"] if info["stop_type"] == 'F' else ''
        self.num_of_stops = 1
        self.stops = {}
        self.stops.update({info["stop_id"]: Stop(info["stop_id"], info["stop_name"],
                                                 datetime.strptime(info["a_time"], '%H:%M'), info["next_stop"])})

    def udpate_line(self, other: dict):
        if self.start == '' and other["stop_type"] == 'S':
            self.start = other["stop_id"]
        if self.finnish == '' and other["stop_type"] == 'F':
            self.finnish = other["stop_id"]
        self.num_of_stops += 1
        self.stops.update({other["stop_id"]: Stop(other["stop_id"],
                                                  other["stop_name"], datetime.strptime(other["a_time"], '%H:%M'),
                                                  other["next_stop"])})

    def show_all(self):
        for key, value in self.__dict__.items():
            print(key, value)

    def check_data(self):
        return self.start != '' and self.finnish != ''


def create_stop_dict(string):
    stops = {}
    for unit in json.loads(string):
        new_part = BusStop(unit)
        if new_part.stop_name in stops:
            stops[new_part.stop_name].update(new_part)
        else:
            stops[new_part.stop_name] = new_part
    return stops


def create_line_dict(string):
    lines = {}
    for unit in json.loads(string):
        new_part = BusLine(unit)
        if new_part.line_nr in lines:
            lines[new_part.line_nr].udpate_line(unit)
        else:
            lines[new_part.line_nr] = new_part
    return lines


def get_statistics(BusStop_dict: Dict[str, BusStop]):
    table = {
        "Start stops": [], "Transfer stops": [], "Finish stops": []
    }
    for name, stop in BusStop_dict.items():
        if stop.is_start:
            table["Start stops"].append(name)
        if stop.is_finnish:
            table["Finish stops"].append(name)
        if len(stop.lines) > 1:
            table["Transfer stops"].append(name)

    for key, content in table.items():
        print(f'{key}: {len(content)} {sorted(content)}')


def get_invalid_stops(BusStop_dict: Dict[str, BusStop]):
    print('On demand stops test:')
    errors = 0
    wrong_stop_type = []
    for name, stop in BusStop_dict.items():
        if (stop.is_start or stop.is_finnish or len(stop.lines) > 1) and stop.is_on_demand:
            wrong_stop_type.append(stop.stop_name)
            errors += 1
    if errors > 0:
        print(f'Wrong stop type: {sorted(wrong_stop_type)}')
    else:
        print("OK")


def arrival_time_test(string):
    print('Arrival time test:')
    errors = 0
    bus_lines = create_line_dict(string)
    for nr, line in bus_lines.items():
        prev_stop = line.stops[line.start]
        current_stop = line.stops[line.stops[line.start].next_stop]
        while current_stop != line.finnish:
            if current_stop.time < prev_stop.time:
                errors += 1
                print(f'bus_id line {nr}: wrong time on station {current_stop.name}')
                break
            try:
                prev_stop = current_stop
                current_stop = line.stops[current_stop.next_stop]
            except KeyError:
                break
    if not errors:
        print("OK")
