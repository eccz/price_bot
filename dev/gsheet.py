import gspread
from dev import GS_TEST_SHEET
from dev import GS_KEY_FILE_NAME

# Указываем путь к JSON igorchernov1544
gc = gspread.service_account(filename=GS_KEY_FILE_NAME)

sht1 = gc.open_by_key(GS_TEST_SHEET)
worksheet1 = sht1.get_worksheet(0)
worksheet2 = sht1.get_worksheet(1)
worksheet2.clear()

worksheet1.update([['1', '2'], ['3', '4']])
