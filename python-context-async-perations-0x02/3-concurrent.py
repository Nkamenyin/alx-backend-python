import aiosqlite
import asyncio

# Asynchronously fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        await cursor.close()
        print("All Users:", results)
        return results

# Asynchronously fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        results = await cursor.fetchall()
        await cursor.close()
        print("Users older than 40:", results)
        return results

# Run both queries concurrently
async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

# Run the async function
asyncio.run(fetch_concurrently())