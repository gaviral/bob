import os

from Bob import Bob

# Initialize Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Globals for thread communication.


if __name__ == '__main__':
    bob = Bob()


# TODO:
# - [ ] app window to show up in the right half of the screen
