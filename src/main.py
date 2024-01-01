from tgtg import TgtgClient
import sched, time
import requests
import os

class magic_bag_notifier:

    def __init__(self):
        self.emailAddress = os.environ["EMAIL_ADDRESS"]
        self.iftttKey = os.environ["IFTTT_KEY"]
        self.iftttTrigger = os.environ["IFTTT_TRIGGER"]
        self.knownFavouritesState = {}

    def auth(self):
        
        self.other_info_request(infoType="AUTH REQUEST", message="Please check your email")
        try:
            # Initial token retrieve
            initClient = TgtgClient(email=self.emailAddress)
            # Auth with Refresh and Access tokens
            credentials = initClient.get_credentials()
            self.client = TgtgClient(access_token=credentials["access_token"], refresh_token=credentials["refresh_token"], user_id=credentials["user_id"], cookie=credentials["cookie"])
        except Exception as err:
            print("Auth Error occured")
            self.other_info_request(infoType="AUTH ERROR", message=str(err))
            quit(1)

    def send_request(self, store_name, bags_available):

        r = requests.post(f'https://maker.ifttt.com/trigger/{self.iftttTrigger}/json/with/key/{self.iftttKey}', json={"Store Name": store_name, "Bags Available": bags_available})
        
    def other_info_request(self, infoType, message):

        r = requests.post(f'https://maker.ifttt.com/trigger/{self.iftttTrigger}/json/with/key/{self.iftttKey}', json={infoType: message})
    
    def fetch_bag_status(self, scheduler):
        
        scheduler.enter(60, 1, self.fetch_bag_status, (scheduler,))
        try:
            items = self.client.get_items()
        except requests.exceptions.ConnectionError as connectionError:
            self.other_info_request("Connection Error", str(connectionError))
            return None
        except Exception as otherError:
            self.other_info_request("Query Error", str(otherError))
            return None
        
        for item in items:
                try:
                    if item["items_available"] != self.knownFavouritesState[item["display_name"]]:
                        if item["items_available"] > 0:
                            print("Notif Sent")
                            self.send_request(item["display_name"], item["items_available"])
                            self.knownFavouritesState[item["display_name"]] = item["items_available"]
                    else:
                        print("item has been found but the number hasn't changed")
                except KeyError as err:
                        print("Item not in the dict, adding now")
                        self.knownFavouritesState[item["display_name"]] = item["items_available"]
                        if item["items_available"] > 0:
                            self.send_request(item["display_name"], item["items_available"])
                
if __name__ == "__main__":

    inst = magic_bag_notifier()
    
    inst.auth()
    
    queryDelay = os.environ["QUERY_TIME"] if os.environ.get("QUERY_TIME") is not None else 60

    my_scheduler = sched.scheduler(time.time, time.sleep)
    my_scheduler.enter(queryDelay, 1, inst.fetch_bag_status, (my_scheduler,))
    my_scheduler.run()