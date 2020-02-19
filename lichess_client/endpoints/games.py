import json
from typing import TYPE_CHECKING, Union, List

from lichess_client.utils.enums import RequestMethods, VariantTypes, ColorType
from lichess_client.abstract_endpoints.abstract_games import AbstractGames
from lichess_client.helpers import Response
from lichess_client.utils.hrefs import GAMES_EXPORT_ONE_URL, GAMES_EXPORT_USER_URL

if TYPE_CHECKING:
    from lichess_client.clients.base_client import BaseClient


class Games(AbstractGames):
    """Class for Games API Endpoint"""

    def __init__(self, client: 'BaseClient') -> None:
        self._client = client

    async def export_one_game(self, game_id: str) -> 'Response':
        """
        Download one game. Only finished games can be downloaded.

        Parameters
        ----------
        game_id: str, required
            ID of the game.

        Returns
        -------
        Response object with response content.

        Example
        -------
        >>> from lichess_client import APIClient
        >>> client = APIClient(token='...')
        >>> response = client.users.export_one_game(game_id='q7zvsdUF')
        # TODO: add more examples
        """
        headers = {
            'Content-Type': 'application/json'
        }
        parameters = {
            'moves': 'true',
            'pgnInJson': 'false',
            'tags': 'true',
            'clocks': 'true',
            'evals': 'true',
            'opening': 'true',
            'literate': 'true'
        }
        response = await self._client.request(method=RequestMethods.GET,
                                              url=GAMES_EXPORT_ONE_URL.format(gameId=game_id),
                                              headers=headers,
                                              params=parameters)
        return response

    async def export_games_of_a_user(self,
                                     username: str,
                                     since: int = None,
                                     until: int = None,
                                     limit: int = None,
                                     vs: str = None,
                                     rated: bool = None,
                                     variant: Union['VariantTypes', List['VariantTypes']] = None,
                                     color: 'ColorType' = None,
                                     analysed: bool = None,
                                     ongoing: bool = False) -> 'Response':
        """
        Download all games of any user in PGN format.

        Games are sorted by reverse chronological order (most recent first)

        We recommend streaming the response, for it can be very long. https://lichess.org/@/german11 for instance has more than 320,000 games.

        The game stream is throttled, depending on who is making the request:

            Anonymous request: 15 games per second
            OAuth2 authenticated request: 25 games per second
            Authenticated, downloading your own games: 50 games per second

        Parameters
        ----------
        username: str, required
            Name of the user.

        since: int, optional
            Default: "Account creation date"
            Download games played since this timestamp.

        until: int, optional
            Default: "Now"
            Download games played until this timestamp.

        limit: int, optional
            Default: None
            How many games to download. Leave empty to download all games.

        vs: str, optional
            [Filter] Only games played against this opponent

        rated: bool, optional
             Default: None
            [Filter] Only rated (true) or casual (false) games

        variant: Union[VariantTypes, List[VariantTypes]], optional
            Default: None
            [Filter] Only games in these speeds or variants.
            Multiple variants can be specified in a list.

        color: ColorType, optional
            Default: None
            [Filter] Only games played as this color.

        analysed: bool, optional
            [Filter] Only games with or without a computer analysis available.

        ongoing: bool, optional
            Default: false
            [Filter] Also include ongoing games

        Returns
        -------
        Response object with response content.

        Example
        -------
        >>> from lichess_client import APIClient
        >>> client = APIClient(token='...')
        >>> response = client.users.export_games_of_a_user(username='amasend')
        # TODO: add more examples
        """
        if isinstance(variant, list):
            variant = ','.join([entry.value for entry in variant])
        elif isinstance(variant, VariantTypes):
            variant = variant.value

        headers = {
            'Content-Type': 'application/json'
        }
        parameters = {
            'since': 'Account creation date' if since is None else since,
            'until': 'Now' if until is None else until,
            'max': 'null' if limit is None else limit,
            'rated': 'null' if rated is None else rated,
            'perfType': 'null' if variant is None else variant,
            'color': 'null' if color is None else color.value,
            'analysed': 'null' if analysed is None else analysed,
            'ongoing': json.dumps(ongoing),
            'moves': 'true',
            'pgnInJson': 'false',
            'tags': 'true',
            'clocks': 'true',
            'evals': 'true',
            'opening': 'true'
        }

        if vs is not None:
            parameters['vs'] = vs

        response = await self._client.request_stream(method=RequestMethods.GET,
                                                     url=GAMES_EXPORT_USER_URL.format(username=username),
                                                     headers=headers,
                                                     params=parameters)
        return response

    async def export_games_by_ids(self):
        pass

    async def stream_current_games(self):
        pass

    async def get_ongoing_games(self):
        pass

    async def get_current_tv_games(self):
        pass
