import pandas as pd
import requests
import sys
from tqdm import tqdm
import time
import re

# 영화 데이터 불러오는 함수

# imdb 영화 상세화면 url 추가 함수: 예) https://www.imdb.com/title/tt0114709/
def add_url(row):
  return f"https://www.imdb.com/title/tt{row}"

# add_rating 함수를 이용하여 평점 추가 rating_count, rating_avg 컬럼 추가
def add_rating(df):
  ratings_df = pd.read_csv('data/ratings.csv')
  ratings_df['movieId'] = ratings_df['movieId'].astype(int).astype(str)
  
  agg_df = ratings_df.groupby('movieId').agg(
    rating_count=('rating', 'count'),
    rating_avg=('rating', 'mean')
  ).reset_index()

  # print(agg_df)
  # rating 소수점 2자리까지만 표시
  agg_df['rating_avg'] = agg_df['rating_avg'].round(2)
  
  # how='left'는 movies_df를 기준으로 머지
  rating_added_df = df.merge(agg_df, on='movieId', how='left') 
  return rating_added_df

  # 포스터 추가
# def add_poster(df):
#   for i, row in tqdm(df.iterrows(), total=df.shape[0]):
#     tmdb_id=row["tmdbId"]
#     tmdb_url=f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key=9b8437c1b16d29a729ff3aa75825a611&language=en-US"
#     result=requests.get(tmdb_url)

#     try:
#       df.at[i, "poster_path"] = "https://image.tmdb.org/t/p/original" + result.json()['poster_path']
#       time.sleep(0.1) # 0.1초 시간 간격으로 생성
#     except (TypeError, KeyError) as e:
#       df.at[i, "poster_path"] = "https://image.tmdb.org/t/p/original/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg"
#   return df

if __name__ == '__main__':
  # 영화 정보 데이터 불러오기
  movies_df = pd.read_csv('data/movies.csv')
  # print(movies_df)

  # 영화 아이디를 문자 형태로 변환
  movies_df['movieId'] = movies_df['movieId'].astype(str)
  # print(movies_df)

  # 링크 파일 읽기
  links_df = pd.read_csv('data/links.csv', dtype=str)
  # print(links_df)

  # 영화 정보와 링크 정보를 합치기
  # merge(): on은 어떤 컬럼으로 머지를 실행할지 결정(join), how는 왼쪽 movies_df를 기준으로 머지할 것인지 결정
  merged_df = movies_df.merge(links_df, on='movieId', how='left')
  # print(merged_df.iloc[1, :])

  # def add_url 함수를 이용하여 imdb 영화 상세화면 url 추가
  merged_df['url'] = merged_df['imdbId'].apply(lambda x: add_url(x))
  result_df = add_rating(merged_df)
  result_df["poster_path"] = None
  # result_df = add_poster(result_df)
  # print(merged_df)

  result_df.to_csv('data/movie_final.csv', index=None)

  # print(add_rating(merged_df))

# 랜덤하게 10개 호출
# 호출된 영화 정보를 반환
# 반환된 영화 정보는 다음과 같은 형태로 반환
item_fname = "data/movie_final.csv"

def random_items():
  movies_df=pd.read_csv(item_fname)
  movies_df = movies_df.fillna("") # 공백을 채워준다
  result_items = movies_df.sample(n=10).to_dict("records")
  return result_items

random_items()
print(random_items())

# 최신 영화 10개 호출
item_fname = "data/movie_final.csv"

def latest_items():
    # CSV 파일을 읽어옴
    movies_df = pd.read_csv(item_fname)
    movies_df = movies_df.fillna("")  # 공백으로 NaN을 채워줌

    # 영화 제목에서 연도를 추출하는 함수 (예: "Journey to the Center of the Earth (1959)" -> 1959)
    def extract_year(title):
        match = re.search(r'\((\d{4})\)', title)
        if match:
            return int(match.group(1))
        return None  # 연도가 없으면 None 반환

    # 연도 정보를 추출해서 새로운 'year' 컬럼에 추가
    movies_df['year'] = movies_df['title'].apply(extract_year)

    # 연도 기준으로 내림차순으로 정렬하고 최신 10개 항목 선택
    latest_movies_df = movies_df.sort_values(by='year', ascending=False).head(10)

    # 결과를 딕셔너리 형태로 반환
    result_items = latest_movies_df.to_dict("records")
    return result_items

latest_items()
print(latest_items())
  