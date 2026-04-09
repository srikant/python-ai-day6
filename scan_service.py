class ScanService:
    def __init__(self, db_collection):
        self.collection = db_collection

    def analyze_and_save(self, image_id: str, image_data: bytes):
        if image_data is None or len(image_data) == 0:
            raise ValueError("Image data cannot be empty")

        print("Calling expensive AI model...")
        result = {"label": "benign", "confidence": 0.98}
        
        doc = {
            "_id": image_id,
            "result": result,
            "status": "processed"
        }

        if self.collection is not None:
            self.collection.insert_one(doc)
        
        return result