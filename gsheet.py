import gspread
# Указываем путь к JSON igorchernov1544
gc = gspread.service_account(filename='magnetic-runway-393913-0c95e82fc0be.json')

sht1 = gc.open_by_key('1XLMvGH8B7BbOXbnYSOywQ-JfhmGQkRLyUR79_Nvgptg')
for i in range(20):
    sht1.sheet1.update(f'A{i+1}', 'ZALUPA')
