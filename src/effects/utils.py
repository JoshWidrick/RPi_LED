def get_status():
    with open("./file/status.txt", "r") as f:
        try:
            status = f.read().strip().split(',')
            return status
        except:
            return 'failed'


def check_status(current_status):
    return True if current_status == get_status() else False
