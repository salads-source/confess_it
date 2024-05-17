<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Install the necessary python libraries and modules
  ```sh
  pip3 install -r requirements.txt
  ```

### Installation

_Follow these steps to be able to start creating custom polls for be sent to the ConfessIt channel._

1. Create an ```.env``` file in the root directory and fill in the following environment variables
    ```ruby

    TELEGRAM_BOT_TOKEN = 'BOT_TOKEN'
    ```
2. Run the main.py file to start the test bot
   ```sh
   py main.py
   ```
3. Alternatively, install the test_package
   ```sh
   py -m pip install --index-url https://test.pypi.org/simple/ --no-deps example-package-salad
   ```
4. Call the main function as such to start the test bot
    ```sh
    from example_package_salad import main

    main.main()
    ```
5. ChannelName = https://t.me/confessit_test
6. Bot Name = https://t.me/confessit_test_bot
