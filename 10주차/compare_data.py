import pandas as pd

# 1. 파일 불러오기
df_10k = pd.read_csv("10주차/csic2010_10k.csv")
df_full = pd.read_csv("10주차/csic2010_full.csv")

# 2. 비교 결과 출력
print("=== 데이터셋 비교 보고서 ===")
print(f"1만건 데이터 크기: {df_10k.shape}")
print(f"6만건 데이터 크기: {df_full.shape}")
print("-" * 30)

print("[라벨 분포 비교 (비율)]")
print("\n[1만건 샘플]")
print(df_10k['label'].value_counts(normalize=True))

print("\n[6만건 전체]")
print(df_full['label'].value_counts(normalize=True))

print("-" * 30)
print("[HTTP 메서드 분포 비교]")
print("\n[1만건 샘플]")
print(df_10k['method'].value_counts())

print("\n[6만건 전체]")
print(df_full['method'].value_counts())