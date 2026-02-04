import os, uuid
from processors.loader import load_file
from processors.analysis import analyze_data
from processors.missing import handle_missing
from processors.duplicates import remove_duplicates
from processors.outliers import handle_outliers_smart
from processors.normalization import normalize

UPLOAD_FOLDER = "uploads"

class DataProcessor:

    def process(self, file_path, options):
        df = load_file(file_path)

        original = analyze_data(df)

        df = remove_duplicates(df)
        df = handle_missing(df, options.get("handle_missing", "fill_mean"))

        if options.get("handle_outliers") == "smart":
            df = handle_outliers_smart(df)

        if options.get("normalize") == "true":
            df = normalize(df, options.get("norm_method", "minmax"))

        final = analyze_data(df)

        filename = f"proc_{uuid.uuid4()}.csv"
        df.to_csv(os.path.join(UPLOAD_FOLDER, filename), index=False)

        return {
            "success": True,
            "processed_filename": filename,
            "original_analysis": original,
            "final_analysis": final
        }
