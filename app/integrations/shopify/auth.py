import os
import time

import requests


class ShopifyAuth:
    def __init__(self):
        self.shop = os.getenv("SHOPIFY_SHOP")
        self.client_id = os.getenv("SHOPIFY_CLIENT_ID")
        self.client_secret = os.getenv("SHOPIFY_CLIENT_SECRET")

        if not self.shop:
            raise ValueError("SHOPIFY_SHOP is not configured")

        if not self.client_id:
            raise ValueError("SHOPIFY_CLIENT_ID is not configured")

        if not self.client_secret:
            raise ValueError("SHOPIFY_CLIENT_SECRET is not configured")

        self._access_token: str | None = None
        self._expires_at: float = 0

    def get_access_token(self) -> str:
        if (
            self._access_token is not None
            and time.time() < self._expires_at
        ):
            return self._access_token

        response = requests.post(
            f"https://{self.shop}.myshopify.com/admin/oauth/access_token",
            json={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials",
            },
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        self._access_token = data["access_token"]

        expires_in = data.get("expires_in", 86400)

        # Обновляем токен за минуту до истечения
        self._expires_at = time.time() + expires_in - 60

        return self._access_token