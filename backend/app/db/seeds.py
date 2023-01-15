import argparse
import asyncio
import asyncpg

from app.core.config import get_app_settings
from app.db.repositories.users import UsersRepository
from app.db.repositories.items import ItemsRepository
from app.db.repositories.comments import CommentsRepository
from app.services.items import get_slug_for_item


async def populate_db(amount):
    settings = get_app_settings()
    async with asyncpg.create_pool(dsn=settings.database_url) as pool:
        async with pool.acquire() as conn:
            users_repo = UsersRepository(conn)
            items_repo = ItemsRepository(conn)
            comments_repo = CommentsRepository(conn)
            for i in range(amount):
                user_str = f"user_{i}"
                user = await users_repo.create_user(
                    username=user_str,
                    email=f"{user_str}@gmail.com",
                    password=user_str,
                )

                item_str = f"item_{i}"
                item = await items_repo.create_item(
                    slug=get_slug_for_item(item_str),
                    title=item_str,
                    description=f"{item_str} description",
                    seller=user,
                    body=f"{item_str} body",
                    image="https://anythink.photos/i",
                    tags=["tag1", "tag2"],
                )

                await comments_repo.create_comment_for_item(
                    body=f"{item_str} comment",
                    item=item,
                    user=user,
                )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("amount", type=int)
    args = parser.parse_args()

    asyncio.run(populate_db(args.amount))


if __name__ == "__main__":
    main()
