create_profile_success = {
    'createCustomerProfileRequest': {
        'xmlns': 'AnetApi/xml/v1/schema/AnetApiSchema.xsd',
        'profile': {
            'merchantCustomerId': '42',
            'paymentProfiles': {
                'billTo': {
                    'firstName': 'Danielle',
                    'lastName': 'Thompson',
                    'company': '',
                    'address': '101 Broadway Avenue',
                    'city': 'San Diego',
                    'state': 'CA',
                    'zip': '92101',
                    'country': 'US'
                },
                'payment': {
                    'creditCard': {
                        'cardCode': '123',
                        'cardNumber': "5586086832001747",
                        'expirationDate': '2020-05'
                    }
                }
            }
        },
        'merchantAuthentication': {
            'transactionKey': 'key',
            'name': 'loginid',
        },
    }
}


update_profile_success = {
    'updateCustomerPaymentProfileRequest': {
        'xmlns': 'AnetApi/xml/v1/schema/AnetApiSchema.xsd',
        'customerProfileId': '6666',
        'paymentProfile': {
            'customerPaymentProfileId': '7777',
            'billTo': {
                'firstName': 'Danielle',
                'lastName': 'Thompson',
                'company': '',
                'phoneNumber': '',
                'faxNumber': '',
                'address': '101 Broadway Avenue',
                'city': 'San Diego',
                'state': 'CA',
                'zip': '92101',
                'country': 'US'
            },
            'payment': {
                'creditCard': {
                    'cardCode': '123',
                    'cardNumber': "5586086832001747",
                    'expirationDate': '2020-05'
                }
            }
        },
        'merchantAuthentication': {
            'transactionKey': 'key',
            'name': 'loginid',
        },
    }
}


create_payment_profile_success = {
    'createCustomerPaymentProfileRequest': {
        'xmlns': 'AnetApi/xml/v1/schema/AnetApiSchema.xsd',
        'customerProfileId': '6666',
        'paymentProfile': {
            'billTo': {
                'firstName': 'Danielle',
                'lastName': 'Thompson',
                'phoneNumber': '',
                'faxNumber': '',
                'company': '',
                'address': '101 Broadway Avenue',
                'city': 'San Diego',
                'state': 'CA',
                'zip': '92101',
                'country': 'US'
            },
            'payment': {
                'creditCard': {
                    'cardCode': '123',
                    'cardNumber': "5586086832001747",
                    'expirationDate': '2020-05'
                }
            }
        },
        'merchantAuthentication': {
            'transactionKey': 'key',
            'name': 'loginid',
        },
    }
}
