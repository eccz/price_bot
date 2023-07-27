import gspread
from dev import GS_TEST_SHEET
from dev import GS_KEY_FILE_NAME

# Указываем путь к JSON igorchernov1544
gc = gspread.service_account(filename=GS_KEY_FILE_NAME)

sht1 = gc.open_by_key(GS_TEST_SHEET)
sht1.sheet1.clear()

for i in range(20):
    sht1.sheet1.update([['asd', 'qwe']] + [['123', '345'], ['321', '654']])
