import os

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app.integrations.shopify.auth import ShopifyAuth


class ShopifyClient:
    API_VERSION = "2026-04"

    def __init__(self):
        self.auth = ShopifyAuth()
        self.shop = os.environ["SHOPIFY_SHOP"]

        self.session = requests.Session()

        retry = Retry(
            total=3,
            connect=3,
            read=3,
            backoff_factor=1,
            status_forcelist=[
                429,
                500,
                502,
                503,
                504,
            ],
            allowed_methods=["POST"],
        )

        self.session.mount(
            "https://",
            HTTPAdapter(max_retries=retry),
        )

    def execute_graphql(
        self,
        query: str,
        variables: dict | None = None,
    ) -> dict:
        access_token = self.auth.get_access_token()

        response = self.session.post(
            (
                f"https://{self.shop}.myshopify.com"
                f"/admin/api/{self.API_VERSION}/graphql.json"
            ),
            headers={
                "X-Shopify-Access-Token": access_token,
                "Content-Type": "application/json",
            },
            json={
                "query": query,
                "variables": variables or {},
            },
            timeout=(10, 30),
        )

        response.raise_for_status()

        payload = response.json()

        if payload.get("errors"):
            raise RuntimeError(
                f"Shopify GraphQL errors: {payload['errors']}"
            )

        return payload["data"]

    def get_products(
        self,
        first: int = 50,
        after: str | None = None,
    ) -> dict:
        query = """
        query GetProducts($first: Int!, $after: String) {
          products(first: $first, after: $after) {
            nodes {
              id
              title
              vendor
              status
            }
            pageInfo {
              hasNextPage
              endCursor
            }
          }
        }
        """

        return self.execute_graphql(
            query=query,
            variables={
                "first": first,
                "after": after,
            },
        )