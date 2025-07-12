import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("All users fetched")
            return results

async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            results = await cursor.fetchall()
            print("Older users fetched")
            return results

async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

if __name__ == '__main__':
    # Run the concurrent queries
    all_users, older_users = asyncio.run(fetch_concurrently())
    
    print("\nAll users:")
    for user in all_users:
        print(user)
    
    print("\nUsers older than 40:")
    for user in older_users:
        print(user)