
# Database Check
This program takes in a JSON-like file which is a representation of a bus company database. The file contains an array of JSON objects representing bus line stops. The data contains different kinds of errors, including wrong type, wrong format and logical errors in the schemes of bus lines. The program finds all the mistakes in the database and print the output. 

**Output format**
- Format validation: syntax check
- Key Stops: (Start stops, Transfer stops, Finish stops) 
- Arrival time test (check that arrival times for the upcoming stops make sense: they are supposed to be increasing)
- On demand stops test (on-demand stops cannot be initial, final, or transfer stops)

### Sample usage
The greater-than symbol followed by a space (> ) represents the user input from the command-line. \
**Example 1: File with correct syntax:**
```
> python main.py test_2.txt
Format validation: 0 errors
stop_name: 0
stop_type: 0
a_time: 0
Start stops: 3 ['Bourbon Street', 'Pilotow Street', 'Prospekt Avenue']
Transfer stops: 3 ['Elm Street', 'Sesame Street', 'Sunset Boulevard']
Finish stops: 2 ['Sesame Street', 'Sunset Boulevard']
Arrival time test:
OK
On demand stops test:
Wrong stop type: ['Elm Street', 'Sunset Boulevard']
```
**Example 2: File with incorrect syntax:**
```
python main.py test_3.txt
Format validation: 5 errors
stop_name: 2
stop_type: 0
a_time: 1
bus_id: 1
stop_id: 1
```
**Example 3: File with correct syntax, incorrect arrival times:**
```
python main.py test_1.txt
Format validation: 0 errors
stop_name: 0
stop_type: 0
a_time: 0
Start stops: 1 ['Bourbon Street']
Transfer stops: 0 []
Finish stops: 1 ['Sunset Boulevard']
Arrival time test:
bus_id line 512: wrong time on station Sunset Boulevard
On demand stops test:
OK
```
```
Format validation: 0 errors
stop_name: 0
stop_type: 0
a_time: 0
Start stops: 3 ['Bourbon Street', 'Pilotow Street', 'Prospekt Avenue']
Transfer stops: 3 ['Elm Street', 'Sesame Street', 'Sunset Boulevard']
Finish stops: 2 ['Sesame Street', 'Sunset Boulevard']
Arrival time test:
bus_id line 128: wrong time on station Sesame Street
bus_id line 256: wrong time on station Sesame Street
On demand stops test:
Wrong stop type: ['Elm Street', 'Sunset Boulevard']
```

**Sample file**
```
[
    {
        "bus_id": 128,
        "stop_id": 1,
        "stop_name": "Prospekt Avenue",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": "08:12"
    },
    {
        "bus_id": 128,
        "stop_id": 3,
        "stop_name": "Elm Street",
        "next_stop": 5,
        "stop_type": "",
        "a_time": "08:19"
    },
    {
        "bus_id": 128,
        "stop_id": 5,
        "stop_name": "Fifth Avenue",
        "next_stop": 7,
        "stop_type": "O",
        "a_time": "08:25"
    },
    {
        "bus_id": 128,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:37"
    },
    {
        "bus_id": 512,
        "stop_id": 4,
        "stop_name": "Bourbon Street",
        "next_stop": 6,
        "stop_type": "",
        "a_time": "08:13"
    },
    {
        "bus_id": 512,
        "stop_id": 6,
        "stop_name": "Sunset Boulevard",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:16"
    }
]
```