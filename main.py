from send.send_msg import SendMSG

def main():
    sm = SendMSG()
    sm.get_mails()
    sm.send_msg()

if __name__ == "__main__":
    main()