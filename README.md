# Yosemite reservation snagger

## Usage
1. Install requirements
```sh
$ python3 -m pip install -r requirements.txt
```
2. Run program
```sh
$ python3 snag_yosemite_reservation.py --date="Monday, August 16, 2021"
```

## Example
```sh
$ python3 snag_yosemite_reservation.py --date="Monday, August 16, 2021" 
NO - reservations not available :(
$ python3 snag_yosemite_reservation.py --date="Monday, August 23, 2021"
YES - reservations available :)
```

## Running as a server
```sh
python snag_yosemite_reservation.py --server
```
Runs on port http port 80
