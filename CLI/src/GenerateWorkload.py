### #!/usr/bin/python3
import argparse
import json
from json.decoder import JSONDecodeError
import requests
import os
from pathlib import Path
from pprint import pprint
import WorkLoadGenerator.WorkLoadGenerator as wlGen


'''
gen-workload -o outFile -l '{"s1": 1, "s2": 0.8, "s4": 0.5}' -min 1 -max 1 -r 100 -i 3 -m 101
gen-workload -o outFile -l '{"s1":1,"s2":0.8,"s4":0.5}' -min 1 -max 1 -r 100 -i 3 -m 101

ingress_list = {"s1": 1, "s2": 0.8, "s4": 0.5}
request_parameters = {"event_number": 100, "request_time_interval_s": 3, "interarrival_mean": 100}
'''


def init_args(parser):
    parser.add_argument('-o', action='store', dest='output_file',
                        help='Output File Name', default='workload.json')
    parser.add_argument('-l', action='store', dest='ingress_list',
                        help='List of possibles ingress services', default='{"s1": 1}')
    parser.add_argument('-min', action='store', dest='selected_ingress_min', type=int,
                        help='MIN Number of selected ingress services from the list', default=1)
    parser.add_argument('-max', action='store', dest='selected_ingress_max', type=int,
                        help='MAX Number of selected ingress services from the list', default=1)
    parser.add_argument('-r', action='store', dest='stop_event', type=int,
                        help='Number of event until the end of simulation', default=100)
    parser.add_argument('-m', action='store', dest='mean_interarrival_time', type=int,
                        help='Mean of Request Interarrival Time', default=101)
    parser.set_defaults(func=run)


def run(args):
    print("Generate Workload")
    try:
        print(args.ingress_list)
        ingress_list = json.loads(args.ingress_list)

        min_max = {"min": args.selected_ingress_min,
                   "max": args.selected_ingress_max
                   }
        params = {"stop_event": args.stop_event,
                  "mean_interarrival_time": args.mean_interarrival_time
                  }

        output_file = args.output_file
        workload = wlGen.get_workload(ingress_list, min_max, params)
        pprint(workload)
        with open(output_file, "w") as f:
            f.write(json.dumps(workload, indent=2))

    except JSONDecodeError as err:
        print("Error: parameters MUST be in json.dumps() format!", err)
        exit()
    except Exception as err:
        print("Error :", err)
        exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    init_args(parser)
    args = parser.parse_args()
    args.func(args)
