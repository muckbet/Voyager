from Voyager.fbchat_master import fbchat
import googlemaps
# import json
# from source.location import Location

client = googlemaps.Client(key='key')

login = str(input("Enter your Facebook login: "))
password = str(input("Enter your Facebook password: "))

session = fbchat.Session.login(login, password)

# session = fbchat.Session.login("login", "password")

listener = fbchat.Listener.connect(session, chat_on=False, foreground=False)


class Interface:

    @staticmethod
    def choice(event):
        print(f"{event.message.text} from {event.author.id} in {event.thread.id}")
        # If you're not the author, echo
        if event.author.id != session.user.id:
            event.thread.send_text('Enter "1" for: museums and art galleries \n\n'
                                   'Enter "2" for: food establishments \n\n'
                                   'Enter "/end" to stop \n\n'
                                   'Enter "/new" to start again')


    @staticmethod
    def show_interface(event):
        print(f"{event.message.text} from {event.author.id} in {event.thread.id}")
        # If you're not the author, echo
        if event.author.id != session.user.id:
            event.thread.send_text('Hello, I will help you to find something nearby; to start enter "/start"')

    def start_conversation(self, event):
        if event.message.text != "/start" and event.message.text != "/new":
            self.show_interface(event)
        else:
            location.get_location(event)
            listener1 = fbchat.Listener.connect(session, chat_on=False, foreground=False)
            for event in listener1.listen():
                if isinstance(event, fbchat.MessageEvent):
                    coordinates = location.geocode(event)
                    self.choice(event)
                    listener_choice = fbchat.Listener.connect(session, chat_on=False, foreground=False)
                    for event in listener_choice.listen():
                        if isinstance(event, fbchat.MessageEvent):
                            if event.message.text == "/new":
                                self.start_conversation(event)
                            elif event.message.text == "/end":
                                event.thread.send_text("Have a good time! Bye!")
                                break
                            elif event.message.text == "1":
                                places.museums(coordinates)
                                self.choice(event)
                            elif event.message.text == "2":
                                places.food(coordinates)
                                self.choice(event)


class Places:
    @staticmethod
    def food(coordinates):

        k = 0
        food = client.places_nearby(location=coordinates,
                                    language='en-GB',
                                    radius=1500, type="restaurant")

#         with open('food.json', 'w') as f:
#             json.dump(food, f, indent=4, ensure_ascii=False)

        for data in food['results']:
            if k < 10:
                if 'rating' in data:
                    event.thread.send_text(
                        data['name'] + "\n\n" + data['vicinity'] + "\n\nRating: " + str(data['rating']))
                else:
                    event.thread.send_text(data['name'] + "\n  " + data['vicinity'])
                k += 1
            else:
                break

    @staticmethod
    def museums(coordinates):

        k = 0
        museums = client.places_nearby(location=coordinates,
                                       language='en-GB',
                                       radius=1500, type="museum")

#         with open('museums.json', 'w') as f:
#             json.dump(museums, f, indent=4, ensure_ascii=False)

        for data in museums['results']:
            if k < 10:
                if 'rating' in data:
                    event.thread.send_text(
                        data['name'] + "\n\n" + data['vicinity'] + "\n\nRating: " + str(data['rating']))
                else:
                    event.thread.send_text(data['name'] + "\n  " + data['vicinity'])
                k += 1
            else:
                break

    def hotels(self, coordinates):
        pass


class Location:
    @staticmethod
    def get_location(event):
        print(f"{event.message.text} from {event.author.id} in {event.thread.id}")
        # If you're not the author, echo
        if event.author.id != session.user.id:
            event.thread.send_text('Enter your location: "street, city"')

    @staticmethod
    def geocode(event):
        geocode_result = client.geocode(str(event.message.text))
        for data in geocode_result:
            new_dict = data.get("geometry")
        location_dict = new_dict.get("location")
        lat = location_dict["lat"]
        lng = location_dict["lng"]
        return lat, lng

if __name__ == '__main__':
    places = Places()
    location = Location()
    interface = Interface()

    for event in listener.listen():
        if isinstance(event, fbchat.MessageEvent):
            interface.start_conversation(event)

