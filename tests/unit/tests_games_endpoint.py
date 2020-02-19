import unittest

from lichess_client import APIClient
from lichess_client.helpers import Response
from lichess_client.utils.enums import StatusTypes, VariantTypes
from tests.utils import get_token_from_config, async_test
from chess.pgn import Game


class TestAccountEndpoint(unittest.TestCase):
    client = None
    token = get_token_from_config('amasend')

    @classmethod
    def setUp(cls) -> None:
        cls.client = APIClient(token=cls.token)

    @async_test
    async def test_01__export_one_game__fetching_finished_game_details__response_object_returned_with_success(self):
        response = await self.client.games.export_one_game(game_id='Haw7aw6f')
        print(response)

        self.assertIsInstance(response, Response, msg="Response in not of type \"Response\"")
        self.assertEqual(response.entity.status, StatusTypes.SUCCESS, msg="Request was unsuccessful.")
        self.assertIsInstance(response.entity.content, Game, msg="Game was incorrectly loaded.")

    @async_test
    async def test_02__export_user_games__fetching_finished_user_games_details__response_object_returned_with_success(self):
        response = await self.client.games.export_games_of_a_user(username='amasend')
        print(response)

        self.assertIsInstance(response, Response, msg="Response in not of type \"Response\"")
        self.assertEqual(response.entity.status, StatusTypes.SUCCESS, msg="Request was unsuccessful.")

    # TODO: add more tests for export_user_games with different parameters


if __name__ == '__main__':
    unittest.main()