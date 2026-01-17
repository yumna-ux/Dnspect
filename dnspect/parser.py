def parse_record_types(record: str) -> list[str]:
    return [r.strip().upper() for r in record.split(",") if r.strip()]
