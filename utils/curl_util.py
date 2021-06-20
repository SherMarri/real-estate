import random
import subprocess
import traceback
from typing import Text, Tuple

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
]


def exec_curl(command: Text) -> Tuple[Text, int]:
    print("Running command:\n%s" % command)
    replace_user_agent = True
    if replace_user_agent:
        command = command.replace(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
            random.choice(USER_AGENTS),
        )
    output, error = "", ""
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output_bytes, error_bytes = p.communicate()
        output = output_bytes.decode("utf8")
        # print("Output: %s" % output)
        if error_bytes:
            error_text = error_bytes.decode("utf8")
            print("When trying to execute command:\n%s" % command)
            print("Received this in stderr:\n%s" % error_text)
    except Exception as e:
        traceback.print_exc()
        error = repr(e)

    if error:
        print("Curl request raised exception")
        print("Response text: %s" % output)
        print("Error: %s" % error)
        return output, 400

    return output, 200
