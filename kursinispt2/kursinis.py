from abc import ABC, abstractmethod
from datetime import datetime

class Account(ABC):

    def __init__(self, first_name, last_name, username, join_date):
        self._first_name = first_name
        self._last_name = last_name
        self._username = username
        self._join_date = join_date
        self._friends = []

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def username(self):
        return self._username

    @property
    def join_date(self):
        return self._join_date

    @property
    @abstractmethod
    def account_type(self):
        pass

    def add_friend(self, friend):
      if friend not in self._friends:
        self._friends.append(friend)
      if self not in friend._friends:
        friend._friends.append(self)

    def remove_friend(self, friend):
      if friend in self._friends:
        self._friends.remove(friend)
      if self in friend._friends:
        friend._friends.remove(self)

    def friends_list(self):
      return self._friends

    def get_account_info(self):
      info = (
        f"Vartotojas: {self.first_name} {self.last_name}\n"
        f"Slapyvardis: {self.username}\n"
        f"Paskyros tipas: {self.account_type}\n"
        f"Prisijungė: {self.join_date.strftime('%Y-%m-%d')}\n"
        f"Draugų skaičius: {len(self._friends)}\n"
        f"Draugų sarašas:\n"
      )
      for i, friend in enumerate(self._friends, start=1):
          info += f"{i}. {friend.username}\n"

      return info

#______________________________________________________________________________
class StandardAccount(Account):
   
    def __init__(self, first_name, last_name, username, join_date):
        super().__init__(first_name, last_name, username, join_date)
    @property
    def account_type(self):
        return "Standart"

    def can_add_friend(self):
        return len(self._friends) < 5

    def add_friend(self, friend):
        if not self.can_add_friend():
            print(f"\n{self.username} pasiekė maksimalų draugų limitą (5).\n")
            return False
        if isinstance(friend, StandardAccount) and not friend.can_add_friend():
            print(f"\n{friend.username} pasiekė maksimalų draugų limitą (5).\n")
            return False
        super().add_friend(friend)
        return True

#_______________________________________________________________________________
class PremiumAccount(Account):
    
    def __init__(self, first_name, last_name, username, join_date):
        super().__init__(first_name, last_name, username, join_date)
    @property
    def account_type(self):
        return "Premium"

    def add_friend(self, friend):

      if isinstance(friend, StandardAccount) and not friend.can_add_friend():
        print(f"\n{friend.username} pasiekė maksimalų draugų limitą (5).\n")
        return False
      super().add_friend(friend)
      return True
#_______________________________________________________________________________

