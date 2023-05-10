'''
Listens to the state changes of three buttons on Home Assistant dashboard and calls corresponding scripts.
You need to change the absolute paths to where helion scripts is located on your machine in apps.yaml (param1).

'''

import hassapi as hass
import os

class RunHelion(hass.Hass):

   def initialize(self):
      self.turn_off("input_boolean.run_helion")
      self.turn_off("input_boolean.add_event")
      self.turn_off("input_boolean.reset")
      self.turn_off("input_boolean.next_event")
      self.listen_state(self.helion, "input_boolean.run_helion", new = "on")
      self.listen_state(self.event, "input_boolean.add_event", new="on")
      self.listen_state(self.reset, "input_boolean.reset", new="on")
      self.listen_state(self.next, "input_boolean.next_event", new="on")
      os.chdir(os.path.expanduser("~/.homeassistant"))
      os.system("python3 change_ui_cards.py -c")
      self.log("Hello from AppDaemon")
      self.log("You are now ready to run Apps!")

   def helion(self, entity, attribute, old, new, kwargs):
      self.turn_off("input_boolean.run_helion")
      os.chdir(os.path.expanduser("~/.homeassistant"))
      os.system("python3 change_ui_cards.py -d 2")
      self.call_service("input_number/set_value", entity_id="input_number.event_number", value=0)
      order = self.get_state("input_select.order")
      os.chdir(os.path.join(self.args["param1"], "../data/generated_data/validation/scenarios_from_evaluators/"))
      f = open("ha-scenarios.txt", "r")
      input_list = f.readline().rstrip().split(" ")
      enough_tokens = True
      if ((order == "3 grams") and (len(input_list) < 3)):
         enough_tokens = False
      if ((order == "4 grams") and (len(input_list) < 4)):
         enough_tokens = False
      if (enough_tokens == True):
         os.chdir(self.args["param1"])
         event_no = int(float(self.get_state("input_number.event_number")))
         if (order == "3 grams"):
            os.system("python3 helion_predictions.py ../data/generated_data/validation/scenarios_from_evaluators/ha-scenarios.txt  ../data/generated_data/training/training_model/helion.train -o 3 -v ../data/generated_data/training/training_model/helion.vocab")
            os.chdir(os.path.join(self.args["param1"], "../results/helion.train-helion/3gram"))
         else:
            os.system("python3 helion_predictions.py ../data/generated_data/validation/scenarios_from_evaluators/ha-scenarios.txt  ../data/generated_data/training/training_model/helion.train -o 4 -v ../data/generated_data/training/training_model/helion.vocab")
            os.chdir(os.path.join(self.args["param1"], "../results/helion.train-helion/4gram"))
         f = ""
         flavor = self.get_state("input_select.flavor")
         if (flavor == "up"):
            f = open("up.tsv", "r")
         else:
            f = open("down.tsv", "r")
         result_list = f.readline().split("\t")
         try:
            os.chdir(os.path.join(self.args["param1"], "../data/generated_data/validation/scenarios_from_evaluators/"))
            f = open("ha-scenarios.txt", "r")
            input_list = f.readline().replace("<", "\<").replace(">", "\>").strip().split(" ")
            for i in range(len(input_list)):
               token = input_list[i].strip().replace(" ", "")
               os.chdir(self.args["param1"])
               result = os.system("python3 parse_token.py " + token)
               f = open("parsed_token.txt", "r")
               event = ""
               for line in f:
                  ent = line.strip().split(" ")
                  event += ent[0] + " "
                  self.change_state(ent[0], ent[1])
         except:
            pass
         try:
            output_list = result_list[1].replace("><", ">', '<").replace("[", "").replace("]", "").replace("'", "").replace(", ", " ").replace("\n", "").split(" ")
            token = output_list[0]
            os.chdir(self.args["param1"])
            os.system("python3 parse_token.py " + token.replace("<", "\<").replace(">", "\>"))
            f = open("parsed_token.txt", "r")
            event = ""
            for line in f:
               ent = line.strip().split(" ")
               self.change_state(ent[0], ent[1])
               event += ent[0] + " "
            os.chdir(os.path.expanduser("~/.homeassistant"))
            os.system("python3 change_ui_cards.py -a 2 " + event)
            self.call_service("browser_mod/lovelace_reload")
            self.call_service("input_number/increment", entity_id="input_number.event_number")
         except:
            self.call_service("browser_mod/toast", message="Please input tokens!")
      else:
         self.call_service("browser_mod/toast", message="Please input more tokens!")

   def event(self, entity, attribute, old, new, kwargs):
      self.turn_off("input_boolean.add_event")
      os.chdir(os.path.expanduser("~/.homeassistant"))
      os.system("python3 change_ui_cards.py -d 2")
      self.call_service("input_number/set_value", entity_id="input_number.event_number", value=0)
      tokens_to_add = self.get_state("input_text.token").replace("<", "\<").replace(">", "\>").split(" ")
      for i in range(len(tokens_to_add)):
         token_to_add = tokens_to_add[i].replace(" ", "")
         os.chdir(self.args["param1"])
         result = os.system("python3 parse_token.py " + token_to_add)
         if (result != 0):
            self.call_service("browser_mod/toast", message="Please input valid token(s)!")
            break
         os.system("python3 write_to_text_file.py " + token_to_add)
         f = open("parsed_token.txt", "r")
         event = ""
         for line in f:
            ent = line.strip().split(" ")
            event += ent[0] + " "
            self.change_state(ent[0], ent[1])
         os.chdir(os.path.expanduser("~/.homeassistant"))
         os.system("python3 change_ui_cards.py -a 1 " + event)
         self.call_service("browser_mod/lovelace_reload")
         self.call_service("input_text/set_value", entity_id="input_text.token", value="")
         token = self.get_state("input_text.token").replace("<", "").replace(">", "").split(",")
      try:
         os.chdir(os.path.join(self.args["param1"], "../data/generated_data/validation/scenarios_from_evaluators/"))
         f = open("ha-scenarios.txt", "r")
         input_list = f.readline().replace("<", "\<").replace(">", "\>").strip().split(" ")
         for i in range(len(input_list)):
            token = input_list[i].strip().replace(" ", "")
            os.chdir(self.args["param1"])
            result = os.system("python3 parse_token.py " + token)
            f = open("parsed_token.txt", "r")
            event = ""
            for line in f:
               ent = line.strip().split(" ")
               event += ent[0] + " "
               self.change_state(ent[0], ent[1])
      except:
         pass

   def reset(self, entity, attribute, old, new, kwargs):
      self.turn_off("input_boolean.reset")
      os.chdir(os.path.expanduser("~/.homeassistant"))
      os.system("python3 change_ui_cards.py -d")
      os.chdir(self.args["param1"])
      os.system("python3 write_to_text_file.py")
      self.call_service("browser_mod/lovelace_reload")
      self.call_service("input_number/set_value", entity_id="input_number.event_number", value=0)

   def next(self, entity, attribute, old, new, kwargs):
      self.turn_off("input_boolean.next_event")
      event_no = int(float(self.get_state("input_number.event_number")))
      order = self.get_state("input_select.order")
      if (order == "3 grams"):
         os.chdir(os.path.join(self.args["param1"], "../results/helion.train-helion/3gram"))
      else:
         os.chdir(os.path.join(self.args["param1"], "../results/helion.train-helion/4gram"))
      f = ""
      flavor = self.get_state("input_select.flavor")
      if (flavor == "up"):
         f = open("up.tsv", "r")
      else:
         f = open("down.tsv", "r")
      result_list = f.readline().split("\t")
      output_list = result_list[1].replace("><", ">', '<").replace("[", "").replace("]", "").replace("'", "").replace(", ", " ").replace("\n", "").split(" ")
      if ((event_no >= len(output_list))):
         self.call_service("browser_mod/toast", message="You have already executed every event!")
      else:
         token = output_list[event_no]
         while ((token == "</s>") or (token == "<s>")):
            self.call_service("input_number/increment", entity_id="input_number.event_number")
            event_no = int(float(self.get_state("input_number.event_number")))
            if (event_no >= len(output_list)):
               self.call_service("browser_mod/toast", message="You have already executed every event!")
               return
            token = output_list[event_no]
         os.chdir(self.args["param1"])
         result = os.system("python3 parse_token.py " + output_list[event_no].replace("<", "\<").replace(">", "\>"))
         f = open("parsed_token.txt", "r")
         event = ""
         for line in f:
            ent = line.strip().split(" ")
            self.change_state(ent[0], ent[1])
            event += ent[0] + " "
         os.chdir(os.path.expanduser("~/.homeassistant"))
         os.system("python3 change_ui_cards.py -a 2 " + event)
         self.call_service("browser_mod/lovelace_reload")
         self.call_service("input_number/increment", entity_id="input_number.event_number")

   def change_state(self, entity, state):
      if (entity.startswith("switch")):
         if (state == "on"):
            self.turn_on(entity)
         else:
            self.turn_off(entity)

      else:
         self.call_service("input_select/select_option", entity_id=entity, option=state)
