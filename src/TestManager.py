import sys, os, time, logging, unittest
from threading import Thread

sys.path.insert(0, "C:\\Program Files (x86)\\Experitest\\SeeTest9.8\\clients\\Python\\")
from ExperitestClient import Client
from ExperitestClient import Configuration

global run_path
global cwd
global android_device_path
global ios_device_path
global file
global summary_directory
global android_tests
android_tests = ["test_android_login", "test_android_download_app"]
global ios_tests
ios_tests = ["test_ios_login", "test_ios_download_app"]
# defining dictionaries with keys as test_name and values as list[number of success, number of failures]
global android_dict
android_dict = {'test_android_login': [0, 0], 'test_android_download_app': [0, 0]}
global ios_dict
ios_dict = {'test_ios_login': [0, 0], 'test_ios_download_app': [0, 0]}


def update_file():
    global file
    file = open(summary_directory, 'a')
    file.write("results" + "\n")
    file.write("," + "success, failure\n")
    for k in ios_dict:
        file.write(k + ",")
        file.write(str(ios_dict[k][0]) + "," + str(ios_dict[k][1]).replace("none", ""))
        file.write("\n".replace("none", ""))

    for k in android_dict:
        file.write(k + ",")
        file.write(str(android_dict[k][0]) + "," + str(android_dict[k][1]).replace("none", ""))
        file.write("\n".replace("none", ""))

    file.close()


def run_android_tests():
    for i in range(0, android_tests.__len__()):
        method_name = android_tests[i]
        possibles = globals().copy()
        possibles.update(locals())
        method = possibles.get(method_name)
        client = setup_android()
        method(client, method_name)
        teardown(client)


def run_ios_tests():
    for i in range(0, ios_tests.__len__()):
        method_name = ios_tests[i]
        possibles = globals().copy()
        possibles.update(locals())
        method = possibles.get(method_name)
        client = setup_ios()
        method(client, method_name)
        teardown(client)


def create_run_millis_folder():
    date = str(time.ctime(time.time())).replace(" ", "_")
    date = date.replace(":", "-")
    global run_path
    run_path = "run_" + date
    os.makedirs(run_path)
    global cwd
    cwd = os.getcwd()


def create_summary_file():
    global summary_directory
    summary_directory = run_path + "/Results_Summary.csv"
    global file
    file = open(summary_directory, 'a')
    file.write("device,test_name, exception\n")
    file.close()


def create_device_folder(device_name, operating_system):
    print("cwd is: " + cwd)
    new_path = cwd + "/" + run_path
    print("new_path is: " + new_path)
    # os.chdir(new_path)
    device_name = device_name.replace(":", "_")
    if operating_system == "android":
        global android_device_path
        android_device_path = new_path + "/" + device_name
        if not os.path.exists(android_device_path):
            os.makedirs(android_device_path)
    elif operating_system == "ios":
        global ios_device_path
        ios_device_path = new_path + "/" + device_name
        if not os.path.exists(ios_device_path):
            os.makedirs(ios_device_path)
    else:
        print("no os was selected for device")


def setup_android():
    print("running android_test")
    host = "localhost"
    port = 8889
    client = Client()
    client.init(host, port, True)
    client.setProjectBaseDirectory("C:\\Users\\richi.lebovich\\workspace\\project4")
    # client.setReporter2("xml", android_device_path, test_name)
    print("finished setup_android")
    return client


def setup_ios():
    print("running ios_test")
    host = "localhost"
    port = 8890
    client = Client()
    client.init(host, port, True)
    client.setProjectBaseDirectory("C:\\Users\\richi.lebovich\\workspace\\project4")
    # nir = client.setReporter2("xml", ios_device_path, test_name)
    # # fo = open(nir, 'a')
    # data = bytes(nir)
    # print("AAAAAAAAAAAAAAAAARRRRRRRRRRRRRRRRRRR")
    # arr = []
    # mystr = ""
    # for value in data:
    #     arr.append(value)
    #     mystr += chr(value)
    # print(''.join(chr(i) for i in arr))
    # print("mystr is: " + mystr)
    # fo = open(mystr + "\\file.txt", 'a')
    # # go = os.path.join("file.txt", nir)
    # # print("nir['text']: ", nir['text'])
    # print("RPRPPRPRPRPRPRRPRPRPPRRPRPRPRPPR")
    # print(nir)
    return client


def teardown(client):
    # Generates a report of the test case.
    # For more information - https://docs.experitest.com/display/public/SA/Report+Of+Executed+Test
    client.generateReport2(False)
    # Releases the client so that other clients can approach the agent in the near future.
    client.releaseClient()


def test_android_login(client, test_name):
    try:
        # client.setDevice("adb:SM-G930F")
        device_name = client.waitForDevice("@os='android' and @remote = 'false'", 300000)
        create_device_folder(device_name, "android")
        # print("android_device_path is: " + android_device_path)
        # print(test_name)
        client.setReporter2("xml", android_device_path, test_name)
        # var0 = client.waitForDevice("@os='" + os + "' and @remote = 'false'", 300000)
        client.launch("com.experitest.ExperiBank/.LoginActivity", True, False)
        client.elementSendText("NATIVE", "xpath=//*[@hint='Username']", 0, "company")
        client.elementSendText("NATIVE", "xpath=//*[@hint='Password']", 0, "company")
        client.click("NATIVE", "text=Login", 0, 1)
        client.verifyElementFound("NATIVE", "xpath=//*[@text='Make Payment']", 0)
        client.click("NATIVE", "text=Logout", 0, 1)
        global android_dict
        android_dict[test_name][0] += 1
    except Exception:
        global file
        file = open(summary_directory, 'a')
        file.write(device_name + "," + test_name + "," + str(sys.exc_info()[1]).replace(",", "_") + "\n")
        file.close()
        android_dict[test_name][1] += 1


