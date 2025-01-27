import argparse
from spotylog import SpotifyAuth, SpotifyClient

def main():
    parser = argparse.ArgumentParser(description="Interact with the Spotify API.")
    parser.add_argument("--search", help="Search for tracks, albums, or artists.")
    parser.add_argument("--export", help="Export data to Excel, CSV, or JSON.", choices=["excel", "csv", "json"])
    args = parser.parse_args()

    auth = SpotifyAuth()
    token = auth.get_access_token()
    client = SpotifyClient(token["access_token"])

    if args.search:
        results = client.search(args.search)
        if args.export:
            if args.export == "excel":
                client.save_search_results_to_excel(args.search, filename="search_results.xlsx")
            elif args.export == "csv":
                client.save_search_results_to_csv(args.search, filename="search_results.csv")
            elif args.export == "json":
                client.save_search_results_to_json(args.search, filename="search_results.json")
        else:
            print(results)

if __name__ == "__main__":
    main()