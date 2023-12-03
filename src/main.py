from tgtg import TgtgClient
import sched, time
import requests
import os

class magic_bag_notifier:

    def __init__(self) -> None:
        self.emailAddress = os.environ["EMAIL_ADDRESS"]
        self.iftttKey = os.environ["IFTTT_KEY"]
        self.iftttTrigger = os.environ["IFTTT_TRIGGER"]

    def auth(self):
        
        self.client = TgtgClient(email=self.emailAddress)
        self.client.get_items()
        self.send_request(store_name="AUTH REQUEST", bags_available="")

    def send_request(self, store_name, bags_available):

        r = requests.post(f'https://maker.ifttt.com/trigger/{self.iftttTrigger}/json/with/key/{self.iftttKey}', json={"Store Name": store_name, "Bags Available": bags_available})
        print(r.status_code)

            
    def fetch_bag_status(self, scheduler): 

        scheduler.enter(60, 1, self.fetch_bag_status, (scheduler,))
        items = self.client.get_items()
        for item in items:
            if item["items_available"] < 0:
                print("Notif Sent")
                self.send_request(item["display_name"], item["items_available"])


if __name__ == "__main__":

    inst = magic_bag_notifier()
    
    inst.auth()

    my_scheduler = sched.scheduler(time.time, time.sleep)
    my_scheduler.enter(120, 1, inst.fetch_bag_status, (my_scheduler,))
    my_scheduler.run()