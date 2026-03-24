import os, uuid
from processors.loader import load_file
from processors.analysis import analyze_data
#import
from processors.missing import handle_missing_ultimate as handle_missing
from processors.duplicates import remove_duplicates
from processors.outliers import handle_outliers_smart
from processors.normalization import normalize

UPLOAD_FOLDER = "uploads"
#RESULT_FOLDER = "results"

"""class DataProcessor:

    #def process(self, file_path, options):
    def process(self, file_path, options, result_folder="results"):
        df = load_file(file_path)

        original = analyze_data(df)

        df = remove_duplicates(df)
        # Nettoyage complet
        #df = handle_missing(
            #df,
            #method=options.get("handle_missing", "fill_mean"),
           # categorical_override=["OWN_OCCUPIED"]
        )#
        # Nettoyage automatique des valeurs manquantes
        df =handle_missing(df, method=options.get("handle_missing", "fill_mean"))

        df=handle_outliers_smart(df)

        if options.get("normalize") == "true":
            df = normalize(df, options.get("norm_method", "minmax"))

        final = analyze_data(df)

        # 🔥 Choix du format
        file_format = options.get("file_format", "csv").lower()
        filename = f"proc_{uuid.uuid4()}"
        if file_format == "excel":
            filename += ".xlsx"
            df.to_excel(os.path.join(result_folder, filename), index=False)
        else:
            filename += ".csv"
            df.to_csv(os.path.join(result_folder, filename), index=False)

        return {
            "success": True,
            "processed_filename": filename,
            "original_analysis": original,
            "final_analysis": final
        }"""
class DataProcessor:

    def process(self, file_path, options, result_folder="results"):

        df = load_file(file_path)

        if df is None or df.empty:
            raise Exception("Fichier vide ou invalide")

        original = analyze_data(df)

        df = remove_duplicates(df)

        df = handle_missing(
            df,
            method=options.get("handle_missing", "fill_mean")
        )

        # 🔥 Sécurisation outliers
        try:
            df = handle_outliers_smart(df)
        except Exception as e:
            print("Erreur outliers:", e)

        # 🔥 FIX normalize
        if options.get("normalize", False):
            try:
                df = normalize(df, options.get("norm_method", "minmax"))
            except Exception as e:
                print("Erreur normalize:", e)

        final = analyze_data(df)

        # 🔥 format
        file_format = options.get("file_format", "csv").lower()
        filename = f"proc_{uuid.uuid4()}"

        output_path = os.path.join(result_folder, filename)

        try:
            if file_format == "excel":
                filename += ".xlsx"
                df.to_excel(os.path.join(result_folder, filename), index=False)
            else:
                filename += ".csv"
                df.to_csv(os.path.join(result_folder, filename), index=False)
        except Exception as e:
            print("Erreur export:", e)
            raise Exception("Erreur lors de la génération du fichier")

        return {
            "success": True,
            "processed_filename": filename,
            "original_analysis": original,
            "final_analysis": final
        }