class AccountManager():
    """Paskyrų valdymo klasė"""

    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AccountManager, cls).__new__(cls)
            cls._instance._accounts = []
        return cls._instance

    def get_account_by_username(self, username):
      for acc in self._accounts:
        if acc.username == username:
            return acc
      return None

    def add_friend_by_username(self, username1, username2):
        player1 = self.get_account_by_username(username1)
        player2 = self.get_account_by_username(username2)
        if player1 and player2:
        #Patikrinama ar buvo draugai prieš bandymą pridėti
          old_friends1 = set(player1.friends_list())
          old_friends2 = set(player2.friends_list())

          player1.add_friend(player2)

        #Tikrinama ar po bandymo jie tapo draugais
          became_friends = (player2 in player1.friends_list() and
                            player1 in player2.friends_list() and
                            (player2 not in old_friends1 or player1 not in old_friends2))

          if True and became_friends:
              print(f"\n{username1} ir {username2} tapo draugais.\n")
          if False:
              print(f"\n{username1} ir {username2} netapo draugais (galimai pasiektas limitas).\n")
        else:
            print("\nVienas arba abu vartotojai nebuvo rasti.\n")


    def add_account(self, player):
        if player not in self._accounts:
            self._accounts.append(player)

    def remove_account(self, player):
        if player in self._accounts:
            #Pašalinamas žaidėjas iš visų draugų sąrašų
            for acc in self._accounts:
                acc.remove_friend(player)

            self._accounts.remove(player)

    def get_all_accounts(self):
        return self._accounts

    def printing_info(self, nr, player):
      info = f"{nr+1}.{player.username} ({player.first_name} {player.last_name})"
      return info

    def display_all_accounts(self, what_to_print='All'):
      output = ""
      if what_to_print == 'All':
        output += "\nVisos paskyros:\n"
        nr = 0
        for acc in self._accounts:
            output += self.printing_info(nr, acc)
            output += "\n"
            nr += 1

      elif what_to_print == 'Premium':
        output += "\nPremium paskyros:\n"
        nr = 0
        for acc in self._accounts:
            if acc.account_type == 'Premium':
                output += self.printing_info(nr, acc)
                output += "\n"
                nr += 1

      elif what_to_print == 'Standart':
        output += "\nStandart paskyros:\n"
        nr = 0
        for acc in self._accounts:
            if acc.account_type == 'Standart':
                output += self.printing_info(nr, acc)
                output += "\n"
                nr += 1

      return output


    def update_to_premium(self, username):
      player = self.get_account_by_username(username)
      if player is None:
        print(f"\nPaskyra su slapyvardžiu '{username}' nerasta.\n")
        return None

      if player.account_type == "Standart":
        old_friends = player.friends_list().copy()

        #Sukuriamas naujas Premium žaidėjas
        updated_player = PremiumAccount(
            player.first_name,
            player.last_name,
            player.username,
            player.join_date
        )
        for friend in old_friends:
            friend.remove_friend(player)
        self._accounts.remove(player)

        for friend in old_friends:
            updated_player.add_friend(friend)

        self._accounts.append(updated_player)
        print(f"\n{username} atnaujintas į Premium paskyrą.\n")
        return updated_player
      else:
        print(f"\n{username} jau yra Premium paskyra.\n")
        return player

if __name__ == "__main__":
    manager = AccountManager()
#_______________________________________________________________________________

manager = AccountManager()


with open("accounts_info.txt", "r", encoding="utf-8") as file:

    for line in file:
        line = line.strip()  # pašaliname \n
        if not line:
            continue  # jei eilutė tuščia, praleidžiam
        first_name, last_name, username, join_date, account_type = line.split(",")
        join_date = datetime.strptime(join_date, "%Y-%m-%d")

        if account_type == "Standart":
            tarpinis = StandardAccount(first_name, last_name, username, join_date)
        elif account_type == "Premium":
            tarpinis = PremiumAccount(first_name, last_name, username, join_date)
        else:
            print(f"Nežinomas paskyros tipas: {account_type}")
            continue

        manager.add_account(tarpinis)

manager.update_to_premium("jonukas")
manager.update_to_premium("super_ona")


manager.add_friend_by_username("jonukas", "Emma_xo")
manager.add_friend_by_username("jonukas", "tom.tom")
manager.add_friend_by_username("tom.tom", "Emma_xo")
manager.add_friend_by_username("super_ona", "Emma_xo")
manager.add_friend_by_username("Emma_xo", "Rutele54")
manager.add_friend_by_username("Emma_xo", "tom.tom")
manager.add_friend_by_username("Emma_xo", "Hey_Dom")
manager.add_friend_by_username("Emma_xo", "Emilai")
manager.add_friend_by_username("Hey_Dom", "super_ona")
manager.add_friend_by_username("Hey_Dom", "Emilai")


with open("accounts_output.txt", "w", encoding="utf-8") as failas:
    for player in manager.get_all_accounts():
        failas.write(player.get_account_info())
        failas.write("\n" + "="*40 + "\n")

    failas.write(manager.display_all_accounts('Premium'))
    failas.write("\n" + "="*40 + "\n")
    failas.write(manager.display_all_accounts('Standart'))
    failas.write("\n" + "="*40 + "\n")
    failas.write(manager.display_all_accounts())











