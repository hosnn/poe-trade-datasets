import json
import os

# JSON 데이터 읽기
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# JSON 데이터 병합
def merge_json(kor_data, eng_data):
    kor_dict = {item["id"]: item for item in kor_data["result"]}
    eng_dict = {item["id"]: item for item in eng_data["result"]}
    
    merged_result = []

    for kor_id, kor_item in kor_dict.items():
        eng_item = eng_dict.get(kor_id)
        if not eng_item:
            print(f"Warning: ID {kor_id} missing in English data.")
            continue

        merged_entries = []
        for kor_entry in kor_item["entries"]:
            eng_entry = next((e for e in eng_item["entries"] if e["id"] == kor_entry["id"]), None)
            if not eng_entry:
                print(f"Warning: Entry ID {kor_entry['id']} missing in English data for {kor_id}.")
                continue

            # 병합된 entry 생성
            merged_entry = {
                "id": kor_entry["id"],
                "korText": kor_entry["text"],
                "engText": eng_entry["text"],
                "type": kor_entry.get("type", eng_entry.get("type"))
            }
            merged_entries.append(merged_entry)

        merged_result.append({
            "id": kor_id,
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