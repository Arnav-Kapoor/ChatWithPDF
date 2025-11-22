from transformers import AutoImageProcessor, TableTransformerForObjectDetection

def table_transformer():
    image_processor = AutoImageProcessor.from_pretrained("microsoft/table-transformer-detection")
    model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-detection")

    return model,image_processor