"""
local settings for unittest
"""


DEBUG = True
TEST = False


DATABASES = {
    'default': {
        'ENGINE': 'postgres',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
        'PORT': 5432
    }
}


NONEXISTENT_SETTING = (
    'Only for case '
    '"tests.unittest.conf.test_settings::SettingsTestCases::test_clean_when_resetup"'
)


THRESHOLD = 60
PI = 3.1415927


HTTP_SERVICE = 'https://httpbin.org/'


EMAILS = [
    'mock@demoemail.com',
    'fake@demoemail.com'
]
