#lim_classification.ipynb 시간확인
분류 대상: 100건
라벨 분포: 정상 56건 / 공격 44건

입력: GET /tienda1/publico/anadir.jsp?id=2'+OR+'1'='1 HTTP/1.1
응답: {'label': 'Anomalous', 'reason': "SQL Injection attempt. The request includes ' OR '1'='1', a common SQL injection pattern to bypass authentication or retrieve all data."}

10/100건 완료 (8.1초, 건당 0.81초)
  20/100건 완료 (14.3초, 건당 0.71초)
  30/100건 완료 (21.0초, 건당 0.70초)
  40/100건 완료 (28.9초, 건당 0.72초)
  50/100건 완료 (37.0초, 건당 0.74초)
  60/100건 완료 (45.3초, 건당 0.76초)
  70/100건 완료 (51.6초, 건당 0.74초)
  80/100건 완료 (59.7초, 건당 0.75초)
  90/100건 완료 (67.1초, 건당 0.75초)
  100/100건 완료 (73.9초, 건당 0.74초)

총 소요: 73.9초
1만 건 환산: 약 123분

LLM 정확도: 0.8300
LLM F1:    0.8211
분류 실패(Unknown): 1건

              precision    recall  f1-score   support

      Normal       0.90      0.79      0.84        56
   Anomalous       0.76      0.89      0.82        44

    accuracy                           0.83       100
   macro avg       0.83      0.84      0.83       100
weighted avg       0.84      0.83      0.83       100

#ollma 프롬프트 변경하여 정확도 비교

🚀 Prompt_A (기본 지시) 테스트 시작...
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
 진행 중... (5/20)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
 진행 중... (10/20)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
 진행 중... (15/20)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
 진행 중... (20/20)

🚀 Prompt_B (역할 및 규칙 강화) 테스트 시작...
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
 진행 중... (5/20)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
 진행 중... (10/20)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
 진행 중... (15/20)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
Error: model 'llama3' not found (status code: 404)
 진행 중... (20/20)

==================================================
📊 프롬프트 성능 비교 최종 결과
==================================================
                      Accuracy  F1-Score Time (s)
Prompt_A (기본 지시)          0.45  0.310345     0.04
Prompt_B (역할 및 규칙 강화)     0.45  0.310345     0.03

#few-short 프롬프트 -정확도 높이는 프롬프트 찾기
🚀 Few-Shot_기본 (정상1, 공격1) 테스트 시작...
 진행 중... (5/20)
 진행 중... (10/20)
 진행 중... (15/20)
 진행 중... (20/20)

🚀 Few-Shot_강화 (정상2, 공격2 + 설명 형식 지정) 테스트 시작...
 진행 중... (5/20)
 진행 중... (10/20)
 진행 중... (15/20)
 진행 중... (20/20)

============================================================
📊 Few-shot 프롬프트 최적화 비교 결과
============================================================
                                   Accuracy  F1-Score  Time (s)
Few-Shot_기본 (정상1, 공격1)                 0.45  0.310345      0.05
Few-Shot_강화 (정상2, 공격2 + 설명 형식 지정)      0.45  0.310345      0.04

------------------------------------------------------------
🏆 최적의 프롬프트: Few-Shot_기본 (정상1, 공격1) (정확도: 45.0%)
------------------------------------------------------------