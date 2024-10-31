import pandas as pd
import sys
import json

# CSV 파일 경로
item_fname = "data/movie_final.csv"

# 장르별 영화 검색 함수
def genre_items(genre, count):
    # CSV 파일을 읽어옴
    movies_df = pd.read_csv(item_fname)
    movies_df = movies_df.fillna("")  # 공백으로 NaN을 채워줌

    # 영어 및 한국어 장르 컬럼에서 해당 장르가 포함된 영화 필터링 (대소문자 구분 없이)
    filtered_df = movies_df[
        movies_df['genres_eng'].str.contains(genre, case=False, na=False) |
        movies_df['genres_kor'].str.contains(genre, case=False, na=False)
    ]

    # 영화가 count개보다 적을 수 있으므로, 최소값으로 처리
    count = min(count, len(filtered_df))

    # 필터링된 영화 목록을 무작위로 섞고 지정된 count만큼 선택
    random_df = filtered_df.sample(n=count, random_state=None)

    # 결과를 영어 및 한국어 정보가 포함된 딕셔너리 형태로 반환
    result_items = random_df[[
        'movieId', 'title_eng', 'genres_eng', 'info_eng', 'tmdburl_eng', 'rating_count_eng', 
        'rating_avg_eng', 'poster_path_eng', 'year_eng', 'trailer_url_eng',
        'title_kor', 'genres_kor', 'info_kor', 'tmdburl_kor', 'rating_count_kor', 
        'rating_avg_kor', 'poster_path_kor', 'year_kor', 'trailer_url_kor'
    ]].to_dict("records")
    
    return result_items

if __name__ == '__main__':
    genre = sys.argv[1]  # 첫 번째 인자로 장르
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 10  # 두 번째 인자로 개수, 기본값 10
    result = genre_items(genre, count)
    print(json.dumps(result, ensure_ascii=False))  # 결과를 JSON으로 출력
