import boto3
from boto3.dynamodb.conditions import Attr

REGION = "us-east-1"
TABLE_NAME = "MLB_Players"

def get_table():
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    return dynamodb.Table(TABLE_NAME)

def create_player():
    table = get_table()

    name = input("Enter player name: ").strip()
    hr = int(input("Enter home runs (HR): ").strip())
    rbi = int(input("Enter RBIs: ").strip())

    table.put_item(
        Item={
            "Name": name,
            "HR": hr,
            "RBI": rbi
        }
    )
    print(f"Player '{name}' added successfully!")

def print_player(player):
    name = player.get("Name", "Unknown Name")
    hr = player.get("HR", "Unknown HR")
    rbi = player.get("RBI", "Unknown RBI")

    print(f"  Name : {name}")
    print(f"  HR   : {hr}")
    print(f"  RBI  : {rbi}")

def print_all_players():
    table = get_table()
    response = table.scan()
    items = response.get("Items", [])

    if not items:
        print("No players found. Make sure your DynamoDB table has data.")
        return

    print(f"Found {len(items)} player(s):\n")
    for player in items:
        print_player(player)

def update_hr():
    try:
        table = get_table()
        name = input("Enter player name: ").strip()
        hr = int(input("Enter new home run (HR) total: ").strip())

        table.update_item(
            Key={"Name": name},
            UpdateExpression="SET HR = :h",
            ExpressionAttributeValues={":h": hr}
        )
        print(f"'{name}' HR updated to {hr}!")
    except Exception:
        print("Error updating player home runs.")

def delete_player():
    table = get_table()
    name = input("Enter player name to delete: ").strip()
    table.delete_item(Key={"Name": name})
    print(f"Player '{name}' deleted successfully!")

def query_avg_rbi():
    table = get_table()
    response = table.scan()
    items = response.get("Items", [])

    if not items:
        print("No players found.")
        return

    rbis = [float(p["RBI"]) for p in items if "RBI" in p]

    if not rbis:
        print("No RBI data found.")
        return

    avg = sum(rbis) / len(rbis)
    print(f"Average RBI across {len(rbis)} player(s): {avg:.2f}")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new player")
    print("Press R: to READ all players")
    print("Press U: to UPDATE a player's home runs")
    print("Press D: to DELETE a player")
    print("Press Q: to QUERY average RBIs of all players")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_player()
        elif input_char.upper() == "R":
            print_all_players()
        elif input_char.upper() == "U":
            update_hr()
        elif input_char.upper() == "D":
            delete_player()
        elif input_char.upper() == "Q":
            query_avg_rbi()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()