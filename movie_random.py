import pandas as pd
import sys
import json

# CSV 파일 경로
item_fname = "data/movie_final.csv"

# 무작위 영화 선택 함수
def random_items(count):
    # CSV 파일 읽기
    movies_df = pd.read_csv(item_fname)
    movies_df = movies_df.fillna("")  # NaN 값을 공백으로 대체
    
    # 지정된 개수만큼 무작위 영화 선택
    result_items = movies_df.sample(n=count)[[
        'movieId', 'title_eng', 'genres_eng', 'info_eng', 'tmdburl_eng', 'rating_count_eng', 
        'rating_avg_eng', 'poster_path_eng', 'year_eng', 'trailer_url_eng',
        'title_kor', 'genres_kor', 'info_kor', 'tmdburl_kor', 'rating_count_kor', 
        'rating_avg_kor', 'poster_path_kor', 'year_kor', 'trailer_url_kor'
    ]].to_dict("records")
    
    return result_items

if __name__ == "__main__":
    # Node.js에서 전달된 count 값을 사용
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 10  # 기본값 10
    items = random_items(count)
    print(json.dumps(items, ensure_ascii=False))  # JSON 형식으로 출력 (한글 깨짐 방지)


# import json
# import pandas as pd
# import sys
# from langchain_community.vectorstores import FAISS


# item_fname = "data/movie_final.csv"


# def random_items(count):
#   movies_df=pd.read_csv(item_fname)
#   movies_df = movies_df.fillna("") # 공백을 채워준다
#   result_items = movies_df.sample(n=count).to_dict("records")
#   return result_items


# if __name__ == "__main__":
#   command = sys.argv[1]  # Get the command (random or latest)
#     # count = int(sys.argv[2])  # Get the count value passed as an argument
   
#   if command == "random":
#     count = int(sys.argv[2])
#     print(json.dumps(random_items(count)))
#   else:
#     print("Error: Invalid command provided")
#     sys.exit(1)

