# allegroOBE - allegroOffersBatchEditing
>python's tool for offers multi-editing in Allegro

![thumbnail](https://raw.githubusercontent.com/bvdzynski/allegroOBE/main/thumbnail.jpg)

## Usage

There is test script in "examples" folder, however here are descriptions for all of functions:

**getAuthToken()**

returns Bearer authentication token for requests

**getHeaders()**

takes 1 argument:
1. requestType - HTTP verb of request ("PUT", "POST", "GET")

prepares headers for request

**getOffersIds()**

returns set of offers ids to work on

can take 3 arguments:
1. limit - maximum number of offers returned in the response
2. offset - index of the first returned offer from all search results
3. offerType - publication status of the offer ("INACTIVE", "ACTIVE", "ACTIVATING", "ENDED")

**refreshDrafts()**

"refreshes" all given drafts in a sequence, by temporary changing the field "name"

it makes two requests:
1. temporary name change
2. return to old name

allegro has a rule - if draft is unchanged, and 2 months old - it is removed automatically, but "timer" is restarted by every edit in draft

**generateDeliveriesDocument()**

generates .csv file of offers with assigned shipping rates

**full documentation of available Allegro rest-api service: https://developer.allegro.pl/en/documentation**
