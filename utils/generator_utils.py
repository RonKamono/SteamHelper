class Generator:
    def generate_user(e):
        res = "User info create."
        for i in range(int(slider_counter.value)):
            with open(path, 'a+', encoding="utf-8") as file:
                password = ''.join(choices(chars, k=16))
                login = name.value + ''.join(choices(digits, k=6))
                mail = login + '@outlook.com'
                line_count = sum(1 for line in open(path))
                file.write(
                    'LOGIN = ' + login + ' | ' + 'PASSWORD = ' + password + ' | ' + 'MAIL = ' + mail + ' | ' + str(
                        1 + line_count) + '\n')
        result_info(res)

    def result_info(res):
        result.value = res
        result.opacity = 1
        page.update()
        time.sleep(1.5)
        result.opacity = 0
        page.update()

    def open_txt():
        try:
            os.startfile(path)
        except:
            res = 'Fail not create.'
            result_info(res)

    def clear_txt():
        res = 'File remove.'
        result_info(res)
        try:
            os.remove(path)
        except:
            pass
