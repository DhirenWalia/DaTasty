from src.ingestion.loader import DataLoader
from src.quality.consistency import ConsistencyChecker


def main():

    print("=== CONSISTENCY DEBUG ===\n")

    path = (
        "data/benchmark/"
        "DATATSTY_Enterprise_Benchmark_v1.csv"
    )

    loader = DataLoader()

    df = loader.load_data(path)

    print("Dataset Loaded!")
    print(f"Shape: {df.shape}")

    checker = ConsistencyChecker(
    df,
    "config/rules.json"
)

    report = checker.analyze_consistency()

    print("\nConsistency Report:\n")

    for item in report:
        print(item)


if __name__ == "__main__":
    main()
