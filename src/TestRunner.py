import os
import subprocess
import sys
import time


from Manager import GlobalParamsManager, FilesManager, FailureManager
from Tests import TestsDef
from threading import Thread
sys.path.insert(0, "C:\\Program Files (x86)\\Experitest\\SeeTest9.8\\clients\\Python\\")


def run_android_tests(listoftests):
    for i in range(0, listoftests.__len__()):
        method_name = listoftests[i]
        method = getattr(TestsDef, method_name)
        client = TestsDef.setup_android()
        device_name = client.waitForDevice("@os='android' and @remote = 'false'", 30000)
        method(client, method_name, device_name)
        TestsDef.teardown(client)


def run_ios_tests(listoftests):
    for i in range(0, listoftests.__len__()):
        method_name = listoftests[i]
        method = getattr(TestsDef, method_name)
        client = TestsDef.setup_ios()
        device_name = client.waitForDevice("@os='ios' and @remote = 'false'", 30000)
        print(device_name)
        method(client, method_name, device_name)
        TestsDef.teardown(client)


def main():
    FilesManager.create_run_millis_folder()
    FilesManager.create_summary_file()

    number_of_times = 1
    android_devices_number = 3
    ios_devices_number = 0

    for x in range(0, number_of_times):
        if x > 0:
            FailureManager.activate_failure_mechanism()
        for y in range(0, android_devices_number):
            t1 = Thread(target=run_android_tests(GlobalParamsManager.android_tests))
            print("################starting thread 1#################")
            t1.start()
        for y in range(0, ios_devices_number):
            t2 = Thread(target=run_ios_tests(GlobalParamsManager.ios_tests))
            print("################starting thread 2#################")
            t2.start()
        if android_devices_number != 0:
            t1.join()
        if ios_devices_number != 0:
            t2.join()

    # for x in range(0, ios_devices_number):
    #     t2 = Thread(target=run_ios_tests())
    #     print("################starting thread 12#################")
    #     t2.start()
    #
    # for x in range(0, times_android):
    #     t1 = Thread(target=run_android_tests)
    #     print("################starting thread 1#################")
    #     t1.start()
    #     t1.join()
    # for x in range(0, times_ios):
    #     t2 = Thread(target=run_ios_tests)
    #     print("################starting thread 2#################")
    #     t2.start()
    #     t2.join()
    # if times_android != 0:
    #     t1.join()
    # if times_ios != 0:
    #     t2.join()

    FailureManager.activate_failure_mechanism()

    FailureManager.run_tests_forth_time(GlobalParamsManager.four_times_test_dict, android_devices_number, ios_devices_number)

    t3 = Thread(target=FilesManager.update_file)
    t3.start()
    t3.join()
    # FilesManager.update_file()
    print("main complete")


def foo():
    androidlist = []
    ioslist = []
    mymap = {'android': androidlist, 'ios': ioslist}

    print(mymap)

    androidlist.append("testA")
    androidlist.append("testG")
    print(mymap)
    print(mymap['android'])

    # ioslist.append("testB")
    # print(mymap)
    # ioslist.append("testC")
    # print(mymap)

if __name__ == '__main__':
    main()
    # foo()
