from vncorenlp import VnCoreNLP
import time

annotator = VnCoreNLP('/home/misa/PycharmProjects/lightning-projects/VnCoreNLP/VnCoreNLP-1.1.jar')
text = "Ông Nguyễn Khắc Chúc  đang làm việc tại Đại học Quốc gia Hà Nội. Bà Lan, vợ ông Chúc, cũng làm việc tại đây."
annotated_text = annotator.annotate(text)
word_segmented_text = annotator.tokenize(text)
for i in range(10):
    semi_text = text[:-i]
    start_time = time.time()
    annotated_text = annotator.annotate(semi_text)
    word_segmented_text = annotator.tokenize(semi_text)
    print(str(start_time - time.time()))
print()