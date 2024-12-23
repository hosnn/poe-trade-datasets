import json
import os

# JSON 데이터 읽기
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# JSON 데이터 병합
def merge_json(kor_data, eng_data):
    merged_result = []

    for kor_item, eng_item in zip(kor_data["result"], eng_data["result"]):
        if kor_item["id"] != eng_item["id"]:
            raise ValueError(f"Mismatched IDs: {kor_item['id']} vs {eng_item['id']}")

        merged_entries = []
        for kor_entry, eng_entry in zip(kor_item["entries"], eng_item["entries"]):
            if kor_entry["id"] != eng_entry["id"]:
                raise ValueError(f"Mismatched Entry IDs: {kor_entry['id']} vs {eng_entry['id']}")

            # 병합된 entry 생성
            merged_entry = {
                "id": kor_entry["id"],
                "korText": kor_entry["text"],
                "engText": eng_entry["text"],
                "type": kor_entry.get("type", eng_entry.get("type"))
            }
            merged_entries.append(merged_entry)

        merged_result.append({
            "id": kor_item["id"],
            "labelKor": kor_item["label"],
            "labelEng": eng_item["label"],
            "entries": merged_entries
        })

    return {"result": merged_result}

# 메인 실행
def stats_merged():
    kor_file_path = "datas/kor/stats.json"
    eng_file_path = "datas/eng/stats.json"
    output_file_path = "datas/merged/stats.json"

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