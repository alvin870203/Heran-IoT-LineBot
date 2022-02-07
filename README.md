# "LINE BOT" 結合 "禾聯物聯網智慧家電" 解決方案



## Deploy the Heran-IoT-LineBot app

### Step 1

Create a new channel on the [LINE Developers Console](https://developers.line.biz/console/) and get the channel secret and channel access token. Add the LINE Official Account associated with your bot as a friend by scanning the QR code on the **Messaging API** tab.

### Step 2

Clone the [Heran-IoT-LineBot](https://github.com/alvin870203/Heran-IoT-LineBot) GitHub repository onto your local machine.

### Step 3

Create a new Heroku app from the [Heroku dashboard](https://dashboard.heroku.com/) and copy the app name.

### Step 4

Go to your Heran-IoT-LineBot directory and add a Git™ remote. Note: {HEROKU_APP_NAME} is the app name from step 3.

```sh
$ heroku git:remote -a {HEROKU_APP_NAME}
```

### Step 5

Push changes to Heroku.
```sh
$ git add .
$ git commit -m 'First commit'
$ git push heroku master
```

### Step 6

Enter the webhook URL in the [LINE Developers Console](https://developers.line.biz/console/) using this URL format: ```https://{HEROKU_APP_NAME}.herokuapp.com/callback```.
