import sys
import os

sys.path.append(os.path.abspath("allegroOBE"))

import allegroOBE

if __name__ == "__main__":

    print("WELCOME TO allegroOBE...")

    clientId = input("YOUR clientId: ")
    clientSecret = input("YOUR clientSecret: ")

    aOBE = allegroOBE.allegroOBE(clientId, clientSecret)
    # ...
    pass