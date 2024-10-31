import pandas as pd
import sys
import json  # JSON으로 변환하기 위해 추가

# 최신 영화 n개 호출
item_fname = "data/movie_final.csv"

def latest_items(count):
    # CSV 파일을 읽어옴
    movies_df = pd.read_csv(item_fname)
    movies_df = movies_df.fillna("")  # 공백으로 NaN을 채워줌

    # year_eng 컬럼을 숫자(float)로 변환, 변환 불가한 값은 NaN 처리
    movies_df['year_eng'] = pd.to_numeric(movies_df['year_eng'], errors='coerce')
    
    # 연도 기준으로 내림차순 정렬 후 최신 count개 항목 선택
    latest_movies_df = movies_df.sort_values(by='year_eng', ascending=False).head(count)
    
    # 영어 및 한국어 필드를 함께 포함하여 딕셔너리 형태로 반환
    result_items = latest_movies_df[[
        'movieId', 'title_eng', 'genres_eng', 'info_eng', 'tmdburl_eng', 'rating_count_eng', 
        'rating_avg_eng', 'poster_path_eng', 'year_eng', 'trailer_url_eng',
        'title_kor', 'genres_kor', 'info_kor', 'tmdburl_kor', 'rating_count_kor', 
        'rating_avg_kor', 'poster_path_kor', 'year_kor', 'trailer_url_kor'
    ]].to_dict("records")
    
    return result_items

if __name__ == '__main__':
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 10  # 인자로 받은 count, 기본값은 10
    result = latest_items(count)
    print(json.dumps(result, ensure_ascii=False))  # Python 리스트를 JSON으로 변환하여 출력
