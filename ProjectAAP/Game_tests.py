from Game import *
import unittest
from unittest.mock import patch

class TestMethod(unittest.TestCase):

    # @patch('Game.Ship.hit')
    def test(self):

        # player = Ship(100, 100)
        # player.kills = 0
        b = Bullet1(120, 120)
        enemy = Enemy( 120, 120, 10)
        player.bullets.append(b)
        enemies.append(enemy)
        player.hit()
        self.assertEqual(player.kills,1)
        self.assertEqual(len(player.bullets), 0)
        self.assertEqual(len(enemies), 0)
         
        
        
if __name__ == '__main__':
    unittest.main()