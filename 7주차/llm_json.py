import ollama
import json

reviews = [
    "배송 빠르고 제품 품질도 좋아요! 재구매 의사 있습니다.",
    "불량품이 왔는데 교환도 안 해주네요. 최악입니다.",
    "가격은 저렴한데 품질은 보통이에요."
]

results = []

for review in reviews:
    try:
        response = ollama.chat(
            model="gemma3:4b",
            messages=[
                {
                    "role": "system",
                    "content": """당신은 리뷰 분석 전문가입니다.
주어진 리뷰를 분석하여 반드시 아래 JSON 형식으로만 응답하세요.
다른 텍스트는 포함하지 마세요.
{"sentiment": "긍정/부정/중립", "confidence": 0.0, "keywords": ["키워드1", "키워드2"]}"""
                },
                {
                    "role": "user",
                    "content": review
                }
            ]
        )

        # 응답 추출 (객체 속성 방식 권장)
        raw = response.message.content
        
        # 1단계: JSON 추출 로직 (더 안전한 방식)
        clean = raw.strip()
        if "```" in clean:
            # ```json ... ``` 또는 ``` ... ``` 내부 텍스트 추출
            clean = clean.split("```")[-2].split("json")[-1].strip()

        # 2단계: 파싱
        data = json.loads(clean)
        results.append(data)
        
        print(f"✅ 리뷰: {review[:20]}...")
        print(f"   감성: {data.get('sentiment')}, 확신도: {data.get('confidence')}")
        print(f"   키워드: {data.get('keywords')}")

    except Exception as e:
        print(f"⚠ 오류 발생: {e}")
    
    print("-" * 50)

print(f"\n총 {len(results)}개 리뷰 분석 완료")