import json
import os

# JSON 데이터 읽기
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# JSON 데이터 병합
def merge_json(kor_data, eng_data):
    merged_result = []

    # `result` 항목 병합
    for kor_item, eng_item in zip(kor_data["result"], eng_data["result"]):
        if kor_item["id"] != eng_item["id"]:
            raise ValueError(f"Mismatched IDs: {kor_item['id']} vs {eng_item['id']}")

        merged_filters = []
        for kor_filter, eng_filter in zip(kor_item["filters"], eng_item["filters"]):
            if kor_filter["id"] != eng_filter["id"]:
                raise ValueError(f"Mismatched Filter IDs: {kor_filter['id']} vs {eng_filter['id']}")

            # 병합된 필터 생성
            merged_filter = {
                "id": kor_filter["id"],
                "korText": kor_filter["text"],
                "engText": eng_filter["text"]
            }
            # 옵션 및 추가 속성 병합
            if "option" in kor_filter or "option" in eng_filter:
                merged_filter["option"] = {
                    "options": [
                        {
                            "id": kor_opt.get("id"),
                            "korText": kor_opt.get("text"),
                            "engText": eng_opt.get("text")
                        }
                        for kor_opt, eng_opt in zip(
                            kor_filter.get("option", {}).get("options", []),
                            eng_filter.get("option", {}).get("options", [])
                        )
                    ]
                }
            if "minMax" in kor_filter or "minMax" in eng_filter:
                merged_filter["minMax"] = kor_filter.get("minMax", eng_filter.get("minMax"))
            if "fullSpan" in kor_filter or "fullSpan" in eng_filter:
                merged_filter["fullSpan"] = kor_filter.get("fullSpan", eng_filter.get("fullSpan"))
            if "input" in kor_filter or "input" in eng_filter:
                merged_filter["input"] = {
                    "korPlaceholder": kor_filter.get("input", {}).get("placeholder"),
                    "engPlaceholder": eng_filter.get("input", {}).get("placeholder")
                }

            merged_filters.append(merged_filter)

        merged_result.append({
            "id": kor_item["id"],
            "titleKor": kor_item["title"],
            "titleEng": eng_item["title"],
            "hidden": kor_item.get("hidden", eng_item.get("hidden")),
            "filters": merged_filters
        })

    return {"result": merged_result}

# 메인 실행
def filters_merged():
    kor_file_path = "datas/kor/filters.json"
    eng_file_path = "datas/eng/filters.json"
    output_file_path = "datas/merged/filters.json"

    kor_data = load_json(kor_file_path)
    eng_data = load_json(eng_file_path)

    merged_data = merge_json(kor_data, eng_data)

    # 출력 디렉토리 생성
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # 병합된 JSON 저장
    with open(output_file_path, "w", encoding="utf-8") as file:
        # json.dump(merged_data, file, ensure_ascii=False, indent=4) # 가독성 들여쓰기
        json.dump(merged_data, file, ensure_ascii=False, separators=(',', ':')) # 들여쓰기 제거

    print(f"Merged JSON saved to {output_file_path}")

