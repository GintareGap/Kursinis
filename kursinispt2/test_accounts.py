import unittest
from datetime import datetime
from kursinis import StandardAccount, PremiumAccount, AccountManager

class TestKursinis(unittest.TestCase):

    def setUp(self):
        # Gauti singleton instanciją ir išvalyti sąrašą tarp testų
        self.manager = AccountManager()
        self.manager._accounts.clear()

        self.acc1 = StandardAccount("Jonas", "Jonaitis", "jonukas", datetime(2023, 5, 1))
        self.acc2 = StandardAccount("Tomas", "Tomaitis", "tom.tom", datetime(2023, 6, 1))
        self.acc3 = PremiumAccount("Ona", "Onaitė", "super_ona", datetime(2022, 1, 1))

        self.manager.add_account(self.acc1)
        self.manager.add_account(self.acc2)
        self.manager.add_account(self.acc3)

    def test_add_friend_standard_limit(self):
        # Sukuriame papildomus vartotojus
        for i in range(4):
            friend = StandardAccount(f"Vardas{i}", f"Pavarde{i}", f"user{i}", datetime.now())
            self.manager.add_account(friend)
            self.acc1.add_friend(friend)

        # Penktas – dar leidžiamas
        extra = StandardAccount("Penkas", "Draugas", "user4", datetime.now())
        self.manager.add_account(extra)
        result = self.acc1.add_friend(extra)
        self.assertTrue(result)

        # Šeštas – turėtų būti atmestas
        blocked = StandardAccount("Šeštas", "Draugas", "user5", datetime.now())
        self.manager.add_account(blocked)
        result = self.acc1.add_friend(blocked)
        self.assertFalse(result)

    def test_friend_connection_bidirectional(self):
        self.acc1.add_friend(self.acc2)
        self.assertIn(self.acc2, self.acc1.friends_list())
        self.assertIn(self.acc1, self.acc2.friends_list())

    def test_update_to_premium(self):
        updated = self.manager.update_to_premium("jonukas")
        self.assertIsInstance(updated, PremiumAccount)
        self.assertEqual(updated.username, "jonukas")

    def test_add_friend_with_premium(self):
        # Premium turi neribotą draugų kiekį
        for i in range(10):
            friend = StandardAccount(f"X{i}", f"Y{i}", f"std{i}", datetime.now())
            self.manager.add_account(friend)
            self.acc3.add_friend(friend)

        self.assertEqual(len(self.acc3.friends_list()), 10)

    def test_display_accounts(self):
        output_all = self.manager.display_all_accounts()
        self.assertIn("jonukas", output_all)
        self.assertIn("tom.tom", output_all)
        self.assertIn("super_ona", output_all)

        output_premium = self.manager.display_all_accounts("Premium")
        self.assertIn("super_ona", output_premium)
        self.assertNotIn("jonukas", output_premium)

        output_standard = self.manager.display_all_accounts("Standart")
        self.assertIn("jonukas", output_standard)
        self.assertNotIn("super_ona", output_standard)

if __name__ == "__main__":
    unittest.main()
