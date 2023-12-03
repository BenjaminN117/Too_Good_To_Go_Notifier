# Too Good To Go Notifier


Get notified when your favourite magic bags become available instantly


## Variables to Change

### Required

|  Data        | Description     | Env Variable Name |
|--------------|-----------|------------|
| Email Address | The email address associated with your Too Good To Go account      | EMAIL_ADDRESS        |
| IFTTT WebHook Key      | The webhook key for your IFTTT account  | IFTTT_KEY       |
| IFTTT WebHook Trigger ID | The webhook trigger ID      | IFTTT_TRIGGER        |

### Advanced

| Data         | Description     | Env Variable Name |
|--------------|-----------|------------|
| Query Time | Change the delay between querying the TGTG API      | QUERY_TIME        |


## Usage

```
docker build -t too-good-to-go-notifier .
```


```
docker run -e EMAIL_ADDRESS='BLANK' -e IFTTT_KEY='BLANK' -e IFTTT_TRIGGER='BLANK'  -it --rm --name tgtgN too-good-to-go-notifier
```

Once the container is running, you need to authorise your Too Good To Go account to be used with the notifier. You will receive an email from Too Good To Go
asking for you to authorise the connection. Additionally you should receive an IFTTT notification informing you of an incoming auth request. If you do receive a request
but not the IFTTT notification, do not accept it as this is most likely not from the notifier.




