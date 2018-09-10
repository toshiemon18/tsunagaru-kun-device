class Recorder:
    """このクラスは、データを Web サーバーへアップロードします。
    内部にキューを持ち、record() メソッドで受け取ったリストを保持します。
    キューが十分な長さになると、データを Web サーバーへ送信します。
    送信に失敗した場合は、次の記録タイミングで送信を試みます。
    """

    def __init__(self, url, ba_id, ba_pass, minimum_upload_queue_length = 1):
        self.data_queue = deque()

        self.url = url
        self.ba_id = ba_id
        self.ba_pass = ba_pass
        self.compression_level = COMPRESSION_LEVEL
        self.minimum_upload_queue_length = minimum_upload_queue_length


    def record(self, data):
        self.data_queue.append(self.__build_message(data))
        tmp_queue=copy.deepcopy(self.data_queue)

        try:
            if self.minimum_upload_queue_length <= len(tmp_queue) :
                self.__send_queue(tmp_queue)
                for dummy in tmp_queue:
                    self.data_queue.popleft()
        except:
            print("=== データを送信できませんでした。 ===")
            d=datetime.datetime.today()
            print d.strftime("%Y-%m-%d %H:%M:%S"),'\n'


    def __send_queue(self, queue):
        send_string = ""
        for data in queue:
            send_string += " " + data
        response=self.__send_string(send_string)


    def __send_string(self, message):

        pswd_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        pswd_mgr.add_password(None, self.url, self.ba_id, self.ba_pass)
        opener = urllib2.build_opener(urllib2.HTTPSHandler(),
            urllib2.HTTPBasicAuthHandler(pswd_mgr))
        urllib2.install_opener(opener)

        request = urllib2.Request(self.url)
        request.add_data(bz2.compress(message,self.compression_level))

        response = urllib2.urlopen(request)
        return response.read()


    def __build_message(self, data):
        message = str(int(time.time()))
        for value in data:
            message += ":" + str(value)
        return message
