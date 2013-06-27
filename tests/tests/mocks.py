from httmock import urlmatch


cim_url_match = urlmatch(scheme='https', netloc=r'^api\.authorize\.net$',
                         path=r'^/xml/v1/request\.api$')


delete_success = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<{0}>'
    '<messages>'
    '<resultCode>Ok</resultCode>'
    '<message><code>I00001</code><text>Successful.</text></message>'
    '</messages>'
    '</{0}>'
)


customer_profile_success = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<{0}>'
    '<messages>'
    '<resultCode>Ok</resultCode>'
    '<message><code>I00001</code><text>Successful.</text></message>'
    '</messages>'
    '<customerProfileId>6666</customerProfileId>'
    '<customerPaymentProfileIdList>'
    '<numericString>7777</numericString>'
    '</customerPaymentProfileIdList>'
    '<customerShippingAddressIdList />'
    '<validationDirectResponseList />'
    '</{0}>'
)


payment_profile_success = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<{0}>'
    '<messages>'
    '<resultCode>Ok</resultCode>'
    '<message><code>I00001</code><text>Successful.</text></message>'
    '</messages>'
    '<customerProfileId>6666</customerProfileId>'
    '<customerPaymentProfileId>7777</customerPaymentProfileId>'
    '</{0}>'
)
