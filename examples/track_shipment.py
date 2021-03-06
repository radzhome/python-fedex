#!/usr/bin/env python
"""
This example shows how to track shipments.
"""
import logging
from example_config import CONFIG_OBJ
from fedex.services.track_service import FedexTrackRequest

# Set this to the INFO level to see the response from Fedex printed in stdout.
logging.basicConfig(level=logging.INFO)

# NOTE: TRACKING IS VERY ERRATIC ON THE TEST SERVERS. YOU MAY NEED TO USE
# PRODUCTION KEYS/PASSWORDS/ACCOUNT #. THE TEST SERVERS OFTEN RETURN A NOT FOUND ERROR.
# WHEN TESTING IN PRODUCTION, GIVE SOME TIME FOR THE TRACKING TO PROPAGATE.


# We're using the FedexConfig object from example_config.py in this dir.
customer_transaction_id = "*** TrackService Request v10 using Python ***"  # Optional transaction_id
track = FedexTrackRequest(CONFIG_OBJ, customer_transaction_id=customer_transaction_id)

# Track by Tracking Number
track.SelectionDetails.PackageIdentifier.Type = 'TRACKING_NUMBER_OR_DOORTAG'
track.SelectionDetails.PackageIdentifier.Value = '781820562774'

# FedEx operating company or delete
del track.SelectionDetails.OperatingCompany

# Can optionally set the TrackingNumberUniqueIdentifier
# del track.SelectionDetails.TrackingNumberUniqueIdentifier

# If you'd like to see some documentation on the ship service WSDL, un-comment
# this line. (Spammy).
#print track.client

# Un-comment this to see your complete, ready-to-send request as it stands
# before it is actually sent. This is useful for seeing what values you can
# change.
#print track.SelectionDetails
#print track.ClientDetail
#print track.TransactionDetail


# Fires off the request, sets the 'response' attribute on the object.
track.send_request()

# See the response printed out.
print track.response
#print rate_request.client.last_received()

# See the request printed out.
#print track.client.last_sent()

# Look through the matches (there should only be one for a tracking number
# query), and show a few details about each shipment.
print "== Results =="
#print track.response
for match in track.response.CompletedTrackDetails[0].TrackDetails:
    print "Tracking #:", match.TrackingNumber
    print "Tracking # UniqueID:", match.TrackingNumberUniqueIdentifier
    print "Status:", match.StatusDetail.Description
    print "Status AncillaryDetails Reason:", match.StatusDetail.AncillaryDetails[-1].Reason
    print "Status AncillaryDetails Description:", match.StatusDetail.AncillaryDetails[-1].ReasonDescription
    print "Commit Message:", match.ServiceCommitMessage
