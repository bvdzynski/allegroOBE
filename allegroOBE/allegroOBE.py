import json
import time
import webbrowser
import re
import base64
import csv
import requests
import os.path


class allegroOBE:
    def __init__(self, clientId, clientSecret):
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.authToken = self.getAuthToken()

        if self.authToken != False:
            print("AUTH TOKEN GENERATED!\n")
        else:
            print("YOU HAVE TO GENERATE AUTH TOKEN FIRST!\n")

    def getAuthToken(self):
        ###########STEP 1 - GET LINK TO ALLEGRO AUTHENTICATION AND LOG IN###########

        # generate Basic token
        decodedBasic = str(self.clientId) + ":" + str(self.clientSecret)
        encodedBasic = str(base64.b64encode(decodedBasic.encode("utf-8"), "utf-8"))

        # setup request
        address = "https://allegro.pl/auth/oauth/device"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic " + str(encodedBasic),
        }
        data = {"client_id": str(self.clientId)}

        # execute request
        response = requests.post(address, data=data, headers=headers)

        # check if ok
        if response.status_code == 400:
            print("Error occurred, status code: " + str(response.status_code) + "...")
            return False

        # response to dict
        response = json.loads(response.text)

        if "error" in response:
            print("Error occurred: " + str(response["error_description"]))
            return False

        print("\nSTEP 1, STATUS: OK\nLOG IN YOUR ACCOUNT...")

        # log in link
        if webbrowser.get():
            webbrowser.open_new_tab(response["verification_uri_complete"])
        else:
            print("USE THIS LINK: " + response["verification_uri_complete"])

        ###########STEP 2 - WAITING FOR CONFIRMATION FROM ALLEGRO###########
        print("\nSTEP 2:")

        # waiting for confirmation
        while True:
            # execute request
            response = requests.post(
                "https://allegro.pl/auth/oauth/token?grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Adevice_code&device_code="
                + str(response["device_code"]), 
                headers="Authorization": "Basic "
                + str(encodedBasic)
            )
            print("WAITING FOR LOG IN... CURRENT STATUS: " + str(response.status_code))
            if response.status_code == 200:
                break
            time.sleep(3)

        response = json.loads(response.text)
        return str(response["access_token"])

    def getHeaders(self, requestType):
        headers = {"Accept": "application/vnd.allegro.public.v1+json"}
        if requestType == "PUT" or requestType == "POST":
            headers["content-type"] = "application/vnd.allegro.public.v1+json"
        headers["Authorization"] = "Bearer " + str(self.authToken)
        return headers

    def getOffersIds(self, limit=1000, offset=0, offerType=None):
        publicationStatuses = {"ACTIVE", "INACTIVE", "ACTIVATING", "ENDED"}

        offersIds = set()  # initiating an empty set

        # offerType filter turn on?
        if offerType != None:
            publicationStatuses = {offerType}

        for status in publicationStatuses:
            request = requests.get(
                "https://api.allegro.pl/sale/offers?publication.status="
                + str(status)
                + "&limit="
                + str(limit)
                + "&offset="
                + str(offset),
                headers=self.getHeaders("GET"),
            )

            request = json.loads(request.text)

            for offer in request["offers"]:
                offersIds.add(offer["id"])

        print("\nNumber of offers overall: " + str(len(offersIds)))
        return offersIds  # return python's set w/ offers ID's

    def refreshDrafts(self, draftsIds):
        # [#1] download the entire offer
        # [#2] then update the choosen fields
        # [#3] send the entire offer back

        draftNumberOf = 0

        for id in draftsIds:
            draftNumberOf += 1
            print(
                "refreshing draft, id: "
                + id
                + " ("
                + str(draftNumberOf)
                + "/"
                + str(len(draftsIds))
                + ")"
            )

            # [#1]
            draft = requests.get(
                "https://api.allegro.pl/sale/offers/" + str(id),
                headers=self.getHeaders("GET"),
            )

            draft = json.loads(draft.text)

            # [#2]
            originalName = draft["name"]

            draft["name"] = "to change"

            response = requests.put(
                "https://api.allegro.pl/sale/offers/" + str(id),
                headers=self.getHeaders("POST"),
                data=json.dumps(draft),
            )

            # check if ok
            if response.status_code == 400:
                print(
                    "Error occurred, status code: " + str(response.status_code) + "..."
                )
            else:
                print(
                    "Request successful, status code: "
                    + str(response.status_code)
                    + "..."
                )

            # [#3]
            draft["name"] = originalName

            response = requests.put(
                "https://api.allegro.pl/sale/offers/" + str(id),
                headers=self.getHeaders("POST"),
                data=json.dumps(draft),
            )

            # check if ok
            if response.status_code == 400:
                print(
                    "Error occurred, status code: " + str(response.status_code) + "..."
                )
            else:
                print(
                    "Request successful, status code: "
                    + str(response.status_code)
                    + "..."
                )

    def generateDeliveriesDocument(self, offersIds):

        shippingRates = requests.get(
            "https://api.allegro.pl/sale/shipping-rates", headers=self.getHeaders("GET")
        )
        shippingRates = json.loads(shippingRates.text)

        if not os.path.exists("docs/allegro_shippingRates.csv"):
            f = open("docs/allegro_shippingRates.csv", "w+")
            f.close()

        with open("docs/allegro_shippingRates.csv", "w") as csvfile:
            filewriter = csv.writer(
                csvfile, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )

            filewriter.writerow(
                ["offer_id", "external", "category", "offer_name", "shipping_rate_name"]
            )

            counter = 0
            for id in offersIds:
                counter += 1
                print(
                    "getting shipping rates for offer, id: "
                    + id
                    + " ("
                    + str(counter)
                    + "/"
                    + str(len(offersIds))
                    + ")"
                )

                offer = requests.get(
                    "https://api.allegro.pl/sale/offers/" + str(id),
                    headers=self.getHeaders("GET"),
                )
                offer = json.loads(offer.text)

                for shippingRate in shippingRates["shippingRates"]:
                    if offer["delivery"]["shippingRates"] is not None:
                        if (
                            shippingRate["id"]
                            == offer["delivery"]["shippingRates"]["id"]
                        ):
                            filewriter.writerow(
                                [
                                    offer["id"],
                                    offer["external"]["id"],
                                    offer["name"][-2:],
                                    offer["name"].replace(",", "."),
                                    shippingRate["name"].replace(",", "-"),
                                ]
                            )
                    else:
                        filewriter.writerow([offer["id"], "0", "0", "0", "0"])
