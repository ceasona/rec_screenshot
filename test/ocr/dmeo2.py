import paddleocr

ocrer = paddleocr.PaddleOCR()


img_words = r'E:\temp\screen\cropim.png'
word_mes = ocrer.ocr(img_words, det=True,rec=True, cls=False)
for i in word_mes:
    print(i[-1][0])