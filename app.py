from fetch_data import fetch_and_save_data
from filters_merged import filters_merged
from items_merged import items_merged
from stats_merged import stats_merged
from leagues_merged import leagues_merged

def main():
  # 도메인 및 URI 정의
  DOMAIN = {
    'eng': 'https://www.pathofexile.com',
    'kor': 'https://poe.game.daum.net'
  }

  URI = {
    "leagues": "/api/trade2/data/leagues",
    "items": "/api/trade2/data/items",
    "stats": "/api/trade2/data/stats",
    "static": "/api/trade2/data/static",
    "filters": "/api/trade2/data/filters"
  }

  # save_folder = "datas"  # 저장 폴더 이름
  # fetch_and_save_data(DOMAIN, URI, save_folder)

  filters_merged()
  items_merged()
  stats_merged()
  leagues_merged()

if __name__ == "__main__":
    main()