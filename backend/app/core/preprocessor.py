import re

class InputPreprocessor:
    def preprocess(self, error: str, code: str = None):
        clean_error = error.strip()
        error_type = self._extract_error_type(error)
        language = self._infer_language(error, code)
        library = self._extract_library(error, code)
        return {
            "clean_error": clean_error,
            "error_type": error_type,
            "language": language,
            "library": library,
        }

    def _extract_error_type(self, error: str):
        match = re.search(r"([A-Za-z_]+Error|Exception|TypeError|ReferenceError)", error)
        return match.group(1) if match else ""

    def _infer_language(self, error: str, code: str = None):
        if code:
            if "def " in code or "import " in code:
                return "python"
            elif "function " in code or "console.log" in code:
                return "javascript"
            elif "#include" in code or "int main" in code:
                return "c/c++"
            elif "public static void main" in code:
                return "java"
        if "pandas" in error or "DataFrame" in error:
            return "python"
        if "TypeError" in error:
            return "python"
        return ""

    def _extract_library(self, error: str, code: str = None):
        patterns = [
            r"pandas", r"numpy", r"scikit-learn", r"tensorflow", r"react", r"express", r"django", r"flask"
        ]
        for pat in patterns:
            if pat in (error or "") or (code and pat in code):
                return pat
        return ""