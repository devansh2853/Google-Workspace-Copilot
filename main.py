from core.agent import GoogleWorkspaceCopilot
from core.tools import show_banner, isValidMail
import asyncio


async def main():
    show_banner()
    user_email = input("Please enter your email: ").strip()
    while not isValidMail(user_email):
            print("❌ Invalid email address. Please try again.")
    agent = GoogleWorkspaceCopilot()

    print("Type 'exit' to quit.\n")

    while True:
        prompt = input("Enter a command: ")
        if prompt.lower() == "exit":
            print("Exiting...")
            break

        response = await agent.run_command(user_email, prompt)
        print("Response:", response)

    await agent.cleanup_user(user_email)



if __name__ == "__main__":
    asyncio.run(main())