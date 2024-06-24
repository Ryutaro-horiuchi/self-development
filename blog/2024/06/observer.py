from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update():
        pass


class Subject():
    def __init__(self):
        self.observers = []

    def register_observer(self, observer: Observer):
        """オブザーバーを登録する"""
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer: Observer):
        """オブザーバーを削除する"""
        self.observers.remove(observer)

    def notify_observers(self):
        """オブザーバーに変更を通知する"""
        for observer in self.observers:
            observer.update()


class WeatherData(Subject):
    """気象観測クラス"""
    def __init__(self):
        super().__init__()
        self._temperature = 0

    def get_temperature(self):
        """気温を取得する"""
        return self._temperature

    def set_temperature(self, temperature: int):
        """新たな気温を設定する"""
        self._temperature = temperature
        self.notify_observers()


class Display(Observer):
    """気温表示クラス"""
    def __init__(self, weather_data: WeatherData):
        self.weather_data = weather_data
        weather_data.register_observer(self)

    def update(self):
        """ディスプレイに表示している気温情報を更新する"""
        temperature = self.weather_data.get_temperature()
        print(f'ディスプレイをアップデート - 現在の気温は{temperature}°Cです')


class EmailNotifier(Observer):
    """メール通知クラス"""
    def __init__(self, weather_data: WeatherData):
        self._email_addresses = []
        self.weather_data = weather_data
        weather_data.register_observer(self)

    def update(self):
        """登録メールアドレスに気温情報を通知する"""
        temperature = self.weather_data.get_temperature()
        print(f'登録メールアドレスに新規気温情報 {temperature}°Cを通知しました')


class WebPortal(Observer):
    """気象情報webサイトクラス"""
    def __init__(self, weather_data: WeatherData):
        self.weather_data = weather_data
        weather_data.register_observer(self)

    def update(self):
        """ウェブサイトに気温情報を表示する"""
        temperature = self.weather_data.get_temperature()
        print(f'ウェブサイトをアップデート - 現在の気温は{temperature}°Cです')


if __name__ == "__main__":
    weather_data = WeatherData()
    display = Display(weather_data)
    email_notifier = EmailNotifier(weather_data)
    web_portal = WebPortal(weather_data)

    # 気温を28度に設定
    weather_data.set_temperature(28)
    weather_data.remove_observer(email_notifier)
    print('-------メール通知をオブザーバーから外しました-------')

    # 気温を23度に設定
    weather_data.set_temperature(23)