def test_ios_login(client, test_name):
    try:
        # client.setDevice("ios_app:iPhone")
        device_name = client.waitForDevice("@os='ios' and @remote = 'false'", 300000)
        create_device_folder(device_name, "ios")
        client.setReporter2("xml", ios_device_path, test_name)
        # var0 = client.waitForDevice("@os='" + os + "' and @remote = 'false'", 300000)
        client.launch("com.experitest.ExperiBank", True, False)
        client.elementSendText("NATIVEyy", "xpath=//*[@accessibilityLabel='usernameTextField']", 0, "company")
        client.elementSendText("NATIVE", "xpath=//*[@accessibilityLabel='passwordTextField']", 0, "company")
        client.click("NATIVE", "text=Login", 0, 1)
        client.verifyElementFound("NATIVE", "text=Make Payment", 0)
        client.click("NATIVE", "text=Logout", 0, 1)
        client.elementSendText("NATIVE", "xpath=//*[@accessibilityLabel='usernameTextField']", 0, "")
        client.elementSendText("NATIVE", "xpath=//*[@accessibilityLabel='passwordTextField']", 0, "")
        global ios_dict
        ios_dict[test_name][0] += 1

    except Exception:
        global file
        file = open(summary_directory, 'a')
        file.write(device_name + "," + test_name + "," + str(sys.exc_info()[1]).replace(",", "_") + "\n")
        file.close()
        ios_dict[test_name][1] += 1


def test_ios_download_app(client, test_name):
    try:
        device_name = client.waitForDevice("@os='ios' and @remote = 'false'", 300000)
        create_device_folder(device_name, "ios")
        client.setReporter2("xml", ios_device_path, test_name)
        client.setProperty("ios.non-instrumented.dump.parameters", "20,1000,50")
        client.launch("com.apple.AppStore", False, True)
        client.click("NATIVE", "xpath=//*[@text='Search']", 0, 1)
        client.elementSendText("NATIVE", "xpath=//*[@placeholder='Search' and ./parent::*[@placeholder='Search']]", 0,
                               "whatsapp")
        client.click("NATIVE", "xpath=//*[@accessibilityLabel='Search']", 0, 1)
        if (client.waitForElement("NATIVE", "xpath=//*[@text='Download']", 0, 10000)):
            # If statement
            pass
        client.click("NATIVE", "xpath=//*[@text='Download']", 0, 1)
        client.setProperty("ios.elementsendtext.action.fire", "true")
        if (client.waitForElement("NATIVE", "xpath=//*[@text='OPEN']", 0, 150000)):
            # If statement
            pass
        client.verifyElementFound("NATIVE", "xpath=//*[@text='OPEN']", 0)
        if (client.uninstall("net.whatsapp.WhatsApp")):
            # If statement
            pass
        global ios_dict
        ios_dict[test_name][0] += 1

    except Exception:
        global file
        file = open(summary_directory, 'a')
        file.write(device_name + "," + test_name + "," + str(sys.exc_info()[1]).replace(",", "_") + "\n")
        file.close()
        ios_dict[test_name][1] += 1


def test_android_download_app(client, test_name):
    try:
        device_name = client.waitForDevice("@os='android' and @remote='false'", 300000)
        create_device_folder(device_name, "android")
        client.setReporter2("xml", android_device_path, test_name)
        client.launch("com.android.vending/com.google.android.finsky.activities.MainActivity", False, False)
        client.click("NATIVE", "xpath=//*[@id='search_button']", 0, 1)
        client.elementSendText("NATIVE", "xpath=//*[@id='search_box_text_input']", 0, "ebay seller profit calculator")
        client.sendText("{ENTER}")
        client.click("NATIVE", "xpath=//*[@text='eBay Seller Profit Calculator']", 0, 1)
        client.click("NATIVE", "xpath=//*[@text='INSTALL']", 0, 1)
        client.click("NATIVE", "xpath=//*[@text='ACCEPT']", 0, 1)
        if (client.waitForElement("NATIVE", "xpath=//*[@text='OPEN']", 0, 90000)):
            # If statement
            pass
        client.verifyElementFound("NATIVE", "xpath=//*[@text='OPEN']", 0)
        client.click("NATIVE", "xpath=//*[@text='UNINSTALL']", 0, 1)
        client.click("NATIVE", "xpath=//*[@text='OK']", 0, 1)
        global android_dict
        android_dict[test_name][0] += 1

    except Exception:
        global file
        file = open(summary_directory, 'a')
        file.write(device_name + "," + test_name + "," + str(sys.exc_info()[1]).replace(",", "_") + "\n")
        file.close()
        android_dict[test_name][1] += 1


def main():
    create_run_millis_folder()
    create_summary_file()

    times_android = 1
    times_ios = 1

    for x in range(0, times_android):
        # print("We're on time %d" % (x))
        t1 = Thread(target=run_android_tests)
        t1.start()
    for x in range(0, times_ios):
        t2 = Thread(target=run_ios_tests)
        t2.start()

    t1.join()
    t2.join()
    update_file()
    print("main complete")


if __name__ == '__main__':
    main()
