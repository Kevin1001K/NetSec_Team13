import requests


url = "https://www-lab.cn.tuwien.ac.at/ns-tuwel/validation/13"
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "iframe",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "referer": "https://www-lab.cn.tuwien.ac.at/ns-tuwel/validation/13",
  }


# Optional: maintain session cookies if "credentials: include" is needed
cookies = {
    'MDL_SSP_AuthToken': '_e1e4525fe195ddfab28bdaf30f0929ab8a2252b342',
    'MDL_SSP_SessID': 'c320c14c6999f098eab60f32875a7b8f',
    'MoodleSessiontuwel': 'op1vtf4h5sivm0s245rs24mous',
    'session': '458cf217-513f-4c78-896d-b7ef27f2148a'
    }
session = requests.Session()

target_string = "Solved!"
expected_count = 3

valid_value_list = []

"""
Checked:
- 0.0 - 100.0
- 70.00 - 100.00
"""
for i in range(1000, 10000):
    index = i/100
    index = "{:.2f}".format(index)
    html_file = f"bruteforce_folder/response_{index}.html"
    index = index + "%"

    data = {
        "rep23b": index,
        "rep23d": index,
        "rep23f": index,
        "validate": "validate"
    }
    response = session.post(url, headers=headers, data=data, cookies=cookies)

    # Print response content
    # print(response.status_code)
    if response.status_code == 200:
        actual_count = response.text.count(target_string)
        print(f"Response: value = {index}, actual = {actual_count}, expected = {expected_count}")
        if actual_count > expected_count:
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(response.text)
            valid_value_list.append(index)
    else:
        print(f"Request failed.")

print(f"Valid Values:")
for valid_value in valid_value_list:
    print(valid_value)