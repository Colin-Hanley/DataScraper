from typing import Optional, Union, Dict


class Card:
    """
    Represents a card with its attributes retrieved from the Scryfall API.

    Attributes:
        name (str): The name of the card.
        scryfall_response (dict): The JSON response obtained from Scryfall API.

    Methods:
        get_base_scryfall_url(name: str) -> str:
            Returns the Scryfall API URL for a card with the given name.

        set_base_scryfall_response():
            Fetches and stores the Scryfall API response for the card.

        get_value_from_base_scryfall_response(key: str, sub_key: Optional[str] = None) -> Union[Dict, None]:
            Retrieves a value from the Scryfall API response using the specified keys.

    Properties:
        dollar_min_price (Union[float, None]): The minimum price of the card in USD.
        euro_min_price (Union[float, None]): The minimum price of the card in EUR.
        online_min_price (Union[float, None]): The minimum price of the card in online tickets (tix).
    """

    def __init__(self, name: str):
        """
        Initializes a Card instance with the given name.

        Args:
            name (str): The name of the card.
        """
        self.name = name
        self.scryfall_response = None
        self.set_base_scryfall_response()

    def __repr__(self) -> str:
        """
        Returns a string representation of the Card instance.

        Returns:
            str: A string representation of the Card.
        """
        return f"Card(name={self.name})"

    @staticmethod
    def get_base_scryfall_url(name: str) -> str:
        """
        Returns the Scryfall API URL for a card with the given name.

        Args:
            name (str): The name of the card.

        Returns:
            str: The Scryfall API URL for the card.
        """
        return f"https://api.scryfall.com/cards/named?exact={name}"

    def set_base_scryfall_response(self):
        """
        Fetches and stores the Scryfall API response for the card.
        """
        url_to_hit = self.get_base_scryfall_url(self.name)
        try:
            self.scryfall_response = fetch_json(url_to_hit)
        except Exception as e:
            print(f"An error occurred while fetching Scryfall response: {e}")

    def get_value_from_base_scryfall_response(self, key: str, sub_key: Optional[str] = None) -> Union[Dict, None]:
        """
        Retrieves a value from the Scryfall API response using the specified keys.

        Args:
            key (str): The key to retrieve from the API response.
            sub_key (Optional[str]): The sub-key to retrieve from the key's value (default: None).

        Returns:
            Union[Dict, None]: The retrieved value or None if not found.
        """
        if self.scryfall_response:
            data = self.scryfall_response.get(key)
            if sub_key and data:
                return data.get(sub_key)
            return data
        else:
            return None

    @property
    def dollar_min_price(self) -> Union[float, None]:
        """
        The minimum price of the card in USD.

        Returns:
            Union[float, None]: The minimum price in USD or None if not available.
        """
        return self.get_value_from_base_scryfall_response('prices', 'usd')

    @property
    def euro_min_price(self) -> Union[float, None]:
        """
        The minimum price of the card in EUR.

        Returns:
            Union[float, None]: The minimum price in EUR or None if not available.
        """
        return self.get_value_from_base_scryfall_response('prices', 'eur')

    @property
    def online_min_price(self) -> Union[float, None]:
        """
        The minimum price of the card in online tickets (tix).

        Returns:
            Union[float, None]: The minimum price in online tickets or None if not available.
        """
        return self.get_value_from_base_scryfall_response('prices', 'tix')
