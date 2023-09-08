import sys
from transformers import AutoModelForSeq2SeqLM,AutoTokenizer

from src1.exception import CustomException
from src1.logger import logger

class Summarizer:
    def load_model(self):
        try:
            logger.info("Loading tokenizer and model...")
            try:
                self.tokenizer=AutoTokenizer.from_pretrained("best_model")
                self.model=AutoModelForSeq2SeqLM.from_pretrained("best_model")
                logger.info("Tokenizer and model loaded from the best directory")
            except:
                try:
                    logger.info("Model not available in the best model directory. Check model trainer artifacts..")

                    self.tokenizer=AutoTokenizer.from_pretrained("artifacts/model_trainer")
                    self.model=AutoModelForSeq2SeqLM.from_pretrained("artifacts/model_trainer")
                    logger.info("Tokenizer and model loaded from the artifacts/model_trainer directory")    

                except:
                    logger.info("Model not available in the artifacts/model_trainer and best model directory. Check model trainer artifacts..")

                    self.tokenizer=AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
                    self.model=AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")
                    logger.info("Tokenizer and model loaded from the best directory")

        except Exception as e:
          logger.error("Error loading the model.")
          raise CustomException(e, sys)


    def summarize_text(self,transcript):
        try:
            logger.info("Initiating summarizer...")

            inputs=self.tokenizer(transcript,
                                  max_length=1024,
                                  truncation=True,
                                  return_tensors="pt")

            summary_ids=self.model.generate(
                inputs["input_ids"],num_beams=2,min_length=50,max_length=1024)
            
            summary=self.tokenizer.batch_decode(
                summary_ids,skip_special_tokens=True,clean_up_tokenization_spaces=False
            )[0]

            return summary

        except Exception as e:
            logger.error("Check your Best Model Directory")
            raise CustomException(e,sys)     
            
