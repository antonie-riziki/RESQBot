from datetime import datetime

import keys
import base64


def sys_time():
    ctime = datetime.now().strftime("%Y%m%d%H%M%S")  # convert the current sys time to string using (strftime)
    print(ctime)

    return ctime


def encode_password():

    data_to_encode = keys.business_short_code + keys.lipa_na_mpesa_passkey + str(sys_time())
    # collection of parameters that make the password variable

    encode_data = base64.b64encode(data_to_encode.encode())  # encode the data to a base64 format

    password = encode_data.decode('utf-8')  # change the byte-like to str by decoding
    print(password)

    return password
